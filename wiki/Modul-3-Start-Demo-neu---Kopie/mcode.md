



# M Code

## Table: Hersteller


This M code is used in Power Query, a data transformation and cleaning tool in Excel and Power BI. 

The code first defines a variable named "Quelle" which is assigned the value of an Excel workbook. The workbook is accessed using the "File.Contents" function and the file path is specified using the "Pfad" variable.

The next line of code retrieves a table named "Hersteller" from the workbook using the syntax "Quelle{[Item="Hersteller", Kind="Table"]}[Data]". This line of code specifies the name of the table ("Hersteller") and the type of item being retrieved ("Table").

The third line of code transforms the column types of the "Hersteller" table. The "Table.TransformColumnTypes" function is used to specify the table to transform ("_Hersteller") and the new data types for each column. In this case, the "Hersteller ID" column is transformed to "Int64" data type and the "Hersteller Name" column is transformed to "text" data type.

The final line of code returns the transformed table ("Geänderter Typ") as the output of the query.

```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Hersteller = Quelle{[Item="Hersteller", Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Hersteller,{{"Hersteller ID", Int64.Type}, {"Hersteller Name", type text}})
in
    #"Geänderter Typ"
```
## Table: Kalender


This M code is loading data from an Excel workbook named "AccessDB.xlsx" located in a file path specified in a variable named "Pfad". It then selects a table named "Kalender" from the workbook and converts some of its columns to specific data types. 

The first line creates a variable named "Quelle" that represents the Excel workbook. The "File.Contents" function loads the contents of the workbook file, and the "Excel.Workbook" function creates a connection to the workbook.

The second line creates a variable named "_Kalender" that represents the "Kalender" table in the workbook. The syntax used to select the table is called "M path notation".

The third line creates a variable named "#Geänderter Typ" that represents the transformed table. The "Table.TransformColumnTypes" function is used to convert the data types of specific columns. The column names and their new data types are specified in a list of pairs. 

Finally, the transformed table is returned as the output of the M code.

```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Kalender = Quelle{[Item="Kalender",Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Kalender,{{"Jahr", Int64.Type}, {"Datum", type date}, {"Tag", Int64.Type}, {"Monat ", type text}, {"Monat Nr", Int64.Type}, {"Quartal", type text}})
in
    #"Geänderter Typ"
```
## Table: Produkte


This M code is used to load and transform data from an Excel workbook file named "AccessDB.xlsx". It first defines a variable "Quelle" that represents the Excel workbook file using the "Excel.Workbook" function. 

Then, it accesses the "Produkte" table from the workbook using "Quelle{[Item="Produkte", Kind="Table"]}[Data]". This table is then transformed by changing the data types of some columns using the "Table.TransformColumnTypes" function. 

Finally, the transformed table is returned as output using "in #"Geänderter Typ"".

```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Produkte = Quelle{[Item="Produkte", Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Produkte,{{"Produkt ID", Int64.Type}, {"Produktname", type text}, {"Kategorie", type text}, {"Segment", type text}, {"Hersteller ID", Int64.Type}, {"Hersteller Name", type text}})
in
    #"Geänderter Typ"
```
## Table: Geo


This M code imports data from an Excel workbook located at a specified path (variable "Pfad") and selects the "Geo" table. It then transforms the data types of certain columns in the table and filters all rows. Finally, it returns the filtered table.

```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Geo = Quelle{[Item="Geo", Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Geo,{{"Stadt", type text}, {"Staat", type text}, {"Region", type text}, {"Distrikt", type text}, {"Land", type text}}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Geänderter Typ", each true)
in
    #"Gefilterte Zeilen"
```
## Table: Sales


This M Code combines two tables ("US Sales" and "International Sales") into one table called "Quelle". Then, a custom column called "Ländername" (which means "country name" in German) is added to the "Quelle" table. The custom column checks if the value in the "Land" column is null (empty) and if it is, it assigns the value "USA" to the "Ländername" column. If the value in the "Land" column is not null, it assigns the value in the "Land" column to the "Ländername" column. 

Finally, the "Land" column is removed from the "Quelle" table, and the resulting table is returned as the output of the code.

```m
let
    Quelle = Table.Combine({#"US Sales", #"International Sales"}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(Quelle, "Ländername", each if [Land] = null then "USA" else [Land]),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Hinzugefügte benutzerdefinierte Spalte",{"Land"})
in
    #"Entfernte Spalten"
```
## Table: StatDatum


This M Code creates a Date parameter query with a default value of January 1st, 2019. 

The "meta" keyword is used to add metadata to the query. In this case, it indicates that this is a parameter query, the data type is "Date", and it is required (IsParameterQuery=true, Type="Date", IsParameterQueryRequired=true). 

This code can be used in Power Query or Power BI to create a user-defined parameter that allows the user to select a date within a specified range.

```m
#date(2019, 1, 1) meta [IsParameterQuery=true, Type="Date", IsParameterQueryRequired=true]
```
## Table: Einwohnerzahlen


This M code imports an Excel workbook located at "C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\Einwohnerzahlen.xlsx" and retrieves the data from the "Einwohnerzahlen" sheet. It then skips the first 4 rows of the sheet, promotes the headers to a higher level, unpivots all columns except for "Land" to create a normalized table, renames the "Attribut" and "Wert" columns to "Jahr" and "Einwohnerzahl" respectively, and changes the data types of the "Jahr" and "Einwohnerzahl" columns to Int64. The final step is to return the transformed table.

```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\Einwohnerzahlen.xlsx"), null, false),
    Einwohnerzahlen_sheet = Quelle{[Item="Einwohnerzahlen",Kind="Sheet"]}[Data],
    #"Entfernte oberste Zeilen" = Table.Skip(Einwohnerzahlen_sheet,4),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Entfernte oberste Zeilen", [PromoteAllScalars=true]),
    #"Entpivotierte andere Spalten" = Table.UnpivotOtherColumns(#"Höher gestufte Header", {"Land"}, "Attribut", "Wert"),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Entpivotierte andere Spalten",{{"Attribut", "Jahr"}, {"Wert", "Einwohnerzahl"}}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Umbenannte Spalten",{{"Jahr", Int64.Type}, {"Einwohnerzahl", Int64.Type}})
in
    #"Geänderter Typ"
```
## Parameter: Parameter1


This M code defines a parameter query named "meta" with the following properties:
- IsParameterQuery=true: This indicates that the query is a parameter query and can be used to pass values to other queries or reports.
- BinaryIdentifier=Beispieldatei: This specifies a unique identifier for the parameter query, which can be used to refer to it in other queries or reports.
- Type="Binary": This indicates that the parameter will accept binary data, such as a file or image.
- IsParameterQueryRequired=true: This specifies that the parameter query is required and must be provided with a value before the report or query can be run.

```m
Beispieldatei meta [IsParameterQuery=true, BinaryIdentifier=Beispieldatei, Type="Binary", IsParameterQueryRequired=true]
```
## Parameter: Pfad


This M code defines a parameter query in Power Query Editor. 

- The first part of the code "C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\" specifies the default value for the parameter, i.e., the folder path where the data files are located.

- The second part "meta [IsParameterQuery=true, List={"C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\"}, DefaultValue="C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\", Type="Text", IsParameterQueryRequired=true]" provides metadata information about the parameter. 

    - "IsParameterQuery=true" indicates that the code is defining a parameter query.
    
    - "List={"C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\"}" specifies the list of values that the parameter can take. In this case, it only has one value, which is the default value.
    
    - "DefaultValue="C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\"" specifies the default value for the parameter.
    
    - "Type="Text"" specifies the data type of the parameter as text.
    
    - "IsParameterQueryRequired=true" indicates that the parameter is required for the query to run.

```m
"C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\" meta [IsParameterQuery=true, List={"C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\"}, DefaultValue="C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\", Type="Text", IsParameterQueryRequired=true]
```