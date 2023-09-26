



# M Code

|Dataset|[Power BI](./../Power-BI.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Sheet1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M800192\Roland Berger Holding GmbH\APS Team - Documents\General\3 Product Catalog\36 Cybersecurity\80 Assessment Tool\Cyber Security Assessment(1-1).xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"ID", Int64.Type}, {"Start time", type datetime}, {"Completion time", type datetime}, {"Email", type text}, {"Name", type any}, {"Last modified time", type any}, {"Please enter your name!", type text}, {"Please enter your organisation!", type text}, {"Please select your position within the company!", type text}, {"The cyber security strategy is…", type any}, {"At what intervals is the cyber security strategy reviewed?#(lf)", type any}, {"How does the organization evaluates the information security performance and the effectiveness of the information management system?", type any}, {"On a scale of 1 (not at all) to 5 (extremely), to what extent are personnel cyber security requirements (prior to employment, during employment and after termination/separation) defined, documente...", type any}, {"What do the personnel cyber security requirements prior to employment include?", type any}, {"On a scale of 1 (not at all) to 5 (extremely), to what extent are security measures implemented when personnel are working remotely to protect information accessed, processed or stored outside the...", type any}, {"At what intervals are personnel cyber security requirements reviewed?#(lf)", type any}})
in
    #"Changed Type"
```

