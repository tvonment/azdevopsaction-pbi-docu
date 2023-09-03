



# M Code

## Table: Population


This M code performs several transformations on an Excel sheet called "Sheet Population" within a file located at "C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\Population.xlsx". 

The transformations include removing top rows and blank rows, skipping the first two rows, promoting headers, unpivoting columns, renaming columns, and changing the type of the "Population" column to Int64.

The resulting table is returned as the output of the M code.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\Population.xlsx"), null, false),
    Population_sheet = Source{[Item="Sheet Population",Kind="Sheet"]}[Data],
    FilterNullAndWhitespace = each List.Select(_, each _ <> null and (not (_ is text) or Text.Trim(_) <> "")),
    #"Removed Top Rows" = Table.Skip(Population_sheet, each try List.IsEmpty(List.Skip(FilterNullAndWhitespace(Record.FieldValues(_)), 1)) otherwise false),
    #"Removed Blank Rows" = Table.SelectRows(#"Removed Top Rows", each not List.IsEmpty(FilterNullAndWhitespace(Record.FieldValues(_)))),
    #"Removed Top Rows1" = Table.Skip(#"Removed Blank Rows",2),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Top Rows1", [PromoteAllScalars=true]),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Promoted Headers", {"Country"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Year"}, {"Value", "Population"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Population", Int64.Type}})
in
    #"Changed Type"
```
## Table: Calendar


This M Code imports an Excel workbook from the specified file path and reads the data from the "Calendar" table. It then transforms the column types of the table to match the appropriate data types, such as changing the "Date" column to a date type and the "Month Nr." column to an integer type. Finally, the transformed table is outputted as the result.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Calendar_Table = Source{[Item="Calendar",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Calendar_Table,{{"Date", type date}, {"Day", Int64.Type}, {"Month", type text}, {"Month Nr.", Int64.Type}, {"Quarter", type text}, {"Year", Int64.Type}})
in
    #"Changed Type"
```
## Table: Geo


This M code is importing data from an Excel file located at "C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx". It then selects the "Geo" table from the Excel file and transforms the data types of certain columns using the Table.TransformColumnTypes function. Finally, the transformed data is returned as a new table.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Geo_Table = Source{[Item="Geo",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Geo_Table,{{"Postalcode", type text}, {"City", type text}, {"State", type text}, {"Region", type text}, {"District", type text}, {"Country", type text}})
in
    #"Changed Type"
```
## Table: Manufacturers


This M code imports data from an Excel file located at "C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx". It then selects the "Manufacturers" table from the imported data and transforms the "Manufacturer ID" column to data type Int64 and the "Manufacturer Name" column to data type text. The final result is a transformed table with the updated data types.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Manufacturers_Table = Source{[Item="Manufacturers",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Manufacturers_Table,{{"Manufacturer ID", Int64.Type}, {"Manufacturer Name", type text}})
in
    #"Changed Type"
```
## Table: Products


This M code imports an Excel workbook file named "AccessDB.xlsx" located in the specified file path. It then selects the "Products" table from the workbook and transforms the data types of certain columns (Product ID and Manufacturer ID) to Int64 and the remaining columns (Name, Category, and Segment) to text. The final result is a transformed table that can be used for further data analysis and visualization in Power BI.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Products_Table = Source{[Item="Products",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Products_Table,{{"Product ID", Int64.Type}, {"Name", type text}, {"Category", type text}, {"Segment", type text}, {"Manufacturer ID", Int64.Type}})
in
    #"Changed Type"
```
## Table: Sales


This M code is used in Power Query Editor in Microsoft Excel. It combines two tables named "US Sales" and "International Sales" into a single table named "Source". Then, a custom column named "Country name" is added to the "Source" table. 

The custom column is added using the if-else statement. If the value in the "Country" column is null, then the value "USA" is assigned to the "Country name" column, otherwise the value in the "Country" column is assigned to the "Country name" column. 

After adding the custom column, the "Country" column is removed from the "Source" table using the "Removed Columns" step. Finally, the data types of the columns are changed to text, Int64 and number using the "Changed Type" step.

```m
let
    Source = Table.Combine({#"US Sales", #"International Sales"}),
    #"Added Custom" = Table.AddColumn(Source, "Country name", each if [Country] = null then "USA" else [Country]),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"Country"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"Country name", type text}, {"Amount", Int64.Type}, {"Product ID", Int64.Type}, {"Postalcode", type text}, {"Revenue", type number}})
in
    #"Changed Type"
```
## Parameter: Parameter1


This M code defines a parameter query in Power Query that is named "Sample File". 

- "IsParameterQuery=true" indicates that this is a parameter query, which means that it allows the user to specify a value for the query parameter when the query is loaded or refreshed. 

- "BinaryIdentifier=#"Sample File"" indicates that the parameter is of type "Binary", which means that it expects binary data as input. The "#" character is used to delimit the name of the parameter, and in this case the name is "Sample File". 

- "IsParameterQueryRequired=true" indicates that the user must specify a value for this parameter when the query is loaded or refreshed. 

Overall, this M code is defining a parameter query that expects binary data and requires the user to specify a value for the "Sample File" parameter.

```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```