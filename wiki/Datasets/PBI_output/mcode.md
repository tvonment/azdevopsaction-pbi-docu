



# M Code

|Dataset|[PBI_output](./../PBI_output.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Average margins


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714026\Roland Berger Holding GmbH\Group 6 - General\02_output\Power BI input\ClienData_Complete_WorkingFile_v1.xlsx"), null, true),
    #"Average margins_Sheet" = Source{[Item="Average margins",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Average margins_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Product Category", type text}, {"Average Margin Range", type text}, {"Product Assortment (Own Judgement for graph) ", type number}, {"Total Sales (for Product Assortment Graph) ", type any}})
in
    #"Changed Type"
```


## Table: Transactions


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714026\Roland Berger Holding GmbH\Group 6 - General\02_output\Power BI input\ClienData_Complete_WorkingFile_v1.xlsx"), null, true),
    #"Merged doc date included_Sheet" = Source{[Item="Merged doc date included",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Merged doc date included_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"transaction_id", type text}, {"Transaction_day", type date}, {"Transaction_hour", type time}, {"hierarchy_id", Int64.Type}, {"hierarchy_name", type text}, {"customer_id", Int64.Type}, {"organic", type logical}, {"returnable", type logical}, {"private_label", type logical}, {"total_net_sales", type number}, {"cluster_label", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Subtransaction_id"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"hierarchy_id", type text}, {"total_net_sales", type number}, {"Subtransaction_id", type text}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type1",{{"Transaction_day", Order.Ascending}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Sorted Rows",{{"Transaction_day", type date}, {"Transaction_hour", type time}})
in
    #"Changed Type2"
```


## Table: DimDate


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714026\Roland Berger Holding GmbH\Group 6 - General\02_output\Power BI input\Date dimension.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Date relative", Int64.Type}})
in
    #"Changed Type"
```


## Table: DimCustomer


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714026\Roland Berger Holding GmbH\Group 6 - General\02_output\Power BI input\customer_info.xlsx"), null, true),
    customer_info_Sheet = Source{[Item="customer_info",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(customer_info_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"customer_id", type text}, {"total_net_sales", type number}, {"last_purchase_date", type date}, {"first_purchase_date", type date}, {"visit_count", Int64.Type}, {"days_since_last_purchase_from_today", Int64.Type}, {"avg_sales_per_day", Currency.Type}, {"days_since_last_purchases_recorded", Int64.Type}, {"active_days", Int64.Type}, {"Position", Int64.Type}, {"Top percentile", type number}, {"Value segmentation", type text}}),
    #"Inserted Literal" = Table.AddColumn(#"Changed Type", "Fixed value", each "15", type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Literal",{{"Fixed value", Int64.Type}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type1", {"customer_id"}, labeled_final_data, {"customer_id"}, "labeled_final_data", JoinKind.LeftOuter),
    #"Expanded labeled_final_data" = Table.ExpandTableColumn(#"Merged Queries", "labeled_final_data", {"Business segmentation", "Behavorial segmentation"}, {"Business segmentation", "Behavorial segmentation"})
in
    #"Expanded labeled_final_data"
```


## Table: labeled_final_data


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M714026\Roland Berger Holding GmbH\Group 6 - General\02_output\Power BI input\labeled_final_data.csv"),[Delimiter=";", Columns=17, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"", type text}, {"customer_id", type text}, {"customer_H1_label", type text}, {"Wine_Vault", Int64.Type}, {"convinience", Int64.Type}, {"Harvest_House", type text}, {"Cheese_Haven", Int64.Type}, {"organic", Int64.Type}, {"returnable", Int64.Type}, {"private_label", Int64.Type}, {"food", type text}, {"non-alcoholic", type text}, {"alcoholic", Int64.Type}, {"hygeine", type text}, {"pet product", type text}, {"baby product", type text}, {"label", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Wine_Vault", "convinience", "Harvest_House", "Cheese_Haven", "organic", "returnable", "private_label", "food", "non-alcoholic", "alcoholic", "hygeine", "pet product", "baby product"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"customer_H1_label", "Business segmentation"}, {"label", "Behavorial segmentation"}})
in
    #"Renamed Columns"
```

