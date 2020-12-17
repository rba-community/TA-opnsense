# encoding = utf-8

import os
import sys
import time
import datetime
import json
import requests
from requests.exceptions import RequestException
import opnsense_constants as constant


def validate_input(helper, definition):
    # We have nothing to validate
    pass


def collect_events(helper, ew):
    # Get Credentials
    account = helper.get_arg('account')
    api_key = account["username"]
    api_secret = account["password"]
    host = account["host"]

    # Get Log Level
    log_level = helper.get_log_level()
    helper.set_log_level(log_level)
    helper.log_info(f'log_level="{log_level}"')

    # Get Interval
    interval = int(helper.get_arg('interval'))

    # Get Checkpoint
    key = 'opnsense_system'
    current_time = int(time.time())
    check_time = current_time - interval

    if helper.get_check_point(key):
        old_state = int(helper.get_check_point(key)['checkpoint'])
        helper.log_info('msg="Checkpoint found"')
        helper.log_debug(
            f'msg="Checkpoint information", checkpoint="{old_state}", interval="{interval}"')

        if check_time < old_state:
            helper.log_info(
                'msg="Skipping because interval is too close to previous run", action="stopped"')
            sys.exit(0)
        else:
            helper.log_info('msg="Running scheduled Interval"')

    else:
        helper.log_info('msg="Checkpoint file not found"')

    new_state = {'checkpoint': f'{current_time}'}

    # Get Proxy
    proxy = helper.get_proxy()

    if proxy:
        if proxy["proxy_username"]:
            helper.log_info('msg="Proxy is configured with authenticaiton"')
            helper.log_debug(
                f'proxy_type="{proxy["proxy_type"]}", proxy_url="{proxy["proxy_url"]}", proxy_port="{proxy["proxy_port"]}", proxy_username="{proxy["proxy_username"]}"')
            proxy_string = f'{proxy["proxy_type"]}://{proxy["proxy_username"]}:{proxy["proxy_password"]}@{proxy["proxy_url"]}:{proxy["proxy_port"]}'
        else:
            helper.log_info('msg="Proxy is configured with no authentication"')
            helper.log_debug(
                f'proxy_type="{proxy["proxy_type"]}", proxy_url="{proxy["proxy_url"]}", proxy_port="{proxy["proxy_port"]}"')
            proxy_string = f'{proxy["proxy_type"]}://{proxy["proxy_url"]}:{proxy["proxy_port"]}'

        proxy_config = {'http': proxy_string, 'https': proxy_string}
    else:
        proxy_config = None

    # URL
    url = f'https://{host}/{constant.api_firmware_status}'

    try:
        r = requests.get(url, proxies=proxy_config, auth=(
            api_key, api_secret), verify=False)
    except RequestException as e:
        helper.log_error('msg="Unable to make api call"')
        helper.log_debug(f'error_msg="{e}"')
        sys.exit(1)

    if r.status_code == 200:
        helper.log_info('msg="connection established", action="success"')
        response = json.loads(r.text)
        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(
        ), sourcetype=helper.get_sourcetype(), data=json.dumps(response))
        ew.write_event(event)
        helper.save_check_point(key, new_state)
        helper.log_info(
            f'msg="Updating Checkpoint", checkpoint="{new_state["checkpoint"]}"')
    else:
        helper.log_error('msg="unable to retrieve events", action="failed"')
        helper.log_debug(f'status_code="{r.status_code}"')
