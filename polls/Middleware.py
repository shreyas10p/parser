from django.conf import settings
from django.http import JsonResponse
from django.http import JsonResponse
from .ratelimit import Bucket
import requests
import json
from rest_framework.response import Response

class Middleware(object):
    master_server = Bucket(2,10,2)
    slave1_server = Bucket(2,10,2)
    slave2_server = Bucket(2,10,2)

    @staticmethod
    def get_master_value():
        return Middleware.master_server.get()

    @staticmethod
    def get_slave1_value():
        return Middleware.slave1_server.get()

    @staticmethod
    def get_slave2_value():
        return Middleware.slave2_server.get()

    @staticmethod
    def reduce_master_value():
        Middleware.master_server.reduce(1)
        return True

    @staticmethod
    def reduce_slave1_value():
        Middleware.slave1_server.reduce(1)
        return True
    @staticmethod
    def reduce_slave2_value():
        Middleware.slave2_server.reduce(1)
        return True

    def process_request(self, request):
        if(Middleware.get_master_value() == 0):
            if(Middleware.get_slave1_value() == 0):
                if(Middleware.get_slave2_value() == 0):
                    return False
                else:
                    Middleware.reduce_slave2_value(1)
                    self.call_slaves(request,'<slave2_server_addr>')
            else:
                Middleware.reduce_slave1_value(1)
                self.call_slaves(request,'<slave1_server_addr>')
        else:
            Middleware.reduce_master_value()


    def call_slaves(self,request,addr):
        headers = {"Content-Type": "application/json"}
        if request.method == 'GET':
            r = requests.get(addr,headers=headers, verify=True)
            r.json()

    def process_exception(self, request, exception):
        print("exception",exception)

    def get__headers(self):
        headers = {}
        if 'HTTP_SLUG' in self:
            headers['slug'] = self.get('HTTP_SLUG')
        if 'CONTENT_TYPE' in self:
            headers['content_type'] = self.get('CONTENT_TYPE')
        if 'HTTP_USER_AGENT' in self:
            headers['user_agent'] = self.get('HTTP_USER_AGENT')
        return headers


