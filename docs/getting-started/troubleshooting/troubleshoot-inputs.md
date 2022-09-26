# Troubleshoot Monitoring Inputs

There is a variety of issues when getting new data into Splunk. Below are a few of the most common issues:

Issue | Description | Solution
----- | ----------- | --------
Splunk cannot read the file | If the user running Splunk (default is `splunk`) cannot read the contents of the file, the data will not be sent to Splunk. | log in as the Splunk user and verify the contents can be read. If not, update the permissions of the file to allow read access to the Splunk user.
Incorrect timestamps | Having the incorrect time setup on either the Splunk instance or syslog server may result in not ingesting the data. | In Splunk web, try switching the time range to "All Time" when looking for the data. If the data is found and the incorrect time is observed, update the servers to the correct time and consider utilizing a NTP server for proper time synchronization.
Splunk Forwarder communication | It is possible that the Splunk Universal Forwarder does not have a connection to the Splunk instance. | Verify connection by running the following command on the universal forwarder: `$SPLUNK_HOME/bin/splunk list forward-server`. $SPLUNK_HOME is the installation directory. The output from this command will show active/inactive connections to the Splunk Instance. Alternatively the internal logs can be searched in Splunk Web. Run the following command on the search head: `index=_internal source=*metrics.log* tcpin_connections | stats count by sourceIp`. The output of this search will show a list of sources connecting to the Splunk Instance.

For more troubleshooting steps, see [Splunk Docs: Troubleshooting Data](https://docs.splunk.com/Documentation/Splunk/latest/Troubleshooting/Cantfinddata).