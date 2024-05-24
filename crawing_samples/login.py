# -*- coding: utf-8 -*-
# @Time    : 2020/5/10 23:25
# @Author  : 我就是任性-Amo
# @FileName: 77.通过爬虫实现GitHub网页的模拟登录.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/xw1680

import requests  # 导入网络请求模块
from lxml import etree  # 导入数据解析模块 都是第三方模块需要安装 
# pip install requests/lxml如果太慢 可以加上镜像服务器 或者在Pycharm中使用图形化界面进行安装


class GitHubLogin(object):
    def __init__(self, username, password):
        # 构造头部信息
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Host": "github.com",
            "Referer": "https://github.com/login"
        }
        self.login_url = "https://github.com/login"  # 登录页面地址
        self.post_url = "https://github.com/session"  # 实现登录的请求地址
        self.session = requests.Session()  # 创建Session会话对象
        self.user_name = username  # 用户名
        self.password = password  # 密码

    # 获取authenticity_token信息
    def get_token(self):
        # 发送登录页面的网络请求
        response = self.session.get(self.login_url, headers=self.headers)
        if response.status_code == 200:  # 判断请求是否成功
            html = etree.HTML(response.text)  # 解析html
            # 提取authenticity_token信息
            token = html.xpath("//div[@id='login']/form/input[1]/@value")[0]
            # print(token) 测试是否能够获取到token
        return token  # 返回信息

    # 实现登录
    def login(self):
        # 请求参数
        post_data = {
            "commit": "Sign in",
            "authenticity_token": self.get_token(),
            "login": self.user_name,
            "password": self.password,
            "webauthn - support": "supported"
        }
        # 发送登录请求
        response = self.session.post(self.post_url, headers=self.headers, data=post_data)
        if response.status_code == 200:  # 判断请求是否成功
            html = etree.HTML(response.text)  # 解析html
            # 获取注册号码
            register_number = html.xpath("//div[contains(@class,'Header-item')][last()]//strong")[0]
            print(f"注册号码为: {register_number.text}")
        else:
            print("登录失败")


if __name__ == '__main__':
    login = GitHubLogin(username='11611803@mail.sustech.edu.cn', password='zhaolida98')  # 创建登录类对象并传递输入的用户名与密码
    login.login()