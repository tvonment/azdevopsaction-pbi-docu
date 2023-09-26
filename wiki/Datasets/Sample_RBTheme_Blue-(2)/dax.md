



# DAX

|Dataset|[Sample_RBTheme_Blue (2)](./../Sample_RBTheme_Blue-(2).md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: BU

### Measures:


```dax
Count of BU = COUNTA('BU'[BU])
```


### Calculated Columns:


```dax
Region = mid([RegionSeq], 3,15)
```


## Table: Date

### Measures:


```dax
Count of Date = COUNTA('Date'[Date])
```


### Calculated Columns:


```dax
MonthIncrementNumber = ([Year]-MIN([Year]))*12 +[MonthNumber]
```


## Table: Employee

### Measures:


```dax
EmpCount = CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])))
```



```dax
Seps = CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))
```



```dax
Actives = CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))
```



```dax
New Hires = SUM([isNewHire])
```



```dax
AVG Tenure Days = AVERAGE([TenureDays])
```



```dax
AVG Tenure Months = ROUND([AVG Tenure Days]/30, 1)-1
```



```dax
AVG Age = ROUND(AVERAGE([Age]), 0)
```



```dax
Sum of BadHires = SUM([BadHires])
```



```dax
New Hires SPLY = CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
Actives SPLY = CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
Seps SPLY = CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
EmpCount SPLY = CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])),SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
Seps YoY Var = [Seps]-[Seps SPLY]
```



```dax
Actives YoY Var = [Actives]-[Actives SPLY]
```



```dax
New Hires YoY Var = [New Hires]-[New Hires SPLY]
```



```dax
Seps YoY % Change = DIVIDE([Seps YoY Var], [Seps SPLY])
```



```dax
Actives YoY % Change = DIVIDE([Actives YoY Var], [Actives SPLY])
```



```dax
New Hires YoY % Change = DIVIDE([New Hires YoY Var], [New Hires SPLY])
```



```dax
Bad Hires SPLY = CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
Bad Hires YoY Var = [Sum of BadHires]-[Bad Hires SPLY]
```



```dax
Bad Hires YoY % Change = DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY])
```



```dax
TO % = DIVIDE([Seps], [Actives])
```



```dax
TO % Norm = CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnicity[Ethnicity]))
```



```dax
TO % Var = [TO %]-[TO % Norm]
```



```dax
Sep%ofActive = DIVIDE([Seps],[Actives])
```



```dax
Sep%ofSMLYActives = DIVIDE([Seps SPLY],[Actives SPLY])
```



```dax
BadHire%ofActives = DIVIDE([Sum of BadHires],[Actives])
```



```dax
BadHire%ofActiveSPLY = DIVIDE([Bad Hires SPLY],[Actives SPLY])
```



```dax
MIN Tenure Days = MIN([TenureDays])
```



```dax
MAX Tenure Days = Max([TenureDays])
```



```dax
Sum of Tenure Days = Sum([TenureDays])
```



```dax
Target Tenure Days = Max([TenureDays])/2
```


### Calculated Columns:


```dax
isNewHire = IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)
```



```dax
AgeGroupID = IF([Age]<30, 1, IF([Age]<50, 2, 3))
```



```dax
TenureDays = IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])
```



```dax
TenureMonths = CEILING([TenureDays]/30, 1) -1
```



```dax
BadHires = IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1)
```

