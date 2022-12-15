# Intrusion Detection Logging Setup

This guide assumes that you already have the packaged necessary for the Intrusion detection service. For more information see [OPNsense Docs: Intrusion Detection](https://docs.opnsense.org/manual/ips.html).

1. Log in to OPNsense.
1. Navigate to Services > Intrusion Detection > Administration.
1. Click the "advanced mode" toggle.

It is recommended to use the eve syslog output setting. This will provide the most verbose output. Additionally, the payload can be logged by checking the "log package payload" box.

Once you are satisfied with all other settings, click enable and then apply. For more information on all other settings see [OPNsense Docs: Intrusion Detection](https://docs.opnsense.org/manual/ips.html).

--8<-- "includes/abbreviations.md"