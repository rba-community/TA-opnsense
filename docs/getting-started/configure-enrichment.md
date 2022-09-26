# Configure Enrichment

???+ info "Optional Step"
    Mapping interfaces to their names can help in being able to quickly identify them in Splunk (i.e. `vmx0` -> `LAN`). This step can be skipped if enrichment is not required.

The steps to setup enrichment for this add-on utilize Splunk Lookups. For more information on lookups see [Splunk Docs: About lookups](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutlookupsandfieldactions).

Steps to configure enrichment:

1. [Create a CSV Lookup](#create-a-csv-lookup).
1. [Create a Lookup Definition](#create-a-lookup-definition).
1. [Create an Automatic Lookup](#create-an-automatic-lookup)

???+ tip
    To get a full list of interfaces being used in OPNsense:

    From the OPNsense UI, navigate to Interfaces > Assignments.

## Create a CSV Lookup

### Method 1 - Use the Lookup Editor

<small>Recommended</small>

The lookup editor may be the easiest way to create and mange lookups in Splunk. You can download and install the Lookup Editor from [Splunkbase: Lookup Editor](https://splunkbase.splunk.com/app/1724).

Once installed, the lookup editor can be used to create a new CSV lookup.

1. Open the Lookup Editor in Splunk Web.
1. Click "Create a New Lookup" > CSV lookup.
1. Give the lookup a descriptive name <small>(i.e. opn_interfaces.csv)</small>.
1. Choose which App context this lookup will be stored in <small>(i.e. Search & Reporting)</small>.
1. Leave the "User-only" box **uncheked**. This will give the lookup the global scope permissions it needs.
1. Create column headers (row 1). These headers will be referenced later.
1. Populate the remaing rows with the interface name mappings.

    ???+ example

        host | interface | interface_name
        ---- | --------- | --------------
        opnsense-01 | em0 | LAN
        opnsense-01 | em1 | WAN
        opnsense-01 | vmx1 | IOT
        opnsense-01 | wg0 | WIREGUARD
        opnsense-02 | vmx1 | LAN
        opnsense-02 | vmx2 | WAN

1. After saving, move to [Create a Lookup Definition](#create-a-lookup-definition).

### Method 2 - Create and Upload a new CSV file

A lookup file can be created outside of Splunk and then uploaded via the web interface.

1. Use an editor to create a file in CSV format.
1. Create column headers (row 1). These headers will be referenced later.
1. Populate the remaing rows with the interface name mappings.

    ???+ example

        ```text title="opn_interfaces.csv"
        host,interface,interface_name
        opnsense-01,em0,LAN
        opnsense-01,em1,WAN
        opnsense-01,vmx1,IOT
        opnsense-01,wg0,WIREGUARD
        opnsense-02,vmx1,LAN
        opnsense-02,vmx2,WAN
        ```

1. Be sure to save the file with a `.csv` extension.
1. Open Splunk Web.
1. Navigate to Settings > Lookups > Lookup table files (click "+ Add new")
1. Select the Destination App <small>(i.e. Search & Reporting)</small>.
1. Upload the file.
1. Provide the Destination filename. This can be the same name as the one created <small>(i.e. opn_interfaces.csv)</small>.
1. Once saved, Navigate back to Settings > Lookups > Lookup table files, if you are not already there.
1. Search for the name of the file you just uploaded.
1. Modify the permissions for the file by clicking "Permissions."
1. Select "All apps (system)" from the two radio options.
1. Check "Read" permissions for Everyone. Write permissions can be given as needed (typically set to admin & power).
1. After saving, move to [Create a Lookup Definition](#create-a-lookup-definition).

## Create a Lookup Definition

After the CSV lookup has been created, a lookup definition needs to be created.

1. In Splunk Web, Navigate to Settings > Lookups > Lookup definitions (click "+ Add new").
1. Choose a destination app, or leave as default.
1. Give the lookup a name <small>(i.e. opn_interfaces)</small>
1. Select the previously created CSV lookup from the dropdown.
1. Click the "Advanced" checkbox.
1. Click the "Case Sensitive Match" checkbox to disable case sensitive matching.
1. Once saved, Navigate back to Settings > Lookups > Lookup definitions.
1. Search for the name of the lookup definition you just created.
1. Modify the permissions for the file by clicking "Permissions."
1. Select "All apps (system)" from the two radio options.
1. Check "Read" permissions for Everyone. Write permissions can be given as needed (typically set to admin & power).
1. After saving, move on to [Create Automatic Lookup](#create-automatic-lookup)

## Create an Automatic Lookup

After the Lookup definition has been created, an automatic lookup has to be configured for automatic enrichment.

1. In Splunk Web, Navigate to Settings > Lookups > Automatic lookups (click "+ Add new").
1. Choose a destination app, or leave as default.
1. Give the lookup a name <small>(i.e. opn_interfaces_auto_lookup)</small>
1. Select the previously created lookup definition from the dropdown.
1. For the "Apply to" field, select sourcetype and type `opnsense:filterlog`.
1. For the input fields, first specify the interface field from the created lookup. Then type `dest_int` for the second field.

    ???+ example
        `field_from_lookup` = `dest_int`

        ```text
        interface = dest_int
        ```

1. For the next input field, set `host` equal to a blank field. There is no need to rename this field.

    ???+ example
        `host` =

1. For the output fields, first specify the interface name field from the created lookup. Then type `dest_int_name` for the second field.

    ???+ example
        `field_from_lookup` = `dest_int_name`

        ```text
        interface_name = dest_int_name
        ```
1. Once saved, Navigate back to Settings > Lookups > Automatic lookups.
1. Search for the name of the automatic lookup you just created.
1. Modify the permissions for the file by clicking "Permissions."
1. Select "All apps (system)" from the two radio options.
1. Check "Read" permissions for Everyone. Write permissions can be given as needed (typically set to admin & power).
1. Click Save.

--8<-- "includes/abbreviations.md"
