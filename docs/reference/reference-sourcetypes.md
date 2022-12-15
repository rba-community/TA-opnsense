# Sourcetypes

Below are a list of sourcetypes which this Add-on uses. It is not necessary to manually set the sourcetype to anything other than `opnsense` as this add-on will automatically transform the sourcetype to the appropriate value.

Source type | Description | CIM Mapping
----------- | ----------- | -----------
{--opnsense:access--} _deprecated v1.5.0_ | Access Events to OPNsense firewall. | [Authentication](https://docs.splunk.com/Documentation/CIM/latest/User/Authentication)
{++opnsense:audit++} _new v1.5.0_ | Audit Events to OPNsense firewall (logins/changes). | [Authentication](https://docs.splunk.com/Documentation/CIM/latest/User/Authentication)
`opnsense:cron` | Cron Events | None
`opnsense:dhcpd` | DHCP Events | [Network Sessions](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkSessions)
`opnsense:filterlog` | Filterlog Events | [Network Traffic](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkTraffic)
`opnsense:lighttpd` | Events from the Web interface | [Web](https://docs.splunk.com/Documentation/CIM/latest/User/Web)
`opnsense:openvpn` | OpenVPN Events | [Authentication](https://docs.splunk.com/Documentation/CIM/latest/User/Authentication)
`opnsense:suricata` `opnsense:suricata:json` | IDS events from suricata | [Intrusion Detection](https://docs.splunk.com/Documentation/CIM/latest/User/IntrusionDetection) [Network Traffic](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkTraffic)
`opnsense:squid` | Proxy events from Squid Proxy | [Web](https://docs.splunk.com/Documentation/CIM/latest/User/Web)
`opnsense:unbound` | DNS events from Unbound DNS | [Network Resolution](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkResolutionDNS)
`opnsense:syslog` | Events from Syslog-ng | None

--8<-- "includes/abbreviations.md"
