



# M Code

|Dataset|[CO2 Dashboard](./../CO2-Dashboard.md)|
| :--- | :--- |
|Workspace|[Travel & Mobility](../../Workspaces/Travel-&-Mobility.md)|

## Table: co2kg


```m
let
    Source = Flights,
    #"Appended Query" = Table.Combine({Source, FuelCards, Taxi}),
    #"Added Index" = Table.AddIndexColumn(#"Appended Query", "Index", 0, 1, Int64.Type),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Added Index", "FirstOfMonth", each #date(Date.Year([date]), Date.Month([date]), 1), Date.Type),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Hinzugefügte benutzerdefinierte Spalte", {"emp_id", "FirstOfMonth"}, hr_statistics, {"emp_id", "validfrom_date"}, "hr_statistics", JoinKind.LeftOuter),
    #"Erweiterte hr_statistics" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "hr_statistics", {"peer_group"}, {"peer_group"})
in
    #"Erweiterte hr_statistics"
```


## Table: _meta


```m
let
    Source = DateTimeZone.RemoveZone( DateTimeZone.UtcNow() + #duration(0,2,0,0)),
    #"Converted to Table" = #table(1, {{Source}}),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "LastRefresh"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"LastRefresh", type datetime}})
in
    #"Changed Type"
```


## Table: employee


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Source{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_employee, each ([country_code] = "DEU" or [country_code] = "AUT" or [country_code] = "CHE" or [country_code] = "CHN" or [country_code] = "ITA" or [country_code] = "HKG") and ([empl_class_descr] = "Active Employee" or [empl_class_descr] = "Diplomate" or [empl_class_descr] = "Doctorate program" or [empl_class_descr] = "Exemption with exit" or [empl_class_descr] = "Leave of absence <1 month" or [empl_class_descr] = "Leave of absence >=1 month" or [empl_class_descr] = "Maternity leave" or [empl_class_descr] = "MBA program" or [empl_class_descr] = "Parental leave" or [empl_class_descr] = "Retiree" or [empl_class_descr] = "Sabbatical")),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"job_category", "peer_group"}}),
    #"Replaced Value1" = Table.ReplaceValue(#"Renamed Columns",null,"Other",Replacer.ReplaceValue,{"peer_group"}),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Replaced Value1",each [peer_group], each [country_code] & "_" & [peer_group] ,Replacer.ReplaceText,{"peer_group"}),
    #"Appended Query" = Table.Combine({#"Ersetzter Wert", M999999})
in
    #"Appended Query"
```


## Table: Types


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCskvScxR0lEyVIrViVZyy8lMzygBco0g3NLUHAXnxKIUoIgxWCQksSITyDFRio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Type = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Type", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: Who


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WiswvVdJRMlSK1YlWCkhNLQJyjJRiYwE=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Who = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Who", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: rls own user


```m
let
    Source = employee
in
    Source
```


## Table: Total


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCskvScxRio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Total = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Total", type text}})
in
    #"Changed Type"
```


## Table: Flights Detail


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_co2_flights = Source{[Schema="rep",Item="co2_flights"]}[Data],
    #"Filtered Year" = Table.SelectRows(rep_co2_flights, each (Date.Year([flight_period]) = Status_Year )),
    #"Added StartOfMonth" = Table.AddColumn(#"Filtered Year", "start_of_month", each #date( Date.Year([flight_period]), Date.Month([flight_period]) ,1), Date.Type),
    #"filter max date" = Table.SelectRows(#"Added StartOfMonth", each [start_of_month] <= Status_Date),
    #"Renamed Columns1" = Table.RenameColumns(#"filter max date",{{"flight_date", "date"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns1", "type", each "Flight", type text),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"avoidable_emissions", "avoidable emissions"}, {"duration_train", "duration train"}})
in
    #"Renamed Columns"
```


## Table: FuelCards Detail


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_co2_fuel_cards = Source{[Schema="rep",Item="co2_fuel_cards"]}[Data],
    #"Filtered Year" = Table.SelectRows(rep_co2_fuel_cards, each ( Date.Year([fuel_date]) = Status_Year)),
    #"Added StartOfMonth" = Table.AddColumn(#"Filtered Year", "start_of_month", each #date( Date.Year([fuel_date]), Date.Month([fuel_date]) ,1), Date.Type),
    #"filter max date" = Table.SelectRows(#"Added StartOfMonth", each [start_of_month] <= Status_Date),
    #"Renamed Columns" = Table.RenameColumns(#"filter max date",{{"fuel_date", "date"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "type", each "Fuel Card", type text),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"fuel_type", "fuel type"}})
in
    #"Renamed Columns1"
```


## Table: Texts


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: Status_Date


```m
let
    Source = MaxDate
in
    Source
```


## Table: M999999


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8rUEAyUdJRfX0Hj3ovzSAgW30rzkksz8PKXYWAA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [emp_id = _t, peer_group = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"emp_id", type text}, {"peer_group", type text}})
in
    #"Changed Type"
```


## Table: hr_statistics


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_co2_flights = Source{[Schema="rep",Item="v_hr_statistic"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(rep_co2_flights, each ([country_company] = "AUT" or [country_company] = "CHE" or [country_company] = "DEU" or [country_company] = "CHN" or [country_company] = "HKG" or [country_company] = "ITA") and ([toe] <> "Intern" and [toe] <> "Retiree" and [toe] <> "Temporary Help")),
    #"Andere entfernte Spalten" = Table.SelectColumns(#"Gefilterte Zeilen",{"validfrom_date", "emp_id", "last_name", "first_name", "jobcode_id", "toe", "country_company"}),
    #"Gefilterte Zeilen1" = Table.SelectRows(#"Andere entfernte Spalten", each [validfrom_date] >= #date(Status_Year, 1, 1) and [validfrom_date] < Date.AddMonths(#date(Status_Year, Status_Month, 1), 1 ) ),
    #"Zusammengeführte Abfragen1" = Table.NestedJoin(#"Gefilterte Zeilen1", {"jobcode_id"}, ll_job, {"jobcode_id"}, "ll_job", JoinKind.LeftOuter),
    #"Erweiterte ll_job" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen1", "ll_job", {"job_category"}, {"job_category"}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Erweiterte ll_job",{{"job_category", "peer_group"}}),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Umbenannte Spalten",each [peer_group], each [peer_group] & "_" & [country_company],Replacer.ReplaceText,{"peer_group"}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Ersetzter Wert", {"emp_id"}, #"all emp", {"emp_id"}, "all emp", JoinKind.LeftOuter),
    #"Erweiterte all emp" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "all emp", {"email"}, {"email"})
in
    #"Erweiterte all emp"
```


## Table: rls own hr_statistics


```m
let
    Source = hr_statistics
in
    Source
```


## Roles

### User


Model Permission: Read

rls own user

```m
[email] = userprincipalname()
```



rls own hr_statistics

```m
[email] = userprincipalname()
```

