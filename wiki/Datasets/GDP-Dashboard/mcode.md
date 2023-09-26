



# M Code

|Dataset|[GDP Dashboard](./../GDP-Dashboard.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Abfrage1


```m
let
    Quelle = AzureStorage.Blobs("https://intstoragesawprod.blob.core.windows.net/datalake"),
    #"Sortierte Zeilen" = Table.Sort(Quelle,{{"Name", Order.Descending}}),
    #"Beibehaltener Zeilenbereich" = Table.Range(#"Sortierte Zeilen",158,1),
    #"https://intstoragesawprod blob core windows net/datalake_3_product_layer/01_GDP_DASHBOARD/OECD_Annual/part-00000-tid-906132688243242540-70f04f73-e067-4aa9-8295-97127cda6274-56-1 c000 snappy parquet" = #"Beibehaltener Zeilenbereich"{[#"Folder Path"="https://intstoragesawprod.blob.core.windows.net/datalake",Name="3_product_layer/01_GDP_DASHBOARD/OECD_Annual/part-00000-tid-906132688243242540-70f04f73-e067-4aa9-8295-97127cda6274-56-1.c000.snappy.parquet"]}[Content],
    #"Importierte Parquet-Daten" = Parquet.Document(#"https://intstoragesawprod blob core windows net/datalake_3_product_layer/01_GDP_DASHBOARD/OECD_Annual/part-00000-tid-906132688243242540-70f04f73-e067-4aa9-8295-97127cda6274-56-1 c000 snappy parquet")
in
    #"Importierte Parquet-Daten"
```

