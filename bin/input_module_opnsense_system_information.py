# encoding = utf-8

import opnsense_constants as const
from opnsense_helper import *


def validate_input(helper, definition):
    # We have nothing to verify
    pass


def collect_events(helper, ew):
    account = helper.get_arg('account')
    host = account["host"]

    # Get Log Level
    log_level = helper.get_log_level()
    helper.set_log_level(log_level)
    helper.log_info(f'log_level="{log_level}"')


    def get_system_status():
        event_name = 'system_status'
        helper.log_info(
            f'event_name="{event_name}", msg="starting system status collection", hostname="{host}"')
        response = sendit(host, event_name, helper, endpoint=const.api_firmware_status, method='POST')

        if not response:
            return False

        # Create Splunk Event
        response['collection_type'] = 'system'
        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(
        ), sourcetype=helper.get_sourcetype(), host=host, data=json.dumps(response))
        ew.write_event(event)

        # Checkpointer
        opn_checkpointer(host, event_name, helper, set_checkpoint=True)


    def get_plugin_info():
        event_name = 'plugin_info'
        helper.log_info(
            f'event_name="{event_name}", msg="starting system plugin information collection", hostname="{host}"')
        response = sendit(host, event_name, helper, endpoint=const.api_firmware_info)

        if not response:
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

        # Checkpointer
        opn_checkpointer(host, event_name, helper, set_checkpoint=True)


    get_system_status()
    get_plugin_info()
