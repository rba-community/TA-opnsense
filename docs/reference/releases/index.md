# Release notes for the OPNsense Add-on for Splunk

## v1.5.1 <small>Nov 30, 2021</small>

???+ warning
    **_Only applies if you are upgrading from a version < 1.5.0_**

    This version includes packages for the new version of Add-on builder (v4.0.0) which may cause API credentials to no longer work after updating. After updating to this version, you may have to re-enter the API credentials for the modular inputs to work again by editing the existing account configurations.

### New features

- Adding default allowed action for suricata events

### Fixed issues

- Updating field extractions for Suricata events in Drop mode - [#58](https://github.com/ZachChristensen28/TA-opnsense/issues/58)
- Fixed certificate issue when no cert checking is enabled - [#61](https://github.com/ZachChristensen28/TA-opnsense/issues/61)

### Known issues

This version of the OPNsense addon for Splunk has the following known issues. If no issues appear here, no issues have been reported. Issues can be reported on the [OPNsense addon for Splunk's Github page](https://github.com/ZachChristensen28/TA-opnsense/issues).

--8<-- "includes/abbreviations.md"
