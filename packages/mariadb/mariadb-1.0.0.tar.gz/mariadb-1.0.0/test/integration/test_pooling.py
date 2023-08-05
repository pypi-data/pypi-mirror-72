#!/usr/bin/env python -O
# -*- coding: utf-8 -*-

import collections
import datetime
import unittest

import mariadb
import platform

from test.base_test import create_connection, conf


@unittest.skipIf(platform.python_implementation() == "PyPy", "skip pooling tests for PyPy")
class TestPooling(unittest.TestCase):

    def setUp(self):
        self.connection = create_connection()
        self.connection.autocommit = False

    def tearDown(self):
        del self.connection

    def test_connection_pools(self):
        pool= mariadb.ConnectionPool(pool_name="test_connection")
        self.assertEqual(mariadb._CONNECTION_POOLS["test_connection"], pool)
        del pool
        self.assertEqual(mariadb._CONNECTION_POOLS, {})

    def test_conpy39(self):
        try:
            pool= mariadb.ConnectionPool()
        except mariadb.ProgrammingError:
            pass

    def test_connection_pool_conf(self):
        pool= mariadb.ConnectionPool(pool_name="test_conf")
        default_conf= conf()
        conn= create_connection()
        try:
            pool.add_connection(conn)
        except mariadb.PoolError:
            pass
        try:
            pool.set_config(**default_conf)
        except:
            del pool
            raise

        pool.add_connection(conn)
        c= pool.get_connection()
        self.assertEqual(c, conn)
        del pool

    def test_connection_pool_maxconn(self):
        default_conf= conf()
        pool= mariadb.ConnectionPool(pool_name="test_max_size", **default_conf)
        connections= []
        for i in range(1, 6):
           connections.append(pool.get_connection())
        try:
            x= pool.get_connection()
        except mariadb.PoolError:
            pass
        for c in connections:
            c.close()
        x= pool.get_connection()
        del pool

    def test_connection_pool_add(self):
        default_conf= conf()
        pool= mariadb.ConnectionPool(pool_name="test_connection_pool_add")
        try:
            pool.set_config(**default_conf)
        except:
            del pool
            raise

        for i in range(1,6):
            pool.add_connection()
        try:
            pool.add_connection()
        except mariadb.PoolError:
            pass
        del pool

    def test_conpy69(self):
        conn= create_connection()
        cursor1= conn.cursor()
        cursor1.execute("CREATE SCHEMA IF NOT EXISTS 中文考试")
        default_conf= conf()
        default_conf["database"]= "中文考试"
        pool= mariadb.ConnectionPool(pool_name="test_conpy69")
        try:
            pool.set_config(**default_conf)
        except:
            del pool
            raise

        for i in range(1,6):
            pool.add_connection()
        conn= mariadb.connect(pool_name="test_conpy69")
        cursor= conn.cursor()
        cursor.execute("select database()")
        row= cursor.fetchone()
        self.assertEqual(row[0], "中文考试")
        cursor.execute("CREATE TABLE t1 (a varchar(255)) character set utf8mb4")
        cursor.execute("insert into t1 values (?)", ("123.45 中文考试",))
        cursor.execute("select a from t1")
        row= cursor.fetchone()
        self.assertEqual(row[0], "123.45 中文考试")
        cursor1.execute("DROP SCHEMA 中文考试")
        del pool

    def test__CONNECTION_POOLS(self):
        default_conf= conf()
        pool= mariadb.ConnectionPool(pool_name="test_use", **default_conf)
        conn= mariadb.connect(pool_name="test_use")
        cursor= conn.cursor()
        cursor.execute("SELECT 1")
        row= cursor.fetchone()
        self.assertEqual(row[0], 1)
        del cursor
        del pool

    def test_create_pool_from_conn(self):
        default_conf= conf()
        key= "t1"
        conn= mariadb.connect(pool_name=key, **default_conf)
        cursor=conn.cursor()
        del mariadb._CONNECTION_POOLS["t1"]
        self.assertEqual(mariadb._CONNECTION_POOLS, {})
        try:
            cursor.execute("SELECT 1")
        except mariadb.ProgrammingError:
            pass

    def test_pool_getter(self):
        default_conf= conf()
        conn= mariadb.connect(pool_name="getter_test", pool_size=4, **default_conf)
        p= mariadb._CONNECTION_POOLS["getter_test"]
        self.assertEqual(p.pool_name, "getter_test")
        self.assertEqual(p.pool_size, 4)
        if "pool_reset_connection" in default_conf:
            self.assertEqual(p.pool_reset_connection, default_conf["pool_reset_connection"])
        else:
            self.assertEqual(p.pool_reset_connection, True)
        self.assertEqual(p.max_size, 64)
        del mariadb._CONNECTION_POOLS["getter_test"]

    def test_pool_connection_reset(self):
        default_conf= conf()
        conn= mariadb.connect(pool_name="reset_test", pool_size=1, **default_conf)
        cursor= conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        conn= mariadb.connect(pool_name="reset_test")
        cursor= conn.cursor()
        cursor.execute("SELECT 2")
        row= cursor.fetchone()
        self.assertEqual(row[0], 2)
        del mariadb._CONNECTION_POOLS["reset_test"]

    def test_conpy40(self):
        default_conf= conf()
        pool = mariadb.ConnectionPool(pool_name = 'test_conpy40')

        try:
            pool.set_config(pool_size = 3)
        except mariadb.PoolError:
            pass

        try:
            pool.set_config(**default_conf)
        except:
            del pool
            raise

        for j in range(3):
            c = mariadb.connect(**default_conf)
            pool.add_connection(c)
        del pool

    def test_pool_add(self):
        default_conf= conf()
        pool= mariadb.ConnectionPool(pool_name="test_pool_add")
        try:
          mariadb.ConnectionPool(pool_name="test_pool_add")
        except mariadb.ProgrammingError as e:
           pass
        del pool

if __name__ == '__main__':
    unittest.main()
