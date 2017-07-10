#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 20:52:17 2017

@author: 
"""
import sys,os
sys.path.append("..")

import socket
import time
import threading,time,socketserver,queue

unrepeated_url_io=0

####尽力而为TCP#####
def TCP_receiver(ip,port):
    #没有对应的匹配字符串的接受函数
    global receive_string
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen(1)
    print('Server is running...')  
    sock, addr = s.accept()                            #接收一个新连接
    data = sock.recv(1024)                         #接受其数据
    data=data.decode("utf-8")
    data=str(data)
    print("received data: ",data)
    sock.close()                                      #关闭连接
    print('Connection from %s:%s closed.' %addr) 
    return data

#####尽全力服务#####
def receiver(ip,port):
    data=""
    while(1):
        try:
            data=TCP_receiver(ip,port)
            print("data in receiver: ",data)
        except Exception as e:
            print(e)
            continue
        break
#####尽全力基础上加上字符串匹配####
def receiver_with_string_compare(ip,port,input_string):
    data=""
    while(1):
        data=TCP_receiver(ip,port)
        print("data in receiver: ",data)
        if(input_string in data):
            return "ok"
        
#######################多线程接受url+去重模块#############################
def processing_the_url(conn,data):
    global set_
    global unrepeated_url_io
    if data in set_:
        q=data+"  repeated"
        #lock.wait(t_num)
        try:
            conn.sendall(q.encode())
        except Exception as e:
            print(e)
        #lock.signal(t_num)
    else:
        if('http' not in data):
            data='http:'+data
        q=data+"  unrepeated"
        print("接受到的正确的url: ",q)
        #print('\n吞吐量计数: ',unrepeated_url_io,'\n')
        #lock.wait(t_num)
        set_.add(str(data))
        try:
            conn.sendall(q.encode())
        except Exception as e:
            print(e)
##################################################
class MyServer(socketserver.BaseRequestHandler):
    def __init__(self, request,client_address,server):
        global set_
        self.set_=set_
        socketserver.BaseRequestHandler.__init__(self,request,client_address,server)
    def handle(self):
        global unrepeated_url_io,set_
        #去重用的set还有接受用的队列
        conn = self.request
        try:
            while (1):
                print("start listening.")
                try:
                    data = conn.recv(1024)
                except Exception as e:
                    if('主机'in str(e)):  #对方切断连接后会不断报错,所以要掐掉这种报错。
                        break
                    else:
                        print("无关紧要的bug: ",e)
                        continue
                cur_thread = threading.current_thread()
                if(data!=b""):
                    data=str(data)[1:]
                    unrepeated_url_io=unrepeated_url_io+1
                    print("\n当前吞吐量为:%d\n"%unrepeated_url_io)
                    print(cur_thread.name,"  :",data)
                    processing_the_url(conn,data)
                    #导入TCP，数据，去重容器，当前线程名
        except Exception as e:
                print(e)
def TCP_threads_receiver(ip='127.0.0.1',port=8888):
    t=threading.Thread(target=calculate_url_io,args=())
    t.start()
    server = socketserver.ThreadingTCPServer((ip,port),MyServer)
    ip,port=server.server_address
    server.serve_forever()
    print("注意一下这里,说不定没启动守候进程....")
    t.join()
'''
TCP_threads_receiver('127.0.0.1',8888)
#print(receiver('127.0.0.1',8888,'1111'))
#返回接受的信息
'''
