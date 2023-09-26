



# DAX

|Dataset|[20230801_Power BI Output_v03](./../20230801_Power-BI-Output_v03.md)|
| :--- | :--- |
|Workspace|[1,000 Assets](../../Workspaces/1,000-Assets.md)|

## Table: Asset

### Measures:


```dax
Energy generation TWh = SUM(Asset[Energy generation])/10^6
```



```dax
Capacity GW = SUM(Asset[Capacity])/10^3
```


### Calculated Columns:


```dax
Pictures = "https://s3-eu-west-1.amazonaws.com/blog-ecotree/blog/0001/01/ad46dbb447cd0e9a6aeecd64cc2bd332b0cbcb79.jpeg"
```

