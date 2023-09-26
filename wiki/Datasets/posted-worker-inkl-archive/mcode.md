



# M Code

|Dataset|[posted worker inkl archive](./../posted-worker-inkl-archive.md)|
| :--- | :--- |
|Workspace|[Global Mobility](../../Workspaces/Global-Mobility.md)|

## Table: RLS Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: Requests


```m
let
    Source = #"Requests SharePoint" & #"Archive SharePoint"
in
    Source
```


## Table: Employees


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_pwd_employee = Source{[Schema="rep",Item="v_pwd_employee"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(rep_v_pwd_employee,{{"last_name", "Lastname"}, {"first_name", "Firstname"}, {"full_name", "Fullname"}, {"entry_date", "Entry date"}, {"exit_date", "Exit date"}, {"jobcode", "Jobcode"}, {"jobfunction", "Jobfunction"}, {"company", "Company"}, {"country_code", "Country code"}, {"country", "Country"}, {"office", "Office"}, {"work_location", "Work location"}, {"platform", "Platform"}, {"cost_center", "Cost center"}, {"gender", "Gender"}, {"email", "Email"}, {"birthday", "Birthday"}, {"cost_center_id", "Cost center id"}, {"birthplace_city", "Birthplace city"}, {"home_address_street", "Street"}, {"home_address_zipcode", "Zipcode"}, {"home_address_city", "City"}, {"home_address_country", "Country code (Addr)"}, {"home_address_country_descr", "Country (Addr)"}, {"phone_mobile", "Phone mobile"}, {"type_of_employment", "Type of employment"}, {"per_org", "per org"}, {"platform_id", "Platform id"}, {"company_id", "Company id"}, {"jobfunction_id", "Jobfunction id"}, {"jobcode_id", "Jobcode id"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each ([Email] <> null and [Email] <> "NoMail@rolandberger.com" and [Email] <> "no_mail@rolandberger.com" and [Email] <> "No_Mail@rolandberger.com")),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"Company id"}, #"pub ll_company_legal_entity", {"company_id"}, "pub ll_company_legal_entity", JoinKind.LeftOuter),
    #"Expanded pub ll_company_legal_entity" = Table.ExpandTableColumn(#"Merged Queries", "pub ll_company_legal_entity", {"legal_entity"}, {"Legal Entity"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Expanded pub ll_company_legal_entity", each ([emp_id] <> "M713796")),
    #"Entfernte Duplikate" = Table.Distinct(#"Gefilterte Zeilen", {"Email"})
in
    #"Entfernte Duplikate"
```


## Table: StaticExportData


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUTI0BRJeUIwVmRsaG5mAFCjACWQMEjDCpZcg8iNKBWFVEOSFgWNjAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Rechtsform = _t, Wirtschaftssektor = _t, #"Umsatzanteil >25% in D" = _t, #"Personal >25% in D" = _t, Strasse = _t, Hausnummer = _t, Adresszusatz = _t, Postleitzahl = _t, Ort = _t, Land = _t, #"Mitgliedsnummer bei Zuständigkeit ABV" = _t, Tätigkeit = _t, Geltung = _t, #"EG-Anspruch" = _t, Anwerbung = _t, Arbeitsvertrag = _t, Entlassung = _t, Aufgaben = _t, Beschäftigungsstelle = _t, Name = _t, Strasse.1 = _t, #"Haus-nummer" = _t, #"Adress-zusatz" = _t, PLZ = _t, Ort.1 = _t, Name.1 = _t, Strasse.2 = _t, #"Haus-nummer.1" = _t, #"Adress-zusatz.1" = _t, PLZ.1 = _t, Ort.2 = _t, Name.2 = _t, Strasse.3 = _t, #"Haus-nummer.2" = _t, #"Adress-zusatz.2" = _t, PLZ.2 = _t, Ort.3 = _t, #"Bisheriger Einsatz" = _t, #"Beginn-EZ" = _t, #"Ende-EZ" = _t, #"Beginn-EZ.1" = _t, #"Ende-EZ.1" = _t, #"Beginn-EZ.2" = _t, #"Ende-EZ.2" = _t, #"Beginn-EZ.3" = _t, #"Ende-EZ.3" = _t, #"Beginn-EZ.4" = _t, #"Ende-EZ.4" = _t, #"AN-Ueberlassung" = _t, #"AN-Abloesung" = _t, Geschlecht = _t, Vorname = _t, Familienname = _t, Vorsatzwort = _t, Namenszusatz = _t, Titel = _t, Geburtsdatum = _t, #"Beginn-GEZ" = _t, #"Ende-GEZ" = _t, #"Beginn-TEZ" = _t, #"Ende-TEZ" = _t, Grund = _t, Angaben = _t, #"Info Pflicht-1" = _t, #"Info Pflicht-2" = _t, #"Info Pflicht-3" = _t, #"Info Pflicht-4" = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Rechtsform", Int64.Type}, {"Wirtschaftssektor", Int64.Type}, {"Umsatzanteil >25% in D", type text}, {"Personal >25% in D", type text}, {"Strasse", type text}, {"Hausnummer", type text}, {"Adresszusatz", type text}, {"Postleitzahl", type text}, {"Ort", type text}, {"Land", type text}, {"Mitgliedsnummer bei Zuständigkeit ABV", type text}, {"Tätigkeit", Int64.Type}, {"Geltung", type text}, {"EG-Anspruch", type text}, {"Anwerbung", type text}, {"Arbeitsvertrag", type text}, {"Entlassung", type text}, {"Aufgaben", type text}, {"Beschäftigungsstelle", Int64.Type}, {"Name", type text}, {"Strasse.1", type text}, {"Haus-nummer", type text}, {"Adress-zusatz", type text}, {"PLZ", type text}, {"Ort.1", type text}, {"Name.1", type text}, {"Strasse.2", type text}, {"Haus-nummer.1", type text}, {"Adress-zusatz.1", type text}, {"PLZ.1", type text}, {"Ort.2", type text}, {"Name.2", type text}, {"Strasse.3", type text}, {"Haus-nummer.2", type text}, {"Adress-zusatz.2", type text}, {"PLZ.2", type text}, {"Ort.3", type text}, {"Bisheriger Einsatz", type text}, {"Beginn-EZ", type text}, {"Ende-EZ", type text}, {"Beginn-EZ.1", type text}, {"Ende-EZ.1", type text}, {"Beginn-EZ.2", type text}, {"Ende-EZ.2", type text}, {"Beginn-EZ.3", type text}, {"Ende-EZ.3", type text}, {"Beginn-EZ.4", type text}, {"Ende-EZ.4", type text}, {"AN-Ueberlassung", type text}, {"AN-Abloesung", type text}, {"Geschlecht", type text}, {"Vorname", type text}, {"Familienname", type text}, {"Vorsatzwort", type text}, {"Namenszusatz", type text}, {"Titel", type text}, {"Geburtsdatum", type text}, {"Beginn-GEZ", type text}, {"Ende-GEZ", type text}, {"Beginn-TEZ", type text}, {"Ende-TEZ", type text}, {"Grund", type text}, {"Angaben", type text}, {"Info Pflicht-1", type text}, {"Info Pflicht-2", type text}, {"Info Pflicht-3", type text}, {"Info Pflicht-4", type text}})
in
    #"Geänderter Typ"
```


## Table: CountryInfo


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("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", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Title = _t, Code = _t, #"Mitgliedsstaat/Flaggenstaat" = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Title", type text}, {"Code", type text}, {"Mitgliedsstaat/Flaggenstaat", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: FixedExportData


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Spalte ""1""" = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Spalte ""1""", type text}})
in
    #"Geänderter Typ"
```

