



# M Code

|Dataset|[Agile Cloud Migration](./../Agile-Cloud-Migration.md)|
| :--- | :--- |
|Workspace|[IT_Agile_Cloud_Migration](../../Workspaces/IT_Agile_Cloud_Migration.md)|

## Table: All epics


```m
let
    Quelle = VSTS.AnalyticsViews("RolandBerger-IT", "Agile Cloud Migration", []),
    #"6a6c76ab-4273-43ed-86a7-e9c0e3a03f03_Table" = Quelle{[Id="6a6c76ab-4273-43ed-86a7-e9c0e3a03f03",Kind="Table"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(#"6a6c76ab-4273-43ed-86a7-e9c0e3a03f03_Table",{{"Assignee short version", "Resp."}, {"Title short version", "Project/product"}})
in
    #"Renamed Columns"
```


## Table: All features


```m
let
    Quelle = VSTS.AnalyticsViews("RolandBerger-IT", "Agile Cloud Migration", []),
    #"783f6e7e-ee30-4153-88d2-166069dc8f58_Table" = Quelle{[Id="783f6e7e-ee30-4153-88d2-166069dc8f58",Kind="Table"]}[Data]
in
    #"783f6e7e-ee30-4153-88d2-166069dc8f58_Table"
```


## Table: All user stories


```m
let
    Quelle = VSTS.AnalyticsViews("RolandBerger-IT", "Agile Cloud Migration", []),
    #"bf46cf4c-ac97-4f18-96a9-39c3e39b3b27_Table" = Quelle{[Id="bf46cf4c-ac97-4f18-96a9-39c3e39b3b27",Kind="Table"]}[Data]
in
    #"bf46cf4c-ac97-4f18-96a9-39c3e39b3b27_Table"
```

