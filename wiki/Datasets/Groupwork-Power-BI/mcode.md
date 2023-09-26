



# M Code

|Dataset|[Groupwork Power BI](./../Groupwork-Power-BI.md)|
| :--- | :--- |
|Workspace|[GA_march23](../../Workspaces/GA_march23.md)|

## Table: 0_raw data_iowa_houses


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712522\Downloads\2023-03-14_Project work_Team Excalarators.xlsx"), null, true),
    #"0_raw data_iowa_houses_Sheet" = Source{[Item="0_raw data_iowa_houses",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"0_raw data_iowa_houses_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Neighborhood", type text}, {"LotArea", Int64.Type}, {"MSZoning", type text}, {"HouseStyle", type text}, {"LotFrontage", Int64.Type}, {"OverallQual", Int64.Type}, {"OverallCond", Int64.Type}, {"YearBuilt", Int64.Type}, {"YearRemodAdd", Int64.Type}, {"TotalBsmtSF", Int64.Type}, {"1stFlrSF", Int64.Type}, {"2ndFlrSF", Int64.Type}, {"LowQualFinSF", Int64.Type}, {"GrLivArea", Int64.Type}, {"FullBath", Int64.Type}, {"HalfBath", Int64.Type}, {"BedroomAbvGr", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"TotRmsAbvGrd", Int64.Type}, {"Fireplaces", Int64.Type}, {"GarageYrBlt", Int64.Type}, {"GarageCars", Int64.Type}, {"GarageArea", Int64.Type}, {"WoodDeckSF", Int64.Type}, {"OpenPorchSF", Int64.Type}, {"EnclosedPorch", Int64.Type}, {"SalePrice", Int64.Type}, {"Price/SQM", type number}})
in
    #"Changed Type"
```


## Table: 0_1_raw data_selected variable2


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712522\Downloads\2023-03-14_Project work_Team Excalarators.xlsx"), null, true),
    #"0_1_raw data_selected variable2_Sheet" = Source{[Item="0_1_raw data_selected variable2",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"0_1_raw data_selected variable2_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"OverallQual", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"FullBath", Int64.Type}, {"GarageCars", Int64.Type}, {"Fireplaces", Int64.Type}, {"Price/SQM", type number}})
in
    #"Changed Type"
```


## Table: 0_1_raw data_selected variables


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712522\Downloads\2023-03-14_Project work_Team Excalarators.xlsx"), null, true),
    #"0_1_raw data_selected variables_Sheet" = Source{[Item="0_1_raw data_selected variables",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"0_1_raw data_selected variables_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Neighborhood", type text}, {"OverallQual", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"FullBath", Int64.Type}, {"GarageCars", Int64.Type}, {"WoodDeckSF", Int64.Type}, {"Price/SQM", type number}})
in
    #"Changed Type"
```


## Table: 0_raw data_iowa_houses (2)


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712522\Desktop\2023-03-14_Project work_Team Excalarators.xlsx"), null, true),
    #"0_raw data_iowa_houses_Sheet" = Source{[Item="0_raw data_iowa_houses",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"0_raw data_iowa_houses_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Neighborhood", type text}, {"LotArea", Int64.Type}, {"MSZoning", type text}, {"HouseStyle", type text}, {"LotFrontage", Int64.Type}, {"OverallQual", Int64.Type}, {"OverallCond", Int64.Type}, {"YearBuilt", Int64.Type}, {"YearRemodAdd", Int64.Type}, {"TotalBsmtSF", Int64.Type}, {"1stFlrSF", Int64.Type}, {"2ndFlrSF", Int64.Type}, {"LowQualFinSF", Int64.Type}, {"GrLivArea", Int64.Type}, {"FullBath", Int64.Type}, {"HalfBath", Int64.Type}, {"BedroomAbvGr", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"TotRmsAbvGrd", Int64.Type}, {"Fireplaces", Int64.Type}, {"GarageYrBlt", Int64.Type}, {"GarageCars", Int64.Type}, {"GarageArea", Int64.Type}, {"WoodDeckSF", Int64.Type}, {"OpenPorchSF", Int64.Type}, {"EnclosedPorch", Int64.Type}, {"SalePrice", Int64.Type}, {"Price/SQM", type number}})
in
    #"Changed Type"
```


## Table: 0_raw data_iowa_houses (3)


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712522\Desktop\2023-03-14_Project work_Team Excalarators.xlsx"), null, true),
    #"0_raw data_iowa_houses_Sheet" = Source{[Item="0_raw data_iowa_houses",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"0_raw data_iowa_houses_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Neighborhood", type text}, {"LotArea", Int64.Type}, {"MSZoning", type text}, {"HouseStyle", type text}, {"LotFrontage", Int64.Type}, {"OverallQual", Int64.Type}, {"OverallCond", Int64.Type}, {"YearBuilt", Int64.Type}, {"YearRemodAdd", Int64.Type}, {"TotalBsmtSF", Int64.Type}, {"1stFlrSF", Int64.Type}, {"2ndFlrSF", Int64.Type}, {"LowQualFinSF", Int64.Type}, {"GrLivArea", Int64.Type}, {"FullBath", Int64.Type}, {"HalfBath", Int64.Type}, {"BedroomAbvGr", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"TotRmsAbvGrd", Int64.Type}, {"Fireplaces", Int64.Type}, {"GarageYrBlt", Int64.Type}, {"GarageCars", Int64.Type}, {"GarageArea", Int64.Type}, {"WoodDeckSF", Int64.Type}, {"OpenPorchSF", Int64.Type}, {"EnclosedPorch", Int64.Type}, {"SalePrice", Int64.Type}, {"Price/SQM", type number}})
in
    #"Changed Type"
```


## Table: 0_1_raw data_selected variable


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712522\Desktop\2023-03-14_Project work_Team Excalarators.xlsx"), null, true),
    #"0_1_raw data_selected variable_Sheet" = Source{[Item="0_1_raw data_selected variable",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"0_1_raw data_selected variable_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"OverallQual", Int64.Type}, {"YearBuilt", Int64.Type}, {"HalfBath", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"GarageCars", Int64.Type}, {"Price/SQM", type number}})
in
    #"Changed Type"
```

