



# M Code

|Dataset|[20230125_iowa_housing](./../20230125_iowa_housing.md)|
| :--- | :--- |
|Workspace|[GA](../../Workspaces/GA.md)|

## Table: iowa_houses csv


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714213\OneDrive - Roland Berger Holding GmbH\Admin\KickOff\DataAnalytics\ProjectWork\iowa_houses.xlsx"), null, true),
    iowa_houses.csv_Sheet = Source{[Item="iowa_houses.csv",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(iowa_houses.csv_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Neighborhood", type text}, {"LotArea", Int64.Type}, {"MSZoning", type text}, {"HouseStyle", type text}, {"LotFrontage", type any}, {"OverallQual", Int64.Type}, {"OverallCond", Int64.Type}, {"YearBuilt", Int64.Type}, {"YearRemodAdd", Int64.Type}, {"TotalBsmtSF", Int64.Type}, {"1stFlrSF", Int64.Type}, {"2ndFlrSF", Int64.Type}, {"LowQualFinSF", Int64.Type}, {"GrLivArea", Int64.Type}, {"FullBath", Int64.Type}, {"HalfBath", Int64.Type}, {"BedroomAbvGr", Int64.Type}, {"KitchenAbvGr", Int64.Type}, {"TotRmsAbvGrd", Int64.Type}, {"Fireplaces", Int64.Type}, {"GarageYrBlt", type any}, {"GarageCars", Int64.Type}, {"GarageArea", Int64.Type}, {"WoodDeckSF", Int64.Type}, {"OpenPorchSF", Int64.Type}, {"EnclosedPorch", Int64.Type}, {"SalePrice", Int64.Type}})
in
    #"Changed Type"
```

