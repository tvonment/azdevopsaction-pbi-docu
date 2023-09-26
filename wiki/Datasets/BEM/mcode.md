



# M Code

|Dataset|[BEM](./../BEM.md)|
| :--- | :--- |
|Workspace|[HR_BEM](../../Workspaces/HR_BEM.md)|

## Table: Query1


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "data_staging", [Query="select eth.*, eabs.TIME_TYPE, COALESCE(eabs.ILLNESS, 0) AS ILLNESS, eabs.ABSENCE_TIME  #(lf)from [data_staging].[dbo].[EMPLOYEE_TARGET_HOURS_JOINED] eth#(lf)left outer join (#(lf)            select *, 1 AS ILLNESS #(lf)            from [data_staging].[dbo].[vBYD_EMPLOYEE_ABSENCE]#(lf)            where TIME_TYPE_CATEGORY = 'Illness'#(lf)            --and  ABSENCE_TIME <> 0#(lf)) eabs#(lf)on eth.EMPLOYEE_ID = eabs.EMPLOYEE_ID#(lf)and eth.CALENDAR_DAY >= eabs.DATE_FROM#(lf)and eth.CALENDAR_DAY <= eabs.DATE_TO#(lf)where eth.Target_hours > 0#(lf)--(eth.Target_hours > 0 or COALESCE(eabs.ILLNESS, 0) > 0)#(lf)and eth.CALENDAR_DAY >= Dateadd(year, -1, getdate())#(lf)and eth.CALENDAR_DAY <= Dateadd(day, 1, getdate())#(lf)#(lf)--and eth.CALENDAR_DAY >= '2022-7-1'#(lf)--and eth.CALENDAR_DAY <= '2022-7-31'#(lf)--and eth.EMPLOYEE_ID = 'M002448'#(lf)"]),
    #"Filtered Rows" = Table.SelectRows(Source, each [CALENDAR_DAY] > #datetime(2018, 5, 31, 0, 0, 0)),
    #"Merged DEU only" = Table.NestedJoin(#"Filtered Rows", {"EMPLOYEE_ID"}, merge_employees_germany, {"emp_id"}, "merge_employees_germany", JoinKind.Inner),
    #"Expanded merge_employees_germany" = Table.ExpandTableColumn(#"Merged DEU only", "merge_employees_germany", {"country_code"}, {"country_code"})
in
    #"Expanded merge_employees_germany"
```


## Table: vEMPLOYEES


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "data_staging", [Query="select [EMPLID], [FIRST_NAME], [LAST_NAME], [COMPANY_DESCR] as Company#(lf)from [dbo].[vEMPLOYEES]"]),
    #"Merged DEU only" = Table.NestedJoin(Source, {"EMPLID"}, merge_employees_germany, {"emp_id"}, "merge_employees_germany", JoinKind.Inner),
    #"Expanded merge_employees_germany" = Table.ExpandTableColumn(#"Merged DEU only", "merge_employees_germany", {"last_hire_date", "ter_max_date", "jobcode", "jobfunction", "sex", "country_code", "platform_1_name"}, {"last_hire_date", "ter_max_date", "jobcode", "jobfunction", "sex", "country_code", "platform_1_name"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded merge_employees_germany",{{"sex", "gender"}, {"platform_1_name", "platform"}})
in
    #"Renamed Columns"
```


## Table: AggregatedData


```m
let
    Source = Query1,
    #"Filtered Country DEU" = Table.SelectRows(Source, each [country_code] = "DEU"),
    #"Duplicated Column" = Table.DuplicateColumn(#"Filtered Country DEU", "CALENDAR_DAY", "CALENDAR_DAY - Copy"),
    #"Changed Type" = Table.TransformColumnTypes(#"Duplicated Column",{{"CALENDAR_DAY - Copy", Int64.Type}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type", "Workday", each [#"CALENDAR_DAY - Copy"] - [#"CALENDAR_DAY - Copy"] + 1),
    #"Added Custom" = Table.AddColumn(#"Added Custom1", "KW", each Date.WeekOfYear([CALENDAR_DAY])),
    #"Added Custom2" = Table.AddColumn(#"Added Custom", "Year", each Date.Year([CALENDAR_DAY])),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Month", each Date.Month([CALENDAR_DAY])),
    #"Grouped Rows" = Table.Group(#"Added Custom3", {"EMPLOYEE_ID", "KW", "Year"}, {{"SickDays", each List.Sum([ILLNESS]), type number}, {"WorkDays", each List.Sum([Workday]), type number}, {"Month", each List.Min([Month]), type number}})
in
    #"Grouped Rows"
```


## Table: WochenCluster


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("TcrdCoAgDIbhWxk7jrDNBK/FPIjyKEroh26/OQIdfDBenhBweozhBQjelLYLOzSywfvey5UXYxeQ4M7wU5ZKpjCqjJRxw6xUVsaVsTLbMCfVKhsrs8oczMcKez6TJKemMIzxAw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Anzahl Wochen Arbeitsunfähigkeit" = _t, biggerOrEqual = _t, smallerThan = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Anzahl Wochen Arbeitsunfähigkeit", type text}, {"biggerOrEqual", type number}, {"smallerThan", type number}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: Calculated Date Filter


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WcsvMKUktUoqNBQA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```

