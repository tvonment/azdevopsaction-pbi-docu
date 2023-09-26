



# M Code

|Dataset|[Access_test](./../Access_test.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: rep v_hr_employee_active


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_active = Source{[Schema="rep",Item="v_hr_employee_active"]}[Data]
in
    rep_v_hr_employee_active
```


## Table: pub v_ll_company_to_region


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_company_to_region = Source{[Schema="pub",Item="v_ll_company_to_region"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_v_ll_company_to_region, each ([region_reporting_level1] <> null))
in
    #"Filtered Rows"
```


## Table: test user


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202309_Test user.xlsx"), null, true),
    test_Sheet = Source{[Item="test",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(test_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"company_id", Int64.Type}, {"email", type text}})
in
    #"Changed Type"
```


## Roles

### Austria


Model Permission: Read

rep v_hr_employee_active

```m
[company] = "Austria"
```


### Country1


Model Permission: Read

rep v_hr_employee_active

```m
[company] = USERPRINCIPALNAME()
```


### Country_dim


Model Permission: Read

test user

```m
[email] = USERPRINCIPALNAME()
```

