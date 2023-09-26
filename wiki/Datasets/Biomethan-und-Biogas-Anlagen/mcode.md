



# M Code

|Dataset|[Biomethan und Biogas Anlagen](./../Biomethan-und-Biogas-Anlagen.md)|
| :--- | :--- |
|Workspace|[Biomethan-Anlagenregister](../../Workspaces/Biomethan-Anlagenregister.md)|

## Table: Biogas Anlagen by PLZ


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M711492\OneDrive - Roland Berger Holding GmbH\development\Biomethan-Anlagenregister\Biomethan und Biogas Anlagen.xlsx"), null, true),
    #"Biogas Anlagen by PLZ_Sheet" = Source{[Item="Biogas Anlagen by PLZ",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Biogas Anlagen by PLZ_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"postcode", type text}, {"Insg. installierte #(lf)Kapazität [kW]", type number}, {"Inst. Kapazität seit #(lf)2018 [kW]", Int64.Type}})
in
    #"Changed Type"
```


## Table: Biomethan Anlagen by PLZ


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M711492\OneDrive - Roland Berger Holding GmbH\development\Biomethan-Anlagenregister\Biomethan und Biogas Anlagen.xlsx"), null, true),
    #"Biomethan Anlagen by PLZ_Sheet" = Source{[Item="Biomethan Anlagen by PLZ",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Biomethan Anlagen by PLZ_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"postcode", type text}, {"Insg. inst. Kapazität [kW]", type number}, {"Inst. Kapazität seit #(lf)2018 [kW]", type number}})
in
    #"Changed Type"
```

