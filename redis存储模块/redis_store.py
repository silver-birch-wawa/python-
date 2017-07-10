#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

class database():
    def __init__(self):
        self.r=redis.Redis(host='127.0.0.1', port=6379,db=0)
    def store(self,goods_name,goods_price,store_name):
        try:
            self.r.sadd(goods_name, store_name)
            self.r.sadd(goods_name,goods_price)
        except Exception as e:
            print("error in storing.....",e)
'''
d1=database()
d2=database()
d3=database()
d1.store('1','2','3')
d2.store('2','3','4')
d3.store('3','4','5')
'''
