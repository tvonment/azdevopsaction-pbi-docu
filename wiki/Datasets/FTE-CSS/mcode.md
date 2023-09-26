



# M Code

|Dataset|[FTE CSS](./../FTE-CSS.md)|
| :--- | :--- |
|Workspace|[CSS](../../Workspaces/CSS.md)|

## Table: RLS Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: rep v_hr_employee


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Source{[Schema="rep",Item="v_hr_employee"]}[Data]
in
    rep_v_hr_employee
```


## Table: rep v_hr_employee_ps_job_matrix


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_ps_job_matrix = Source{[Schema="rep",Item="v_hr_employee_ps_job_matrix"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(rep_v_hr_employee_ps_job_matrix,{"function_code", "std_hours", "job_entry_date", "company_id_byd", "dept_entry_dt", "tax_location", "approver", "reports_to"})
in
    #"Removed Columns"
```


## Table: pub ll_cost_center


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_cost_center = Source{[Schema="pub",Item="ll_cost_center"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(pub_ll_cost_center,{"effective_date", "effective_status"})
in
    #"Removed Columns"
```


## Table: rep v_hr_employee_costcenter_fte_per_MONTH


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select byMonth.*, loc.country_code_iso3 #(lf)from#(lf)#(tab)(select year([calendar_day]) as year, month([calendar_day]) as month, [emp_id], [work_location], [cost_center_id], sum([target_hours_adj]) as target_hours, sum([target_hours_fte]) as [target_hours_fte]#(lf)#(tab)#(tab) from [rep].[v_hr_employee_costcenter_fte_per_date] as fte#(lf)#(tab)#(tab) group by year([calendar_day]), month([calendar_day]), [emp_id], [work_location], [cost_center_id]) as byMonth#(lf)#(tab)left join pub.ll_location as loc #(lf)#(tab)#(tab)on loc.location = byMonth.work_location "]),
    #"Added Custom" = Table.AddColumn(Source, "StartOfMonth", each #date([year],[month],1), Date.Type)
in
    #"Added Custom"
```


## Table: pub ll_country_to_region


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_country_to_region = Source{[Schema="pub",Item="ll_country_to_region"]}[Data],
    #"Merged Queries" = Table.NestedJoin(pub_ll_country_to_region, {"region_id"}, #"pub ll_region", {"region_id"}, "pub ll_region", JoinKind.LeftOuter),
    #"Expanded pub ll_region" = Table.ExpandTableColumn(#"Merged Queries", "pub ll_region", {"region", "report_id", "sort_id"}, {"region", "report_id", "sort_id"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded pub ll_region", each ([report_id] = 31))
in
    #"Filtered Rows"
```


## Table: Org


```m
let
    Source = #"pub ll_company_org_unit",
    #"Merged Queries" = Table.NestedJoin(Source, {"parent_org_unit_id"}, Source, {"org_unit_id"}, "Source", JoinKind.LeftOuter),
    #"Expanded Source" = Table.ExpandTableColumn(#"Merged Queries", "Source", {"company_id"}, {"Source.company_id"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Source", "parent_id", 

each if [parent_org_unit_id] = null then null else if [Source.company_id] = null then "9999" else [Source.company_id]

),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"parent_id", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"parent_org_unit_id", "Source.company_id"}),
    Custom1 = Table.InsertRows( #"Removed Columns", 0, 
{[ 
company_id="9999",
org_unit_id = "9999", org_unit = "!parent not found!", org_unit_responsible_id=  null, org_unit_responsible =  null, org_unit_hierarchy_level = 1, parent_id = null
]}
),
    #"Replaced Value" = Table.ReplaceValue(Custom1,null,"NOT ASSIGNED",Replacer.ReplaceValue,{"org_unit_responsible_id"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","","NOT ASSIGNED",Replacer.ReplaceValue,{"org_unit_responsible_id"})
in
    #"Replaced Value1"
```


## Table: OrgResponsible


```m
let
    Source = Org,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"org_unit_responsible_id"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns")
in
    #"Removed Duplicates"
```


## Table: TOEs


```m
let
    Source = #"employee toe build",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"toe"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Added Index" = Table.AddIndexColumn(#"Removed Duplicates", "ToeId", 0, 1, Int64.Type)
in
    #"Added Index"
```


## Table: employee toe by month


```m
let
    Source = #"employee toe build",
    #"Merged Queries" = Table.NestedJoin(Source, {"toe"}, TOEs, {"toe"}, "TOEs", JoinKind.LeftOuter),
    #"Expanded TOEs" = Table.ExpandTableColumn(#"Merged Queries", "TOEs", {"ToeId"}, {"ToeId"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded TOEs",{"toe"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"emp_id", "validfrom_date"})
in
    #"Removed Duplicates"
```

