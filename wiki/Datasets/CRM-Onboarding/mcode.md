



# M Code

|Dataset|[CRM Onboarding](./../CRM-Onboarding.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: systemusers


```m
let
    Quelle = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Quelle{[Name="systemusers",Signature="table"]}[Data],
    #"Erweiterte nxtgn_costcenterid" = Table.ExpandRecordColumn(systemusers_table, "nxtgn_costcenterid", {"nxtgn_name", "nxtgn_lookupcostcenterid"}, {"nxtgn_costcenterid.nxtgn_name", "nxtgn_costcenterid.nxtgn_lookupcostcenterid"}),
    #"Erweiterte nxtgn_lookupcountryid" = Table.ExpandRecordColumn(#"Erweiterte nxtgn_costcenterid", "nxtgn_lookupcountryid", {"nxtgn_name", "nxtgn_lookupcountryid"}, {"nxtgn_lookupcountryid.nxtgn_name", "nxtgn_lookupcountryid.nxtgn_lookupcountryid"}),
    #"Erweiterte nxtgn_platformid" = Table.ExpandRecordColumn(#"Erweiterte nxtgn_lookupcountryid", "nxtgn_platformid", {"nxtgn_name", "nxtgn_lookupplatformid"}, {"nxtgn_platformid.nxtgn_name", "nxtgn_platformid.nxtgn_lookupplatformid"}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Erweiterte nxtgn_platformid", "nxtgn_outlookcontactsyncprofile_meta", each Value.Metadata([nxtgn_outlookcontactsyncprofile])[OData.Community.Display.V1.FormattedValue])
in
    #"Hinzugefügte benutzerdefinierte Spalte"
```


## Table: nxtgn_lookupcountryaliases


```m
let
    Quelle = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    nxtgn_lookupcountryaliases_table = Quelle{[Name="nxtgn_lookupcountryaliases",Signature="table"]}[Data]
in
    nxtgn_lookupcountryaliases_table
```


## Table: nxtgn_contactresponsibilities


```m
let
    Quelle = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_contactresponsibilities_table = Quelle{[Name="nxtgn_contactresponsibilities",Signature="table"]}[Data],
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(nxtgn_contactresponsibilities_table, "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Removed Other Columns" = Table.SelectColumns(#"Hinzugefügte benutzerdefinierte Spalte",{"_nxtgn_contactid_value", "nxtgn_contactresponsibilityid", "statuscode_meta", "_nxtgn_userid_value"})
in
    #"Removed Other Columns"
```


## Table: mailboxes


```m
let
    Quelle = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    mailboxes_table = Quelle{[Name="mailboxes",Signature="table"]}[Data],
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(mailboxes_table, "actstatus_meta", each Value.Metadata([actstatus])[OData.Community.Display.V1.FormattedValue]),
    #"Hinzugefügte benutzerdefinierte Spalte (1)" = Table.AddColumn(#"Hinzugefügte benutzerdefinierte Spalte", "incomingemailstatus_meta", each Value.Metadata([incomingemailstatus])[OData.Community.Display.V1.FormattedValue]),
    #"Hinzugefügte benutzerdefinierte Spalte (2)" = Table.AddColumn(#"Hinzugefügte benutzerdefinierte Spalte (1)", "outgoingemailstatus_meta", each Value.Metadata([outgoingemailstatus])[OData.Community.Display.V1.FormattedValue])
in
    #"Hinzugefügte benutzerdefinierte Spalte (2)"
```


## Table: contacts


```m
let
    Quelle = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    contacts_table = Quelle{[Name="contacts",Signature="table"]}[Data],
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(contacts_table, "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Hinzugefügte benutzerdefinierte Spalte (1)" = Table.AddColumn(#"Hinzugefügte benutzerdefinierte Spalte", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Removed Other Columns" = Table.SelectColumns(#"Hinzugefügte benutzerdefinierte Spalte (1)",{"contactid", "statuscode_meta", "statecode_meta"})
in
    #"Removed Other Columns"
```

