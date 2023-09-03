



# M Code

## Table: Population


This M Code imports data from an Excel workbook called "Population.xlsx" and performs several transformations on the "Sheet Population" in the workbook. 

The first step is to load the workbook into a variable called "Source". 

Next, the "Population_sheet" variable is created to reference the "Sheet Population" in the workbook. 

The "FilterNullAndWhitespace" step removes any null or whitespace values from the table. 

The "Removed Top Rows" step removes any rows at the top of the table that do not contain any data. 

The "Removed Blank Rows" step removes any rows that contain only blank cells. 

The "Removed Top Rows1" step skips the first two rows of the table. 

The "Promoted Headers" step promotes the first row of the table as headers. 

The "Unpivoted Other Columns" step unpivots all columns except for the "Country" column. 

The "Renamed Columns" step renames the "Attribute" column to "Year" and the "Value" column to "Population". 

Finally, the "Changed Type" step changes the data type of the "Population" column to Int64. 

The result of these transformations is a table with columns "Country", "Year", and "Population", which can be used for further analysis and visualization in Power BI.

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


This M code connects to an Excel workbook located at "C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx". It then selects the "Calendar" table from the workbook and transforms the column types to match the expected data types. The resulting table is then returned as the output.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Calendar_Table = Source{[Item="Calendar",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Calendar_Table,{{"Date", type date}, {"Day", Int64.Type}, {"Month", type text}, {"Month Nr.", Int64.Type}, {"Quarter", type text}, {"Year", Int64.Type}})
in
    #"Changed Type"
```
## Table: Geo


This M code imports data from an Excel workbook located at "C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx". It then selects a specific table within the workbook called "Geo" and transforms the data types of the columns. Specifically, it changes the "Postalcode", "City", "State", "Region", "District", and "Country" columns to be of type "text". The final result is a table with the transformed data.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Geo_Table = Source{[Item="Geo",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Geo_Table,{{"Postalcode", type text}, {"City", type text}, {"State", type text}, {"Region", type text}, {"District", type text}, {"Country", type text}})
in
    #"Changed Type"
```
## Table: Manufacturers


This M code is used to load data from an Excel workbook named "AccessDB.xlsx". The code accesses the "Manufacturers" table from the workbook and transforms the data types of the columns "Manufacturer ID" and "Manufacturer Name" to Int64 and text, respectively. The transformed table is then returned as the final output.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Manufacturers_Table = Source{[Item="Manufacturers",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Manufacturers_Table,{{"Manufacturer ID", Int64.Type}, {"Manufacturer Name", type text}})
in
    #"Changed Type"
```
## Table: Products


This M code imports data from an Excel workbook located at "C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx". The code then selects the "Products" table from the workbook and transforms the data types of the columns "Product ID" and "Manufacturer ID" to Int64 (integer) and the columns "Name", "Category", and "Segment" to text. The resulting transformed table is returned as the output of the M code.

```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Products_Table = Source{[Item="Products",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Products_Table,{{"Product ID", Int64.Type}, {"Name", type text}, {"Category", type text}, {"Segment", type text}, {"Manufacturer ID", Int64.Type}})
in
    #"Changed Type"
```
## Table: Sales


This M code is a sequence of transformations applied to a table. 

The first transformation combines two tables named "US Sales" and "International Sales". 

The second transformation adds a custom column named "Country name" using the "AddColumn" function. The values in this column are determined by checking if the "Country" column is null, and if so, assigning the value "USA". Otherwise, the value from the "Country" column is used. 

The third transformation removes the original "Country" column using the "RemoveColumns" function. 

The fourth transformation changes the data types of some columns using the "TransformColumnTypes" function. Specifically, the "Country name" column is changed to type text, the "Amount" and "Product ID" columns are changed to type Int64, and the "Postalcode" and "Revenue" columns are changed to type text and number, respectively. 

Finally, the transformed table is returned using the "in" keyword.

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


This M code defines a binary parameter named "Sample File" which is used in a Power Query or Power BI report. 

- "IsParameterQuery=true" indicates that this is a parameter query that can be used to dynamically change the behavior of the report. 
- "BinaryIdentifier=#"Sample File"" is the identifier for the binary parameter, which is the name of the file being referenced. 
- "Type=Binary" specifies that the parameter is a binary type, meaning it will store binary data such as images or files. 
- "IsParameterQueryRequired=true" indicates that this parameter is required for the query to function properly.

```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```