# -*- coding: utf-8 -*-

import os
import json
import redis
import jwt
import pymysql
from flask import Flask, session, make_response,request
from datetime import timedelta
from functools import lru_cache


app = Flask(__name__)
screct_key = "bjc_screct_key"
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # 配置7天有效


def before_request():
    request_ip = request.environ.get("HTTP_ORIGIN")
    token = request.cookies.get("token")
    if token:
        data = jwt.decode(token, key=screct_key, algorithms='HS256')
        if data.get("user_id"):
            resp = make_response("")
            resp.headers['Access-Control-Allow-Origin'] = request_ip
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
        else:
            return "校验码错误"
    else:
        return "请求失败"

app.before_request(before_request)


@app.route("/")
def welcome():
    return "服务端启动成功"


@app.route('/test')
def cors_test():
    token = request.cookies.get("token")
    return "动态跨域成功，跨域token:{0}".format(token)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5500")
