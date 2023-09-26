



# DAX

|Dataset|[CV reporting_Shah](./../CV-reporting_Shah.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: CV LCM

### Measures:


```dax
Percentage CV availability = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	VALUES('Employees by Platform'[Employees by platform])
)
```



```dax
Percentage CV availability by country = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	VALUES('Employees by country'[Employees (country)])
)
```



```dax
Count of CV availability % difference from Count of CV up-to-dateness = 
VAR __BASELINE_VALUE = COUNTA('CV LCM'[CV up-to-dateness])
VAR __VALUE_TO_COMPARE = COUNTA('CV LCM'[CV availability])
RETURN
	IF(
		NOT ISBLANK(__VALUE_TO_COMPARE),
		DIVIDE(__BASELINE_VALUE,__VALUE_TO_COMPARE)
	)
```



```dax
Average = 
DIVIDE(
	COUNTA('CV LCM'[CV availability]),
	SUM('Employees by Platform'[Employees by platform])
)
```


### Calculated Columns:


```dax
CV up-to-dateness = IF(DATEDIFF('CV LCM'[Publication date].[Date], TODAY(), DAY) >= 365, "Old", "Recent")
```

