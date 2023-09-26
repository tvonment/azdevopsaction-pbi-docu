



# M Code

|Dataset|[IBCSBubbleChart.performanceBubbleChartFBAAA829CB604E5CAB4F21729F233294.1.0.0.0](./../IBCSBubbleChart.performanceBubbleChartFBAAA829CB604E5CAB4F21729F233294.1.0.0.0.md)|
| :--- | :--- |
|Workspace|[BR_Test_Client_Access_Premium](../../Workspaces/BR_Test_Client_Access_Premium.md)|

## Table: Orders


```m
let
    Source = Excel.Workbook(File.Contents("E:\visual\DS\Superstores.xlsx"), null, true),
    Orders_Sheet = Source{[Item="Orders",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Orders_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Row ID", Int64.Type}, {"Order ID", type text}, {"Order Date", type date}, {"Ship Date", type date}, {"Ship Mode", type text}, {"Customer ID", type text}, {"Customer Name", type text}, {"Segment", type text}, {"Country", type text}, {"City", type text}, {"State", type text}, {"Postal Code", Int64.Type}, {"Region", type text}, {"Product ID", type text}, {"Category", type text}, {"Sub-Category", type text}, {"Product Name", type text}, {"Sales", type number}, {"Quantity", Int64.Type}, {"Discount", type number}, {"Profit", type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Region] = "Central" or [Region] = "East"))
in
    #"Filtered Rows"
```


## Table: Returns


```m
let
    Source = Excel.Workbook(File.Contents("E:\visual\DS\Superstores.xlsx"), null, true),
    Returns_Sheet = Source{[Item="Returns",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Returns_Sheet,{{"Column1", type text}, {"Column2", type text}})
in
    #"Changed Type"
```


## Table: People


```m
let
    Source = Excel.Workbook(File.Contents("E:\visual\DS\Superstores.xlsx"), null, true),
    People_Sheet = Source{[Item="People",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(People_Sheet,{{"Column1", type text}, {"Column2", type text}})
in
    #"Changed Type"
```

