from flask import Flask, request, url_for, redirect
import config
from ext.db import db, QuerySetNull, QueryParamsError
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    if not config.DOMAIN:
        return "请在根目录下的config.py中配置主域名"

    ret = {
        'http://'+ config.DOMAIN +'/': 'dosc',
        'http://'+ config.DOMAIN +'/insert/?param1=xxx&param2=xxx': '插入: 通过拼接url的方式传递一条记录的字段',
        'http://'+ config.DOMAIN +'/find/?param1=xxx&param2=xxx': '查找: 通过拼接url的方式传递查询的条件',
        'http://'+ config.DOMAIN +'/update/?multi=true&q_param1=xxx&q_param2=xxx&u_param1=xxx&u_param2=xxx':
            '更新: multi=true, 如果查询到了多条记录, 则全部更新, multi=false, 查询到了多条记录,只更新第一条, '
            '需要传递查询字段和更新字段, 查询字段前加q_前缀, 更新字段前加u_前缀',
        'http://' + config.DOMAIN + '/remove/?multi=true&param1=xxx': '删除: multi,指定是否适用多条, 再拼接查询条件'
    }
    return json.dumps(ret)


@app.route('/insert/')
def insert():
    kwargs = dict(request.args.items())
    try:
        db.insert(kwargs)
        return '插入成功!'
    except Exception as err:
        return str(err)


@app.route('/find/')
def find():
    kwargs = {}
    for k, v in request.args.items():
        try:
            v = int(v)
        except Exception:
            pass
        kwargs[k] = v
    datas = db.find(kwargs)
    ret = json.dumps(datas)
    return ret


@app.route('/update/')
def update():
    query, update = {}, {}
    for arg in request.args:
        if arg[0:2] == 'q_':
            try:
                value = int(request.args.get(arg))
            except ValueError:
                value = request.args.get(arg)
            query[arg[2:]] = value

        if arg[0:2] == 'u_':
            try:
                value = int(request.args.get(arg))
            except ValueError:
                value = request.args.get(arg)
            update[arg[2:]] = value

    multi = request.args.get('multi', default='')
    try:
        count = db.update(query, update, multi=multi)
        return '''
            <br>
            <html>
                <body>
                    <head></head>
                    <h3>成功更新{count}条记录</h3>
                    <h3>查询刚更新的记录: <a href="{url}">{url}</a></h3>
                    <a href="/">接口文档</a>
                </body>
            </html>
        '''.format(url=url_for('find', **update), count=count)
    except QueryParamsError as err:
        return str(err)
    except QuerySetNull as err:
        return str(err)
    except Exception as err:
        if not update:
            return '更新参数未传入'
        return str(err)


@app.route('/remove/')
def remove():
    query = {}
    for k, v in request.args.items():
        try:
            v = int(v)
        except Exception:
            pass
        query[k] = v

    if 'multi' in query:
        query.pop('multi')

    multi = request.args.get('multi', default='')
    try:
        count = db.remove(query, multi)
        return '成功删除%d记录' % count
    except QueryParamsError as err:
        return str(err)
    except Exception as err:
        return str(err)


if __name__ == '__main__':
    app.run()
