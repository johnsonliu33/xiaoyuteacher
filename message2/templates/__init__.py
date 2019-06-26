#!/usr/bin/python
# coding=utf-8

"""
@contact: yu.jing@nio.com<br />
@description:<br />
@cases:<br />
"""

import sys
import pytest
import allure
from utils import httptool as requests
from utils.logger import log
from utils.comn_tool import get_test_data, get_data_path, comp_keys, show_json
from config.settings import APIS

case, precondition, parameter = get_test_data(get_data_path(__file__))


class Test(object):
    """
    """

    @pytest.fixture(scope="class", autouse=True)
    def prepare(self, request, mysql_new, env):
        with allure.step("测试数据准备:"):
            pass

        @allure.step("测试数据数据清理:")
        def fin():
            """
            Clean up test environment after testing
            """
            pass

        request.addfinalizer(fin)

    @pytest.mark.parametrize("checkpoint,headers,querystring,payload,expected", parameter, ids=case)
    def test_(self, env, api, checkpoint, headers, querystring, payload, expected, info_http):
        with allure.step("发起API请求"):
            log('INFO', 'Test case is: {0}'.format(checkpoint))

            url = env['host']['tsp'] + APIS['auth_group_new']
            info_http.switch_user(headers.get('role'), querystring.get('app_id'))
            r = info_http.post(url, data=payload, headers=headers, params=querystring)
            response = r.json()

        with allure.step("校验结果"):
            assert response["result_code"] == expected["result_code"]
            allure.attach('Actual result', show_json(response))
            allure.attach('Expected result', show_json(expected))
            if response['result_code'] == "success":
                pass