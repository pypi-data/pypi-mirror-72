import os
import json
import uuid
import time
import pickle
import random
import hashlib
import requests
from instapv import DeviceGenerator, Config, Tools
from instapv.exceptions import *
from instapv.logger import Logger
from instapv.ig.user import User
from instapv.ig.media import Media
from instapv.ig.business import Business 
from instapv.ig.live import Live 
from instapv.ig.account import Account 
from urllib.parse import urlencode

# Ignore InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Logger for debugging
log = Logger()


if not os.path.exists('cache'):
    os.mkdir('cache')

class Bot:


    def __init__(self, username: str, password: str, debug: bool = False, login_cache = False):
        self.cache = hashlib.md5(username.encode('utf-8')).hexdigest()
        self.config = Config()
        self.tools = Tools()
        self.device = DeviceGenerator()
        self.is_logged_in = False
        self.last_response = None
        self.debug = debug
        self.login_cache = login_cache
        self.username = username
        if not os.path.exists(f'cache/{self.username}'):
            os.mkdir(f'cache/{self.username}')
        try:
            if os.path.exists(f'cache/{username}/{self.cache}.pkl'):
                if self.debug:
                    log.info('Loading session...')
                self.session(False)
            else:
                if self.debug:
                    log.warn('Creating new session ...')
                self.req = requests.Session()
                self.login_cache = False
        except IOError:
            if self.debug:
                log.warn('Creating new session ...')
            self.req = requests.Session()
        self.set_user(username, password)
        self.device_id = self.device.generate_device_id(self._s.hexdigest())

        # Call Classes
        self.user  = User(self)
        self.media = Media(self)
        self.business = Business(self)
        self.live = Live(self)
        self.account = Account(self)


    def set_proxy(self, proxy=None):
        if proxy is not None:
            proxies = {'http': proxy}
            self.req.proxies.update(proxies)
        else:
            self.req.proxies.clear()

    def set_user(self, username: str, password: str):
        self._s = hashlib.md5()
        self._s.update(username.encode('utf-8') + password.encode('utf-8'))
        self.username = username
        self.password = password
        self.uuid = self.tools.generate_uuid(True)

    def session(self, create=False):
        if create:
            with open(f'cache/{self.username}/{self.cache}.pkl', 'wb') as f:
                pickle.dump(self.req, f)
        else:
            with open(f'cache/{self.username}/{self.cache}.pkl', 'rb') as f:
                self.req = pickle.load(f)

    def login(self, relogin=False):
        if self.login_cache and not relogin:
            with open(f'cache/{self.username}/data.json', 'r', encoding='utf-8') as _data:
                _dict = json.loads(_data.read())
            self.is_logged_in = _dict['is_logged_in']
            self.account_id = _dict['account_id']
            self.rank_token = _dict['rank_token']
            self.token = _dict['token']
            self.phone_id = _dict['phone_id']
            return True
        else:
            self.is_logged_in = False
            if not self.is_logged_in:
                endpoint = f'si/fetch_headers/?challenge_type=signup&guid={self.tools.generate_uuid(False)}'
                request  = self.request(endpoint, login=True)
                if request: 
                    data = {
                        'phone_id': self.tools.generate_uuid(True),
                        '_csrftoken': self.last_response.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'
                    }
                    if self.request('accounts/login/', data, True):
                        self.phone_id = self.tools.generate_uuid(True)
                        self.is_logged_in = True
                        self.account_id = self.last_json_response["logged_in_user"]["pk"]
                        self.rank_token = self.uuid
                        self.token = self.last_response.cookies["csrftoken"]
                        data = {
                            'phone_id': self.phone_id,
                            'is_logged_in': self.is_logged_in,
                            'account_id': self.account_id,
                            'rank_token': self.rank_token,
                            'token': self.token
                        }
                        # os.mkfifo('cache/{self.username}/data.json')
                        with open(f'cache/{self.username}/data.json', 'w', encoding='utf-8') as _f:
                            json.dump(data, _f, ensure_ascii=False, sort_keys=True ,indent=4)
                        if (not os.path.exists(f'cache/{self.cache}.pkl')):
                            pass
                        if (self.debug):
                            log.info(f'INFO: LOGGED IN AS {self.username}\n')
                        self.sync()
                        self.load_user_list()
                        self.get_inbox()
                        self.get_activity()
                        return True

    def sync(self):
        data = {
            '_uuid': self.uuid,
            '_uid': self.account_id,
            'id': self.account_id,
            '_csrftoken': self.token,
            'experiments': self.config.EXPERIMENTS
        }
        return self.request('qe/sync/', params=data)

    def load_user_list(self):
        return self.request('friendships/autocomplete_user_list/')

    def time_line_feed(self):
        return self.request('feed/timeline/')
    
    def get_inbox(self):
        inbox = self.request('direct_v2/inbox/?')
        return inbox

    def get_activity(self):
        activity = self.request('news/inbox/?')
        return activity

    def request(self, endpoint: str, params: dict = None, login: bool = False, signed_post: bool = True, files = None, get_params: dict = None):
        if self.debug:
            log.info(f"REQUEST: {self.config.API_URL + endpoint}")

        if not self.is_logged_in and not login:
            return False

        self.req.headers.update({'Connection': 'close',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie2': '$Version=1',
            'Accept-Language': 'en-US',
            'User-Agent': self.device.build_user_agent()
        })

        if params:
            if signed_post:
                params = self.tools.generate_signature(
                    json.dumps(params)
                )
            if files:
                self.req.headers.update({
                    'Content-Type': 'application/octet-stream',
                    'Content-Transfer-Encoding': 'binary'
                })
                response = self.req.post(self.config.API_URL + endpoint, files=files, data=params, verify=True)
            else:
                response = self.req.post(self.config.API_URL + endpoint, data=params, verify=True)
        else:
            if get_params:
                response = self.req.get(self.config.API_URL + endpoint, params=urlencode(get_params), verify=True)
            else:
                response = self.req.get(self.config.API_URL + endpoint, params=get_params , verify=True)
        if self.debug:
            log.info(f'CODE: {str(response.status_code)}', True)
            log.info(f"RESPONSE: {response.text}\n")

        if response.status_code == 200:
            self.last_response = response
            self.last_json_response = json.loads(response.text)
            self.session(True)
            return self.last_json_response
        elif response.status_code == 405:
            raise AccessDeniedException(f'Access deniend to request: {self.config.API_URL + endpoint}')
        else:
            if (self.debug):
                log.error(f'CODE: {str(response.status_code)}')
            try:
                self.last_response = response
                self.last_json_response = json.loads(response.text)
                if self.last_json_response['message'] == 'login_required':
                    os.remove(f'cache/{self.username}/{self.cache}.pkl')
                    raise LogedOutException('Ssaved account password has changed and the old session has been deleted. Please log back in.')
                if self.last_json_response['message'] == 'challenge_required':
                    raise ChallengeRequiredException('Challenge required')
                if self.last_json_response['message'] == 'The password you entered is incorrect. Please try again.':
                    os.remove(f'cache/{self.username}/{self.cache}.pkl')
                    raise InvalidCredentialsException(self.last_json_response['message'])
                if (self.debug):
                    log.info(f'RESPONSE: {str(self.last_json_response)}')
            except SentryBlockException:
                raise
            return self.last_json_response
