



# M Code

|Dataset|[Working Capital DACH- Health_Consumer](./../Working-Capital-DACH--Health_Consumer.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: MeasureTable


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: RollingCalender


```m
let
    Source = #date(2016,1,1),
    Custom1 = List.Dates (Source, Number.From(DateTime.LocalNow()) - Number.From(Source), #duration(1,0,0,0)),
    #"Converted to Table" = Table.FromList(Custom1, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{{"Column1", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Date"}}),
    #"Inserted Month Name" = Table.AddColumn(#"Renamed Columns", "Month Name", each Date.MonthName([Date]), type text),
    #"Extracted First Characters" = Table.TransformColumns(#"Inserted Month Name", {{"Month Name", each Text.Start(_, 3), type text}}),
    #"Inserted Year" = Table.AddColumn(#"Extracted First Characters", "Year", each Date.Year([Date]), Int64.Type),
    #"Extracted Last Characters" = Table.TransformColumns(#"Inserted Year", {{"Year", each Text.End(Text.From(_, "de-DE"), 2), type text}}),
    #"Merged Columns" = Table.CombineColumns(#"Extracted Last Characters",{"Month Name", "Year"},Combiner.CombineTextByDelimiter("-", QuoteStyle.None),"Date_short"),
    #"Inserted Year1" = Table.AddColumn(#"Merged Columns", "Year", each Date.Year([Date]), Int64.Type),
    #"Multiplied Column" = Table.TransformColumns(#"Inserted Year1", {{"Year", each _ * 100, type number}}),
    #"Inserted Month" = Table.AddColumn(#"Multiplied Column", "Month", each Date.Month([Date]), Int64.Type),
    #"Inserted Addition" = Table.AddColumn(#"Inserted Month", "Addition", each [Year] + [Month], type number),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Addition",{{"Addition", "Date_sort"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns1", "0", each 0)
in
    #"Added Custom"
```


## Table: WIP


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WORK_IN_PROGRESS = WorkingCapitalMgmt{[Schema="dbo",Item="WORK_IN_PROGRESS"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_WORK_IN_PROGRESS, each ([PROJECT_FOR_CALCULATION] = "Yes")),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"PROJECT_ID"}, Controller, {"PROJECT_ID"}, "Controller", JoinKind.LeftOuter),
    #"Expanded Controller" = Table.ExpandTableColumn(#"Merged Queries", "Controller", {"F&C Reponsible"}, {"Controller.F&C Reponsible"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded Controller", each ([COMPANY] = "Austria" or [COMPANY] = "Germany" or [COMPANY] = "Switzerland")),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows1",{{"LAST_INVOICE_DATE", type date}, {"PROJECT_START", type date}}),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type", "AGE_OF_WIP_for Traffic light", each if [OPEN_WIP] > 1 then [AGE_OF_WIP] else 0),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Overdue ID", each if [AGE_OF_WIP] > 30 then 1 else 0),
    #"Added Conditional Column2" = Table.AddColumn(#"Added Conditional Column1", "Open Amount Positive ID", each if [OPEN_WIP] > 1 then 1 else 0)
in
    #"Added Conditional Column2"
```


## Table: AR


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES"]}[Data],
    #"Merged Queries" = Table.NestedJoin(dbo_RECEIVABLES, {"PROJECT_ID"}, Controller, {"PROJECT_ID"}, "Controller", JoinKind.LeftOuter),
    #"Expanded Controller" = Table.ExpandTableColumn(#"Merged Queries", "Controller", {"F&C Reponsible"}, {"Controller.F&C Reponsible"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Controller", each ([RECEIVABLE_COMPANY] = "Austria" or [RECEIVABLE_COMPANY] = "Germany" or [RECEIVABLE_COMPANY] = "Switzerland")),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"NET_DUE_DATE_ADJUSTED", type date}, {"NET_DUE_DATE", type date}, {"INVOICE_DATE", type date}}),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type", "Overdue ID", each if [DAYS_OVERDUE] > 0 then 1 else 0),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Open Amount Positive ID", each if [OPEN_AMOUNT] > 1 then 1 else 0),
    #"Filtered Rows1" = Table.SelectRows(#"Added Conditional Column1", each Text.StartsWith([PROJECT_ID], "CP"))
in
    #"Filtered Rows1"
```


## Table: Aging


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: Controller


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_PROJECT_RESPONSIBLE_ACCOUNTING = ByD_ODP{[Schema="dbo",Item="BYD_PROJECT_RESPONSIBLE_ACCOUNTING"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(dbo_BYD_PROJECT_RESPONSIBLE_ACCOUNTING,{{"RESPONSIBLE_PROJECT_ACCOUNTING_ID", "RESPONSIBLE_PROJECT_ACCOUNTING_ID"}, {"RESPONSIBLE_PROJECT_ACCOUNTING", "F&C Reponsible"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns", {"PROJECT_ID"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Duplicates", {"PROJECT_ID"})
in
    #"Removed Duplicates1"
```


## Table: Partner List


```m
let
    Source = Table.Combine({AR, WIP}),
    #"Removed Duplicates" = Table.Distinct(Source, {"EMPLOYEE_RESPONSIBLE_OLD"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Duplicates", {"EMPLOYEE_RESPONSIBLE_ID"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Removed Duplicates1", "CompanyID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [PROJECT_COMPANY_ID]}, ""), type text),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Merged Column",{"CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "PROJECT_STATUS", "COMPANY_ID", "COMPANY", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"EMPLOYEE_RESPONSIBLE", "P/PRI"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns",null,"NA",Replacer.ReplaceValue,{"EMPLOYEE_RESPONSIBLE_ID"})
in
    #"Replaced Value"
```


## Table: Customer List


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Removed Other Columns" = Table.SelectColumns(Source,{"CUSTOMER_ID", "CUSTOMER"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns", {"CUSTOMER_ID"})
in
    #"Removed Duplicates"
```


## Table: CP List


```m
let
    Source = Table.Combine({AR, WIP}),
    #"Replaced Value" = Table.ReplaceValue(Source,null,"NA",Replacer.ReplaceValue,{"PROJECT_ID"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Replaced Value", "CompanyID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [PROJECT_COMPANY_ID]}, ""), type text),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Merged Column",{"CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "PROJECT_STATUS", "COMPANY_ID", "COMPANY", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "CUSTOMER_ID", "CUSTOMER"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"PROJECT_ID", "Project ID"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns", {"Project ID"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([CompanyID2] = "1000000" or [CompanyID2] = "12000000" or [CompanyID2] = "24000000" or [CompanyID2] = "25000000" or [CompanyID2] = "26000000" or [CompanyID2] = "65000000" or [CompanyID2] = "78000000" or [CompanyID2] = "97000000"))
in
    #"Filtered Rows"
```


## Table: Controller List


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_PROJECT_RESPONSIBLE_ACCOUNTING = ByD_ODP{[Schema="dbo",Item="BYD_PROJECT_RESPONSIBLE_ACCOUNTING"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(dbo_BYD_PROJECT_RESPONSIBLE_ACCOUNTING,{{"RESPONSIBLE_PROJECT_ACCOUNTING_ID", "RESPONSIBLE_PROJECT_ACCOUNTING_ID"}, {"RESPONSIBLE_PROJECT_ACCOUNTING", "F&C Reponsible"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns", {"PROJECT_ID"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Duplicates", {"PROJECT_ID"}),
    #"Removed Duplicates2" = Table.Distinct(#"Removed Duplicates1", {"RESPONSIBLE_PROJECT_ACCOUNTING_ID"})
in
    #"Removed Duplicates2"
```


## Table: SAP_Industry


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Removed Other Columns" = Table.SelectColumns(Source,{"INDUSTRY", "INDUSTRY_ID"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns", {"INDUSTRY_ID"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Duplicates", {"INDUSTRY"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Duplicates1",null,"""not assigned""",Replacer.ReplaceValue,{"INDUSTRY"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,"""not assigned""",Replacer.ReplaceValue,{"INDUSTRY_ID"}),
    #"Sorted Rows" = Table.Sort(#"Replaced Value1",{{"INDUSTRY", Order.Ascending}, {"INDUSTRY_ID", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: SAP_Functions


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Filtered Rows1" = Table.SelectRows(Source, each ([COMPANY] = "Austria" or [COMPANY] = "Germany" or [COMPANY] = "Switzerland")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"FUNCTION", "FUNCTION_ID"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns", {"FUNCTION_ID"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each true),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION_ID"})
in
    #"Replaced Value1"
```


## Table: SAP_Platform


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Filtered Rows" = Table.SelectRows(Source, each ([COMPANY] = "Austria" or [COMPANY] = "Germany" or [COMPANY] = "Switzerland")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"EMP_PLATFORM", "EMP_PLATFORM_ID"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns", {"EMP_PLATFORM"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Duplicates",null,"""not assigned""",Replacer.ReplaceValue,{"EMP_PLATFORM"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,"""not assigned""",Replacer.ReplaceValue,{"EMP_PLATFORM_ID"})
in
    #"Replaced Value1"
```


## Table: SAP_Sales_Unit


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Filtered Rows1" = Table.SelectRows(Source, each ([COMPANY] = "Austria" or [COMPANY] = "Germany" or [COMPANY] = "Switzerland")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"SALES_UNIT", "SALES_UNIT_ID"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each true),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows", {"SALES_UNIT_ID"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Duplicates", {"SALES_UNIT"}),
    #"Removed Duplicates2" = Table.Distinct(#"Removed Duplicates1", {"SALES_UNIT_ID"}),
    #"Removed Duplicates3" = Table.Distinct(#"Removed Duplicates2", {"SALES_UNIT_ID"})
in
    #"Removed Duplicates3"
```


## Table: RB Companies


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "byd_odp", [Query="SELECT [ACT_AS_ORG_UNIT]#(lf)      ,[ACCOUNT_ID]#(lf)      ,[ACCOUNT]#(lf)      ,[STREET]#(lf)      ,[HOUSE_NUMBER]#(lf)      ,[STREET_NR_FMT]#(lf)      ,[POSTAL_CODE]#(lf)      ,[CITY]#(lf)      ,[DISTRICT]#(lf)      ,[STATE]#(lf)      ,[ADDRESS_FMT]#(lf)      ,[COUNTRY_ISO2]#(lf)      ,[COUNTRY_ISO3]#(lf)      ,[COUNTRY]#(lf)      ,[REGION]#(lf)      ,[ZONE]#(lf)      ,[ORGANIZATIONAL_CCENTER_ID]#(lf)      ,[FUNCTIONAL_UNIT_ID]#(lf)      ,[FUNCTIONAL_UNIT]#(lf)      ,[COMPANY_NAME]#(lf)      ,[COMPANY_ID_MIS]#(lf)      ,[SAP_START]#(lf)      ,[COUNTRY_CURRENCY]#(lf)      ,[EXPORTED_ON]#(lf)  FROM [ByD_ODP].[dbo].[BYD_RB_COMPANIES]#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ACCOUNT_ID", Int64.Type}, {"FUNCTIONAL_UNIT_ID", Int64.Type}, {"ORGANIZATIONAL_CCENTER_ID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EXPORTED_ON", "ACT_AS_ORG_UNIT"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"COUNTRY_ISO3", "COUNTRY_ISO3"}}),
    #"ISO3 PlX" = Table.AddColumn(#"Renamed Columns", "Country_ISO3_PLX", each if [ORGANIZATIONAL_CCENTER_ID] = 46000000 then "PLX" else if [ORGANIZATIONAL_CCENTER_ID] = 47000000 then "PLX" else if [ORGANIZATIONAL_CCENTER_ID] = 48000000 then "PLX" else if [ORGANIZATIONAL_CCENTER_ID] = 49000000 then "PLX" else [COUNTRY_ISO3])
in
    #"ISO3 PlX"
```


## Table: DACH Platform Mapping


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/DACH%20Platform%20Mapping.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Sheet1_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}})
in
    #"Changed Type"
```


## Table: DACH Platform_mapping


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/DACH%20Platform%20Mapping.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Sheet1_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Project (Sales Unit)", type text}, {"Project (Sales Unit Text)", type text}, {"Platform", type text}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Changed Type1",{"Project (Sales Unit Text)", "Platform", "Project (Sales Unit)"}),
    #"Removed Duplicates" = Table.Distinct(#"Reordered Columns", {"Project (Sales Unit Text)"}),
    #"Added Conditional Column" = Table.AddColumn(#"Removed Duplicates", "Platform_Adjusted(INV)", each if Text.Contains([#"Project (Sales Unit Text)"], "Investor Support") then "Investor Support" else if [#"Project (Sales Unit Text)"] = null then "Other" else [Platform])
in
    #"Added Conditional Column"
```


## Table: Query1


```m
let
    Source = ""
in
    Source
```


## Table: Overdue ID Mapped


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUYpMLVaK1YlWMgCy/fKVYmMB", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Overdue ID" = _t, #"Overdue Status" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Overdue ID", Int64.Type}, {"Overdue Status", type text}})
in
    #"Changed Type"
```


## Table: Open Amount Positive ID Mapped


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUYpMLVaK1YlWMgCy/fKVYmMB", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Open Amount Positive ID" = _t, #"Open Amount Positive" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Open Amount Positive ID", Int64.Type}, {"Open Amount Positive", type text}})
in
    #"Changed Type"
```

