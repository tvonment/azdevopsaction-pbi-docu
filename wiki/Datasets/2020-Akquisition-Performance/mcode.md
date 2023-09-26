



# M Code

|Dataset|[2020 Akquisition Performance](./../2020-Akquisition-Performance.md)|
| :--- | :--- |
|Workspace|[Acquisition Performance](../../Workspaces/Acquisition-Performance.md)|

## Table: FactOrderIncomeByMonth


```m
let
    Source = Table.Combine({#"Order Income by month SAP", #"Order Income by month AS400", #"AdditionalEmployee Adjustment Order Income"}),
    #"Merged Queries" = Table.NestedJoin(Source, {"EmployeeID", "ProjectNumber"}, Contribution, {"EmployeeID", "ProjectNumber"}, "Contribution", JoinKind.LeftOuter),
    #"Expanded Contribution" = Table.ExpandTableColumn(#"Merged Queries", "Contribution", {"Index"}, {"Contribution.Index"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Contribution", each [Month] <= #"SAP MAX Month")
in
    #"Filtered Rows"
```


## Table: FactPaidByYear


```m
let
    Source = Table.Combine({#"Paid by year SAP", #"Paid by year AS400", #"Paid by year Adjustment", #"AdditionalEmployee Adjustment Paid"}),
    #"Merged Queries" = Table.NestedJoin(Source, {"EmployeeID", "ProjectNumber"}, Contribution, {"EmployeeID", "ProjectNumber"}, "Contribution", JoinKind.LeftOuter),
    #"Expanded Contribution" = Table.ExpandTableColumn(#"Merged Queries", "Contribution", {"Index"}, {"Contribution.Index"})
in
    #"Expanded Contribution"
```


## Table: FactInvoicedByYear


```m
let
    Source = Table.Combine({#"Invoiced by year SAP", #"Invoiced by year AS400", #"AdditionalEmployee Adjustment Invoiced"}),
    #"Merged Queries" = Table.NestedJoin(Source, {"EmployeeID", "ProjectNumber"}, Contribution, {"EmployeeID", "ProjectNumber"}, "Contribution", JoinKind.LeftOuter),
    #"Expanded Contribution" = Table.ExpandTableColumn(#"Merged Queries", "Contribution", {"Index"}, {"Contribution.Index"})
in
    #"Expanded Contribution"
```


## Table: DimProjects


```m
let
    Source = Table.SelectColumns(#"Contribution Building", { "ProjectNumber"}),
    #"Removed Duplicates" = Table.Distinct(Source),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"ProjectNumber"}, #"rep v_acp_fc_project_data", {"project_number"}, "rep v_acp_fc_project_data", JoinKind.LeftOuter),
    #"Expanded rep v_fc_psr_project_data" = Table.ExpandTableColumn(#"Merged Queries", "rep v_acp_fc_project_data", {"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "dm_cc_id", "dm_cc", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "project_status", "sales_unit_cou_iso3", "sales_unit_cou_country","responsible_unit_cou_iso3", "function_id", "industry_id"}, {"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_start", "project_planned_end", "project_closedate", "dm_cc_id", "dm_cc", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "project_status", "sales_unit_cou_iso3", "sales_unit_cou_country","responsible_unit_cou_iso3", "function_id", "industry_id"}),
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
    Source = Table.SelectColumns(#"Contribution Building", {"EmployeeID"}),
    #"Removed Duplicates" = Table.Distinct(Source),
    #"Merged Queries1" = Table.NestedJoin(#"Removed Duplicates", {"EmployeeID"}, hide_employees, {"emp_id"}, "hide_employees", JoinKind.LeftAnti),
    #"Removed Columns1" = Table.RemoveColumns(#"Merged Queries1",{"hide_employees"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns1", {"EmployeeID"}, #"rep v_acp_hr_employee", {"emp_id"}, "rep v_acp_hr_employee", JoinKind.LeftOuter),
    #"Expanded sec imp_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_acp_hr_employee", {"emp_id", "last_name", "first_name", "full_name", "jobcode_id", "jobcode", "job_subcategory_short", "job_subcategory", "jobfunction", "cc_id", "cc_name", "email", "country_code_iso3", "country", "emp_status", "termination_date", "ExitInApYear"}, {"emp_id", "last_name", "first_name", "full_name", "jobcode_id", "jobcode", "job_subcategory_short", "job_subcategory", "jobfunction", "cc_id", "cc_name", "email", "country_code_iso3", "country", "emp_status", "termination_date", "ExitInApYear"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded sec imp_hr_employee",{{"ExitInApYear", type logical}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{ "jobfunction"}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Removed Columns", "CleanedJobCode", each Text.BeforeDelimiter([jobcode], " "), type text),
    #"Merged Force Show" = Table.NestedJoin(#"Inserted Text Before Delimiter", {"EmployeeID"}, #"Adjust ForceShow", {"EmployeeID"}, "Adjust ForceShow", JoinKind.LeftOuter),
    #"Expanded Adjust ForceShow" = Table.ExpandTableColumn(#"Merged Force Show", "Adjust ForceShow", {"EmployeeID"}, {"ForceShow"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Adjust ForceShow", each ([CleanedJobCode] = "Partner" or [CleanedJobCode] = "Principal" or [CleanedJobCode] = "Director" or ([ForceShow] <> null and [ForceShow] <> ""))),
    #"Change emp_status to active for force show" = Table.ReplaceValue(#"Filtered Rows",each [emp_status], each if [ForceShow] <> null then "A" else [emp_status],Replacer.ReplaceText,{"emp_status"}),
    #"Added Conditional Column" = Table.AddColumn(#"Change emp_status to active for force show", "IsPartner", each if [CleanedJobCode] = "Partner" then 1 else  0, type number),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "IsPrincipal", each if [CleanedJobCode] = "Principal" then 1 else 0, type number),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Conditional Column1", "Employee (Job)", each Text.Combine({[full_name], " (", [CleanedJobCode], ")"}), type text),
    #"Merged Columns" = Table.CombineColumns(#"Inserted Merged Column",{"full_name"},Combiner.CombineTextByDelimiter(", ", QuoteStyle.None),"Employee"),
    #"Renamed Columns" = Table.RenameColumns(#"Merged Columns",{{"CleanedJobCode", "Job"}})
in
    #"Renamed Columns"
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
    Source = Table.Combine({#"FileModified SAP", #"FileModified AS400"}),
    Result = Table.InsertRows(Source, 0, {[Date modified = DateTime.LocalNow(), Source = "datahub"]})
in
    Result
```


## Table: rls cc permission


```m
let
    Source = permission,
    #"Merged Columns" = Table.CombineColumns(Source,{"TO Mail Adress", "CC Mail Adress", "Group Mail Adress To", "Group Mail CC"},Combiner.CombineTextByDelimiter(",", QuoteStyle.None),"email"),
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(#"Merged Columns", {{"email", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "email"),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"email", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [email] <> ""),
    #"Trimmed Text" = Table.TransformColumns(#"Filtered Rows",{{"email", Text.Trim, type text}})
in
    #"Trimmed Text"
```


## Table: Contribution


```m
let
    Source = #"Contribution Building"
in
    Source
```


## Table: SAP MAX Month


```m
let
    Source = #"AP SAP",
    Column1 = Date.Month(Date.From(Source{0}[Column7]))
in
    Column1
```


## Table: Display


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WckwuySxLVYrViVZyrcgsKVaKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Type = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Type", type text}})
in
    #"Changed Type"
```


## Table: rls direct emp permission


```m
let
    Source = #"direct emp permission",
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(Source, {{"Additional employee AP", Splitter.SplitTextByDelimiter(",", QuoteStyle.None), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "Additional employee AP"),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Additional employee AP", type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type",{{"Additional employee AP", Text.Trim, type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Trimmed Text",{{"Additional employee AP", "Additional EmpId"}})
in
    #"Renamed Columns"
```


## Table: global cc permission


```m
let
    Source = Excel.Workbook(File.Contents(#"Folder Path" & "AP permission.xlsx"), null, true),
    globalCCs_Table = Source{[Item="globalCCs",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(globalCCs_Table,{{"User Email", type text}, {"Global CC ID", Int64.Type}, {"global cc name", type text}, {"Bemerkung", type text}})
in
    #"Changed Type"
```


## Table: DimProjectsForGlobalCCs


```m
let
    Source = Table.SelectColumns(#"Contribution Building", { "ProjectNumber"}),
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
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded DimCC",{{"function_id", Int64.Type}, {"industry_id", Int64.Type}}),
    #"Filtered Rows1" = Table.SelectRows(#"Changed Type", each [project_number] <> null and [project_number] <> ""),
    #"Filtered Rows2" = Table.SelectRows(#"Filtered Rows1", each [ProjectNumber] <> null and [ProjectNumber] <> "")
in
    #"Filtered Rows2"
```


## Table: FactCC_OrderIncomeByMonth


```m
let
    Source = Table.Combine({#"Order Income by month SAP", #"Order Income by month AS400"}),
    #"Filtered Rows" = Table.SelectRows(#"Source", each [Month] <= #"SAP MAX Month"),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"EmployeeID"}),
    #"Grouped Rows" = Table.Group(#"Removed Columns", {"ProjectNumber", "Month", "Year"}, {{"Order Income", each List.Max([Order Income]), type number}})
in
    #"Grouped Rows"
```


## Table: FactCC_PaidByYear


```m
let
    Source = Table.Combine({#"Paid by year SAP", #"Paid by year AS400"}),
    #"Removed Columns" = Table.RemoveColumns(Source,{"EmployeeID"}),
    #"Grouped Rows" = Table.Group(#"Removed Columns", {"ProjectNumber", "Year"}, {{"Paid Year", each List.Max([Paid Year]), type number}})
in
    #"Grouped Rows"
```


## Table: FactCC_InvoicedByYear


```m
let
    Source = Table.Combine({#"Invoiced by year SAP", #"Invoiced by year AS400"}),
    #"Removed Columns" = Table.RemoveColumns(Source,{"EmployeeID"}),
    #"Grouped Rows" = Table.Group(#"Removed Columns", {"ProjectNumber", "Year"}, {{"Invoiced Year", each List.Max([Invoiced Year]), type number}})
in
    #"Grouped Rows"
```


## Table: CCContribution


```m
let
    Source = Contribution
in
    Source
```


## Table: Paid SapAndAS400 by project


```m
let
    Source = Table.Combine({#"Paid by year SAP", #"Paid by year AS400"}),
    #"Removed Columns" = Table.RemoveColumns(Source,{"EmployeeID"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns")
in
    #"Removed Duplicates"
```


## Table: AdditionalEmployee Adjustment Paid


```m
let
    Source = Table.NestedJoin(#"Adjust AdditionalEmployees", {"ProjectID"}, #"Paid SapAndAS400 by project", {"ProjectNumber"}, "Paid SapAndAS400 by project", JoinKind.LeftOuter),
    #"Removed Columns" = Table.RemoveColumns(Source,{ "Contribution", "Employee", "Client", "Project", "angelegt am", "angelegt von", "Bemerkung"}),
    #"Expanded Paid SapAndAS400 by project" = Table.ExpandTableColumn(#"Removed Columns", "Paid SapAndAS400 by project", {"ProjectNumber", "Paid Year", "Year"}, {"ProjectNumber", "Paid Year", "Year"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Paid SapAndAS400 by project", each [ProjectNumber] <> null),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows",{"ProjectID"})
in
    #"Removed Columns1"
```


## Table: Invoiced SapAndAS400 by project


```m
let
    Source = Table.Combine({#"Invoiced by year SAP", #"Invoiced by year AS400"}),
    #"Removed Columns" = Table.RemoveColumns(Source,{"EmployeeID"}),
    #"Trimmed Text" = Table.TransformColumns(#"Removed Columns",{{"ProjectNumber", Text.Trim, type text}}),
    #"Removed Duplicates" = Table.Distinct(#"Trimmed Text")
in
    #"Removed Duplicates"
```


## Table: AdditionalEmployee Adjustment Invoiced


```m
let
    Source = Table.NestedJoin(#"Additional Employee Adjustment", {"ProjectNumber"}, #"Invoiced SapAndAS400 by project", {"ProjectNumber"}, "Invoiced SapAndAS400 by project", JoinKind.LeftOuter),
    #"Expanded Invoiced SapAndAS400 by project" = Table.ExpandTableColumn(Source, "Invoiced SapAndAS400 by project", {"ProjectNumber", "Invoiced Year", "Year"}, {"ProjectNumber.1", "Invoiced Year", "Year"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Invoiced SapAndAS400 by project", each [ProjectNumber.1] <> null),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Contribution", "ProjectNumber.1"})
in
    #"Removed Columns"
```


## Table: Order Income SapAndAS400 by project


```m
let
    Source = Table.Combine({#"Order Income by month SAP", #"Order Income by month AS400"}),
    #"Removed Columns" = Table.RemoveColumns(Source,{"EmployeeID"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns")
in
    #"Removed Duplicates"
```


## Table: AdditionalEmployee Adjustment Order Income


```m
let
    Source = Table.NestedJoin(#"Additional Employee Adjustment", {"ProjectNumber"}, #"Order Income SapAndAS400 by project", {"ProjectNumber"}, "Order Income SapAndAS400 by project", JoinKind.LeftOuter),
    #"Expanded Order Income SapAndAS400 by project" = Table.ExpandTableColumn(Source, "Order Income SapAndAS400 by project", { "Order Income", "Month", "Year"}, { "Order Income", "Month", "Year"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Order Income SapAndAS400 by project", each [Year] <> null),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Contribution"})
in
    #"Removed Columns"
```


## Parameter: SAP FileName


```m
"AP input by SAP.XLSX" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: AS400 FileName


```m
"Acquisition_performance_nach_Zahlung_Partner.csv" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: Year


```m
2020 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true]
```


## Parameter: Folder Path


```m
"\\muc-file-1\Services\Holding\SSIS_Resources\Aquisition_Performance\2020\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: Adjustments FileName


```m
"AP adjustments.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Roles

### default


Model Permission: Read

DimEmployees

```m
//all ccs
if(LOOKUPVALUE('rls cc permission'[CCId], 'rls cc permission'[email], UserPrincipalName(),'rls cc permission'[CCId], "-9999", Blank())<> Blank(), True(),

//own user
if( DimEmployees[email] == UserPrincipalName(), true()
  
	//permissionfor cc_id  
	, if(LOOKUPVALUE('rls cc permission'[CCId], 'rls cc permission'[email], UserPrincipalName(), 'rls cc permission'[CCId], DimEmployees[cc_id], Blank())<> Blank()
			,True()
			
			,if(Calculate(
				CountRows('rls direct emp permission')
							, Filter
								('rls direct emp permission',
								EARLIER(DimEmployees[emp_id]) = 'rls direct emp permission'[Additional EmpId] 
								&& UserPrincipalName() = 'rls direct emp permission'[User Email]
								)
					)>0
				, True()
				, False()
				)
		)
	)
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

