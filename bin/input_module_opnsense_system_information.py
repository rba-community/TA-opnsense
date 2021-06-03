# encoding = utf-8

import os
import time
import json
import requests
from requests import RequestException
import opnsense_constants as const


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

    if verify_cert == "1":
        # Check for absolute path
        if os.path.isfile(certificate):
            check_cert = certificate

        # Check for Relative path to $SPLUNK_HOME/etc/auth
        elif os.path.isfile(os.path.join(os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'auth'), certificate)):
            check_cert = os.path.join(os.path.join(
                os.environ['SPLUNK_HOME'], 'etc', 'auth'), certificate)

        # Fail to locate certificate
        else:
            helper.log_error(
                f'msg="Certificate not found", action="failed", hostname="{host}"')
            helper.log_debug(
                f'msg="missing certificate", certificate_location="{certificate}", action="failed", hostname="{host}"')
            return False

        helper.log_info(
            f'msg="found certificate", action="success", hostname="{host}"')
        helper.log_debug(
            f'msg="found certificate", certificate_location="{check_cert}", action="success", hostname="{host}"')

    else:
        helper.log_info(
            f'msg="Certificate Check Disabled", hostname="{host}"')
        check_cert = False

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
        check_time = current_time - interval + 60

        if helper.get_check_point(key):
            old_state = int(helper.get_check_point(key))
            helper.log_info(
                f'event_name="{event_name}", msg="Checkpoint found", hostname="{host}"')
            helper.log_debug(
                f'event_name="{event_name}", msg="Checkpoint information", checkpoint="{old_state}", interval="{interval}", hostname="{host}"')

            if check_time < old_state:
                helper.log_info(
                    f'event_name="{event_name}", msg="Skipping because interval is too close to previous run", '
                    f'action="aborted", hostname="{host}"')
                return False
            else:
                helper.log_info(
                    f'event_name="{event_name}", msg="Running scheduled Interval", hostname="{host}"')

        else:
            helper.log_info(
                f'event_name="{event_name}", msg="Checkpoint file not found", hostname="{host}"')

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
            return False, None

        try:
            r = requests.get(url, proxies=proxy_config, auth=(
                api_key, api_secret), verify=check_cert)
            helper.log_debug(
                f'msg="connection info", proxy_config="{proxy_config}", certificate="{check_cert}", hostname="{host}"')

            if r.status_code == 200:
                helper.log_info(
                    f'event_name="{event_name}", msg="connection established", action="success", hostname="{host}"')
                return True, json.loads(r.text)
            else:
                helper.log_info(
                    f'event_name="{event_name}", msg="connection failed", action="failed", hostname="{host}"')
                helper.log_debug(
                    f'event_name="{event_name}", status_code="{r.status_code}", action="failed", hostname="{host}"')
                return False, None

        except RequestException as e:
            helper.log_error(
                f'event_name="{event_name}", msg="Unable to make api call", hostname="{host}"')
            helper.log_debug(
                f'event_name="{event_name}", error_msg="{e}", hostname="{host}"')
            return False, None

    def get_system_status():
        event_name = 'system_status'
        helper.log_info(
            f'event_name="{event_name}", msg="starting system status collection", hostname="{host}"')
        key = f'opnsense_system_{host}'
        url = f'https://{host}/{const.api_firmware_status}'
        r_succeeded, response = sendit(key, url, event_name)

        # Return if Applicable
        if not r_succeeded:
            return False

        response['collection_type'] = 'system'
        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(
        ), sourcetype=helper.get_sourcetype(), host=host, data=json.dumps(response))
        ew.write_event(event)

        # Write checkpoint
        new_state = int(time.time())
        helper.save_check_point(key, new_state)
        helper.log_info(
            f'event_name="{event_name}", msg="Updating Checkpoint", checkpoint="{new_state}", hostname="{host}"')
        helper.log_info(
            f'event_name="{event_name}", msg="completed", action="success", hostname="{host}"')
        return True

    def get_plugin_info():
        event_name = 'plugin_info'
        helper.log_info(
            f'event_name="{event_name}", msg="starting system plugin information collection", hostname="{host}"')
        key = f'opnsense_info_{host}'
        url = f'https://{host}/{const.api_firmware_info}'
        r_succeeded, response = sendit(key, url, event_name)

        # Return if Applicable
        if not r_succeeded:
            return False

        plugin_count = 0
        package_count = 0
        for item in response['package']:
            if item['installed'] == '1':
                item['collection_type'] = 'package'
                event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(),
                                         sourcetype=helper.get_sourcetype(), host=host, data=json.dumps(item))
                ew.write_event(event)
                package_count += 1

        for item in response['plugin']:
            if item['installed'] == '1':
                item['collection_type'] = 'plugin'
                event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(
                ), sourcetype=helper.get_sourcetype(), host=host, data=json.dumps(item))
                ew.write_event(event)
                plugin_count += 1

        event_count = package_count + plugin_count

        # Write checkpoint
        new_state = int(time.time())
        helper.save_check_point(key, new_state)
        helper.log_info(f'event_name="{event_name}", msg="completed", action="success", events_collected="'
                        f'{event_count}", package_count="{package_count}", plugin_count="{plugin_count}", hostname='
                        f'"{host}"')
        return True

    get_system_status()
    get_plugin_info()
