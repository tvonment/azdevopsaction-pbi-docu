



# DAX

|Dataset|[posted worker (SP User Information List)](./../posted-worker-(SP-User-Information-List).md)|
| :--- | :--- |
|Workspace|[Global Mobility](../../Workspaces/Global-Mobility.md)|

## Table: RLS Measures

### Measures:


```dax
RLS Current User Mail = if(USERPRINCIPALNAME() = "florian.zrenner@org.rolandberger.com"
    //;"christian.boehler@rolandberger.com"
    //; "christian-simon.ernst@rolandberger.com"
    ,"matthias.ermer@rolandberger.com"

   // ;"tim.femmer@rolandberger.com"
    , USERPRINCIPALNAME() 
//"christian.weber@rolandberger.com" //"caroline.merk@rolandberger.com" //"florian.kalt@rolandberger.com" //"claudia.fischer-mayer@rolandberger.com" // ////  //////// // "christian.weber@rolandberger.com" //  // "florian.zrenner@org.rolandberger.com" // 
//change to test other user    
    )


```


## Table: Requests

### Measures:


```dax
Calendar Selection = 
if(max(Requests[TravelEnd])< min('Calendar'[Date]) || min(Requests[TravelStart]) < min('Calendar'[Date])
    , "not in filter"
    , "in filter") 
```


### Calculated Columns:


```dax
International = if(Requests[EmployeeCountry] <> Requests[Country], "international", "domestic")
```



```dax
Beginn = Format(Requests[TravelStart], "dd.MM.yyyy")
```



```dax
Ende = Format(if(format(Requests[TravelFinal],"ddmmyyyy")<>"",Requests[TravelFinal],Requests[TravelEnd]),"dd.MM.yyyy")
```


## Table: Calendar


```dax
CALENDARAUTO()
```


## Table: Employees

### Calculated Columns:


```dax
Firmen-Kz = "C" & Employees[Company id]
```



```dax
TripsNo = calculate(COUNTX(Requests,RELATED(Employees[Email])))
```



```dax
LastTripDate = format(calculate(MAXX(Requests,Requests[TravelStart])),"dd.mm.yyyy")
```

