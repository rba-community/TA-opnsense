# Release history for the OPNsense addon for Splunk

The latest version of the OPNsense addon for Splunk is version 1.5.7. See [Release notes for the OPNsense addon for Splunk](../../releases/) of the latest version.

## v1.5.6 <small>July 10, 2024</small>

### What's changed

- Initial Release under The RBA Community

## v1.5.5 <small>May 29, 2024</small>

### What's changed

- Fixed logging for openvpn logs - [#127](https://github.com/rba-community/TA-opnsense/issues/127) by [ChrisSiedler](https://github.com/ChrisSiedler)
- Updated License to SGT

## v1.5.4 <small>October 5, 2023</small>

### What's changed

- Updated Splunk Add-on version to 4.1.3.
- Updated Splunk Python SDK to version 1.7.4

## v1.5.3 <small>May 14, 2023</small>

### What's changed

- Fixed "unknown" action for nat rules [#85](https://github.com/rba-community/TA-opnsense/issues/85).
- Added the field `dest_interface` for CIM compliance.

### Known issues

This version of the OPNsense addon for Splunk has the following known issues. If no issues appear here, no issues have been reported. Issues can be reported on the [OPNsense addon for Splunk's Github page](https://github.com/rba-community/TA-opnsense/issues).

## v1.5.2 <small>Dec 15, 2022</small>

???+ warning
    **_Only applies if you are upgrading from a version < 1.5.0_**

    This version includes packages for the new version of Add-on builder (v4.0.0) which may cause API credentials to no longer work after updating. After updating to this version, you may have to re-enter the API credentials for the modular inputs to work again by editing the existing account configurations.

### What's changed

- Updated Add-on builder packages.
- Updated documentation to address required log formats [#67](https://github.com/rba-community/TA-opnsense/issues/67).

## v1.5.1 <small>Nov 30, 2021</small>

???+ warning
    **_Only applies if you are upgrading from a version < 1.5.0_**

    This version includes packages for the new version of Add-on builder (v4.0.0) which may cause API credentials to no longer work after updating. After updating to this version, you may have to re-enter the API credentials for the modular inputs to work again by editing the existing account configurations.

- Adding default allowed action for suricata events
- Updating field extractions for Suricata events in Drop mode - [#58](https://github.com/rba-community/TA-opnsense/issues/58)
- Fixed certificate issue when no cert checking is enabled - [#61](https://github.com/rba-community/TA-opnsense/issues/61)

## v1.5.0 <small>Aug 7, 2021</small>

???+ warning
    This version includes packages for the new version of Add-on builder (v4.0.0) which may cause API credentials to no longer work after updating. After updating to this version, you may have to re-enter the API credentials for the modular inputs to work again by editing the existing account configurations.

* deprecating sourcetype "opnsense:access" and moving to "opnsense:audit"
* updated CIM mapping for Authentication events
* updated to latest add-on builder version

## v1.4.3 <small>July 8, 2021</small>

* fixed script to initial an upgrade check - [#49](https://github.com/rba-community/TA-opnsense/issues/49)
* added ability to use a cron schedule for the modular input interval - [#52](https://github.com/rba-community/TA-opnsense/issues/52)
* added ability to specify port number for modular input - [#53](https://github.com/rba-community/TA-opnsense/issues/53)

## v1.4.2 <small>June 2, 2021</small>

* Adding support for absolute paths in modular input setup for certificates - [#44](https://github.com/rba-community/TA-opnsense/issues/44)
* Fixed issue with the Verify Certificate checkbox not working properly - [#47](https://github.com/rba-community/TA-opnsense/issues/47)

## v1.4.1 <small>May 27, 2021</small>

* Fixed incorrect sourcetype transform for modular input - issue [#41](https://github.com/rba-community/TA-opnsense/issues/41)
* Increased the truncate limit to allow large events.

## v1.4.0 <small>May 27, 2021</small>

* Added modular input to pull system information (Available Updates, Versions, Installed Packages/Plugins).
* Updated the suricata sourcetyper to recognize the json data without the standard syslog message header.
* Fixed ipv6 ICMP events not extracting properly - issue [#37](https://github.com/rba-community/TA-opnsense/issues/37)

## v1.3.2 <small>Dec 14, 2020</small>

* Added meta field for event length (opnsense_event_length).
* Added sourcetype for Syslog-ng logs (opnsense:syslog).
* Added action for "Redirect" if port forwarding logging rules exist.
* Fixed "unknown" severity for opnsense:suricata:json events - issue [#27](https://github.com/rba-community/TA-opnsense/issues/27).
* Fixed IGMP events not being extracted - issue [#32](https://github.com/rba-community/TA-opnsense/issues/32).
* Fixed Access logs not being extracted - issue [#35](https://github.com/rba-community/TA-opnsense/issues/35).

## v1.3.1 <small>Oct 31, 2020</small>

* fixed KV_MODE for opnsense:unbound sourcetype.

## v1.3.0 <small>Aug 15, 2020</small>

* Added compatibility for eve syslog format for Suricata events.
* Removed incorrect field extraction for DHCP events.

## v1.2.9 <small>Aug 5, 2020</small>

* Added compatibility for new syslog format released in OPNSense v20.7.
* Updated the 'vendor_options' field to be multi-valued.
* Appinspect fixes.

## v1.2.7 <small>Jul 15, 2020</small>

* Removed Dependency for CIM app.
* Fixed multiple regex statements under one stanza.

--8<-- "includes/abbreviations.md"
