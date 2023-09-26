



# DAX

|Dataset|[RAR](./../RAR.md)|
| :--- | :--- |
|Workspace|[Regional Attractivator](../../Workspaces/Regional-Attractivator.md)|

## Table: Analysis

### Measures:


```dax
Cluster1 = CALCULATE(
    sumx(Analysis, 
    'Avg. wage/hour score weight'[Avg. wage/hour score weight-Wert] * Analysis[Average wage per hour score] 
    + 'Avg wage/hour in manuf. score weight'[Avg wage/hour in manuf. score weight Value] * Analysis[Average wage per hour (USD) in manufacturing score]
    + 'Min. wage/hour score'[Min. wage/hour score Value] * Analysis[Minimum wage per hour (USD) score]
    ))
```



```dax
Cluster1_filter = 
VAR minValue = MIN(Analysis_Cluster1_values[Cluster1])
VAR maxValue = MAX(Analysis_Cluster1_values[Cluster1])
VAR cluster1_in_range = IF(AND([Cluster1]>=minValue,[Cluster1]<=maxValue),1,0)
return
cluster1_in_range
```


## Table: Avg. wage/hour score weight


```dax
GENERATESERIES(0, 1, 0.01)
```


### Measures:


```dax
Avg. wage/hour score weight-Wert = SELECTEDVALUE('Avg. wage/hour score weight'[Avg. wage/hour score weight], 0.33)
```


## Table: Avg wage/hour in manuf. score weight


```dax
GENERATESERIES(0, 1, 0.01)
```


### Measures:


```dax
Avg wage/hour in manuf. score weight Value = SELECTEDVALUE('Avg wage/hour in manuf. score weight'[Avg wage/hour in manuf. score weight], 0.33)
```


## Table: Min. wage/hour score


```dax
GENERATESERIES(0, 1, 0.01)
```


### Measures:


```dax
Min. wage/hour score Value = SELECTEDVALUE('Min. wage/hour score'[Min. wage/hour score], 0.33)
```


## Table: Analysis_Cluster1_values


```dax

var x1 = SUMMARIZE('Analysis',Analysis[Country name],"Cluster1",[Cluster1])

return

SUMMARIZE(x1,[Cluster1])
```

