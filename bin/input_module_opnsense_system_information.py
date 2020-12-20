# encoding = utf-8

import os
import time
import json
import requests
from requests import RequestException
import opnsense_constants as const

cert_dir = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'auth')


def validate_input(helper, definition):
    # We have nothing to verify
    pass


def collect_events(helper, ew):
    # Get Credentials
    account = helper.get_arg('account')
    api_key = account["username"]
    api_secret = account["password"]
    host = account["host"]
    certificate = account["certificate"]
    verify_cert = account["verify_cert"]

    if verify_cert:
        cert = os.path.join(cert_dir, certificate)
        if not os.path.isfile(cert):
            helper.log_error(f'msg="Certificate not found", action="failed"')
            helper.log_debug(f'msg="missing certificate", certificate_location="{cert}", action="failed"')
            return False
        helper.log_info('msg="found certificate", action="success"')
        helper.log_debug(f'msg="found certificate", certificate_location="{cert}", action="success"')
    else:
        cert = False

    # Get Log Level
    log_level = helper.get_log_level()
    helper.set_log_level(log_level)
    helper.log_info(f'log_level="{log_level}"')

    # Get Interval
    interval = int(helper.get_arg('interval'))

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

    def check_run(key, event_name):
        """Checks and returns checkpoint

        :param key: key to check
        :param event_name: Name of the event
        :return: bool
        """
        current_time = int(time.time())
        check_time = current_time - interval

        if helper.get_check_point(key):
            old_state = int(helper.get_check_point(key))
            helper.log_info(f'event_name="{event_name}", msg="Checkpoint found"')
            helper.log_debug(
                f'event_name="{event_name}", msg="Checkpoint information", checkpoint="{old_state}", interval="{interval}"')

            if check_time < old_state:
                helper.log_info(
                    f'event_name="{event_name}", msg="Skipping because interval is too close to previous run", '
                    f'action="aborted"')
                return False
            else:
                helper.log_info(f'event_name="{event_name}", msg="Running scheduled Interval"')

        else:
            helper.log_info(f'event_name="{event_name}", msg="Checkpoint file not found"')

        return True

    def sendit(key, url, event_name):
        """Send Request

        :param key: Key for checkpointer
        :param url: url to send request
        :param event_name: Name of event performing the request
        :return: response
        """
        # Skip run if too close to previous run interval
        if not check_run(key, event_name):
            return False

        try:
            r = requests.get(url, proxies=proxy_config, auth=(api_key, api_secret), verify=cert)
            helper.log_debug(f'msg="connection info", proxy_config="{proxy_config}", certificate="{cert}"')

            if r.status_code == 200:
                helper.log_info(f'event_name="{event_name}", msg="connection established", action="success"')
                return json.loads(r.text)
            else:
                helper.log_info(f'event_name="{event_name}", msg="connection failed", action="failed"')
                helper.log_debug(f'event_name="{event_name}", status_code="{r.status_code}", action="failed"')
                return False

        except RequestException as e:
            helper.log_error(f'event_name="{event_name}", msg="Unable to make api call"')
            helper.log_debug(f'event_name="{event_name}", error_msg="{e}"')
            return False

    def get_system_status():
        event_name = 'system_status'
        helper.log_info(f'event_name="{event_name}", msg="starting system status collection')
        key = 'opnsense_system'
        url = f'https://{host}/{const.api_firmware_status}'
        response = sendit(key, url, event_name)

        # Return if Applicable
        if not response:
            return False

        response['collection_type'] = 'system'
        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(
        ), sourcetype=helper.get_sourcetype(), host=host, data=json.dumps(response))
        ew.write_event(event)

        # Write checkpoint
        new_state = int(time.time())
        helper.save_check_point(key, new_state)
        helper.log_info(
            f'event_name="{event_name}", msg="Updating Checkpoint", checkpoint="{new_state}"')
        helper.log_info(f'event_name="{event_name}", msg="completed", action="success"')
        return True

    def get_plugin_info():
        event_name = 'plugin_info'
        helper.log_info(f'event_name="{event_name}", msg="starting system plugin information collection')
        key = 'opnsense_info'
        url = f'https://{host}/{const.api_firmware_info}'
        response = sendit(key, url, event_name)

        # Return if Applicable
        if not response:
            return False

        event_count = 0
        for item in response['plugin']:
            if item['installed'] == '1':
                item['collection_type'] = 'plugin'
                event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), host=host, data=json.dumps(item))
                ew.write_event(event)
                event_count += 1

        # Write checkpoint
        new_state = int(time.time())
        helper.save_check_point(key, new_state)
        helper.log_info(f'event_name="{event_name}", msg="completed", action="success", events_collected="{event_count}"')
        return True

    get_system_status()
    get_plugin_info()
