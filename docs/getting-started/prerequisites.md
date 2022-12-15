# Prerequisites

## OPNsense logging requirement

Do not select the `rfc5424` log format when setting up a new logging target. Doing so will cause this add-on to not properly extract fields.

__Leave `rfc5424` unchecked__ <small>(see example below)</small>

![OPNsense example logging configuration](/images/opn-logging-example.png)
