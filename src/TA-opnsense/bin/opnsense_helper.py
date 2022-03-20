
# encoding = utf-8

import time
import os
import requests
from requests import RequestException
import json


def sendit(opn_host, event_name, helper, endpoint=None, method='GET', params=None):
    """Send Request
    :param opn_host: Host server to query
    :param event_name: Name of event performing the request
    :param helper: Splunk Helper
    :param endpoint: API endpoint
    :param method: Method for new Request
    :param params: Parameters for request
    :param params: Port to use for call
    :return: response
    """
    # Skip run if too close to previous run interval
    if not opn_checkpointer(opn_host, event_name, helper):
        return False

    account = helper.get_arg('account')
    api_key = account['username']
    api_secret = account["password"]
    verify_cert = account["verify_cert"]
    api_port = None
    try:
        account['api_port']
    except KeyError:
        helper.log_info(f'msg="API port not defined", hostname="{opn_host}"')
    else:
        api_port = account['api_port']

    if api_port:
        url = f'https://{opn_host}:{api_port}/{endpoint}'
    else:
        url = f'https://{opn_host}/{endpoint}'

    helper.log_info(
        f'event_name="{event_name}", msg="starting {event_name} collection", hostname="{opn_host}"')

    # Get Proxy Information
    proxy = helper.get_proxy()
    if proxy:
        if proxy["proxy_username"]:
            helper.log_info('msg="Proxy is configured with authentication"')
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

    if verify_cert == "1":
        certificate = account["certificate"]
        if os.path.isfile(certificate):
            check_cert = certificate
        # Check for Relative path to $SPLUNK_HOME/etc/auth
        elif os.path.isfile(os.path.join(os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'auth'), certificate)):
            check_cert = os.path.join(os.path.join(
                os.environ['SPLUNK_HOME'], 'etc', 'auth'), certificate)
        else:
            helper.log_error(
                f'msg="Certificate not found", action="failed", hostname="{opn_host}"')
            helper.log_debug(
                f'msg="missing certificate", certificate_location="{certificate}", action="failed", hostname="'
                f'{opn_host}"')
            return False
        helper.log_info(
            f'msg="found certificate", action="success", hostname="{opn_host}"')
        helper.log_debug(
            f'msg="found certificate", certificate_location="{check_cert}", action="success", hostname="{opn_host}"')
    else:
        helper.log_info(
            f'msg="Certificate Check Disabled", hostname="{opn_host}"')
        check_cert = False

    try:
        helper.log_info(
            f'event_name="{event_name}", msg="starting http request", action="starting", hostname="{opn_host}"')
        r = requests.request(method, url, proxies=proxy_config, auth=(api_key, api_secret), verify=check_cert)
    except RequestException as e:
        helper.log_error(
            f'event_name="{event_name}", error_msg="Unable to complete request", action="failed", hostname="'
            f'{opn_host}"')
        helper.log_debug(
            f'event_name="{event_name}", hostname="{opn_host}", error_msg="{e}"')
        return False

    if r.status_code == 200:
        helper.log_info(
            f'event_name="{event_name}", msg="request completed", action="success", hostname="{opn_host}"')
        return json.loads(r.text)
    else:
        helper.log_error(
            f'event_name="{event_name}", error_msg="Unable to retrieve information", action="failed", hostname="'
            f'{opn_host}"')
        helper.log_debug(
            f'event_name="{event_name}", hostname="{opn_host}", status_code="{r.status_code}"')
        return False


def opn_checkpointer(opn_host, event_name, helper, set_checkpoint=False):
        """Checks and returns checkpoint

        :param opn_host: Host to check for checkpointer
        :param event_name: Name of the event
        :param helper: Splunk Helper
        :param set_checkpoint: Whether to set a new checkpoint
        :return: bool
        """
        # Get Interval
        interval = helper.get_arg('interval')

        try:
            int(interval)
        except ValueError:
            helper.log_info(f'msg="Checkpointer not needed, using cron schedule", hostname="{opn_host}", event_name="{event_name}"')
            return True
        else:
            interval = int(interval)

        current_time = int(time.time())
        check_time = current_time - interval + 60
        key = f'{opn_host}_{event_name}'

        if set_checkpoint:
            new_state = int(time.time())
            helper.save_check_point(key, new_state)
            helper.log_info(
                f'msg="Updating Checkpoint", checkpoint="{new_state}", hostname="{opn_host}", event_name="'
                f'{event_name}"')
            return True

        if helper.get_check_point(key):
            old_state = int(helper.get_check_point(key))
            helper.log_info(
                f'event_name="{event_name}", msg="Checkpoint found", hostname="{opn_host}"')
            helper.log_debug(
                f'event_name="{event_name}", msg="Checkpoint information", checkpoint="{old_state}", interval="'
                f'{interval}", hostname="{opn_host}"')

            if check_time < old_state:
                helper.log_info(
                    f'event_name="{event_name}", msg="Skipping because interval is too close to previous run", '
                    f'action="aborted", hostname="{opn_host}"')
                return False
            else:
                helper.log_info(
                    f'event_name="{event_name}", msg="Running scheduled Interval", hostname="{opn_host}"')

        else:
            helper.log_info(
                f'event_name="{event_name}", msg="Checkpoint file not found", hostname="{opn_host}"')
        return True
