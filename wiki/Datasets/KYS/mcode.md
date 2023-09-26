



# M Code

|Dataset|[KYS](./../KYS.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_dandb_adhocqueries


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_dandb_adhocqueries_table = Source{[Name="nxtgn_dandb_adhocqueries",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_dandb_adhocqueries_table, each ([nxtgn_externalrequest] = true) and ([statuscode] = 1)),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows", "nxtgn_compliancecheckstatus_meta", each if [nxtgn_compliancecheckstatus] is null then "In Progress" else Value.Metadata([nxtgn_compliancecheckstatus])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "nxtgn_compliancecheckresultstatus_meta", each if [nxtgn_compliancecheckresultstatus] is null then "In Progress" else Value.Metadata([nxtgn_compliancecheckresultstatus])[OData.Community.Display.V1.FormattedValue]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"createdon", type date}, {"nxtgn_compliancecheckdate", type date}, {"nxtgn_birthdate", type date}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type",{"nxtgn_dandb_adhocqueryid", "emailaddress", "createdon", "nxtgn_city", "nxtgn_complianceriskscore_rb", "nxtgn_birthdate", "nxtgn_critical_unassigned_complianceentries", "nxtgn_contractorrelationshiphalfyear", "nxtgn_country_iso2", "nxtgn_totalunassigned", "nxtgn_searchterm", "nxtgn_kysresultsent", "nxtgn_postalcode", "nxtgn_lowriskunassignedcomplianceentries", "nxtgn_compliancecheckdate", "nxtgn_compliancecheckstatus_meta", "nxtgn_compliancecheckresultstatus_meta"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Other Columns",{"nxtgn_dandb_adhocqueryid", "createdon", "emailaddress", "nxtgn_searchterm", "nxtgn_postalcode", "nxtgn_city", "nxtgn_country_iso2", "nxtgn_birthdate", "nxtgn_contractorrelationshiphalfyear", "nxtgn_compliancecheckresultstatus_meta", "nxtgn_compliancecheckstatus_meta", "nxtgn_complianceriskscore_rb", "nxtgn_compliancecheckdate", "nxtgn_lowriskunassignedcomplianceentries", "nxtgn_critical_unassigned_complianceentries", "nxtgn_totalunassigned", "nxtgn_kysresultsent"})
in
    #"Reordered Columns"
```


## Table: RB_EMPLOYEES


```m
let
    Source = Sql.Database("muc-mssql-1a", "ByD_ODP"),
    dbo_RB_EMPLOYEES = Source{[Schema="dbo",Item="RB_EMPLOYEES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_RB_EMPLOYEES, each ([EMAIL] <> null and [EMAIL] <> "no_mail@rolandberger.com"))
in
    #"Filtered Rows"
```

