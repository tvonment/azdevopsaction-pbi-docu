



# DAX

|Dataset|[posted worker inkl archive](./../posted-worker-inkl-archive.md)|
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



```dax
EntryCount = COUNTROWS(Requests)
```



```dax
Entry date = LOOKUPVALUE(Employees[Entry date],Employees[Email], SELECTEDVALUE(Requests[Email]))
```



```dax
Firmen-Kz = LOOKUPVALUE(Employees[Firmen-Kz], Employees[Email], SELECTEDVALUE(Requests[Email]))
```



```dax
Personalnummer = LOOKUPVALUE(Employees[emp_id], Employees[Email], SELECTEDVALUE(Requests[Email]))
```



```dax
Mitgliedsstaat/Flaggenstaat = LOOKUPVALUE(CountryInfo[Mitgliedsstaat/Flaggenstaat], CountryInfo[Title], SELECTEDVALUE(Requests[Country]))
```


### Calculated Columns:


```dax
International = if(Requests[EmployeeCountry] <> Requests[Country], "international", "domestic")
```



```dax
Beginn = [TravelStart] //Format(Requests[TravelStart], "dd.MM.yyyy")
```



```dax
Ende = //Format(
    if(format(Requests[TravelFinal],"ddmmyyyy")<>"",Requests[TravelFinal],Requests[TravelEnd])
    //,"dd.MM.yyyy"))
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


## Table: FixedExportData

### Measures:


```dax
Wirtschaftssektor = 15
```



```dax
Rechtsform = 1
```



```dax
Tätigkeit = 71324
```



```dax
fix_N = "N"
```



```dax
Umsatzanteil >25% in D = "J"
```



```dax
fix_2 = 2
```



```dax
Empty = blank() 
```



```dax
Personal >25% in D = "J"
```



```dax
Strasse = [Empty]
```



```dax
Hausnummer = [Empty]
```



```dax
Adresszusatz = [Empty] 
```



```dax
Postleitzahl = [Empty]
```



```dax
Ort = [Empty]
```



```dax
Land = [Empty]
```



```dax
Mitgliedsnummer bei Zuständigkeit ABV = [Empty]
```



```dax
Geltung = "J"
```



```dax
EG-Anspruch = "J"
```



```dax
Anwerbung = "J"
```



```dax
Arbeitsvertrag = "J"
```



```dax
Entlassung = "J"
```



```dax
Aufgaben = "J"
```



```dax
Beschäftigungsstelle = 2
```



```dax
Name2 = [Empty]
```



```dax
Strasse2 = [Empty]
```



```dax
Haus-nummer2 = [Empty]
```



```dax
Adress-zusatz = [Empty]
```



```dax
PLZ2 = [Empty]
```



```dax
Ort2 = [Empty]
```



```dax
Name3 = [Empty]
```



```dax
Strasse3 = [Empty]
```



```dax
Haus-nummer3 = [Empty]
```



```dax
Adress-zusatz3 = [Empty]
```



```dax
PLZ3 = [Empty]
```



```dax
Ort3 = [Empty]
```

