# Copyright 2022 NEC Corporation#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from common_libs.common.dbconnect import *  # noqa: F403
import requests
import json


class APIClientCommon:
    def __init__(self, event_settings):

        self.request_method = event_settings["request_method"]
        self.url = event_settings["api_url"]
        self.headers = json.loads(event_settings["header"])
        self.proxy = {
            "http": event_settings["proxy"],
            "https": event_settings["proxy"]
        }
        self.auth_token = event_settings["auth_token"]
        self.username = event_settings["username"]
        self.password = event_settings["password"]

    def call_api(self, parameter):
        self.parameter = parameter  # APIのパラメータ
        try:
            response = requests.request(
                method=self.request_method,
                url=self.url,
                headers=self.headers,
                params=parameter if self.request_method == "GET" else None,
                data=json.dumps(self.parameter) if self.request_method == "POST" else None,
                proxies=self.proxy
            )
            # ステータス400系500系は例外へ
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            http_error = f"HTTP Error: {e}"
            error_message = f"Error Message: {e.response.text}"
            print(http_error)
            print(error_message)
