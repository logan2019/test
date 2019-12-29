# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy.utils.project import get_project_settings

class ZhipinPipeline(object):
    def open_spider(self, spider):
        self.fp = open('./job.json', mode='w+', encoding='utf-8')
        # 写入中括号
        self.fp.write('['+'\n')

    def process_item(self, item, spider):
        self.fp.write(json.dumps(dict(item), ensure_ascii=False) + ',\n')
        return item

    def close_spider(self, spider):
        self.fp.write('\n' + ']')
        self.fp.close()

class JobMysqlPipeline(object):
    def open_spider(self, spider):
      # 创建数据库链接
        setting = get_project_settings()
        host = setting.get('DB_HOST')
        port = setting.get('DB_PORT')
        user = setting.get('DB_USER')
        password = setting.get('DB_PASSWWORD')
        database = setting.get('DB_DATABASE')
        charset = setting.get('DB_CHARSET')
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password,
                        database=database, charset=charset)

        #创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f'insert into boss({keys}) values({values})'

        try:
            self.cursor.execute(sql, (tuple(data.values())))
            print('successful')
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

