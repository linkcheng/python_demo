#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# pip install python-rocksdb

import rocksdb


db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
batch = rocksdb.WriteBatch()
batch.put(b"zset_k_test_c_100", "member1")
batch.pub(b"zset_k_test_v_member1", "100")
db.write(batch)
db.put(b"zset_k_test_c", "1")
