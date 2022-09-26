# Modular Input Troubleshooting

If no logs appear in the index you specified after configuring the input, use the following to troubleshoot.

1. Set the logging mode to "Debug" on the Configuration Tab.
1. Search the internal logs for errors:

```shell
index=_internal sourcetype=taopnsense:log
```