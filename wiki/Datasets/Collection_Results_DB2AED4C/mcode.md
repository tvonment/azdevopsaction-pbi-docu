



# M Code

|Dataset|[Collection_Results_DB2AED4C](./../Collection_Results_DB2AED4C.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Collection_Results_DB2AED4C_289_Page_1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712709\Downloads\Collection_Results_DB2AED4C_289_Page_1.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"rank", Int64.Type}, {"position", Int64.Type}, {"title", type text}, {"asin", type text}, {"link", type text}, {"image", type text}, {"rating", type number}, {"ratings_total", Int64.Type}, {"price", type number}, {"current_category", type text}, {"parent_category", type text}, {"amazon_domain", type text}})
in
    #"Changed Type"
```


## Table: Collection_Results_DB2AED4C_290_Page_1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712709\Downloads\Collection_Results_DB2AED4C_290_Page_1.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"rank", Int64.Type}, {"position", Int64.Type}, {"title", type text}, {"asin", type text}, {"link", type text}, {"image", type text}, {"rating", type number}, {"ratings_total", Int64.Type}, {"price", type number}, {"current_category", type text}, {"parent_category", type text}, {"amazon_domain", type text}, {"variant", type text}, {"price_lower", type any}, {"price_upper", type any}, {"sub_title", type any}})
in
    #"Changed Type"
```


## Table: Collection_Results_DB2AED4C_291_Page_1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712709\Downloads\Collection_Results_DB2AED4C_291_Page_1.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"rank", Int64.Type}, {"position", Int64.Type}, {"title", type text}, {"asin", type text}, {"link", type text}, {"image", type text}, {"rating", type number}, {"ratings_total", Int64.Type}, {"price", type number}, {"current_category", type text}, {"parent_category", type text}, {"amazon_domain", type text}, {"variant", type text}, {"sub_title", type any}, {"price_lower", type any}, {"price_upper", type any}})
in
    #"Changed Type"
```


## Table: Collection_Results_DB2AED4C_292_Page_1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712709\Downloads\Collection_Results_DB2AED4C_292_Page_1.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"rank", Int64.Type}, {"position", Int64.Type}, {"title", type text}, {"asin", type text}, {"link", type text}, {"image", type text}, {"rating", type number}, {"ratings_total", Int64.Type}, {"price", type number}, {"current_category", type text}, {"parent_category", type text}, {"amazon_domain", type text}, {"variant", type any}, {"sub_title", type any}, {"price_lower", type any}, {"price_upper", type any}})
in
    #"Changed Type"
```


## Table: Sheet1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712709\Downloads\Collection_Results_DB2AED4C.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"rank", Int64.Type}, {"position", Int64.Type}, {"title", type text}, {"asin", type text}, {"link", type text}, {"image", type text}, {"rating", type number}, {"ratings_total", Int64.Type}, {"price", type number}, {"current_category", type text}, {"parent_category", type text}, {"amazon_domain", type text}, {"day", Int64.Type}})
in
    #"Changed Type"
```

