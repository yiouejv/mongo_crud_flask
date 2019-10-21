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

    def find(self, query:dict, is_deleted=0):
        '''
            查询文档
        :param query: 查询条件
        :param is_deleted: 逻辑删除，0 未删除, 1 删除
        :return: 文档列表
        '''
        query['is_deleted'] = is_deleted
        cursor = self.myset.find(query)
        ret = []
        for data in cursor:
            data = dict(zip(data.keys(), map(lambda v: str(v) if not isinstance(v, int) else v, data.values())))
            ret.append(data)
        return ret

    def update(self, query:dict, update:dict, multi:bool, is_deleted=0):
        '''
            更新集合文档
        :param query: 查询文档条件
        :param update: 文档更新
        :param multi: true 多条记录全部更新, false 只更新匹配到的第一条记录
        :param is_deleted: 缺省未删除的文档
        :return: 影响的行数
        '''
        if multi not in ['true', 'false']:
            raise QueryParamsError('multi参数错误, 必须为true或false')
        multi = False if multi == 'false' else True

        query_set = self.find(query, is_deleted=is_deleted)
        if not query_set:
            raise QuerySetNull('查询结果为空, 未进行相关操作!!!')

        update = {'$set': update}
        self.myset.update(query, update, upsert=True, multi=multi)
        return 1 if multi== False else len(query_set)

    def remove(self, query, multi):
        query_set = self.find(query)
        if not query_set:
            return 0

        self.update(query, {'is_deleted': 1}, multi=multi)
        return 1 if multi== False else len(query_set)

    def recovery(self, query, multi):
        '''
            恢复数据
        :param query: 查询条件
        :param multi: true 多条记录全部适用, false 只适用匹配到的第一条记录
        :return: 影响的行数
        '''
        return self.update(query, {'is_deleted': 0}, multi, is_deleted=1)


db = MongoTools()


