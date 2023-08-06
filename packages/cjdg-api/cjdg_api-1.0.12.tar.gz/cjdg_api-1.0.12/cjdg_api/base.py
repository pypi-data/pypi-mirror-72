# 开放平台接口基类
import requests


def request_accesstoken(acc: str, pwd: str) -> str:
    # 请求accesstooke函数
    url = "http://bms.microc.cn/shopguide/api/auth/logon"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        # print(response.json())
        accessToken = response.json().get("accessToken")
        return accessToken


class base:
    def __init__(self, token, app_secret=None):
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, method="GET", url=None, json={}):
        host_name = "http://bms.microc.cn/shopguide/api/"
        # host_name = "http://test.xxynet.com/shopguide/api/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"

        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret

        if method == "GET":
            params.update(data)
            response = requests.get(url, params=params)
        elif method == "POST":
            # print(method, data, json)
            if data:
                response = requests.post(url, params=params, data=data)
            elif json:
                response = requests.post(url, params=params, json=json)
            else:
                raise ValueError("网络请求数据格式错误。")

        else:
            raise ValueError("请求方法错误。")
        # print(url, response.status_code)
        if response.status_code == 200:
            # print(data, response.json())
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw
