



# DAX

|Dataset|[CV reporting](./../CV-reporting.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: CV LCM

### Measures:


```dax
Count of CV availability divided by Count of Employees by platform = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	VALUES('Employees by Platform'[Employees by platform])
)*100
```



```dax
Count of CVs Count divided by Employees (country) = 
DIVIDE(
	COUNTA('CV LCM'[CVs Count]),
	VALUES('Employees by country'[Employees (country)])
)*100
```



```dax
Count of CV availability divided by Employees (country) = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	VALUES('Employees by country'[Employees (country)])
)*100
```



```dax
Count of CV availability divided by Count of Employees (country) = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	VALUES('Employees by country'[Employees (country)])
)*100
```



```dax
Count of CV availability divided by Count of Employees (country) 2 = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	COUNTA('Employees by country'[Employees (country)])
)
```



```dax
Count of CV availability divided by Employees (country) 2 = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	SUM('Employees by country'[Employees (country)])
)
```



```dax
Count of CV availability divided by Count of Employees (country) 3 = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	COUNTA('Employees by country'[Employees (country)])
)
```


### Calculated Columns:


```dax
CV up-to-dateness = IF(DATEDIFF('CV LCM'[Publication date].[Date], TODAY(), DAY) >= 365, "Old", "Recent")
```

