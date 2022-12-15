# Where to Install

For detailed information on where to install Splunk Apps/add-ons, including best practices, can be found at [Splunk Docs: About Installing Splunk add-ons](https://docs.splunk.com/Documentation/AddOns/released/Overview/Wheretoinstall)

## Standalone Deployments

Install this add-on to the single instance. For more information see [Splunk Docs: Install add-on in a single-instance Splunk deployment](https://docs.splunk.com/Documentation/AddOns/released/Overview/Singleserverinstall)

## Distributed Deployments

Splunk Instance type | Supported | Required | Comments
-------------------- | --------- | -------- | --------
Search Heads | Yes | Yes | Install this add-on to all search heads.
Indexers | Yes | Conditional | Not required if heavy forwarders are used to collect data, required if not.
Heavy Forwarders | Yes | Conditional | Required, if HFs are used to collect this data source.
Universal Forwarders | Yes | Not required | The add-on includes an inputs.conf file that is disabled by default. This can be used to create an input on the forwarder if enabled.

The installation steps for deploying Apps/add-ons in a distributed environment can be found at [Splunk Docs: Install an add-on in a distributed Splunk deployment](https://docs.splunk.com/Documentation/AddOns/released/Overview/Distributedinstall)

## Distributed Deployment Compatibility

Distributed deployment feature | Supported | Comments
------------------------------ | --------- | --------
Search Head Clusters | Yes | You can install this add-on to a search head cluster.
Indexer Clusters | Yes | You can install this add-on to a indexer cluster.
Deployment Server | Yes | You can use a deployment server to push this add-on to Splunk Universal Forwarders.

\* For more information, see Splunk's [documentation](https://docs.splunk.com/Documentation/AddOns/released/Overview/Installingadd-ons) on installing Add-ons.

--8<-- "includes/abbreviations.md"