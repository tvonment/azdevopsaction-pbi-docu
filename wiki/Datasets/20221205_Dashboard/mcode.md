



# M Code

|Dataset|[20221205_Dashboard](./../20221205_Dashboard.md)|
| :--- | :--- |
|Workspace|[Purchase Optimization](../../Workspaces/Purchase-Optimization.md)|

## Table: flat_table


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M713820\Purchase Optimization\dummy_data\final_dummy_data.xlsx"), null, true),
    flat_table_Sheet = Source{[Item="flat_table",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(flat_table_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"commodity", type text}, {"contract", type text}, {"date", Int64.Type}, {"demand_bought", Int64.Type}, {"demand_planned", Int64.Type}, {"enddate", Int64.Type}, {"identifier", type text}, {"key", type text}, {"number_of_months", Int64.Type}, {"startdate", Int64.Type}, {"strategy", type text}, {"total_costs_acc_bought", type number}, {"unit", type text}, {"unit_cost_bought", type number}, {"unit_cost_planned", type number}, {"year", Int64.Type}, {"unit_price_bought", type number}, {"unit_price_planned", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Columns",{{"date", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"unit", "currency_unit"}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Renamed Columns", "currency_unit", "currency_unit - Copy"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Duplicated Column", "currency_unit - Copy", Splitter.SplitTextByEachDelimiter({"/"}, QuoteStyle.Csv, true), {"currency_unit - Copy.1", "currency_unit - Copy.2"}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"currency_unit - Copy.1", type text}, {"currency_unit - Copy.2", type text}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type2",{{"currency_unit - Copy.1", "currency"}, {"currency_unit - Copy.2", "unit"}})
in
    #"Renamed Columns1"
```


## Table: Evaluation


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M713820\Purchase Optimization\dummy_data\final_dummy_data.xlsx"), null, true),
    evaluation_table_Sheet = Source{[Item="evaluation_table",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(evaluation_table_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"strategy", type text}, 
    {"sum_of_demand_bought", Int64.Type}, {"sum_of_demand_planned", Int64.Type}, {"average_of_unit_price_bought", type number}, 
    {"average_of_unit_price_planned", type number}, {"sum_of_unit_cost_bought", type number}, 
    {"commodity", type text}, {"year", type text}, {"rel_delta_to_1/N_bought", type number}, {"abs_delta_to_1/N_bought", type number}, {"rel_delta_to_Client_bought", type number}, {"abs_delta_to_Client_bought", type number}, {"rel_delta_to_DDA-ML_bought", type number}, {"abs_delta_to_DDA-ML_bought", type number}, {"rel_delta_to_Forecast based_bought", type number}, {"abs_delta_to_Forecast based_bought", type number}, {"rel_delta_to_M1_bought", type number}, {"abs_delta_to_M1_bought", type number}, {"rel_delta_to_M2_bought", type number}, {"abs_delta_to_M2_bought", type number}, {"rel_delta_to_M3_bought", type number}, {"abs_delta_to_M3_bought", type number}, {"rel_delta_to_M4_bought", type number}, {"abs_delta_to_M4_bought", type number}, {"rel_delta_to_Perfect Foresight_bought", type number}, {"abs_delta_to_Perfect Foresight_bought", type number}, {"rel_delta_to_Reoptimization_bought", type number}, {"abs_delta_to_Reoptimization_bought", type number}, {"rel_delta_to_Spot_bought", type number}, {"abs_delta_to_Spot_bought", type number}, {"rel_delta_to_Worst Case_bought", type number}, {"abs_delta_to_Worst Case_bought", type number}, {"best_performing_strategy", type text}, {"rank", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Removed Columns", "currency_unit", "currency_unit - Copy"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Duplicated Column", "currency_unit - Copy", Splitter.SplitTextByEachDelimiter({"/"}, QuoteStyle.Csv, true), {"currency_unit - Copy.1", "currency_unit - Copy.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"currency_unit - Copy.1", type text}, {"currency_unit - Copy.2", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"currency_unit - Copy.1", "currency"}, {"currency_unit - Copy.2", "unit"}})
in
    #"Renamed Columns"
```

