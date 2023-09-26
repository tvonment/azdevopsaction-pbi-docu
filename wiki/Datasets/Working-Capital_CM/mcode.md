



# M Code

|Dataset|[Working Capital_CM](./../Working-Capital_CM.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: QAP


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "AccountingReportingPackage"),
    dbo_GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC = Source{[Schema="dbo",Item="GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(dbo_GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC,{{"MIS_COMPANY_ID", Int64.Type}, {"BYD_COMPANY_ID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"SYSTEM", "CHART_OF_ACCOUNTS", "AMOUNT", "AMOUNT_CUR", "FX_RATE", "MIS_COMPANY_ID", "ACCOUNT_FLAG", "ACCOUNT_FLAG_IC", "BP_1", "ACCOUNT_FLAG_TD_PL", "TRANS_DEVEL", "TCF", "ALLOC_CHART_OF_ACCOUNTS", "BP_2", "GL_IDENTIFIER", "GL_ACCOUNT"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Columns",{"BYD_COMPANY_ID", "COMPANY", "GL_ACCOUNT_ID", "GL_ACCOUNT_DESCRIPTION", "GL_ACCOUNT_SHORT_NAME", "PERIOD_M", "PERIOD_Q", "PERIOD_Y", "CS_FU", "ALLOC_GL_ACCOUNT", "ALLOC_GL_ACCOUNT_DESCRIPTION", "ALLOC_GL_ACCOUNT_SHORT_NAME", "ACCOUNTING_PERIOD", "FISCAL_YEAR", "XY_IDENTIFIER", "PARENT_GL_ACCOUNT_ID", "AMOUNT_EUR"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Reordered Columns", "Merged", each Text.Combine({Text.From([ACCOUNTING_PERIOD], "de-DE"), Text.From([FISCAL_YEAR], "de-DE")}, "."), type text),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Merged Column",{{"Merged", "Date_interim"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", each 15),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Custom", "Date_interim_2"}}),
    #"Reordered Columns1" = Table.ReorderColumns(#"Renamed Columns1",{"BYD_COMPANY_ID", "COMPANY", "GL_ACCOUNT_ID", "GL_ACCOUNT_DESCRIPTION", "GL_ACCOUNT_SHORT_NAME", "PERIOD_M", "PERIOD_Q", "PERIOD_Y", "CS_FU", "ALLOC_GL_ACCOUNT", "ALLOC_GL_ACCOUNT_DESCRIPTION", "ALLOC_GL_ACCOUNT_SHORT_NAME", "ACCOUNTING_PERIOD", "FISCAL_YEAR", "XY_IDENTIFIER", "PARENT_GL_ACCOUNT_ID", "AMOUNT_EUR", "Date_interim_2", "Date_interim"}),
    #"Inserted Merged Column1" = Table.AddColumn(#"Reordered Columns1", "Merged", each Text.Combine({Text.From([Date_interim_2], "de-DE"), [Date_interim]}, "."), type text),
    #"Renamed Columns2" = Table.RenameColumns(#"Inserted Merged Column1",{{"Merged", "Date_interim_3"}}),
    #"Inserted Parsed Date" = Table.AddColumn(#"Renamed Columns2", "Parse", each Date.From(DateTimeZone.From([Date_interim_3])), type date),
    #"Inserted End of Month" = Table.AddColumn(#"Inserted Parsed Date", "End of Month", each Date.EndOfMonth([Parse]), type date),
    #"Renamed Columns3" = Table.RenameColumns(#"Inserted End of Month",{{"Parse", "Date_interim_4"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns3", each ([COMPANY] <> "Czech Republic" and [COMPANY] <> "Poland")),
    #"Inserted Month Name" = Table.AddColumn(#"Filtered Rows", "Month Name", each Date.MonthName([End of Month]), type text),
    #"Trimmed Text" = Table.TransformColumns(#"Inserted Month Name",{{"Month Name", Text.Trim, type text}}),
    #"Extracted First Characters" = Table.TransformColumns(#"Trimmed Text", {{"Month Name", each Text.Start(_, 3), type text}})
in
    #"Extracted First Characters"
```


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


## Table: RB_COMPANIES


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "byd_odp", [Query="SELECT [ACT_AS_ORG_UNIT]#(lf)      ,[ACCOUNT_ID]#(lf)      ,[ACCOUNT]#(lf)      ,[STREET]#(lf)      ,[HOUSE_NUMBER]#(lf)      ,[STREET_NR_FMT]#(lf)      ,[POSTAL_CODE]#(lf)      ,[CITY]#(lf)      ,[DISTRICT]#(lf)      ,[STATE]#(lf)      ,[ADDRESS_FMT]#(lf)      ,[COUNTRY_ISO2]#(lf)      ,[COUNTRY_ISO3]#(lf)      ,[COUNTRY]#(lf)      ,[REGION]#(lf)      ,[ZONE]#(lf)      ,[ORGANIZATIONAL_CCENTER_ID]#(lf)      ,[FUNCTIONAL_UNIT_ID]#(lf)      ,[FUNCTIONAL_UNIT]#(lf)      ,[COMPANY_NAME]#(lf)      ,[COMPANY_ID_MIS]#(lf)      ,[SAP_START]#(lf)      ,[COUNTRY_CURRENCY]#(lf)      ,[EXPORTED_ON]#(lf)  FROM [ByD_ODP].[dbo].[BYD_RB_COMPANIES]#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ACCOUNT_ID", Int64.Type}, {"FUNCTIONAL_UNIT_ID", Int64.Type}, {"ORGANIZATIONAL_CCENTER_ID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EXPORTED_ON", "ACT_AS_ORG_UNIT"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"COUNTRY_ISO3", "COUNTRY_ISO3"}}),
    #"ISO3 PlX" = Table.AddColumn(#"Renamed Columns", "Country_ISO3_PLX", each if [ORGANIZATIONAL_CCENTER_ID] = 46000000 then "PLX" else if [ORGANIZATIONAL_CCENTER_ID] = 47000000 then "PLX" else if [ORGANIZATIONAL_CCENTER_ID] = 48000000 then "PLX" else if [ORGANIZATIONAL_CCENTER_ID] = 49000000 then "PLX" else [COUNTRY_ISO3]),
    #"Inserted Merged Column" = Table.AddColumn(#"ISO3 PlX", "Merged", each Text.Combine({[Country_ISO3_PLX], Text.From([ORGANIZATIONAL_CCENTER_ID], "de-DE")}, "-"), type text),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Merged Column",{{"Merged", "Country_ISO3_PLX-ID"}, {"ORGANIZATIONAL_CCENTER_ID", "ID"}})
in
    #"Renamed Columns1"
```


## Table: WIP


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WORK_IN_PROGRESS = WorkingCapitalMgmt{[Schema="dbo",Item="WORK_IN_PROGRESS"]}[Data],
    #"Inserted Multiplication" = Table.AddColumn(dbo_WORK_IN_PROGRESS, "Multiplication", each [AGE_OF_WIP] * [OPEN_WIP], type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Multiplication", each ([PROJECT_FOR_CALCULATION] = "Yes")),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Multiplication", "WIP_Sorting"}}),
    #"Filtered Rows1" = Table.SelectRows(#"Renamed Columns", each ([EMPLOYEE_RESPONSIBLE] <> null)),
    #"Filtered Rows2" = Table.SelectRows(#"Filtered Rows1", each [AGE_OF_WIP] < 1000),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows2",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION_ID"}),
    #"Added Custom" = Table.AddColumn(#"Replaced Value1", "PROJECT_COMPLETION_IE(PBi_calculate)", each if [COST_ESTIMATE_IE] <> 0 then ([INCURRED_COSTS_IE] + 0.01)/ [COST_ESTIMATE_IE]

else if [BUDGET_IE] <> 0 then ([INCURRED_COSTS_IE] + 0.01)[COST_ESTIMATE_IE]
else 0),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"PROJECT_COMPLETION_IE(PBi_calculate)", type number}}),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type", "Open WIP Cluster", each if [OPEN_WIP] < 0 then "<0" else if [OPEN_WIP] < 30000 then "<30000" else if [OPEN_WIP] = 60000 then "<60000" else if [OPEN_WIP] = 100000 then "<100000" else if [OPEN_WIP] = 200000 then "<200000" else ">300000")
in
    #"Added Conditional Column"
```


## Table: AR


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES"]}[Data],
    #"Renamed Columns1" = Table.RenameColumns(dbo_RECEIVABLES,{{"TYPE", "TYPE-sql"}}),
    #"Inserted Multiplication" = Table.AddColumn(#"Renamed Columns1", "Multiplication", each [INVOICE_AGE] * [OPEN_AMOUNT], type number),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Multiplication",{{"Multiplication", "AR_Sorting"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each ([EMPLOYEE_RESPONSIBLE] <> null)),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [INVOICE_AGE] < 1000),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows1", "Unique_Project&Invoice_ID", each Text.Combine({[PROJECT_ID], [CUSTOMER_INVOICE_ID]}, "_"), type text),
    #"Added Custom" = Table.AddColumn(#"Inserted Merged Column", "Age_Cluster_CONTRACTED_PAYMENT_TERMS", each if [CONTRACTED_PAYMENT_TERMS]  <= 14 then "0-14"
else if [CONTRACTED_PAYMENT_TERMS] >=15 and [CONTRACTED_PAYMENT_TERMS] <= 30 then "15-30"
else if [CONTRACTED_PAYMENT_TERMS] >=31 and [CONTRACTED_PAYMENT_TERMS] <= 60 then "31-60"
else if [CONTRACTED_PAYMENT_TERMS] >=61 and [CONTRACTED_PAYMENT_TERMS] <= 90 then "61-90"
else if [CONTRACTED_PAYMENT_TERMS] >=91 and [CONTRACTED_PAYMENT_TERMS] <= 180 then "91-180"
else if [CONTRACTED_PAYMENT_TERMS] >=181 and [CONTRACTED_PAYMENT_TERMS] <270 then "181-270"
else if [CONTRACTED_PAYMENT_TERMS] >=271 and [CONTRACTED_PAYMENT_TERMS] <=360 then "271-360"
else "361+"),
    #"Inserted Merged Column1" = Table.AddColumn(#"Added Custom", "Unique_3", each Text.Combine({[#"Unique_Project&Invoice_ID"], [CUSTOMER]}, "_"), type text),
    #"Replaced Value" = Table.ReplaceValue(#"Inserted Merged Column1",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION_ID"}),
    #"Added Conditional Column" = Table.AddColumn(#"Replaced Value1", "Open Amout Cluster", each if [OPEN_AMOUNT] < 0 then "<0" else if [OPEN_AMOUNT] < 30000 then "<30000" else if [OPEN_AMOUNT] < 60000 then "<60000" else if [OPEN_AMOUNT] < 100000 then "<100000" else if [OPEN_AMOUNT] < 200000 then "<200000" else if [OPEN_AMOUNT] < 300000 then "<300000" else ">300000")
in
    #"Added Conditional Column"
```


## Table: CARDINAL_ACC


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_DSO_REPORTING_ARCHIVE = WorkingCapitalMgmt{[Schema="dbo",Item="DSO_REPORTING_ARCHIVE"]}[Data],
    #"Calculated End of Month" = Table.TransformColumns(dbo_DSO_REPORTING_ARCHIVE,{{"YEAR_MONTH", Date.EndOfMonth, type date}})
in
    #"Calculated End of Month"
```


## Table: Targets


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RB_COMPANY_WC_TARGETS = WorkingCapitalMgmt{[Schema="dbo",Item="RB_COMPANY_WC_TARGETS"]}[Data]
in
    dbo_RB_COMPANY_WC_TARGETS
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


## Table: Customer List


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Inserted Merged Column" = Table.AddColumn(Source, "Company_ID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [PROJECT_COMPANY_ID]}, ""), type text),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Merged Column", {"CUSTOMER_ID"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Duplicates",{"AGE_CLUSTER", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "LOCAL_CURRENCY", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "SOURCE", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "EMPLOYEE_RESPONSIBLE_STATUS", "WIP_Sorting", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "AR_Sorting", "EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "PROJECT_ID", "PROJECT", "PROJECT_STATUS", "COMPANY_ID", "COMPANY"})
in
    #"Removed Columns"
```


## Table: P List


```m
let
    Source = Table.Combine({AR, WIP}),
    #"Removed Duplicates" = Table.Distinct(Source, {"EMPLOYEE_RESPONSIBLE_ID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"EMPLOYEE_RESPONSIBLE", "P/PRI"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "AR_Sorting", "PROJECT_STATUS", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "WIP_Sorting"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Removed Columns", "Company_ID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [COMPANY_ID]}, ""), type text),
    #"Removed Columns1" = Table.RemoveColumns(#"Inserted Merged Column",{"RECEIVABLE_COMPANY_ID", "COMPANY_ID"}),
    #"Inserted Merged Column1" = Table.AddColumn(#"Removed Columns1", "Company.1", each Text.Combine({[RECEIVABLE_COMPANY], [COMPANY]}, ""), type text),
    #"Removed Columns2" = Table.RemoveColumns(#"Inserted Merged Column1",{"RECEIVABLE_COMPANY", "COMPANY"})
in
    #"Removed Columns2"
```


## Table: Regions


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "byd_odp", [Query="SELECT [ACT_AS_ORG_UNIT]#(lf)      ,[ACCOUNT_ID]#(lf)      ,[ACCOUNT]#(lf)      ,[STREET]#(lf)      ,[HOUSE_NUMBER]#(lf)      ,[STREET_NR_FMT]#(lf)      ,[POSTAL_CODE]#(lf)      ,[CITY]#(lf)      ,[DISTRICT]#(lf)      ,[STATE]#(lf)      ,[ADDRESS_FMT]#(lf)      ,[COUNTRY_ISO2]#(lf)      ,[COUNTRY_ISO3]#(lf)      ,[COUNTRY]#(lf)      ,[REGION]#(lf)      ,[ZONE]#(lf)      ,[ORGANIZATIONAL_CCENTER_ID]#(lf)      ,[FUNCTIONAL_UNIT_ID]#(lf)      ,[FUNCTIONAL_UNIT]#(lf)      ,[COMPANY_NAME]#(lf)      ,[COMPANY_ID_MIS]#(lf)      ,[SAP_START]#(lf)      ,[COUNTRY_CURRENCY]#(lf)      ,[EXPORTED_ON]#(lf)  FROM [ByD_ODP].[dbo].[BYD_RB_COMPANIES]#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ACCOUNT_ID", Int64.Type}, {"FUNCTIONAL_UNIT_ID", Int64.Type}, {"ORGANIZATIONAL_CCENTER_ID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EXPORTED_ON", "ACT_AS_ORG_UNIT"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows",{"ACCOUNT_ID", "ACCOUNT", "STREET", "HOUSE_NUMBER", "STREET_NR_FMT", "POSTAL_CODE", "CITY", "DISTRICT", "STATE", "ADDRESS_FMT", "COUNTRY_ISO2", "COUNTRY_ISO3", "COUNTRY", "ZONE", "ORGANIZATIONAL_CCENTER_ID", "FUNCTIONAL_UNIT_ID", "FUNCTIONAL_UNIT", "COMPANY_NAME", "COMPANY_ID_MIS", "SAP_START", "COUNTRY_CURRENCY"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns1"),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Duplicates", each ([REGION] <> "No Region"))
in
    #"Filtered Rows1"
```


## Table: Zones


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "byd_odp", [Query="SELECT [ACT_AS_ORG_UNIT]#(lf)      ,[ACCOUNT_ID]#(lf)      ,[ACCOUNT]#(lf)      ,[STREET]#(lf)      ,[HOUSE_NUMBER]#(lf)      ,[STREET_NR_FMT]#(lf)      ,[POSTAL_CODE]#(lf)      ,[CITY]#(lf)      ,[DISTRICT]#(lf)      ,[STATE]#(lf)      ,[ADDRESS_FMT]#(lf)      ,[COUNTRY_ISO2]#(lf)      ,[COUNTRY_ISO3]#(lf)      ,[COUNTRY]#(lf)      ,[REGION]#(lf)      ,[ZONE]#(lf)      ,[ORGANIZATIONAL_CCENTER_ID]#(lf)      ,[FUNCTIONAL_UNIT_ID]#(lf)      ,[FUNCTIONAL_UNIT]#(lf)      ,[COMPANY_NAME]#(lf)      ,[COMPANY_ID_MIS]#(lf)      ,[SAP_START]#(lf)      ,[COUNTRY_CURRENCY]#(lf)      ,[EXPORTED_ON]#(lf)  FROM [ByD_ODP].[dbo].[BYD_RB_COMPANIES]#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ACCOUNT_ID", Int64.Type}, {"FUNCTIONAL_UNIT_ID", Int64.Type}, {"ORGANIZATIONAL_CCENTER_ID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EXPORTED_ON", "ACT_AS_ORG_UNIT"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows",{"ACCOUNT_ID", "ACCOUNT", "STREET", "HOUSE_NUMBER", "STREET_NR_FMT", "POSTAL_CODE", "CITY", "DISTRICT", "STATE", "ADDRESS_FMT", "COUNTRY_ISO2", "COUNTRY_ISO3", "COUNTRY", "REGION", "ORGANIZATIONAL_CCENTER_ID", "FUNCTIONAL_UNIT_ID", "FUNCTIONAL_UNIT", "COMPANY_NAME", "COMPANY_ID_MIS", "SAP_START", "COUNTRY_CURRENCY"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns1"),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Duplicates", each ([ZONE] <> null and [ZONE] <> "CZE" and [ZONE] <> "No Zone" and [ZONE] <> "POL" and [ZONE] <> "TUR"))
in
    #"Filtered Rows1"
```


## Table: Countries


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "byd_odp", [Query="SELECT [ACT_AS_ORG_UNIT]#(lf)      ,[ACCOUNT_ID]#(lf)      ,[ACCOUNT]#(lf)      ,[STREET]#(lf)      ,[HOUSE_NUMBER]#(lf)      ,[STREET_NR_FMT]#(lf)      ,[POSTAL_CODE]#(lf)      ,[CITY]#(lf)      ,[DISTRICT]#(lf)      ,[STATE]#(lf)      ,[ADDRESS_FMT]#(lf)      ,[COUNTRY_ISO2]#(lf)      ,[COUNTRY_ISO3]#(lf)      ,[COUNTRY]#(lf)      ,[REGION]#(lf)      ,[ZONE]#(lf)      ,[ORGANIZATIONAL_CCENTER_ID]#(lf)      ,[FUNCTIONAL_UNIT_ID]#(lf)      ,[FUNCTIONAL_UNIT]#(lf)      ,[COMPANY_NAME]#(lf)      ,[COMPANY_ID_MIS]#(lf)      ,[SAP_START]#(lf)      ,[COUNTRY_CURRENCY]#(lf)      ,[EXPORTED_ON]#(lf)  FROM [ByD_ODP].[dbo].[BYD_RB_COMPANIES]#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ACCOUNT_ID", Int64.Type}, {"FUNCTIONAL_UNIT_ID", Int64.Type}, {"ORGANIZATIONAL_CCENTER_ID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EXPORTED_ON", "ACT_AS_ORG_UNIT"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each true),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows",{"ACCOUNT_ID", "ACCOUNT", "STREET", "HOUSE_NUMBER", "STREET_NR_FMT", "POSTAL_CODE", "CITY", "DISTRICT", "STATE", "ADDRESS_FMT", "REGION", "ZONE", "FUNCTIONAL_UNIT_ID", "FUNCTIONAL_UNIT", "COMPANY_ID_MIS", "SAP_START", "COUNTRY_CURRENCY"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns1", {"COUNTRY"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Duplicates", each ([COUNTRY] <> "Croatia" and [COUNTRY] <> "Czech Republic" and [COUNTRY] <> "Nigeria" and [COUNTRY] <> "Poland" and [COUNTRY] <> "Turkey")),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows1",{{"COUNTRY_ISO3", "Entity"}})
in
    #"Renamed Columns"
```


## Table: AR (2)


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES"]}[Data],
    #"Inserted Multiplication" = Table.AddColumn(dbo_RECEIVABLES, "Multiplication", each [INVOICE_AGE] * [OPEN_AMOUNT], type number),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Multiplication",{{"Multiplication", "AR_Sorting"}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Renamed Columns", "CompanyID_Partner", each Text.Combine({[RECEIVABLE_COMPANY_ID], [EMPLOYEE_RESPONSIBLE_ID]}, "_"), type text),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Merged Column", each ([EMPLOYEE_RESPONSIBLE] <> null)),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [INVOICE_AGE] < 1000)
in
    #"Filtered Rows1"
```


## Table: WIP (2)


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WORK_IN_PROGRESS = WorkingCapitalMgmt{[Schema="dbo",Item="WORK_IN_PROGRESS"]}[Data],
    #"Inserted Multiplication" = Table.AddColumn(dbo_WORK_IN_PROGRESS, "Multiplication", each [AGE_OF_WIP] * [OPEN_WIP], type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Multiplication", each ([PROJECT_FOR_CALCULATION] = "Yes")),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Multiplication", "WIP_Sorting"}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Renamed Columns", "CompanyID_Partner", each Text.Combine({[PROJECT_COMPANY_ID], [EMPLOYEE_RESPONSIBLE_ID]}, "_"), type text),
    #"Filtered Rows1" = Table.SelectRows(#"Inserted Merged Column", each ([EMPLOYEE_RESPONSIBLE] <> null)),
    #"Filtered Rows2" = Table.SelectRows(#"Filtered Rows1", each [AGE_OF_WIP] < 1000)
in
    #"Filtered Rows2"
```


## Table: AR (3)


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES"]}[Data],
    #"Inserted Multiplication" = Table.AddColumn(dbo_RECEIVABLES, "Multiplication", each [INVOICE_AGE] * [OPEN_AMOUNT], type number),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Multiplication",{{"Multiplication", "AR_Sorting"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each ([EMPLOYEE_RESPONSIBLE] <> null)),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [INVOICE_AGE] < 1000)
in
    #"Filtered Rows1"
```


## Table: WIP (3)


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WORK_IN_PROGRESS = WorkingCapitalMgmt{[Schema="dbo",Item="WORK_IN_PROGRESS"]}[Data],
    #"Inserted Multiplication" = Table.AddColumn(dbo_WORK_IN_PROGRESS, "Multiplication", each [AGE_OF_WIP] * [OPEN_WIP], type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Multiplication", each ([PROJECT_FOR_CALCULATION] = "Yes")),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Multiplication", "WIP_Sorting"}}),
    #"Filtered Rows1" = Table.SelectRows(#"Renamed Columns", each ([EMPLOYEE_RESPONSIBLE] <> null)),
    #"Filtered Rows2" = Table.SelectRows(#"Filtered Rows1", each [AGE_OF_WIP] < 1000)
in
    #"Filtered Rows2"
```


## Table: P List (2)


```m
let
    Source = Table.Combine({AR, WIP}),
    #"Removed Duplicates" = Table.Distinct(Source, {"EMPLOYEE_RESPONSIBLE_ID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"EMPLOYEE_RESPONSIBLE", "P/PRI"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "AR_Sorting", "PROJECT_STATUS", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "WIP_Sorting"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Removed Columns", "Company_ID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [COMPANY_ID]}, ""), type text),
    #"Removed Columns1" = Table.RemoveColumns(#"Inserted Merged Column",{"RECEIVABLE_COMPANY_ID", "COMPANY_ID"}),
    #"Inserted Merged Column1" = Table.AddColumn(#"Removed Columns1", "Company.1", each Text.Combine({[RECEIVABLE_COMPANY], [COMPANY]}, ""), type text),
    #"Removed Columns2" = Table.RemoveColumns(#"Inserted Merged Column1",{"RECEIVABLE_COMPANY", "COMPANY"})
in
    #"Removed Columns2"
```


## Table: Customer List (2)


```m
let
    Source = Table.Combine({WIP, AR}),
    #"Inserted Merged Column" = Table.AddColumn(Source, "Company_ID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [PROJECT_COMPANY_ID]}, ""), type text),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Merged Column", {"CUSTOMER_ID"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Duplicates",{"AGE_CLUSTER", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "LOCAL_CURRENCY", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "SOURCE", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "EMPLOYEE_RESPONSIBLE_STATUS", "WIP_Sorting", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "AR_Sorting", "EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "PROJECT_ID", "PROJECT", "PROJECT_STATUS", "COMPANY_ID", "COMPANY"})
in
    #"Removed Columns"
```


## Table: Aging (2)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: Aging (3)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: P List (3)


```m
let
    Source = Table.Combine({AR, WIP}),
    #"Inserted Merged Column" = Table.AddColumn(Source, "Company_ID2", each Text.Combine({[RECEIVABLE_COMPANY_ID], [PROJECT_COMPANY_ID]}, ""), type text),
    #"Inserted Merged Column2" = Table.AddColumn(#"Inserted Merged Column", "Merged", each Text.Combine({[Company_ID2], [EMPLOYEE_RESPONSIBLE_ID]}, "_"), type text),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Merged Column2",{{"Merged", "CompanyID_Partner"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns", {"CompanyID_Partner"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Duplicates",{"CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "AR_Sorting", "PROJECT_STATUS", "COMPANY_ID", "COMPANY", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "WIP_Sorting"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"EMPLOYEE_RESPONSIBLE", "P/PRI"}})
in
    #"Renamed Columns1"
```


## Table: User_Roles


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WCM_SECURITY_ADJUSTMENTS = WorkingCapitalMgmt{[Schema="dbo",Item="WCM_SECURITY_ADJUSTMENTS"]}[Data]
in
    dbo_WCM_SECURITY_ADJUSTMENTS
```


## Table: User


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WCM_SECURITY_ADJUSTMENTS = WorkingCapitalMgmt{[Schema="dbo",Item="WCM_SECURITY_ADJUSTMENTS"]}[Data],
    #"Removed Duplicates" = Table.Distinct(dbo_WCM_SECURITY_ADJUSTMENTS, {"EMPLOYEE_ID"})
in
    #"Removed Duplicates"
```


## Table: ZZ_DateLastRefresh


```m
let
    Source = "let#(cr)#(lf)#(cr)#(lf)Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}})#(cr)#(lf)#(cr)#(lf)in#(cr)#(lf)#(cr)#(lf)Source",
    #"Converted to Table" = let

Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}})

in

Source
in
    #"Converted to Table"
```


## Table: V_BYD_PROJECT_INVOICES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_V_BYD_PROJECT_INVOICES = WorkingCapitalMgmt{[Schema="dbo",Item="V_BYD_PROJECT_INVOICES"]}[Data],
    #"Added Custom" = Table.AddColumn(dbo_V_BYD_PROJECT_INVOICES, "TermDays", each [NET_DUE_DATE]-[INVOICE_DATE]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"TermDays", Int64.Type}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type", "TotalCollectionDays", each [CLEARING_DATE_1]-[INVOICE_DATE]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom1",{{"TotalCollectionDays", Int64.Type}}),
    #"Added Custom2" = Table.AddColumn(#"Changed Type1", "OverdueDays", each [CLEARING_DATE_1]-[NET_DUE_DATE]),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom2",{{"OverdueDays", Int64.Type}}),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type2", "TerrmDays_P", each if [TermDays] >= 0 then [TermDays] else 0),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "TotalCollectionDays_P", each if [TotalCollectionDays] >= 0 then [TotalCollectionDays] else 0),
    #"Added Conditional Column2" = Table.AddColumn(#"Added Conditional Column1", "OverdueDays_P", each if [OverdueDays] >= 0 then [OverdueDays] else 0),
    #"Added Custom3" = Table.AddColumn(#"Added Conditional Column2", "TermDays_Clusters", each if [TerrmDays_P] <= 14 then "0-14"
else if [TerrmDays_P] <= 30 and [TerrmDays_P] > 14 then "15-30"
else if [TerrmDays_P] <= 60 and [TerrmDays_P] > 30 then "31-60"
else if [TerrmDays_P] <= 90 and [TerrmDays_P] > 60 then "61-90"
else if [TerrmDays_P] <= 180 and [TerrmDays_P] > 90 then "91-180"
else if [TerrmDays_P] <= 270 and [TerrmDays_P] > 180 then "181-270"
else if [TerrmDays_P] <= 360 and [TerrmDays_P] > 270 then "271-360"
else "360+"),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "OverdueDays_Cluster", each if [OverdueDays_P]<= 14 then "0-14"
else if [OverdueDays_P]<= 30 and [OverdueDays_P]> 14 then "15-30"
else if [OverdueDays_P]<= 60 and [OverdueDays_P]> 30 then "31-60"
else if [OverdueDays_P]<= 90 and [OverdueDays_P]> 60 then "61-90"
else if [OverdueDays_P]<= 180 and [OverdueDays_P]> 90 then "91-180"
else if [OverdueDays_P]<= 270 and [OverdueDays_P]> 180 then "181-270"
else if [OverdueDays_P]<= 360 and [OverdueDays_P]> 270 then "271-360"
else "360+"),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "TotalCollectionDays_Cluster", each if [TotalCollectionDays_P]<= 14 then "0-14"
else if [TotalCollectionDays_P]<= 30 and [TotalCollectionDays_P]> 14 then "15-30"
else if [TotalCollectionDays_P]<= 60 and [TotalCollectionDays_P]> 30 then "31-60"
else if [TotalCollectionDays_P]<= 90 and [TotalCollectionDays_P]> 60 then "61-90"
else if [TotalCollectionDays_P]<= 180 and [TotalCollectionDays_P]> 90 then "91-180"
else if [TotalCollectionDays_P]<= 270 and [TotalCollectionDays_P]> 180 then "181-270"
else if [TotalCollectionDays_P]<= 360 and [TotalCollectionDays_P]> 270 then "271-360"
else "360+"),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom5", each ([PROJECT_ID] <> ""))
in
    #"Filtered Rows"
```


## Table: DSO Aging Cluster_TermDays


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: DSO Aging Cluster_OverdueDays


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: DSO Aging Cluster_TotalCollectionDays


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: SAP_Industry


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_SAP_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="SAP_RECEIVABLES"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(dbo_SAP_RECEIVABLES,{"EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "SALES_UNIT_ID", "SALES_UNIT", "FUNCTION_ID", "FUNCTION", "EMP_PLATFORM_ID", "EMP_PLATFORM"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"INDUSTRY"}),
    #"Sorted Rows" = Table.Sort(#"Removed Duplicates",{{"INDUSTRY", Order.Ascending}, {"INDUSTRY_ID", Order.Ascending}}),
    #"Filtered Rows" = Table.SelectRows(#"Sorted Rows", each ([INDUSTRY_ID] <> null))
in
    #"Filtered Rows"
```


## Table: SAP_EMP_Plateform


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_SAP_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="SAP_RECEIVABLES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_SAP_RECEIVABLES, each [EMP_PLATFORM_ID] <> null and [EMP_PLATFORM_ID] <> ""),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "SALES_UNIT_ID", "SALES_UNIT", "FUNCTION_ID", "FUNCTION", "INDUSTRY_ID", "INDUSTRY"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"EMP_PLATFORM"}),
    #"Sorted Rows" = Table.Sort(#"Removed Duplicates",{{"EMP_PLATFORM_ID", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: SAP_Function


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_SAP_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="SAP_RECEIVABLES"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(dbo_SAP_RECEIVABLES,{"EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "SALES_UNIT_ID", "SALES_UNIT", "INDUSTRY_ID", "INDUSTRY", "EMP_PLATFORM_ID", "EMP_PLATFORM"}),
    #"Appended Query" = Table.Combine({#"Removed Columns", WIP}),
    #"Removed Other Columns" = Table.SelectColumns(#"Appended Query",{"FUNCTION", "FUNCTION_ID"}),
    #"Sorted Rows" = Table.Sort(#"Removed Other Columns",{{"FUNCTION_ID", Order.Ascending}}),
    #"Replaced Value" = Table.ReplaceValue(#"Sorted Rows",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION_ID"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,"""not assigned""",Replacer.ReplaceValue,{"FUNCTION"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value1", each ([FUNCTION_ID] <> null)),
    #"Removed Duplicates1" = Table.Distinct(#"Filtered Rows", {"FUNCTION_ID"})
in
    #"Removed Duplicates1"
```


## Table: SAP_Sales_Unit


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_SAP_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="SAP_RECEIVABLES"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(dbo_SAP_RECEIVABLES,{"EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "CUSTOMER_ID", "CUSTOMER", "PROJECT_ID", "PROJECT", "CUSTOMER_INVOICE_ID", "INVOICE_DATE", "NET_DUE_DATE", "NET_DUE_DATE_ADJUSTED", "INVOICE_AGE", "DAYS_OVERDUE", "AGE_CLUSTER", "OPEN_AMOUNT", "FEE_TOTAL_NET_VALUE", "INC_EXP_TOTAL_NET_VALUE", "NET_VALUE", "TAX", "TOTAL", "LOCAL_CURRENCY", "OPEN_AMOUNT_LC", "FEE_TOTAL_NET_VALUE_LC", "INC_EXP_TOTAL_NET_VALUE_LC", "NET_VALUE_LC", "TAX_LC", "TOTAL_LC", "TRANSACTION_CURRENCY", "SOURCE", "DUNNING_LEVEL", "DUNNING_CREATED_ON", "DUNNING_CURRENCY", "DUNNING_BLOCK", "DUNNING_BLOCK_NOTE", "DUNNING_BLOCK_EXPIRATION_DATE", "DUNNING_BLOCK_REASON_ID", "DUNNING_BLOCK_REASON", "HIGHEST_DUNNING_LEVEL", "DUNNING_DATE", "EMPLOYEE_RESPONSIBLE_COUNTRY", "EMPLOYEE_RESPONSIBLE_STATUS", "NEXT_DUNNING_INTERVAL", "APROXIMATE_DUNNING_DATE", "CONTRACTED_PAYMENT_TERMS", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", "EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", "RECEIVABLE_COMPANY_ID", "RECEIVABLE_COMPANY", "CUSTOMER_COUNTRY_ISO2", "CUSTOMER_COUNTRY_ISO3", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "FUNCTION_ID", "FUNCTION", "INDUSTRY_ID", "INDUSTRY", "EMP_PLATFORM_ID", "EMP_PLATFORM"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"SALES_UNIT"})
in
    #"Removed Duplicates"
```


## Table: Last Refresh_CARDINAL_ACC


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_DSO_REPORTING_ARCHIVE = WorkingCapitalMgmt{[Schema="dbo",Item="DSO_REPORTING_ARCHIVE"]}[Data],
    #"Calculated End of Month" = Table.TransformColumns(dbo_DSO_REPORTING_ARCHIVE,{{"YEAR_MONTH", Date.EndOfMonth, type date}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Calculated End of Month",{"ARCHIVED_AT"}),
    #"Sorted Rows" = Table.Sort(#"Removed Other Columns",{{"ARCHIVED_AT", Order.Descending}}),
    #"Removed Duplicates" = Table.Distinct(#"Sorted Rows"),
    #"Kept First Rows" = Table.FirstN(#"Removed Duplicates",1)
in
    #"Kept First Rows"
```


## Table: GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    AccountingReportingPackage = Source{[Name="AccountingReportingPackage"]}[Data],
    dbo_GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC = AccountingReportingPackage{[Schema="dbo",Item="GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC"]}[Data],
    #"Added Conditional Column" = Table.AddColumn(dbo_GL_ACCOUNT_BALANCE_MAPPED_TBL_SEC, "System_Company_ID", each if [SYSTEM] = "DCW" then [MIS_COMPANY_ID] else [BYD_COMPANY_ID]),
    #"Added Custom" = Table.AddColumn(#"Added Conditional Column", "Custom", each [System_Company_ID]&"_"&[GL_ACCOUNT_ID])
in
    #"Added Custom"
```


## Table: GL_ACCOUNT_BALANCE_MAPPED_DCW


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    AccountingReportingPackage = Source{[Name="AccountingReportingPackage"]}[Data],
    dbo_GL_ACCOUNT_BALANCE_MAPPED_DCW = AccountingReportingPackage{[Schema="dbo",Item="GL_ACCOUNT_BALANCE_MAPPED_DCW"]}[Data]
in
    dbo_GL_ACCOUNT_BALANCE_MAPPED_DCW
```


## Table: WORK_IN_PROGRESS_ADJUSTED


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WORK_IN_PROGRESS_ADJUSTED = WorkingCapitalMgmt{[Schema="dbo",Item="WORK_IN_PROGRESS_ADJUSTED"]}[Data],
    #"Merged Queries" = Table.NestedJoin(dbo_WORK_IN_PROGRESS_ADJUSTED, {"ReportIndexNumber"}, Max_ReceivablesAdj_ReportIndex_ID, {"ReportIndexNumber"}, "Max_ReceivablesAdj_ReportIndex_ID", JoinKind.LeftOuter),
    #"Expanded Max_ReceivablesAdj_ReportIndex_ID" = Table.ExpandTableColumn(#"Merged Queries", "Max_ReceivablesAdj_ReportIndex_ID", {"ReportIndexNumber"}, {"Max_ReceivablesAdj_ReportIndex_ID.ReportIndexNumber"}),
    #"Added Conditional Column" = Table.AddColumn(#"Expanded Max_ReceivablesAdj_ReportIndex_ID", "Max_ReportIndex_ID", each if [ReportIndexNumber] = [Max_ReceivablesAdj_ReportIndex_ID.ReportIndexNumber] then 1 else 0),
    #"Filtered Rows" = Table.SelectRows(#"Added Conditional Column", each ([Max_ReportIndex_ID] = 1))
in
    #"Filtered Rows"
```


## Table: RECEIVABLES_ADJUSTED


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES_ADJUSTED = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES_ADJUSTED"]}[Data],
    #"Sorted Rows" = Table.Sort(dbo_RECEIVABLES_ADJUSTED,{{"ReportIndexNumber", Order.Descending}}),
    #"Merged Queries" = Table.NestedJoin(#"Sorted Rows", {"ReportIndexNumber"}, Max_ReceivablesAdj_ReportIndex_ID, {"ReportIndexNumber"}, "Max_ReceivablesAdj_ReportIndex_ID", JoinKind.LeftOuter),
    #"Expanded Max_ReceivablesAdj_ReportIndex_ID" = Table.ExpandTableColumn(#"Merged Queries", "Max_ReceivablesAdj_ReportIndex_ID", {"ReportIndexNumber"}, {"Max_ReceivablesAdj_ReportIndex_ID.ReportIndexNumber"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Max_ReceivablesAdj_ReportIndex_ID", each true),
    #"Added Conditional Column" = Table.AddColumn(#"Filtered Rows", "Custom", each if [ReportIndexNumber] = [Max_ReceivablesAdj_ReportIndex_ID.ReportIndexNumber] then 1 else 0),
    #"Filtered Rows1" = Table.SelectRows(#"Added Conditional Column", each ([Custom] = 1)),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows1", "Unique_Project&Invoice_ID", each Text.Combine({[PROJECT_ID], [CUSTOMER_INVOICE_ID]}, "_"), type text),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Merged Column",{{"Custom", "Max_ReportIndex_ID"}})
in
    #"Renamed Columns"
```


## Table: Max_ReceivablesAdj_ReportIndex_ID


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES_ADJUSTED = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES_ADJUSTED"]}[Data],
    #"Sorted Rows" = Table.Sort(dbo_RECEIVABLES_ADJUSTED,{{"ReportIndexNumber", Order.Descending}}),
    #"Kept First Rows" = Table.FirstN(#"Sorted Rows",1),
    #"Removed Other Columns" = Table.SelectColumns(#"Kept First Rows",{"ReportIndexNumber"})
in
    #"Removed Other Columns"
```


## Table: Agging(Term_days)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value"
```


## Table: RB_CHART_OF_BANK_ACCOUNTS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RB_CHART_OF_BANK_ACCOUNTS = WorkingCapitalMgmt{[Schema="dbo",Item="RB_CHART_OF_BANK_ACCOUNTS"]}[Data],
    #"Added Custom" = Table.AddColumn(dbo_RB_CHART_OF_BANK_ACCOUNTS, "System_GL_Account", each [COMPANY_ID]&"_"&[ACCOUNT_ID])
in
    #"Added Custom"
```


## Table: RB_CORIMA_VALUE DATES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_COPS_LIP_CARDINAL_IMPORT = Corima{[Schema="dbo",Item="V_COPS_LIP_CARDINAL_IMPORT"]}[Data],
    #"Filtered Rows1" = Table.SelectRows(dbo_V_COPS_LIP_CARDINAL_IMPORT, each ([PLAN_VARIANT_SHORT_NAME] <> null) and ([AMOUNT_EUR] <> null)),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows1", "Planvariant_Note", each Text.Combine({[NOTE], [PLAN_VARIANT_SHORT_NAME]}, "_"), type text),
    #"Merged Queries1" = Table.NestedJoin(#"Inserted Merged Column", {"Planvariant_Note"}, FC_CARDINAL_ADJ, {"Planvariant_Note"}, "FC_CARDINAL_ADJ", JoinKind.LeftOuter),
    #"Expanded FC_CARDINAL_ADJ1" = Table.ExpandTableColumn(#"Merged Queries1", "FC_CARDINAL_ADJ", {"CLIENT_SHORT_NAME"}, {"CLIENT_SHORT_NAME"}),
    #"Inserted Division" = Table.AddColumn(#"Expanded FC_CARDINAL_ADJ1", "Division", each [AMOUNT_EUR] / 1000, type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Division", each ([PLAN_VARIANT_SHORT_NAME] <> null)),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Division", "Amount_EURk"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns", each [UNIQUE_IDENTIFIER] <> "DH Diagnostics, LLC // CP10077: Multiple Myeloma Dx Market Study / SE-150-202110512.0000"),
    #"Inserted Merged Column1" = Table.AddColumn(#"Filtered Rows2", "Unique_Project&Invoice_ID", each Text.Combine({[PROJECT_ID], [CUSTOMER_INVOICE_ID]}, "_"), type text),
    #"Duplicated Column" = Table.DuplicateColumn(#"Inserted Merged Column1", "PLAN_VARIANT_SHORT_NAME", "PLAN_VARIANT_SHORT_NAME - Copy"),
    #"Extracted Last Characters" = Table.TransformColumns(#"Duplicated Column", {{"PLAN_VARIANT_SHORT_NAME - Copy", each Text.End(_, 4), type text}}),
    #"Duplicated Column1" = Table.DuplicateColumn(#"Extracted Last Characters", "PLAN_VARIANT_SHORT_NAME", "PLAN_VARIANT_SHORT_NAME - Copy.1"),
    #"Extracted Text Before Delimiter" = Table.TransformColumns(#"Duplicated Column1", {{"PLAN_VARIANT_SHORT_NAME - Copy.1", each Text.BeforeDelimiter(_, "/"), type text}}),
    #"Split Column by Position" = Table.SplitColumn(#"Extracted Text Before Delimiter", "PLAN_VARIANT_SHORT_NAME - Copy.1", Splitter.SplitTextByPositions({0, 2}, true), {"PLAN_VARIANT_SHORT_NAME - Copy.1.1", "PLAN_VARIANT_SHORT_NAME - Copy.1.2"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Position",{{"PLAN_VARIANT_SHORT_NAME - Copy.1.1", type text}, {"PLAN_VARIANT_SHORT_NAME - Copy.1.2", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type","W","0",Replacer.ReplaceText,{"PLAN_VARIANT_SHORT_NAME - Copy.1.2"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value"," 9","09",Replacer.ReplaceValue,{"PLAN_VARIANT_SHORT_NAME - Copy.1.2"}),
    #"Filtered Rows3" = Table.SelectRows(#"Replaced Value1", each ([#"PLAN_VARIANT_SHORT_NAME - Copy"] <> "20v2" and [#"PLAN_VARIANT_SHORT_NAME - Copy"] <> "21v2")),
    #"Inserted Merged Column2" = Table.AddColumn(#"Filtered Rows3", "Merged_CW", each Text.Combine({[#"PLAN_VARIANT_SHORT_NAME - Copy"], [#"PLAN_VARIANT_SHORT_NAME - Copy.1.2"]}, ""), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Merged Column2",{{"Merged_CW", Int64.Type}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type1",{{"Merged_CW", Order.Descending}}),
    #"Inserted Merged Column3" = Table.AddColumn(#"Sorted Rows", "Merged_3", each Text.Combine({[#"Unique_Project&Invoice_ID"], [CUSTOMER]}, "_"), type text),
    #"Merged Queries" = Table.NestedJoin(#"Inserted Merged Column3", {"Merged_CW"}, #"Current  FC CW", {"Merged_CW - Copy"}, "Current  FC CW", JoinKind.LeftOuter),
    #"Expanded Current  FC CW" = Table.ExpandTableColumn(#"Merged Queries", "Current  FC CW", {"Merged_CW - Copy"}, {"Current  FC CW.Merged_CW - Copy"}),
    #"Added Conditional Column" = Table.AddColumn(#"Expanded Current  FC CW", "Current_FC_CW_ID", each if [Merged_CW] = [#"Current  FC CW.Merged_CW - Copy"] then 1 else 0),
    #"Filtered Rows4" = Table.SelectRows(#"Added Conditional Column", each ([Current_FC_CW_ID] = 1)),
    #"Added Conditional Column1" = Table.AddColumn(#"Filtered Rows4", "VALUE_DATE_NoDEU", each if [CLIENT_SHORT_NAME] <> "1000000" then [VALUE_DATE] else null),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Conditional Column1",{{"VALUE_DATE_NoDEU", type date}})
in
    #"Changed Type2"
```


## Table: FC_CARDINAL_ADJ


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_COPS_LIP_IMPORT_DATE_ADJ = Corima{[Schema="dbo",Item="COPS_LIP_IMPORT_DATE_ADJ"]}[Data],
    #"Inserted Merged Column" = Table.AddColumn(dbo_COPS_LIP_IMPORT_DATE_ADJ, "Planvariant_Note", each Text.Combine({[NOTE], [PLAN_VARIANT_SHORT_NAME]}, "_"), type text)
in
    #"Inserted Merged Column"
```


## Table: FC_DATA


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_DATA_SUM = Corima{[Schema="dbo",Item="V_DW_LIP_DATA_SUM"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_DATA_SUM, each [PLAN_VARIANT_ID] > 87),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows", {"PLAN_VARIANT_SHORT_NAME"}),
    #"Removed Other Columns" = Table.SelectColumns(#"Removed Duplicates",{"PLAN_VARIANT_ID", "PLAN_VARIANT_SHORT_NAME", "CLIENT_RATE_DATE"})
in
    #"Removed Other Columns"
```


## Table: Current  FC CW


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_COPS_LIP_CARDINAL_IMPORT = Corima{[Schema="dbo",Item="V_COPS_LIP_CARDINAL_IMPORT"]}[Data],
    #"Filtered Rows1" = Table.SelectRows(dbo_V_COPS_LIP_CARDINAL_IMPORT, each ([PLAN_VARIANT_SHORT_NAME] <> null) and ([AMOUNT_EUR] <> null)),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows1", "Planvariant_Note", each Text.Combine({[NOTE], [PLAN_VARIANT_SHORT_NAME]}, "_"), type text),
    #"Merged Queries1" = Table.NestedJoin(#"Inserted Merged Column", {"Planvariant_Note"}, FC_CARDINAL_ADJ, {"Planvariant_Note"}, "FC_CARDINAL_ADJ", JoinKind.LeftOuter),
    #"Expanded FC_CARDINAL_ADJ1" = Table.ExpandTableColumn(#"Merged Queries1", "FC_CARDINAL_ADJ", {"CLIENT_SHORT_NAME"}, {"CLIENT_SHORT_NAME"}),
    #"Inserted Division" = Table.AddColumn(#"Expanded FC_CARDINAL_ADJ1", "Division", each [AMOUNT_EUR] / 1000, type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Division", each ([PLAN_VARIANT_SHORT_NAME] <> null)),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Division", "Amount_EURk"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns", each [UNIQUE_IDENTIFIER] <> "DH Diagnostics, LLC // CP10077: Multiple Myeloma Dx Market Study / SE-150-202110512.0000"),
    #"Inserted Merged Column1" = Table.AddColumn(#"Filtered Rows2", "Unique_Project&Invoice_ID", each Text.Combine({[PROJECT_ID], [CUSTOMER_INVOICE_ID]}, "_"), type text),
    #"Duplicated Column" = Table.DuplicateColumn(#"Inserted Merged Column1", "PLAN_VARIANT_SHORT_NAME", "PLAN_VARIANT_SHORT_NAME - Copy"),
    #"Extracted Last Characters" = Table.TransformColumns(#"Duplicated Column", {{"PLAN_VARIANT_SHORT_NAME - Copy", each Text.End(_, 4), type text}}),
    #"Duplicated Column1" = Table.DuplicateColumn(#"Extracted Last Characters", "PLAN_VARIANT_SHORT_NAME", "PLAN_VARIANT_SHORT_NAME - Copy.1"),
    #"Extracted Text Before Delimiter" = Table.TransformColumns(#"Duplicated Column1", {{"PLAN_VARIANT_SHORT_NAME - Copy.1", each Text.BeforeDelimiter(_, "/"), type text}}),
    #"Split Column by Position" = Table.SplitColumn(#"Extracted Text Before Delimiter", "PLAN_VARIANT_SHORT_NAME - Copy.1", Splitter.SplitTextByPositions({0, 2}, true), {"PLAN_VARIANT_SHORT_NAME - Copy.1.1", "PLAN_VARIANT_SHORT_NAME - Copy.1.2"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Position",{{"PLAN_VARIANT_SHORT_NAME - Copy.1.1", type text}, {"PLAN_VARIANT_SHORT_NAME - Copy.1.2", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type","W","0",Replacer.ReplaceText,{"PLAN_VARIANT_SHORT_NAME - Copy.1.2"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value"," 9","09",Replacer.ReplaceValue,{"PLAN_VARIANT_SHORT_NAME - Copy.1.2"}),
    #"Filtered Rows3" = Table.SelectRows(#"Replaced Value1", each ([#"PLAN_VARIANT_SHORT_NAME - Copy"] <> "20v2" and [#"PLAN_VARIANT_SHORT_NAME - Copy"] <> "21v2")),
    #"Inserted Merged Column2" = Table.AddColumn(#"Filtered Rows3", "Merged_CW", each Text.Combine({[#"PLAN_VARIANT_SHORT_NAME - Copy"], [#"PLAN_VARIANT_SHORT_NAME - Copy.1.2"]}, ""), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Merged Column2",{{"Merged_CW", Int64.Type}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type1",{{"Merged_CW", Order.Descending}}),
    #"Inserted Merged Column3" = Table.AddColumn(#"Sorted Rows", "Merged_3", each Text.Combine({[#"Unique_Project&Invoice_ID"], [CUSTOMER]}, "_"), type text),
    #"Duplicated Column2" = Table.DuplicateColumn(#"Inserted Merged Column3", "Merged_CW", "Merged_CW - Copy"),
    #"Sorted Rows1" = Table.Sort(#"Duplicated Column2",{{"Merged_CW - Copy", Order.Descending}}),
    #"Kept First Rows" = Table.FirstN(#"Sorted Rows1",1),
    #"Removed Other Columns" = Table.SelectColumns(#"Kept First Rows",{"Merged_CW - Copy"})
in
    #"Removed Other Columns"
```


## Table: BYD_EMPLOYEE_DATA


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_EMPLOYEE_DATA = ByD_ODP{[Schema="dbo",Item="BYD_EMPLOYEE_DATA"]}[Data]
in
    dbo_BYD_EMPLOYEE_DATA
```


## Table: PROJECT_RESPONSIBLE_ACCOUNTING


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


## Table: PROJECT_RESPONSIBLE_ACCOUNTING by Projects


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


## Table: WIP_MIGRATION_CALC_LC


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WIP_MIGRATION_CALC_LC = WorkingCapitalMgmt{[Schema="dbo",Item="WIP_MIGRATION_CALC_LC"]}[Data]
in
    dbo_WIP_MIGRATION_CALC_LC
```


## Table: RESPONSIBLES_TBL


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RESPONSIBLES_TBL = WorkingCapitalMgmt{[Schema="dbo",Item="RESPONSIBLES_TBL"]}[Data]
in
    dbo_RESPONSIBLES_TBL
```


## Table: BYD_OPPORTUNITY_DATA_NEW


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_OPPORTUNITY_DATA_NEW = ByD_ODP{[Schema="dbo",Item="BYD_OPPORTUNITY_DATA_NEW"]}[Data]
in
    dbo_BYD_OPPORTUNITY_DATA_NEW
```


## Table: BYD_PROJECT_DATA


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_PROJECT_DATA = ByD_ODP{[Schema="dbo",Item="BYD_PROJECT_DATA"]}[Data]
in
    dbo_BYD_PROJECT_DATA
```


## Table: BYD_PROJECT_COMPLETION_PREVIOUS_MONTH


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_PROJECT_COMPLETION_PREVIOUS_MONTH = ByD_ODP{[Schema="dbo",Item="BYD_PROJECT_COMPLETION_PREVIOUS_MONTH"]}[Data]
in
    dbo_BYD_PROJECT_COMPLETION_PREVIOUS_MONTH
```


## Table: Merge_ Project Data_Invoice


```m
let
    Source = Table.NestedJoin(V_BYD_PROJECT_INVOICES, {"PROJECT_ID"}, BYD_PROJECT_DATA, {"PROJECT_ID"}, "BYD_PROJECT_DATA", JoinKind.LeftOuter),
    #"Expanded BYD_PROJECT_DATA" = Table.ExpandTableColumn(Source, "BYD_PROJECT_DATA", {"SALES_UNIT", "EARLIEST_START_DATE", "LATEST_START_DATE", "EARLIEST_FINISH_DATE", "LATEST_FINISH_DATE", "ACTUAL_PROJECT_FINISH_DATE", "ACTUAL_PROJECT_START_DATE", "COMPLETION_DATE"}, {"BYD_PROJECT_DATA.SALES_UNIT", "BYD_PROJECT_DATA.EARLIEST_START_DATE", "BYD_PROJECT_DATA.LATEST_START_DATE", "BYD_PROJECT_DATA.EARLIEST_FINISH_DATE", "BYD_PROJECT_DATA.LATEST_FINISH_DATE", "BYD_PROJECT_DATA.ACTUAL_PROJECT_FINISH_DATE", "BYD_PROJECT_DATA.ACTUAL_PROJECT_START_DATE", "BYD_PROJECT_DATA.COMPLETION_DATE"}),
    #"Added Conditional Column" = Table.AddColumn(#"Expanded BYD_PROJECT_DATA", "Investor Support_ID", each if Text.Contains([SALES_UNIT], "Investor") then 1 else 0),
    #"Filtered Rows" = Table.SelectRows(#"Added Conditional Column", each ([PROJECT_TYPE] = "Customer project with sales integration")),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows", "Today date", each DateTime.LocalNow()),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Today date", type date}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Changed Type", "Today date", "Today date - Copy")
in
    #"Duplicated Column"
```


## Table: SAP_CUSTOMER_DOWN_PAYMENTS_Open and Paid


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_SAP_CUSTOMER_DOWN_PAYMENTS = WorkingCapitalMgmt{[Schema="dbo",Item="SAP_CUSTOMER_DOWN_PAYMENTS"]}[Data],
    #"Added Custom1" = Table.AddColumn(dbo_SAP_CUSTOMER_DOWN_PAYMENTS, "Downpayment ID", each 1),
    #"Added Custom" = Table.AddColumn(#"Added Custom1", "Open_Amount_TC", each [TOTAL_AMOUNT_TC]+[CLEARED_AMOUNT]),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each ([PROJECT_ID] <> null and [PROJECT_ID] <> "") and ([INVOICE_LIFECYCLE_STATUS] = "Released") and ([CANCELLATION_INVOICE_INDICATOR_ID] = "False") and ([PROJECT_STATUS] <> "Closed"))
in
    #"Filtered Rows"
```


## Table: SAP_CUSTOMER_DOWN_PAYMENTS_Sum_Open & Paid


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_SAP_CUSTOMER_DOWN_PAYMENTS = WorkingCapitalMgmt{[Schema="dbo",Item="SAP_CUSTOMER_DOWN_PAYMENTS"]}[Data],
    #"Added Custom1" = Table.AddColumn(dbo_SAP_CUSTOMER_DOWN_PAYMENTS, "Downpayment ID", each 1),
    #"Added Custom" = Table.AddColumn(#"Added Custom1", "Open_Amount_TC", each [TOTAL_AMOUNT_TC]+[CLEARED_AMOUNT]),
    #"C1 Open Amount TC" = Table.SelectRows(#"Added Custom", each ([INVOICE_LIFECYCLE_STATUS] = "Released") and ([PROJECT_STATUS] <> "Closed") and ([PROJECT_TYPE] = "Customer project with sales integration") and ([CANCELLATION_INVOICE_INDICATOR_ID] = "False")),
    #"Removed Other Columns" = Table.SelectColumns(#"C1 Open Amount TC",{"INVOICING_UNIT_ID", "PROJECT_ID", "TOTAL_AMOUNT_TC", "TOTAL_AMOUNT_CUR", "Downpayment ID"}),
    #"Sorted Rows" = Table.Sort(#"Removed Other Columns",{{"PROJECT_ID", Order.Ascending}}),
    #"Grouped Rows" = Table.Group(#"Sorted Rows", {"PROJECT_ID", "Downpayment ID"}, {{"Sum_Total_Amount_TC", each List.Sum([TOTAL_AMOUNT_TC]), type nullable number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Grouped Rows",{{"Sum_Total_Amount_TC", "Total DP"}})
in
    #"Renamed Columns"
```

