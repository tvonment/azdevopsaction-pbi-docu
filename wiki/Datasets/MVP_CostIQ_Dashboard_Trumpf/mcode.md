



# M Code

|Dataset|[MVP_CostIQ_Dashboard_Trumpf](./../MVP_CostIQ_Dashboard_Trumpf.md)|
| :--- | :--- |
|Workspace|[Purchase Optimization](../../Workspaces/Purchase-Optimization.md)|

## Table: flat_table


```m
let
    Source = SharePoint.Files("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/", [ApiVersion = 15]),
    #"Sorted Rowss" = Table.Sort(Source,{{"Date modified", Order.Descending}}),
    Simulation_output = #"Sorted Rowss"{[Name="Simulation_output.xlsx",#"Folder Path"="https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/Shared Documents/General/12_Deliverables_Client/02_Trumpf/"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"Simulation_output"),
    flat_table_Sheet = #"Imported Excel Workbook"{[Item="flat_table",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(flat_table_Sheet, [PromoteAllScalars=true]),
    #"Removed Columns" = Table.RemoveColumns(#"Promoted Headers",{"Column1"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"commodity", type text}, {"contract", type text}, {"date",  type date}, {"demand_bought", type number}, {"demand_planned",type number}, {"enddate",  type date}, {"identifier", type text}, {"key", type text}, {"startdate",  type date}, {"strategy", type text}, {"unit", type text}, {"unit_cost_bought", type number}, {"unit_cost_planned", type number}, {"year",  Int64.Type}, {"unit_price_bought", type number}, {"unit_price_planned", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"unit", "currency_unit"}}),
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
    Source = SharePoint.Files("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/", [ApiVersion = 15]),
    #"Sorted Rows" = Table.Sort(Source,{{"Date modified", Order.Descending}}),
    Simulation_output = #"Sorted Rows"{[Name="Simulation_output.xlsx",#"Folder Path"="https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/Shared Documents/General/12_Deliverables_Client/02_Trumpf/"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"Simulation_output"),
    evaluation_table_Sheet = #"Imported Excel Workbook"{[Item="Evaluation",Kind="Sheet"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(evaluation_table_Sheet,{"Column1"}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Columns", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"strategy", type text}, 
    {"sum_of_demand_bought", Int64.Type}, {"sum_of_demand_planned", Int64.Type}, {"average_of_unit_price_bought", type number}, 
    {"average_of_unit_price_planned", type number}, {"sum_of_unit_cost_bought", type number}, 
    {"commodity", type text}, {"year", Int64.Type}, {"rel_delta_to_1/N_bought", type number}, {"abs_delta_to_1/N_bought", type number}, 
    {"rel_delta_to_Client_bought", type number}, {"abs_delta_to_Client_bought", type number}, 
  {"rel_delta_to_DDA-ML_bought", type number}, 
    {"abs_delta_to_DDA-ML_bought", type number}, {"rel_delta_to_Forecast based_bought", type number}, {"abs_delta_to_Forecast based_bought", type number}, 
    {"rel_delta_to_M1_bought", type number}, {"abs_delta_to_M1_bought", type number}, {"rel_delta_to_M2_bought", type number}, {"abs_delta_to_M2_bought", type number}, 
    {"rel_delta_to_M3_bought", type number}, {"abs_delta_to_M3_bought", type number}, {"rel_delta_to_M4_bought", type number}, {"abs_delta_to_M4_bought", type number}, 
    {"rel_delta_to_Perfect Foresight_bought", type number}, {"abs_delta_to_Perfect Foresight_bought", type number}, {"rel_delta_to_Reoptimization_bought", type number}, 
    {"abs_delta_to_Reoptimization_bought", type number}, {"rel_delta_to_Spot_bought", type number}, {"abs_delta_to_Spot_bought", type number}, {"rel_delta_to_Worst Case_bought", type number}, 
    {"abs_delta_to_Worst Case_bought", type number}, {"best_performing_strategy", type text}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Changed Type", "unit", "currency_unit"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Duplicated Column", "unit", Splitter.SplitTextByEachDelimiter({"/"}, QuoteStyle.Csv, true), {"currency", "unit"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"currency", type text}, {"unit", type text}}),
    Custom1 = #"Changed Type1",
    #"Sorted Rows1" = Table.Sort(Custom1,{{"rel_delta_to_Perfect Foresight_bought", Order.Descending}})
in
    #"Sorted Rows1"
```


## Table: Forward_Input_Values


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials", [Implementation="2.0", ViewMode="All"]),
    #"7cd63bdf-8510-45e6-98ed-f633b978a659" = Source{[Id="7cd63bdf-8510-45e6-98ed-f633b978a659"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"7cd63bdf-8510-45e6-98ed-f633b978a659",{"ID", "Content Type", "Modified", "Created", "Created By", "Modified By", "Version", "Attachments", "Edit", "Type", "Item Child Count", "Folder Child Count", "Label setting", "Retention label", "Retention label Applied", "Label applied by", "App Created By", "App Modified By", "Compliance Asset Id", "Item is a Record"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"Contract"}, Forecast_Input_Values, {"contract"}, "Forecast_Input_Values", JoinKind.LeftOuter),
    #"Expanded Forecast_Input_Values" = Table.ExpandTableColumn(#"Merged Queries", "Forecast_Input_Values", {"price_forecast"}, {"Forecast_Input_Values.price_forecast"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Forecast_Input_Values",{{"Forecast_Input_Values.price_forecast", "price_forecast_input"}})
in
    #"Renamed Columns"
```


## Table: feature_beta_input


```m
let
    Source = SharePoint.Files("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/", [ApiVersion = 15]),
    #"Sorted Rowss" = Table.Sort(Source,{{"Date modified", Order.Descending}}),
    Simulation_output = #"Sorted Rowss"{[Name="Simulation_output.xlsx",#"Folder Path"="https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/Shared Documents/General/12_Deliverables_Client/02_Trumpf/"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"Simulation_output"),
    feature_beta_input_Sheet = #"Imported Excel Workbook"{[Item="feature_beta_input_updated",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(feature_beta_input_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"beta", type text}, {"beta_value", type number}, {"contract", type text}, {"feature", type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"feature"}, Feature_Input_Values, {"feature"}, "Feature_Input_Values", JoinKind.LeftOuter),
    #"Expanded Feature_Input_Values" = Table.ExpandTableColumn(#"Merged Queries", "Feature_Input_Values", {"feature_value"}, {"Feature_Input_Values.feature_value"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Feature_Input_Values",{{"Feature_Input_Values.feature_value", "feature_value_input"}})
in
    #"Renamed Columns"
```


## Table: Feature_Input_Values


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials", [Implementation="2.0", ViewMode="Default"]),
    #"3c977e56-8eb2-48d7-a554-afd68ceda57f" = Source{[Id="3c977e56-8eb2-48d7-a554-afd68ceda57f"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"3c977e56-8eb2-48d7-a554-afd68ceda57f",{"ID"}),
    #"Demoted Headers" = Table.DemoteHeaders(#"Removed Columns"),
    #"Transposed Table" = Table.Transpose(#"Demoted Headers"),
    #"Renamed Columns" = Table.RenameColumns(#"Transposed Table",{{"Column1", "feature"}, {"Column2", "feature_value"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"feature_value", type number}})
in
    #"Changed Type"
```


## Table: Forecast_Input_Values


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials", [Implementation="2.0", ViewMode="Default"]),
    #"cb2c76af-43fd-459c-94c7-247ceba84ade" = Source{[Id="cb2c76af-43fd-459c-94c7-247ceba84ade"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"cb2c76af-43fd-459c-94c7-247ceba84ade",{"ID"}),
    #"Demoted Headers" = Table.DemoteHeaders(#"Removed Columns"),
    #"Changed Type" = Table.TransformColumnTypes(#"Demoted Headers",{{"Column1", type any}, {"Column2", type any}, {"Column3", type any}, {"Column4", type any}}),
    #"Transposed Table" = Table.Transpose(#"Changed Type"),
    #"Renamed Columns" = Table.RenameColumns(#"Transposed Table",{{"Column1", "contract"}, {"Column2", "price_forecast"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"price_forecast", type number}})
in
    #"Changed Type1"
```


## Table: Strategy_performance_evaluation


```m
let
    Source = SharePoint.Files("https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/", [ApiVersion = 15]),
    #"Sorted Rows" = Table.Sort(Source,{{"Date modified", Order.Descending}}),
    Simulation_output = #"Sorted Rows"{[Name="Simulation_output.xlsx",#"Folder Path"="https://rberger.sharepoint.com/sites/PurchasingOptimizationRawMaterials/Shared Documents/General/12_Deliverables_Client/02_Trumpf/"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"Simulation_output"),
    evaluation_table_Sheet = #"Imported Excel Workbook"{[Item="Evaluation",Kind="Sheet"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(evaluation_table_Sheet,{"Column1"}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Columns", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"strategy", type text}, 
    {"sum_of_demand_bought", Int64.Type}, {"sum_of_demand_planned", Int64.Type}, {"average_of_unit_price_bought", type number}, 
    {"average_of_unit_price_planned", type number}, {"sum_of_unit_cost_bought", type number}, 
    {"commodity", type text}, {"year", Int64.Type}, {"rel_delta_to_1/N_bought", type number}, {"abs_delta_to_1/N_bought", type number}, 
    {"rel_delta_to_Client_bought", type number}, {"abs_delta_to_Client_bought", type number}, 
  {"rel_delta_to_DDA-ML_bought", type number}, 
    {"abs_delta_to_DDA-ML_bought", type number}, {"rel_delta_to_Forecast based_bought", type number}, {"abs_delta_to_Forecast based_bought", type number}, 
    {"rel_delta_to_M1_bought", type number}, {"abs_delta_to_M1_bought", type number}, {"rel_delta_to_M2_bought", type number}, {"abs_delta_to_M2_bought", type number}, 
    {"rel_delta_to_M3_bought", type number}, {"abs_delta_to_M3_bought", type number}, {"rel_delta_to_M4_bought", type number}, {"abs_delta_to_M4_bought", type number}, 
    {"rel_delta_to_Perfect Foresight_bought", type number}, {"abs_delta_to_Perfect Foresight_bought", type number}, {"rel_delta_to_Reoptimization_bought", type number}, 
    {"abs_delta_to_Reoptimization_bought", type number}, {"rel_delta_to_Spot_bought", type number}, {"abs_delta_to_Spot_bought", type number}, {"rel_delta_to_Worst Case_bought", type number}, 
    {"abs_delta_to_Worst Case_bought", type number}, {"best_performing_strategy", type text}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Changed Type", "unit", "currency_unit"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Duplicated Column", "unit", Splitter.SplitTextByEachDelimiter({"/"}, QuoteStyle.Csv, true), {"currency", "unit"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"currency", type text}, {"unit", type text}}),
    Custom1 = #"Changed Type1",
    #"Sorted Rows1" = Table.Sort(Custom1,{{"rel_delta_to_Perfect Foresight_bought", Order.Descending}}),
    #"Filtered Rows" = Table.SelectRows(#"Sorted Rows1", each ([strategy] <> "Perfect Foresight")),
    #"Grouped Rows" = Table.Group(#"Filtered Rows", {"commodity", "strategy"}, {{"average_delta_to_perfect_foresight", each List.Average([rel_delta_to_Perfect Foresight_bought]), type nullable number}}),
    #"Sorted Rows2" = Table.Sort(#"Grouped Rows",{{"average_delta_to_perfect_foresight", Order.Descending}})
in
    #"Sorted Rows2"
```

