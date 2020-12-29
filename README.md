## 基于flask 实现的动态ip跨域以及单点登录方案

### 简介

​	该项目是用python语言编写，基于flask 的高可用动态ip 跨域以及单点登陆方案。在web项目当中，我们经常会遇到跨域的问题，特别是在当前分布式场景下，需要动态的进行进行一些跨域。本项目在通过jwt实现单点登录前提下，通过flask 的钩子函数去实现动态的ip跨域。



原理: 

  	 1. 服务端拆成两个服务，一个web_auth 用来用户登录，给用户签发token 。另一个web_server 用来校验单点登录和动态跨域是否成功。
  	 2. 用户登录时请求携带用户名和密码到web_auth ，此时web_auth  会去数据库校验数据，如果校验成功，则用jwt 签发token 并设置到cookie 中，并且通过钩子函数获取请求ip和端口，构造响应头，允许跨域，并将token签发给client 客户端浏览器。
  	 3. 此时客户端携带token 来到web_server 端请求服务，web_server端利用钩子函数，在每次请求前首先会获得用户token 进行校验，如果用户无可用token 则返回空值由nginx 重定向web_auth 用户登录验证服务。如果用户token 可用，则反解析用户token, 拿到值后校对，如果成功，则获取请求client端的ip地址，设置到请求头中，实现跨域，并允许用户继续访问。



### 最佳实践

1. 安装依赖

   ```
   pip install pymysql
   pip install flask
   pip install flask-cors
   pip install jwt
   ```

2. 创建数据库

   ```mysql
   create user_info(
   id int,
   username varchar(20),
   password varchar(20),
   user_id int,
   );
   ```

   

3. 依次启动三个项目

   ```
   python web_auth.py
   python web_client.py
   python web_server.py
   ```

4. 测试 

   - 访问 localhost:8000/test 
   - 在输入框输入 /login 此时已经token 登录成功token被设置
   - 拿到token 后可以换一个浏览器，填入token 值，并且去跨域访问 localhost:5500/test  可以看到可以成功访问。
   - 也可以自己将该服务器部署到ecs 公网地址上，拿到token 后使用不同ip ,或不同端口去请求 5500端口 web_server的服务，可以校验均可成功。

   
