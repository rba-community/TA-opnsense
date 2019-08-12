# TA-opnsense
Splunk Add on for [OPNsense firewall](https://opnsense.org/).

```
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
```

## Supported Sourcetypes

```
opnsense:filterlog
opnsense:dhcpd
opnsense:suricata
opnsense:squid
opnsense:cron
opnsense:unbound
```

### Where to Install
Splunk platform Instance type | Supported | Required | Actions required/ Comments
----------------------------- | --------- | -------- | --------------------------
Search Heads | Yes | Yes | Install this add-on to all search heads
Indexers | Yes | Conditional | Not required if heavy forwarders are used to collect data.
Heavy Forwarders | Yes | Conditional | Not required.

\* **This add-on must be installed on either the HF or Indexers.**

## Input Requirements
Set the sourcetype to "opnsense" in the inputs.conf file on the forwarder.

i.e.

```
# Sample inputs.conf

[monitor:///var/log/firewall.log]
disabled = 0
host = opnsense_firewall
sourcetype = opnsense
```

## Bugs
Please open an issue at [github.com](https://github.com/ZachChristensen28/TA-opnsense)

## Versions

```
Version 1.2.0

* Release Notes
- removed static timestamp configurations to work with all syslog timestamp formats.
```
