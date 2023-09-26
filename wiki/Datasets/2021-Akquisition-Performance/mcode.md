



# M Code

|Dataset|[2021 Akquisition Performance](./../2021-Akquisition-Performance.md)|
| :--- | :--- |
|Workspace|[Acquisition Performance](../../Workspaces/Acquisition-Performance.md)|

## Table: FactOrderIncomeByMonth


```m
let
    Source = #"sec acp_orderIncome_byMonth_joined",
    #"Filtered Rows" = Table.SelectRows(Source, each [Month] <= #"SAP MAX Month")
in
    #"Filtered Rows"
```


## Table: FactPaidByYear


```m
let
    Source = #"sec acp_values_byYear_joined",
    #"Removed Columns" = Table.RemoveColumns(Source,{"Invoiced Year", "OrderIncome Year"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each [Paid Year] <> null),
    #"Appended Query Adjust Paid" = Table.Combine({#"Filtered Rows", #"sec acp_adjust_paid"})
in
    #"Appended Query Adjust Paid"
```


## Table: FactInvoicedByYear


```m
let
    Source = #"sec acp_values_byYear_joined",
    #"Removed Columns" = Table.RemoveColumns(Source,{"Paid Year", "OrderIncome Year"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each [Invoiced Year] <> null)
in
    #"Filtered Rows"
```


## Table: DimProjects


```m
let
    Source = Table.SelectColumns(#"Contribution", { "ProjectNumber"}),
    #"Removed Duplicates" = Table.Distinct(Source),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"ProjectNumber"}, #"rep v_acp_fc_project_data", {"project_number"}, "rep v_acp_fc_project_data", JoinKind.LeftOuter),
    #"Expanded rep v_fc_psr_project_data" = Table.ExpandTableColumn(#"Merged Queries", "rep v_acp_fc_project_data", {"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "dm_cc_id", "dm_cc", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "project_status", "sales_unit_cou_iso3", "sales_unit_cou_country", "function_id", "industry_id", "responsible_unit_cou_iso3"}, {"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "dm_cc_id", "dm_cc", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "project_status", "sales_unit_cou_iso3", "sales_unit_cou_country", "function_id", "industry_id", "responsible_unit_cou_iso3"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded rep v_fc_psr_project_data",{"project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "responsible_accounting_emp_id", "responsible_accounting"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Inserted First Characters" = Table.AddColumn(#"Filtered Rows", "Project", each Text.Start([project_name], 40), type text),
    #"merge function cc" = Table.NestedJoin(#"Inserted First Characters", {"function_id"}, #"rep v_ll_industry_functional_cc", {"cc_id"}, "rep v_ll_industry_functional_cc", JoinKind.LeftOuter),
    #"Expanded rep v_ll_CC" = Table.ExpandTableColumn(#"merge function cc", "rep v_ll_industry_functional_cc", {"cc_name"}, {"function_cc_name"}),
    #"merge industry cc" = Table.NestedJoin(#"Expanded rep v_ll_CC", {"industry_id"}, #"rep v_ll_industry_functional_cc", {"cc_id"}, "rep v_ll_industry_functional_cc", JoinKind.LeftOuter),
    #"Expanded DimCC" = Table.ExpandTableColumn(#"merge industry cc", "rep v_ll_industry_functional_cc", {"cc_name"}, {"industry_cc_name"})
in
    #"Expanded DimCC"
```


## Table: DimEmployees


```m
let
    // emp_ids from SAP and MIS
    Source = Table.SelectColumns(#"Contribution", {"EmployeeID"}),
    #"Removed Duplicates (EmployeeID)" = Table.Distinct(Source),
    #"Merged v_hr_statistics (latest ap month per emp)" = Table.NestedJoin(#"Removed Duplicates (EmployeeID)", {"EmployeeID"}, #"rep v_hr_statistic", {"emp_id"}, "rep v_hr_statistics", JoinKind.LeftOuter),
    #"Expanded emp master data" = Table.ExpandTableColumn(#"Merged v_hr_statistics (latest ap month per emp)", "rep v_hr_statistics", {"emp_id", "max_valid_from", "last_name", "first_name", "ter_max_date", "jobcode_id", "jobcode", "jobfunction", "cc_id", "cc_name", "country_code_iso3", "termination_date", "ExitInApYear", "emp_status", "full_name", "email"}, {"emp_id", "max_valid_from", "last_name", "first_name", "ter_max_date", "jobcode_id", "jobcode", "jobfunction", "cc_id", "cc_name", "country_code_iso3", "termination_date", "ExitInApYear", "emp_status", "full_name", "email"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded emp master data",{ "jobfunction"}),
    #"Added CleanedJobcode" = Table.AddColumn(#"Removed Columns", "CleanedJobCode", each Text.BeforeDelimiter([jobcode], " "), type text),
    #"Merged Force Show" = Table.NestedJoin(#"Added CleanedJobcode", {"EmployeeID"}, #"Adjust ForceShow", {"EmployeeID"}, "Adjust ForceShow", JoinKind.LeftOuter),
    #"Expanded Adjust ForceShow" = Table.ExpandTableColumn(#"Merged Force Show", "Adjust ForceShow", {"EmployeeID"}, {"ForceShow"}),
    #"Added ShowDefault" = Table.AddColumn(#"Expanded Adjust ForceShow", "ShowDefault ", each if (([CleanedJobCode] = "Partner" or [CleanedJobCode] = "Principal" or [CleanedJobCode] = "Director" or ([ForceShow] <> null and [ForceShow] <> "")) 
and [emp_status] = "A"
)
  then true else false, Logical.Type), // Table.SelectRows(#"Expanded Adjust ForceShow", each ([CleanedJobCode] = "Partner" or [CleanedJobCode] = "Principal" or [CleanedJobCode] = "Director" or ([ForceShow] <> null and [ForceShow] <> ""))),
    #"Change emp_status to active for force show" = Table.ReplaceValue(#"Added ShowDefault",each [emp_status], each if [ForceShow] <> null then "A" else [emp_status],Replacer.ReplaceText,{"emp_status"}),
    #"Added IsPartner by job" = Table.AddColumn(#"Change emp_status to active for force show", "IsPartner", each if [CleanedJobCode] = "Partner" then 1 else  0, type number),
    #"Added IsPrincipal by job" = Table.AddColumn(#"Added IsPartner by job", "IsPrincipal", each if [CleanedJobCode] = "Principal" then 1 else 0, type number),
    #"Added Employee (Job)" = Table.AddColumn(#"Added IsPrincipal by job", "Employee (Job)", each Text.Combine({[full_name], " (", [CleanedJobCode], ")"}), type text),
    #"Added Employee" = Table.CombineColumns(#"Added Employee (Job)",{"full_name"},Combiner.CombineTextByDelimiter(", ", QuoteStyle.None),"Employee"),
    #"Renamed CleanedJob to Job" = Table.RenameColumns(#"Added Employee",{{"CleanedJobCode", "Job"}}),
    #"Filtered EmployeeId not empty" = Table.SelectRows(#"Renamed CleanedJob to Job", each [EmployeeID] <> null and [EmployeeID] <> ""),
    #"Filtered emp_id not empty" = Table.SelectRows(#"Filtered EmployeeId not empty", each [emp_id] <> null and [emp_id] <> ""),
    #"Merged ll_country" = Table.NestedJoin(#"Filtered emp_id not empty", {"country_code_iso3"}, #"pub ll_country", {"country_code_iso3"}, "pub ll_country", JoinKind.LeftOuter),
    #"Expanded country" = Table.ExpandTableColumn(#"Merged ll_country", "pub ll_country", {"country"}, {"country"})
in
    #"Expanded country"
```


## Table: Key Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: DimCC


```m
let
    Source = #"rep v_ll_CC",
    #"Sorted Rows" = Table.Sort(Source,{{"sort_id", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: File Modified


```m
let
    Source = {[Date modified = DateTime.LocalNow(), Source = "datahub"]},
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"Date modified", "Source"}, {"Date modified", "Source"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Column1",{{"Date modified", type datetime}, {"Source", type text}})
in
    #"Changed Type"
```


## Table: rls cc permission


```m
let
    Source = #"sec acp_permissionCc"
in
    Source
```


## Table: Contribution


```m
let
    Source = #"sec ContributionInclAjdustments"
in
    Source
```


## Table: SAP MAX Month


```m
let
    Source = #"max_acp_month"
in
    Source
```


## Table: Display


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WckwuySxLVYrVATJzcpRiYwE=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Type = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Type", type text}})
in
    #"Changed Type"
```


## Table: rls direct emp permission


```m
let
    Source = #"sec acp_permissionEmployee",
    #"Renamed Columns1" = Table.RenameColumns(Source,{{"emp_ids_concatenated", "Additional employee AP"}, {"userMail", "User Email"}}),
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(#"Renamed Columns1", {{"Additional employee AP", Splitter.SplitTextByDelimiter(",", QuoteStyle.None), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "Additional employee AP"),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Additional employee AP", type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type",{{"Additional employee AP", Text.Trim, type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Trimmed Text",{{"Additional employee AP", "Additional EmpId"}})
in
    #"Renamed Columns"
```


## Table: global cc permission


```m
let
    Source = #"sec acp_permissionGlobal"
in
    Source
```


## Table: DimProjectsForGlobalCCs


```m
let
    Source = Table.SelectColumns(#"Contribution", { "ProjectNumber"}),
    #"Removed Duplicates" = Table.Distinct(Source),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"ProjectNumber"}, #"rep v_acp_fc_project_data", {"project_number"}, "rep v_acp_fc_project_data", JoinKind.LeftOuter),
    #"Expanded rep v_fc_psr_project_data" = Table.ExpandTableColumn(#"Merged Queries", "rep v_acp_fc_project_data", {"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "dm_cc_id", "dm_cc", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "project_status", "sales_unit_cou_iso3", "sales_unit_cou_country", "function_id", "industry_id"}, {"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "dm_cc_id", "dm_cc", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "project_status", "sales_unit_cou_iso3", "sales_unit_cou_country", "function_id", "industry_id"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded rep v_fc_psr_project_data",{"project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "responsible_accounting_emp_id", "responsible_accounting"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Inserted First Characters" = Table.AddColumn(#"Filtered Rows", "Project", each Text.Start([project_name], 40), type text),
    #"merge function cc" = Table.NestedJoin(#"Inserted First Characters", {"function_id"}, #"rep v_ll_industry_functional_cc", {"cc_id"}, "rep v_ll_industry_functional_cc", JoinKind.LeftOuter),
    #"Expanded rep v_ll_CC" = Table.ExpandTableColumn(#"merge function cc", "rep v_ll_industry_functional_cc", {"cc_name"}, {"function_cc_name"}),
    #"merge industry cc" = Table.NestedJoin(#"Expanded rep v_ll_CC", {"industry_id"}, #"rep v_ll_industry_functional_cc", {"cc_id"}, "rep v_ll_industry_functional_cc", JoinKind.LeftOuter),
    #"Expanded DimCC" = Table.ExpandTableColumn(#"merge industry cc", "rep v_ll_industry_functional_cc", {"cc_name"}, {"industry_cc_name"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded DimCC", each [project_number] <> null and [project_number] <> "")
in
    #"Filtered Rows1"
```


## Table: FactCC_OrderIncomeByMonth


```m
let
    Source = #"sec acp_orderIncome_byMonth",
    #"Grouped Rows" = Table.Group(Source, {"ProjectNumber", "Month", "Year"}, {{"Order Income", each List.Max([Order Income]), type number}})
in
    #"Grouped Rows"
```


## Table: FactCC_PaidByYear


```m
let
    Source = #"sec acp_values_byYear",
    #"Grouped Rows" = Table.Group(Source, {"ProjectNumber", "Year"}, {{"Paid Year", each List.Max([Paid Year]), type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Grouped Rows", each [Paid Year] <> null)
in
    #"Filtered Rows"
```


## Table: FactCC_InvoicedByYear


```m
let
    Source = #"sec acp_values_byYear",
    #"Grouped Rows" = Table.Group(Source, {"ProjectNumber", "Year"}, {{"Invoiced Year", each List.Max([Invoiced Year]), type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Grouped Rows", each [Invoiced Year] <> null)
in
    #"Filtered Rows"
```


## Table: CCContribution


```m
let
    Source = Contribution
in
    Source
```


## Table: sec acp_metadata


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    sec_acp_metadata = Source{[Schema="sec",Item="acp_metadata"]}[Data],
    #"Filtered Rows" = Table.SelectRows(sec_acp_metadata, each [year] = Year),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows", "max_acp_month", each Date.Month([max_acp_date]),Int64.Type)
in
    #"Added Custom"
```


## Table: Platforms


```m
let
    Source = #"pub ll_platform"
in
    Source
```


## Table: sec acp_metadata_month


```m
let
    Source = #"sec acp_metadata",
    max_acp_month1 = Source{0}[max_acp_month]
in
    max_acp_month1
```


## Parameter: Year


```m
2021 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true]
```


## Roles

### default


Model Permission: Read

DimEmployees

```m
var _UserPrincipalName = UserPrincipalName()

var employeeCountry = DimEmployees[country_code_iso3]
var employeeCc = DimEmployees[cc_id]

var combinations = CALCULATETABLE('rls cc permission', 'rls cc permission'[email] = _UserPrincipalName)

var ccAllAndCcAll =  CALCULATETABLE('rls cc permission', FILTER('rls cc permission', 'rls cc permission'[CCId] = "-9999" && 'rls cc permission'[country_code_iso3] = "ALL" ), combinations)
var ccSingleAndCcSingle =  CALCULATETABLE('rls cc permission', FILTER('rls cc permission', 'rls cc permission'[CCId] <> "-9999" && 'rls cc permission'[country_code_iso3] <> "ALL" ), combinations)
var ccAllAndCountrySingle =  CALCULATETABLE('rls cc permission', Filter('rls cc permission',  'rls cc permission'[CCId] = "-9999" && 'rls cc permission'[country_code_iso3] <> "ALL"), combinations)
var ccSingleAndCountryAll =  CALCULATETABLE('rls cc permission', Filter('rls cc permission',  'rls cc permission'[CCId] <> "-9999" && 'rls cc permission'[country_code_iso3] = "ALL"), combinations)


return switch(true(),
    //all
    COUNTROWS(ccAllAndCcAll) > 0, true() //"Yes ALL",

    //own user
    , DimEmployees[email] == _UserPrincipalName, true() // "YES own"
  
	//permission for cc_id  
	, countrows(ccSingleAndCountryAll) > 0  && calculate(COUNTROWS('rls cc permission'), FILTER('rls cc permission', 'rls cc permission'[CCId] = employeeCc), ccSingleAndCountryAll) > 0, true() //"YES ccSCAll"
    //permission for country  
    , countrows(ccAllAndCountrySingle) > 0 && calculate(COUNTROWS('rls cc permission'), ccAllAndCountrySingle, FILTER('rls cc permission', 'rls cc permission'[country_code_iso3] = employeeCountry)), true() // "YESccACS"


	//permission for cc_id  and country
	, countrows(ccSingleAndCcSingle) > 0  && calculate(COUNTROWS('rls cc permission'), FILTER('rls cc permission', 'rls cc permission'[CCId] = employeeCc && 'rls cc permission'[country_code_iso3] = employeeCountry), ccSingleAndCcSingle) > 0, true() // "YES cc and country"
    
	//additional employee		
	,Calculate(
				CountRows('rls direct emp permission')
							, Filter
								('rls direct emp permission',
								EARLIER(DimEmployees[emp_id]) = 'rls direct emp permission'[Additional EmpId] 
								&& _UserPrincipalName = 'rls direct emp permission'[User Email]
								)
					)>0
				, true() // "YES direct"
)
```



DimProjectsForGlobalCCs

```m
if(LOOKUPVALUE('global cc permission'[User Email],'global cc permission'[Global CC ID], -9999)<> Blank(),true(),

if(LOOKUPVALUE('global cc permission'[User Email],'global cc permission'[Global CC ID], DimProjectsForGlobalCCs[function_id], 'global cc permission'[User Email], userprincipalname())<> Blank()
    , true()
    , if(LOOKUPVALUE('global cc permission'[User Email],'global cc permission'[Global CC ID], DimProjectsForGlobalCCs[industry_id], 'global cc permission'[User Email], userprincipalname())<> Blank()
        , true()
        , false()
    )
)

)
```



global cc permission

```m
[User Email] = userprincipalname()
```

