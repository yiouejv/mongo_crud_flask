import pymongo
import config


class QuerySetNull(Exception):
    pass


class QueryParamsError(Exception):
    pass


class MongoTools():
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn.jishen
        self.myset = self.db.spider

    def insert(self, kwargs:dict):
        kwargs['is_deleted'] = 0
        self.myset.insert(kwargs)

    def find(self, query:dict):
        query['is_deleted'] = 0
        cursor = self.myset.find(query)
        ret = []
        for data in cursor:
            data = dict(zip(data.keys(), map(lambda v: str(v), data.values())))
            ret.append(data)
        return ret

    def update(self, query:dict, update:dict, multi:bool):
        '''
            更新集合文档
        :param query: 查询文档条件
        :param update: 文档更新
        :param multi: true 多条记录全部更新, false 只更新匹配到的第一条记录
        :return: 影响的行数
        '''
        if multi not in ['true', 'false']:
            raise QueryParamsError('multi参数错误, 必须为true或false')
        multi = False if multi == 'false' else True

        query_set = self.find(query)
        if not query_set:
            raise QuerySetNull('查询结果为空, 未进行更新操作!!!')

        update = {'$set': update}
        self.myset.update(query, update, upsert=False, multi=multi)
        return 1 if multi== False else len(query_set)

    def remove(self, query, multi):
        query_set = self.find(query)
        if not query_set:
            return 0

        self.update(query, {'is_deleted': 1}, multi=multi)
        return 1 if multi== False else len(query_set)


db = MongoTools()


