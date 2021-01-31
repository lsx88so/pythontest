# -*- coding: utf-8 -*-
import cx_Oracle
#import MySQLdb
import logging
import string
from DBUtils.PooledDB import PooledDB

class DbOper:

    def __init__(self, dbType, connStr, maxConn):
        cLogger = logging.getLogger("main")
        self.isReady = False
        if dbType == "oracle":
            try:
                db_conn = connStr.split("#")
                self.db_name = db_conn[2]
                self.pool = PooledDB(cx_Oracle, user=db_conn[0], password=db_conn[1], dsn=db_conn[2], threaded=True,
                                     mincached=maxConn, maxcached=maxConn, maxshared=maxConn, maxconnections=maxConn)
            except Exception as e:
                cLogger.error("create oracle db pool failed, db:%s, exception: %s" % (db_conn[2], e))
        elif dbType == "mysql":
            try:
                db_conn = connStr.split("#")
                self.db_name = db_conn[2]
#                self.pool = PooledDB(MySQLdb, user=db_conn[0], passwd=db_conn[1], host=db_conn[2],
#                                     port=string.atoi(db_conn[3]), db=db_conn[4], mincached=maxConn, maxcached=maxConn,
#                                     maxshared=maxConn, maxconnections=maxConn)
            except Exception as e:
                cLogger.error("create mysql db pool failed, db:%s, exception: %s" % (db_conn[2], e))
        self.isReady = True

    def execute(self, sqlStr):
        cLogger = logging.getLogger("main")
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            cursor.execute(sqlStr)
            conn.close()
            return cursor.fetchall()
        except Exception as e:
            cLogger.error("execute sql error - db:%s, sql:%s, exception: %s" % (self.db_name, sqlStr, e))
            
    def get_conn(self):
    	return self.pool.connection()
