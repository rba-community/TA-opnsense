# TA-opnsense
Splunk Add on for [OPNsense firewall](https://opnsense.org/).

```
Version 1.1.0
```

## Supported Sourcetypes

```
opnsense:filterlog
opnsense:dhcpd
opnsense:suricata
opnsense:squid
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
