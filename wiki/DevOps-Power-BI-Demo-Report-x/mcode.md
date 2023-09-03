



# M Code

## Table: Einwohnerzahlen


This M Code imports an Excel workbook from a specific file path. It then selects a specific sheet within the workbook (named "Einwohnerzahlen") and removes the first four rows. The remaining rows are then promoted to headers and unpivoted, with the "Land" column as the key column. The resulting table is then renamed and a custom column is added based on a condition where if the "Land" column equals "Deutschland", the value in the new column will be "DACH", otherwise it will be "-". Finally, the data types of the columns are transformed and the resulting table is returned.

```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\Einwohnerzahlen.xlsx"), null, false),
    Einwohnerzahlen_sheet = Quelle{[Item="Einwohnerzahlen",Kind="Sheet"]}[Data],
    #"Entfernte oberste Zeilen" = Table.Skip(Einwohnerzahlen_sheet,4),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Entfernte oberste Zeilen", [PromoteAllScalars=true]),
    #"Entpivotierte andere Spalten" = Table.UnpivotOtherColumns(#"Höher gestufte Header", {"Land"}, "Attribut", "Wert"),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Entpivotierte andere Spalten",{{"Attribut", "Jahr"}, {"Wert", "Einwohnerzahl"}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Umbenannte Spalten", "Berechnete Spalte in M", each if [Land] = "Deutschland" then "DACH" else "-"),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Hinzugefügte benutzerdefinierte Spalte",{{"Einwohnerzahl", Int64.Type}, {"Jahr", Int64.Type}, {"Berechnete Spalte in M", type text}})
in
    #"Geänderter Typ"
```
## Table: Geo


This M code is importing data from an Excel workbook located at "C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\AccessDB.xlsx". It then selects a table called "Geo" from the workbook and transforms the column data types for columns "PLZ", "Stadt", "Staat", "Region", "Distrikt", and "Land" to type text. Finally, it returns the transformed table as the output.

```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\AccessDB.xlsx"), null, true),
    Geo_Table = Quelle{[Item="Geo",Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(Geo_Table,{{"PLZ", type text}, {"Stadt", type text}, {"Staat", type text}, {"Region", type text}, {"Distrikt", type text}, {"Land", type text}})
in
    #"Geänderter Typ"
```
## Parameter: Parameter_SingleValue


Parameter mit einem Wert

This M code defines a parameter named "Parameterwert als Text" which is of type "Text". The parameter is marked as a required parameter (IsParameterQueryRequired=true) and can be used as a query parameter (IsParameterQuery=true) in Power Query or Power BI. 

When a query is executed, the user will be prompted to provide a value for this parameter. The parameter value can then be used in the query to filter, transform, or manipulate the data. Since this parameter is of type "Text", the user can enter any text value as the parameter value.

```m
"Parameterwert als Text" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```
## Parameter: Parameter_List


Parameter mit Liste von Werten die ausgewählt werden können

This is an M code for a parameter query that allows users to select a date value. The parameter has the following properties:

- List: A list of available date values that users can choose from. In this case, the list contains three date values: January 1, 2023, January 1, 2022, and January 1, 2021.

- DefaultValue: The default value for the parameter, which is set to January 1, 2023 in this case.

- Type: The data type of the parameter, which is set to "Date". This means that the parameter can only accept date values.

- IsParameterQuery: A Boolean value that indicates whether the query is a parameter query. In this case, it is set to true.

- IsParameterQueryRequired: A Boolean value that indicates whether the parameter query is required. If this is set to true, users must select a value for the parameter before the query can be executed.

```m
#date(2023, 1, 1) meta [IsParameterQuery=true, List={#date(2023, 1, 1), #date(2022, 1, 1), #date(2021, 1, 1)}, DefaultValue=#date(2023, 1, 1), Type="Date", IsParameterQueryRequired=true]
```