



# DAX

|Dataset|[Power BI Release Plan](./../Power-BI-Release-Plan.md)|
| :--- | :--- |
|Workspace|[Power BI Release Plan](../../Workspaces/Power-BI-Release-Plan.md)|

## Table: Measurements

### Measures:


```dax
Total Features = COUNTROWS('Feature Dates')
```



```dax
Selected Description = 
IF ( [Total Features] = 1 , CONCATENATEX('Features', [Description]) )
```



```dax
Shipped = 
VAR shippedFlag = IF ( [Total Features] = 1 , CONCATENATEX('Feature Dates', [Status]) )
RETURN
IF ( shippedFlag = "Shipped", UNICHAR(10003), BLANK() )
```



```dax
URL Link = 
VAR year = VALUES('Features'[Year])
VAR webAddress = "https://learn.microsoft.com/power-platform"
VAR charCode = IF( year < 2023, "-", "/")
VAR fullURL = webAddress & charCode & "release-plan/"
VAR countOfRows =  COUNTROWS('Features')
RETURN
IF ( countOfRows <> 1, BLANK(), 
CONCATENATEX( Features ,  fullURL & [Year] & "wave" & [ReleaseWave] & "/" & [Product] & "/" & [Learn More] ) ) 
```

