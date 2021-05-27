# TA-opnsense - Add-on for OPNsense® Firewall

[![GitHub](https://img.shields.io/github/license/ZachChristensen28/TA-opnsense)]()

 Info | Description
------|----------
Version | 1.4.0 - See on [Splunkbase](https://splunkbase.splunk.com/app/4538/)
Vendor Product Version | [OPNsense® 20.7](https://opnsense.org/)
Add-on has a web UI | No. This add-on does not contain any views.

**NEW:** Try the new [OPNsense App for Splunk](https://github.com/ZachChristensen28/Opnsense_App_for_Splunk)!

The TA-opnsense Add-on allows Splunk data administrators to map the OPNsense® firewall events to the [CIM](https://docs.splunk.com/Splexicon:CommonInformationModel) enabling the data to be used with other Splunk Apps, such as Enterprise Security.

```TEXT
Version 1.4.0

```

Contributors
- [J-C-B](https://github.com/J-C-B)
- [dgersting](https://github.com/dgersting)
- [xpac1985](https://github.com/xpac1985)

### Where to Install

Splunk platform Instance type | Supported | Required | Actions required/ Comments
----------------------------- | --------- | -------- | --------------------------
Search Heads | Yes | Yes | Install this add-on to all search heads
Indexers | Yes | Conditional | Not required if heavy forwarders are used to collect data. Required if using Universal or Light Forwarders.
Heavy Forwarders | Yes | Conditional | Required, if HFs are used to collect this data source.

\* For more information, see Splunk's [documentation](https://docs.splunk.com/Documentation/AddOns/released/Overview/Installingadd-ons) on installing Add-ons.

## Input Requirements

Set the sourcetype to "opnsense" in the inputs.conf file on the forwarder.

\* ***See [Installation Walkthrough](#Installation-Walkthrough) for more information***

## IDS (Suricata) Logging Recommendations

Logging IDS events using the eve syslog output setting will provide the most verbose output. Additionally, the payload can be logged by changing the advanced settings.

## Installation Walkthrough

### Data on-boarding using syslog (Rsyslog Example)

Rsyslog is a default package on most linux distros. The OPNsense firewall can be setup to send logs via syslog to a configured Rsyslog server for a Splunk Forwarder to monitor. Below is a basic configuration to get started with data on-boarding. Note: This may not reflect rsyslog best practices but should be used a starting point.

#### Rsyslog Basic Configuration

Tested with Rsyslog version: rsyslogd 8.32.0 on RHEL/CentOS/Ubuntu

The rsyslog configuration file is located in `/etc/rsyslog.conf`

Open the rsyslog configuration file with your favorite text editor. Place the following in the configuration file or uncomment if already present:

```SHELL
# /etc/rsyslog.conf

# Load Modules
module(load="imudp") # provides UDP syslog reception

# OMFILE Global Permissions
module(load="builtin:omfile" dirCreateMode="0750" dirOwner="root" dirGroup="splunk" fileCreateMode="0640" fileOwner="root" fileGroup="splunk")

# DynaFile Template
template(name="t_opnsense" type="string" string="/var/log/opnsense/%hostname%/opnsense.log")

# ruleset
ruleset(name="r_opnsense" queue.type="linkedlist"){
  action(type="omfile" dynaFile="t_opnsense")
}

# Use port 514 for OPNsense data
input(type="imudp" port="514" ruleset="r_opnsense")
```

Once the above has been configured, Save & Close the file. Then restart the rsyslog process:

`systemctl restart rsyslog`

Verify rsyslog is running with: `service rsyslog status`

The above will create a new file in `/var/log/` which a Splunk Forwarder can monitor and forward to the Splunk Indexers.

##### Troubleshooting

- Ensure firewall rules are configured to allow the rsyslog listening port (514/udp)
- Ensure SELinux is not blocking rsyslog from writing to the file. This may occur if you write data outside of `/var/log`

#### Basic Log Rotation Strategy for syslog server

It is necessary to rotate the logs to ensure the disk space does not fill up. Below is a basic example to get started with log rotation.

The following uses the builtin package `logrotate`. The configuration file can be found at `/etc/logrotate.conf`

Start by creating a new file in `/etc/logrotate.d`. For this example, we will use a created file in `/etc/logrotate.d/opnsense`

Add the following to the file.

```SHELL
/var/log/opnsense/*/*.log
{
        rotate 7
        daily
        missingok
        create 0640 root splunk
        notifempty
        compress
        dateext
        dateformat -%Y-%m-%d
        dateyesterday
        sharedscripts
        postrotate
                /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true
        endscript
}
```

The above may not work for every situation. Please check the man pages for logroate if experiencing issues. It may also be helpful to look at existing configuration files located in `/etc/logrotate.d` for reference.

#### OPNsense Syslog Configuration

The following is necessary to now send syslog data from the OPNsense device to the newly configured syslog server.

Administrator access to the OPNsense Web GUI will be required to perform the following steps.

1. Log into the OPNsense firewall.
1. Navigate to: System > Settings > Logging/targets.
1. Click the `+` (plus sign) to add a new syslog destination.
  - Ensure the `Enabled` checkbox is checked.
  - Transport = UDP(4)
  - Applications = (Leave Blank) to select everything
  - Levels = (Leave default setting)
  - Facilities = (Leave Blank) to select everything
  - Hostname = FQDN or IP of the syslog server configured in previous steps.
  - Port = 514
  - Description = (Optional)
1. Click Save
1. Click Apply

#### Splunk Universal Forwarder Configuration

Download the latest [Splunk Universal Forwarder (UF)](https://www.splunk.com/en_us/download/universal-forwarder.html) appropriate for your server. This UF will be installed on the same server rsyslog was configured in the previous steps.

Install the UF according to [Splunk Docs](https://docs.splunk.com/Documentation/Forwarder/latest/Forwarder/Installtheuniversalforwardersoftware) on the rsyslog server.

Once installed the configurations can be made. The following is a sample inputs.conf that can be pushed using a deployment server or configured on the UF itself.

```SHELL
# inputs.conf
[monitor:///var/log/opnsense]
disabled = 0
host_segment = 4
sourcetype = opnsense
# optionally specify an index, if configured.
#index = firewall
```

Push the configuration to the forwarder, if using a deployment server, or restart the UF if configuring on the UF itself.


## Sourcetypes

Below are a list of sourcetypes which this Add-on will automatically identify and do not need to be set manually.

Source type | Description | CIM Data Models
----------- | ----------- | ---------------
`opnsense:access` | Access Events to OPNsense firewall. | [Authentication](https://docs.splunk.com/Documentation/CIM/latest/User/Authentication)
`opnsense:cron` | Cron Events |
`opnsense:dhcpd` | DHCP Events | [Network Sessions](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkSessions)
`opnsense:filterlog` | Filterlog Events | [Network Traffic](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkTraffic)
`opnsense:lighttpd` | Events from the Web interface | [Web](https://docs.splunk.com/Documentation/CIM/latest/User/Web)
`opnsense:openvpn` | OpenVPN Events | [Authentication](https://docs.splunk.com/Documentation/CIM/latest/User/Authentication)
`opnsense:suricata` `opnsense:suricata:json` | IDS events from suricata | [Intrusion Detection](https://docs.splunk.com/Documentation/CIM/latest/User/IntrusionDetection) [Network Traffic](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkTraffic)
`opnsense:squid` | Proxy events from Squid Proxy | [Web](https://docs.splunk.com/Documentation/CIM/latest/User/Web)
`opnsense:unbound` | DNS events from Unbound DNS | [Network Resolution](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkResolutionDNS)
`opnsense:syslog` | Events from Syslog-ng |


## Bugs
Please open an issue at [github.com](https://github.com/ZachChristensen28/TA-opnsense)

## Versions

```
Version 1.3.1
- fixed KV_MODE for opnsense:unbound sourcetype

Version 1.3.0
- Added compatibility for eve syslog format for Suricata events

Version 1.2.9
- Added compatibility for new syslog format released in OPNSense v20.7
- Updated the 'vendor_options' field to be multi-valued
- appinspect fixes

Version 1.2.8
- Added compatability for new syslog format released in OPNSense v20.7
- Updated the 'vendor_options' field to be multi-valued

Version 1.2.7
- Created http status code lookup, removing the dependency for CIM app.

Version 1.2.6
- Added field extraction for dropped events to suricata when IPS mode is enabled.

Version 1.2.5
- Updated README to include basic syslog configuration and install steps
- Fixed Suricata "signature" field extraction and added input requirements.

Version 1.2.4
- Added openvpn Sourcetype

Version 1.2.3
- Mapped opnsense:dhcpd to CIM.

Version 1.2.2
- Support added for lighttpd (Opnsense Web GUI logs).
- Support added for opnsense access logs.

Version 1.2.1
* Release Notes
- Support added for Unbound DNS logs
- Support added for Cron logs
- Severities have changed for suricata severities (found in lookups/opnsense_suricata_severities).
  - Previously:
   1 (High), 2 (Medium), 3 (Low), 4 (UNDEFINED)
  - Now:
    1 (Critical), 2 (High), 3 (Medium), 4 (Low)
  * It is recommended you update these to match your organization's severities.
- Fixed issue opnsense 19.7 log format change for ICMPv6 and TCP/UDP logs.

Version 1.2.0
* Release Notes
- removed static timestamp configurations to work with all syslog timestamp formats.
```
