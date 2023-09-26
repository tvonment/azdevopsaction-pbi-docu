



# M Code

|Dataset|[AskBrian_Pilot](./../AskBrian_Pilot.md)|
| :--- | :--- |
|Workspace|[AskBrian](../../Workspaces/AskBrian.md)|

## Table: 2022_11_30_user overview PS Spe


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\bernd_reiser\OneDrive - Roland Berger Holding GmbH\Ambassadors\AskBrian\2022_11_30_user overview PS Special.xlsx"), null, true),
    #"2022_11_30_user overview PS Spe_Sheet" = Quelle{[Item="2022_11_30_user overview PS Spe",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(#"2022_11_30_user overview PS Spe_Sheet", [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"user_identifier", type text}, {"#requests", Int64.Type}, {"skillcluster", type text}})
in
    #"Geänderter Typ"
```


## Table: rep v_hr_employee


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Quelle{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Entfernte Spalten" = Table.RemoveColumns(rep_v_hr_employee,{"mentor_emp_id", "mentor_last_name", "pa_emp_id", "pa_emp_last_name"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Entfernte Spalten", each ([email] <> null and [email] <> "no_mail@rolandberger.com")),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Gefilterte Zeilen","Consultant 1","Consultant",Replacer.ReplaceText,{"jobcode"}),
    #"Ersetzter Wert1" = Table.ReplaceValue(#"Ersetzter Wert","Consultant 2","Consultant",Replacer.ReplaceText,{"jobcode"}),
    #"Ersetzter Wert2" = Table.ReplaceValue(#"Ersetzter Wert1","Project Manager 1","Project Manager",Replacer.ReplaceText,{"jobcode"}),
    #"Ersetzter Wert3" = Table.ReplaceValue(#"Ersetzter Wert2","Project Manager 2","Project Manager",Replacer.ReplaceText,{"jobcode"})
in
    #"Ersetzter Wert3"
```


## Table: 2022_11_30_user overview PS Spe (2)


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\bernd_reiser\OneDrive - Roland Berger Holding GmbH\Ambassadors\AskBrian\2022_11_30_user overview PS Special.xlsx"), null, true),
    #"2022_11_30_user overview PS Spe_Sheet" = Quelle{[Item="2022_11_30_user overview PS Spe",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(#"2022_11_30_user overview PS Spe_Sheet", [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"user_identifier", type text}, {"#requests", Int64.Type}, {"skillcluster", type text}}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Geänderter Typ", {"user_identifier"}, #"rep v_hr_employee", {"email"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Erweiterte rep v_hr_employee" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "rep v_hr_employee", {"jobcode", "sex", "country", "platform_1_name"}, {"rep v_hr_employee.jobcode", "rep v_hr_employee.sex", "rep v_hr_employee.country", "rep v_hr_employee.platform_1_name"})
in
    #"Erweiterte rep v_hr_employee"
```

