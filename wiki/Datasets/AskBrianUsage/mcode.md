



# M Code

|Dataset|[AskBrianUsage](./../AskBrianUsage.md)|
| :--- | :--- |
|Workspace|[AskBrian](../../Workspaces/AskBrian.md)|

## Table: user_overview


```m
let
    Quelle = Csv.Document(File.Contents("C:\Users\bernd_reiser\OneDrive - Roland Berger Holding GmbH\Ambassadors\AskBrian\Statistic_Data\User_overview.csv"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Höher gestufte Header" = Table.PromoteHeaders(Quelle, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"user_identifier", type text}, {"skillcluster", type text}, {"channel", type text}, {"#requests", Int64.Type}, {"created_at_month_short", type text}, {"created_at_week", type text}}),
    #"Benutzerdefinierte Spalte hinzugefügt" = Table.AddColumn(#"Geänderter Typ", "Date", each Text.Combine({Text.Middle([created_at_month_short], 5), ".", "01.", Text.Start([created_at_month_short], 4)}), type text),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Benutzerdefinierte Spalte hinzugefügt",{{"Date", type date}}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Geänderter Typ1",{{"Date", "MonthDate"}}),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Umbenannte Spalten","2023_","C",Replacer.ReplaceText,{"created_at_week"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Ersetzter Wert", each not Text.StartsWith([created_at_week], "2022_")),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Gefilterte Zeilen",{"created_at_month_short"}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Entfernte Spalten", {"user_identifier"}, #"rep v_hr_employee", {"email"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Erweiterte rep v_hr_employee" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "rep v_hr_employee", {"jobcode", "jobfunction", "company", "emp_status", "accounting_cat", "per_org", "platform_1_name", "job_display_name", "accounting_category", "country_code_iso3", "work_location_name", "office_location_name", "gender", "toe_id", "job_category", "toe_description", "region"}, {"rep v_hr_employee.jobcode", "rep v_hr_employee.jobfunction", "rep v_hr_employee.company", "rep v_hr_employee.emp_status", "rep v_hr_employee.accounting_cat", "rep v_hr_employee.per_org", "rep v_hr_employee.platform_1_name", "rep v_hr_employee.job_display_name", "rep v_hr_employee.accounting_category", "rep v_hr_employee.country_code_iso3", "rep v_hr_employee.work_location_name", "rep v_hr_employee.office_location_name", "rep v_hr_employee.gender", "rep v_hr_employee.toe_id", "rep v_hr_employee.job_category", "rep v_hr_employee.toe_description", "rep v_hr_employee.region"}),
    #"Entfernte Spalten1" = Table.RemoveColumns(#"Erweiterte rep v_hr_employee",{"rep v_hr_employee.accounting_cat", "rep v_hr_employee.toe_id"}),
    #"Ersetzter Wert1" = Table.ReplaceValue(#"Entfernte Spalten1","CW","",Replacer.ReplaceText,{"created_at_week"}),
    #"Geänderter Typ2" = Table.TransformColumnTypes(#"Ersetzter Wert1",{{"created_at_week", Int64.Type}})
in
    #"Geänderter Typ2"
```


## Table: rep v_hr_employee


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Quelle{[Schema="rep",Item="v_hr_employee"]}[Data]
in
    rep_v_hr_employee
```

