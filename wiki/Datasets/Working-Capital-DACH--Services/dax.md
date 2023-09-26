



# DAX

|Dataset|[Working Capital DACH- Services](./../Working-Capital-DACH--Services.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: MeasureTable

### Measures:


```dax
Provision Gauge = [Theoretical Bad Debt]*1.25
```



```dax
Theoretical Bad Debt general = sum(AR[Basis general bad debt]) * 0.025
```



```dax
Theoretical Bad Debt = sum(AR[Provision Amount]) + [Theoretical Bad Debt general]
```



```dax
Theoretical Bad Debt individual = sum(AR[Provision Amount])
```



```dax
Total WC items = sum(AR[OPEN_AMOUNT]) + sum(WIP[OPEN_WIP])
```



```dax
Weighted avg Age AR = sum(AR[Weighted Age]) / sum(AR[OPEN_AMOUNT])
```



```dax
WAVG overdue Age WIP = if (sum(WIP[Overdue Open WIP]) <> 0, CALCULATE(sum(WIP[WAVG overdue Age WIP]) / sum(WIP[Overdue Open WIP])),BLANK())
```



```dax
Weighted avg Age WC = ([Weighted avg Age AR] * sum(AR[OPEN_AMOUNT]) + [WAVG overdue Age WIP] * sum(WIP[OPEN_WIP]) )/ (sum(WIP[OPEN_WIP])+sum(AR[OPEN_AMOUNT]))
```



```dax
Delta Date = datediff(maxx(RollingCalender,RollingCalender[Date]),minx(RollingCalender,RollingCalender[Date]),DAY)
```



```dax
Min = minx(RollingCalender,RollingCalender[Date])
```



```dax
WAVG overdue Age WC = If( (sum(WIP[Overdue Open WIP])+sum(AR[Overdue Open Amount])) <> 0,  
CALCULATE( ([WAVG overdue Age AR] * sum(AR[Overdue Open Amount]) + [WAVG overdue Age WIP] * sum(WIP[Overdue Open WIP]) )/ (sum(WIP[Overdue Open WIP])+sum(AR[Overdue Open Amount]))),BLANK())
```



```dax
WAVG overdue Age AR = if (sum(AR[Overdue Open Amount]) <> 0, CALCULATE(sum(AR[Weighted OverdueAge]) / sum(AR[Overdue Open Amount])), BLANK())
```



```dax
Weighted avg Age WIP = (sum(WIP[Weighted Age]) / sum(WIP[OPEN_WIP]))
```


## Table: WIP

### Calculated Columns:


```dax
Weighted Age = WIP[AGE_OF_WIP] * WIP[OPEN_WIP]
```



```dax
WAVG overdue Age WIP = WIP[Overdue Open WIP]*WIP[Overdue WIP Age]
```


## Table: AR

### Calculated Columns:


```dax
Provision % = if(AR[INVOICE_AGE]<180,0.0,if(AR[INVOICE_AGE]<270,0.25,if(AR[INVOICE_AGE]<360,0.5,1)))
```



```dax
Provision Amount = AR[Provision %] * AR[OPEN_AMOUNT]
```



```dax
Basis general bad debt = if(AR[INVOICE_AGE]<180,AR[OPEN_AMOUNT],0)
```



```dax
Weighted Age = AR[OPEN_AMOUNT] * AR[INVOICE_AGE]
```



```dax
Weighted OverdueAge = AR[Overdue Open Amount] * AR[DAYS_OVERDUE]
```

