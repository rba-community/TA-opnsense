# Configure Splunk Input

**Objective**: Set the sourcetype to `opnsense` in the inputs.conf file on the forwarder.

## Create new indexes

???+ info "Optional"
    If you do not wish to create a new index, skip to [Splunk Universal Forwarder Configuration](#splunk-universal-forwarder-configuration).

Splunk stores data in indexes. This add-on may be configured to send to a custom event index instead of the default index, main. For more information and steps to create a new index, see [Splunk Docs: Create events indexes](https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Setupmultipleindexes#Create_events_indexes_2).

### Purpose for creating new indexes

The out of the box Splunk configuration stores all data in the default index, main. It is encouraged to create a new index to ensure optimal performance, for setting retention policies, and for providing stricter access controls. For more information about how Splunk indexes work with add-ons, see [Splunk Docs: Add-ons and indexes](https://docs.splunk.com/Documentation/AddOns/released/Overview/Add-onsandindexes).

OPNsense has a variety of data sources that can be broken up in to separate indexes. For more information and some examples on creating and utilizing indexes see the [Guide: Index Utilization](../../../guides/guide-index-utilization) in this documentation.

## Splunk Universal Forwarder Configuration

Download the latest [Splunk Universal Forwarder (UF)](https://www.splunk.com/en_us/download/universal-forwarder.html) appropriate for your server.

??? question "Don't have a syslog server setup yet?"
    See [Syslog Setup](../../../guides/guide-syslog) for guided steps. If you don't want to use a syslog server see [Splunk Docs: Get data from TCP and UDP ports](https://docs.splunk.com/Documentation/Splunk/latest/Data/Monitornetworkports) and skip these steps.

Install the UF according to [Splunk Docs: Install the Universal Forwarder](https://docs.splunk.com/Documentation/Forwarder/latest/Forwarder/Installtheuniversalforwardersoftware) on the server designated as your syslog server.

Once installed the configurations can be made. The following is a sample inputs.conf that can be pushed using a deployment server or configured on the UF itself.

```cfg title="inputs.conf"
[monitor:///var/log/remote/opnsense]
disabled = 0
host_segment = 5
sourcetype = opnsense
# optionally specify an index, if configured.
index = netfw
```

Push the configuration to the forwarder, if using a deployment server, or restart the UF if configuring on the UF itself.

## Verify

Verify the setup has completed successfully by navigating to Splunk web and running a search similar to the following:

```shell
index=<chosen index> sourcetype=opnsense*
```

If you see data then you are all set! Proceed to [Configuring Modular Inputs](configure-modinput.md) or start visualizing your data by downloading and installing the [OPNsense App for Splunk](https://splunkbase.splunk.com/app/5372).

If you are not seeing your data, see [Troubleshooting Monitoring Inputs](../troubleshooting/troubleshoot-inputs.md).

--8<-- "includes/abbreviations.md"
