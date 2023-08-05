import logging
import os
import sqlite3
import time
from time import strftime

import pandas as pd

from notetool.tool import log

logging.basicConfig(format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')


class BaseTable:
    def __init__(self, table_name='default_table', columns=None):
        self.table_name = table_name
        self.columns = columns
        self.logger = log(table_name)

    def execute(self, sql):
        raise Exception("还没有实现")

    def insert(self, properties: dict):
        if self.columns is None:
            raise Exception("origin_keys cannot be None")
        keys = []
        values = []
        for key in self.columns:
            value = str(properties.get(key, '')).replace("'", '')
            if len(key) > 0 and len(value) > 0:
                keys.append(key)
                values.append("'{}'".format(value))

        sql = """insert or ignore into {} ({}) values ({})""".format(self.table_name, ', '.join(keys),
                                                                     ', '.join(values))
        return self.execute(sql)

    def count(self, properties: dict):
        properties = properties or {}
        values = []
        for key in self.columns:
            value = str(properties.get(key, ''))
            if len(value) > 0 and len(key) > 0:
                values.append("{}='{}'".format(key, value))

        sql = """select count(1) from {} where {}""".format(self.table_name, ' and '.join(values))

        rows = self.execute(sql)
        for row in rows:
            return row[0]
        return 0

    def select(self, sql):
        sql = sql.replace('table_name', self.table_name)

        rows = self.execute(sql)
        return [] if rows is None else [row for row in rows]


class SqliteTable(BaseTable):
    def __init__(self, db_path, *args, **kwargs):
        super(SqliteTable, self).__init__(*args, **kwargs)
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        try:
            rows = self.cursor.execute(sql)
            self.conn.commit()
            return rows
        except Exception as e:
            print("{}  with error:{}".format(sql, e))
            return

    def close(self):
        self.cursor.close()
        self.conn.close()

    def save_and_truncate(self):
        result = pd.read_sql("select * from {}".format(self.table_name), self.conn)

        count = len(result)
        path = ('{}/{}-{}-{}'.format(os.path.dirname(self.db_path), self.table_name, count,
                                     strftime("%Y%m%d#%H:%M:%S", time.localtime())))
        result.to_csv(path)
        self.logger.info("save to csv:{}->{}".format(count, path))

        self.execute("delete from {}".format(self.table_name))
        self.logger.info("delete from {}".format(self.table_name))
        self.execute("VACUUM")
        self.logger.info("VACUUM")
        return result
