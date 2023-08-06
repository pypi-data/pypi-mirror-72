

class AppClient(object):
    """
    通行证微服务客户端
    """

    def __init__(self, _app):
        """
        初始化
        :param _app:
        """
        config = _app.config
        self.passport_service_url = config['PASSPORT_SERVICE_URL']
        self.app_url = config['DEFAULT_APP_URL']
        self.access_key_id = config['DEFAULT_APP_ACCESS_KEY_ID']
        self.access_key_secret = config['DEFAULT_APP_ACCESS_KEY_SECRET']
        self.access_token = ''

    def post(self, url, json_data):
        """
        发送POST请求
        :param url:
        :param json_data:
        :return:
        """
        from .common import app_post
        return app_post(client=self, url=url, json_data=json_data)

    def get_access_token(self):
        """
        获取access_token
        :return:
        """

        from .common import post

        if not self.access_token:
            json_data = {
                'access_key_id': self.access_key_id,
                'access_key_secret': self.access_key_secret
            }
            res = post(
                url='%s/user/access/token' % self.passport_service_url,
                json_data=json_data,
                headers=None
            )
            if res and 'data' in res and 'access_token' in res['data']:
                # print('[[get_access_token: ', res['data']['access_token'])
                self.access_token = res['data']['access_token']
                return self.access_token
            return None
        return self.access_token

    def user_register(self, username, password):
        """
        用户注册
        :param username:
        :param password:
        :return:
        """
        json_data = {
            'username': username,
            'password': password
        }
        res = self.post(
            url='/user/register',
            json_data=json_data
        )
        return res

    def user_login(self, username, password):
        """
        用户登录
        :param username:
        :param password:
        :return:
        """
        json_data = {
            'username': username,
            'password': password
        }
        res = self.post(
            url='/user/login',
            json_data=json_data
        )
        print(res)
        return res

    def user_logout(self, user_token):
        """
        用户登出
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = self.post(
            url='/user/logout',
            json_data=json_data
        )
        return res

    def user_info(self, user_token):
        """
        用户信息
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = self.post(
            url='/user/info',
            json_data=json_data
        )
        return res

    def admin_user_list(self, user_token):
        """
        [后台]用户列表
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = self.post(
            url='/admin/user/list',
            json_data=json_data
        )
        return res

    def admin_user_info(self, user_token, user_id):
        """
        [后台]用户信息
        :param user_token:
        :param user_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'user_id': user_id
        }
        res = self.post(
            url='/admin/user/info',
            json_data=json_data
        )
        return res

    def admin_user_modify(self, user_token, user_id, modify_user_info):
        """
        [后台]用户编辑(创建)
        :param user_token:
        :param user_id:
        :param modify_user_info:
        :return:
        """
        json_data = {
            'token': user_token,
            'user_id': user_id,
            'modify_user_info': modify_user_info
        }
        res = self.post(
            url='/admin/user/modify',
            json_data=json_data
        )
        return res
