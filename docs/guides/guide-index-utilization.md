# Index Utilization Guide

The out of the box Splunk configuration stores all data in the default index, main. It is encouraged to create a new index to ensure optimal performance, for setting retention policies, and for providing stricter access controls. For more information about how Splunk indexes work with add-ons, see [Splunk Docs: Add-ons and indexes](https://docs.splunk.com/Documentation/AddOns/released/Overview/Add-onsandindexes).

OPNsense has a variety of data sources that can be broken up in to separate indexes. The below table is an example of the data can be split up in to different indexes.

Index | Sourcetype(s)
----- | -----------
netauth | opnsense:access
netdhcp | opnsense:dhcpd
netfw | opnsense:filterlog
netfwsystem | opnsense, opnsense:cron, opnsense:system, opnsense:syslog
netids | opnsense:suricata, opnsense:suricata:json
netproxy | opnsense:squid, opnsense:lighttpd

New indexes can be created through configuration files or through Splunk web. See [Splunk Docs: Create events indexes](https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Setupmultipleindexes#Create_events_indexes_2) for more information.

This guide walks through the following steps to utilize created indexes:

1. [Set index at input time](#set-index-at-input-time)
1. [Change index at index time](#change-index-at-index-time)

## Set index at input time

Setting the index at input time can save some resources on the indexers. This requires a more advanced syslog configuration to ensure the files are properly broken up by data type.

If you followed the the guide for [Syslog Setup](../guide-syslog) then you should have multiple files broken up by the data source <small>(i.e. filterlog, suricata, dhcpd)</small>. We will create inputs to assign sourcetypes based on these files.

### Configure inputs

??? example "inputs.conf example"

    ```cfg title="inputs.conf"
    [monitor:///var/log/remote/opnsense/*/filterlog.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netfw

    [monitor:///var/log/remote/opnsense/*/access.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netauth

    [monitor:///var/log/remote/opnsense/*/dhcpd.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netdhcp

    [monitor:///var/log/remote/opnsense/*/suricata.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netids

    [monitor:///var/log/remote/opnsense/*/squid.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netproxy

    [monitor:///var/log/remote/opnsense/*/lighttpd.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netproxy

    [monitor:///var/log/remote/opnsense/*/openvpn.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netvpn

    [monitor:///var/log/remote/opnsense/*/cron.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netfwsystem

    [monitor:///var/log/remote/opnsense/*/catchall.log]
    disabled = 0
    host_segment = 5
    sourcetype = opnsense
    index = netfwsystem
    ```

## Change index at index time

The data can be changed to the correct index during index time operations. In this example `INGEST_EVAL` will be used. For more information about INGEST_EVAL see [Splunk Docs: Ingest Eval](https://docs.splunk.com/Documentation/Splunk/latest/Data/IngestEval).

These steps assume the data onboarding process, including index creation, has been completed and data is ready to be collected in Splunk.

The following changes will need to be made on the indexers.

1. Open the configuration file located at $SPLUNK_HOME/etc/apps/TA-opnsense/local/props.conf. This file and directory may have to be created.
1. Create a transforms statement for the `opnsense` sourcetype. This should be the sourcetype set in the inputs.conf file (see [Configure Inputs](../../getting-started/configure-inputs/configure-inputs#splunk-universal-forwarder-configuration)) for more information.

    !!! example ""

        ```cfg title="$SPLUNK_HOME/etc/apps/TA-opnsense/localprops.conf"
        [opnsense]
        TRANSFORMS-z_opn_change_index = opn_change_index
        ```

        Notice the "z" at the beginning of the name (TRANSFORMS-`z`_opn_change_index). This will cause this transform to run later in the index operations. This is important because this add-on utilizes a sourcetype transforms that must run before this transform.

1. Now a transform will need to be created at $SPLUNK_HOME/etc/apps/TA-opnsense/local/transforms.conf. This file may have to be created.
1. Create an `INGEST_EVAL` statement changing the data to the correct index based off the sourcetype.

    !!! example ""

        ```cfg title="$SPLUNK_HOME/etc/apps/TA-opnsense/local/transforms.conf"
        [opn_change_index] # this name MUST match the name in props.conf
        INGEST_EVAL = index=case(match(sourcetype, "dhcpd"), "netdhcp", match(sourcetype, "lighttpd|squid"), "netproxy", match(sourcetype, "access"), "netauth", match(sourcetype, "suricata"), "netids" , match(sourcetype, "cron|system|syslog|opnsense$"), "netfwsystem" , true(), index)
        ```

        This uses a case statement to perform a regex match on the sourcetype to then change to the appropriate index. Note that the match statement does not have to be used here and a simple `sourcetype=="opnsense:dhcpd"` statement could be used.

1. After you finish making the appropriate changes to the INGEST_EVAL command, splunk will need to be restarted for the changes to take affect.
1. Verify by searching the expected indexes for the data.

### Troubleshoot

Ensure that you ingest_eval command works by pasting it in to Splunk web using an eval statement replacing `index` with another name.

!!! example

    ```shell
    index=* sourcetype=opnsense*
    | eval test=case(match(sourcetype, "dhcpd"), "netdhcp", match(sourcetype, "lighttpd|squid"), "netproxy", match(sourcetype, "access"), "netauth", match(sourcetype, "suricata"), "netids" , match(sourcetype, "cron|system|syslog|opnsense$"), "netfwsystem" , true(), index)
    | stats count by sourcetype, test
    ```

If there are no errors and the command works as expected, be sure that splunk was restarted. `$SPLUNK_HOME/bin/splunk btool check` can also be run to see if there are any errors in the configuration file.

If there are no errors, check the spelling in the props.conf and transforms.conf for the name given. The name set in props.conf must match the stanza in transforms.conf.

--8<-- "includes/abbreviations.md"
