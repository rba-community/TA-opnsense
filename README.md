# Add-on for OPNsense® Firewall - TA-opnsense

[![GitHub](https://img.shields.io/github/license/ZachChristensen28/TA-opnsense)]()
[![Documentation Status](https://readthedocs.org/projects/splunk-opnsense-ta-documentation/badge/?version=latest)](https://splunk-opnsense-ta-documentation.readthedocs.io/en/latest/?badge=latest)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/ZachChristensen28/TA-opnsense)
[![Splunkbase App](https://img.shields.io/badge/Splunkbase-TA--opnsense-blue)](https://splunkbase.splunk.com/app/4538/)
[![Splunk CIM Version](https://img.shields.io/badge/Splunk%20CIM%20Version-4.x-success)](https://docs.splunk.com/Documentation/CIM/latest/User/Overview)

 Info | Description
------|----------
Version | 1.5.1 - See on [Splunkbase](https://splunkbase.splunk.com/app/4538/)
Vendor Product Version | [OPNsense® 21.7](https://opnsense.org/)
Add-on has a web UI | Yes, this add-on has a view to setup a modular input.

**NEW:** Try the new [OPNsense App for Splunk](https://github.com/ZachChristensen28/Opnsense_App_for_Splunk)!

The TA-opnsense Add-on allows Splunk data administrators to map the OPNsense® firewall events to the [CIM](https://docs.splunk.com/Splexicon:CommonInformationModel) enabling the data to be used with other Splunk Apps, such as Enterprise Security.

```TEXT
Version 1.5.1

- Updating field extractions for Suricata events in Drop mode - #58
- Adding default allowed action for suricata events
- Fixed certificate issue when no cert checking is enabled - issue #61
```

## Documentation

Full documentation can be found at https://splunk-opnsense-ta-documentation.rtfd.io.

## Bugs

Please open an issue at [github.com](https://github.com/ZachChristensen28/TA-opnsense)
