



# M Code

|Dataset|[Country, Platform Heads_v01](./../Country,-Platform-Heads_v01.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: rep v_ll_unit_responsible


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_unit_responsible = Source{[Schema="rep",Item="v_ll_unit_responsible"]}[Data]
in
    rep_v_ll_unit_responsible
```


## Table: pub v_ll_company


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_company_to_region = Source{[Schema="pub",Item="v_ll_company"]}[Data]
in
    pub_v_ll_company_to_region
```


## Table: DACH platform name


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202308_DACH platforms.xlsx"), null, true),
    #"DACH platform name_Sheet" = Source{[Item="DACH platform name",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"DACH platform name_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"role_name", type text}, {"responsible_unit", type text}, {"responsible_unit_id", Int64.Type}, {"responsible_unit_name", type text}, {"DACH platform", type text}}),
    #"Filter empty Rows" = Table.SelectRows(#"Changed Type", each ([responsible_unit_id] <> null))
in
    #"Filter empty Rows"
```

