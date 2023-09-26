



# DAX

|Dataset|[Personal Assistant Statistics](./../Personal-Assistant-Statistics.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: Assistants

### Measures:


```dax
FTE = if(isinscope(Assistants[Secretary ID]) && [#Gesamt] > 0, Max(Assistants[Secretary FTE]), blank())
```



```dax
P1 = 
var _txt = if(ISINSCOPE(Assistants[Secretary ID]), calculate(CONCATENATEX(values(AllData[Last]), AllData[Last], "/"), AllData[Function]="Partner 1"))
return if(_txt = "", blank(), _txt)
```



```dax
P2 = if(ISINSCOPE(Assistants[Secretary ID]), calculate(CONCATENATEX(values(AllData[Last]), AllData[Last], "/"), AllData[Function]="Partner 2"))
```



```dax
P3 = if(ISINSCOPE(Assistants[Secretary ID]), calculate(CONCATENATEX(values(AllData[Last]), AllData[Last], "/"), AllData[Function]="Partner 3"))
```



```dax
PRI = if(ISINSCOPE(Assistants[Secretary ID]), calculate(CONCATENATEX(values(AllData[Last]), AllData[Last], "/"), AllData[Function]="Principal"))
```



```dax
# PF PA = 
var _ass = values(Assistants[Secretary ID])
var _platforms =(calculate(COUNTROWS(distinct(AllData[platform_DACH_name])), all(AllData), _ass))

return 
if([#Gesamt]>0 && ISINSCOPE(Assistants[Secretary ID])
    , _platforms
    , blank())
```



```dax
FTE PF = if(ISINSCOPE(Assistants[Secretary ID]) || ISINSCOPE(AllData[assistant.platform_DACH_name])
        , sumx(Assistants, divide( [FTE] , [# PF PA], blank()))
        ,
        var _v = ADDCOLUMNS(CROSSJOIN(VALUES(Assistants[Secretary ID]), Values(AllData[platform_DACH_name]))
            , "@FTE", divide( [FTE] , [# PF PA], blank() )  )

        return sumx(_v, [@FTE])
    )
```



```dax
Ratio = 
if(ISINSCOPE(Assistants[Secretary ID])
    , divide( CALCULATE([#P], REMOVEFILTERS(AllData[platform_DACH_name])) , [FTE])
    , divide( [#P], [FTE PF])
)
```


### Calculated Columns:


```dax
Assistant = Assistants[Secretary Last Name] &", " & Assistants[Secretary First Name] & " - " & Assistants[Secretary ID]
```


## Table: AllData

### Measures:


```dax
#P1 = CALCULATE(COUNTROWS(values(AllData[ID])), AllData[Function] ="Partner 1")
```



```dax
#P2 = CALCULATE(COUNTROWS(values(AllData[ID])), AllData[Function] ="Partner 2")
```



```dax
#P3 = CALCULATE(COUNTROWS(values(AllData[ID])), AllData[Function] ="Partner 3")
```



```dax
#P = [#P1] +[#P2]+[#P3] 
```



```dax
#PRI = CALCULATE(COUNTROWS(values(AllData[ID])), AllData[Function] ="Principal")
```



```dax
#other = CALCULATE(COUNTROWS(values(AllData[ID])), not(AllData[Function] in {"Partner 1", "Partner 2", "Partner 3", "Principal"} ))
```



```dax
#Gesamt = CALCULATE(COUNTROWS(values(AllData[ID])))
```

