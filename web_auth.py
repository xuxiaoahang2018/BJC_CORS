

import os
import json
import jwt
import pymysql
import logging
from flask import Flask, session, request, make_response
from functools import lru_cache
from datetime import timedelta, datetime
from flask_cors import CORS

logger = logging.getLogger(__name__)
app = Flask(__name__)
screct_key = "bjc_screct_key"



def after_request(resp):
    request_ip = request.environ.get("HTTP_ORIGIN")
    resp.headers['Access-Control-Allow-Origin'] = request_ip
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    return resp

app.after_request(after_request)


class Auth():
    def __init__(self, host="127.0.0.1", user="root", passwd="123456", database="evan_test", port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port
        self.cursor = self.mysql_conn()

    @lru_cache()
    def mysql_conn(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, database=self.database)
        conn.autocommit(True)
        cursor = conn.cursor()
        return cursor

    def select_user_info(self, username, password):
        try:
            sql = "select user_id from user_info where username='%s' and password='%s';" % (username, password)
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            if data:
                return data[0]
        except Exception as e:
            print(e)
            logger.error("Failed to get data from database. error message: %s" % e)
            return None


    def set_user_token(self, user_id):
        payload = {  # jwt设置过期时间的本质 就是在payload中 设置exp字段, 值要求为格林尼治时间
            "user_id": user_id,
            'exp': datetime.utcnow() + timedelta(seconds=3600)
        }
        token = jwt.encode(payload, key=screct_key, algorithm='HS256')
        return token


auth = Auth()


@app.route('/login',methods=["GET", "POST"])
def loggin():
    username = request.form.get("username") or "test"
    password = request.form.get("password") or "test"
    # 如果校验成功返回user_id
    user_id = auth.select_user_info(username, password)
    if user_id:
        # 设置token
        token = auth.set_user_token(user_id)
        resp = make_response("用户校验成功，已获得令牌")  # 设置响应体
        resp.set_cookie("token", token, max_age=3600)
        return resp
    else:
        return "登录失败"



@app.route("/")
def welcome():
    return "认证服务端登录成功"

if __name__ == "__main__":
    app.run("0.0.0.0",port=5000)
