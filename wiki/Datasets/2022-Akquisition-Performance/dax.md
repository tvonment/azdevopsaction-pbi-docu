



# DAX

|Dataset|[2022 Akquisition Performance](./../2022-Akquisition-Performance.md)|
| :--- | :--- |
|Workspace|[Acquisition Performance](../../Workspaces/Acquisition-Performance.md)|

## Table: FactOrderIncomeByMonth

### Measures:


```dax
OrderIncome = if(sum(FactOrderIncomeByMonth[Order Income])<>0,sum(FactOrderIncomeByMonth[Order Income]) ,blank())
```


## Table: FactPaidByYear

### Measures:


```dax
Paid = Sum(FactPaidByYear[Paid Year])
```


## Table: FactInvoicedByYear

### Measures:


```dax
Invoiced = sum(FactInvoicedByYear[Invoiced Year] ) 
```


## Table: DimProjects

### Measures:


```dax
Multiple Contrib. = 
if(DISTINCTCOUNTNOBLANK(Contribution[ProjectNumber]) =1 && (ISINSCOPE  (DimProjects[project name with id]) || ISINSCOPE  (DimProjects[ProjectNumber]) || ISINSCOPE  (DimProjects[project_number])),
    calculate(sum(Contribution[Contribution]) / 100, filter(all(Contribution), Contribution[ProjectNumber] = min(DimProjects[ProjectNumber])),  DimEmployees[IsPartner]=1),
    blank()
)
```


### Calculated Columns:


```dax
project name with id = CONCATENATE( CONCATENATE(DimProjects[ProjectNumber], " "), DimProjects[Project])
```



```dax
Total Project Contribution = calculate(sum(Contribution[Contribution]) / 100, filter(all(Contribution), Contribution[ProjectNumber] = DimProjects[ProjectNumber]))
```


## Table: DimEmployees

### Calculated Columns:


```dax
RlsTestIsVisible = 
if( DimEmployees[email] == [CurrentUserMail], true()
    , if(LOOKUPVALUE('rls cc permission'[CCId], 'rls cc permission'[email], [CurrentUserMail], 'rls cc permission'[CCId], DimEmployees[cc_id], Blank())<> Blank()
        ,True()
        
        ,False()
    )
)
```



```dax
RLS TESt = 
var _UserPrincipalName = "markus.strietzel@rolandberger.com"

var employeeCountry = DimEmployees[country_code_iso3]
var employeeCc = DimEmployees[cc_id]

var combinations = CALCULATETABLE('rls cc permission', 'rls cc permission'[email] = _UserPrincipalName)

var ccAllAndCcAll =  CALCULATETABLE('rls cc permission', FILTER('rls cc permission', 'rls cc permission'[CCId] = "-9999" && 'rls cc permission'[country_code_iso3] = "ALL" ), combinations)
var ccSingleAndCcSingle =  CALCULATETABLE('rls cc permission', FILTER('rls cc permission', 'rls cc permission'[CCId] <> "-9999" && 'rls cc permission'[country_code_iso3] <> "ALL" ), combinations)
var ccAllAndCountrySingle =  CALCULATETABLE('rls cc permission', Filter('rls cc permission',  'rls cc permission'[CCId] = "-9999" && 'rls cc permission'[country_code_iso3] <> "ALL"), combinations)
var ccSingleAndCountryAll =  CALCULATETABLE('rls cc permission', Filter('rls cc permission',  'rls cc permission'[CCId] <> "-9999" && 'rls cc permission'[country_code_iso3] = "ALL"), combinations)


return switch(true(),
    //all
    COUNTROWS(ccAllAndCcAll) > 0, "Yes ALL",

    //own user
    DimEmployees[email] == _UserPrincipalName, "YES own"
  
	//permission for cc_id  
	, countrows(ccSingleAndCountryAll) > 0  && calculate(COUNTROWS('rls cc permission'), FILTER('rls cc permission', 'rls cc permission'[CCId] = employeeCc), ccSingleAndCountryAll) > 0, "YES ccSCAll"
    //permission for country  
    , countrows(ccAllAndCountrySingle) > 0 && calculate(COUNTROWS('rls cc permission'), ccAllAndCountrySingle, FILTER('rls cc permission', 'rls cc permission'[country_code_iso3] = employeeCountry)), "YESccACS"

    //additional employee		
	,Calculate(
				CountRows('rls direct emp permission')
							, Filter
								('rls direct emp permission',
								EARLIER(DimEmployees[emp_id]) = 'rls direct emp permission'[Additional EmpId] 
								&& _UserPrincipalName = 'rls direct emp permission'[User Email]
								)
					)>0
				, "YES direct"
)//
```



```dax
Column = var _UserPrincipalName = "eva.tippl@rolandberger.com"

var employeeCountry = DimEmployees[country_code_iso3]
var employeeCc = DimEmployees[cc_id]

var combinations = CALCULATETABLE('rls cc permission', 'rls cc permission'[email] = _UserPrincipalName)

var ccAllAndCcAll =  CALCULATETABLE('rls cc permission', FILTER('rls cc permission', 'rls cc permission'[CCId] = "-9999" && 'rls cc permission'[country_code_iso3] = "ALL" ), combinations)
var ccSingleAndCcSingle =  CALCULATETABLE('rls cc permission', FILTER('rls cc permission', 'rls cc permission'[CCId] <> "-9999" && 'rls cc permission'[country_code_iso3] <> "ALL" ), combinations)
var ccAllAndCountrySingle =  CALCULATETABLE('rls cc permission', Filter('rls cc permission',  'rls cc permission'[CCId] = "-9999" && 'rls cc permission'[country_code_iso3] <> "ALL"), combinations)
var ccSingleAndCountryAll =  CALCULATETABLE('rls cc permission', Filter('rls cc permission',  'rls cc permission'[CCId] <> "-9999" && 'rls cc permission'[country_code_iso3] = "ALL"), combinations)


return switch(true(),
    //all
    COUNTROWS(ccAllAndCcAll) > 0, "Yes ALL"

    //own user
    , DimEmployees[email] == _UserPrincipalName,  "YES own"
  
	//permission for cc_id  
	, countrows(ccSingleAndCountryAll) > 0  && calculate(COUNTROWS('rls cc permission'), FILTER('rls cc permission', 'rls cc permission'[CCId] = employeeCc), ccSingleAndCountryAll) > 0, "YES ccSCAll"
    //permission for country  
    , countrows(ccAllAndCountrySingle) > 0 && calculate(COUNTROWS('rls cc permission'), ccAllAndCountrySingle, FILTER('rls cc permission', 'rls cc permission'[country_code_iso3] = employeeCountry)), "YESccACS"

	 //permission for cc_id  and country
	, countrows(ccSingleAndCcSingle) > 0  && calculate(COUNTROWS('rls cc permission'), FILTER('rls cc permission', 'rls cc permission'[CCId] = employeeCc && 'rls cc permission'[country_code_iso3] = employeeCountry), ccSingleAndCcSingle) > 0, "YES cc and country"
	
    //additional employee		
	,Calculate(
				CountRows('rls direct emp permission')
							, Filter
								('rls direct emp permission',
								EARLIER(DimEmployees[emp_id]) = 'rls direct emp permission'[Additional EmpId] 
								&& _UserPrincipalName = 'rls direct emp permission'[User Email]
								)
					)>0
				,  "YES direct"
)
```


## Table: Key Measures

### Measures:


```dax
AP calc = [Paid] * AVERAGE('Contribution'[Contribution Percentage])
```



```dax
AP = CALCULATE(SUMX('Contribution', [AP calc]))
```



```dax
number of employees = DISTINCTCOUNT('Contribution'[EmployeeID])
```



```dax
OI Jan = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=1)
```



```dax
OI Feb = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=2)
```



```dax
OI Mar = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=3)
```



```dax
OI Apr = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=4)
```



```dax
OI May = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=5)
```



```dax
OI Jun = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=6)
```



```dax
OI Jul = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=7)
```



```dax
OI Aug = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=8)
```



```dax
OI Sep = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=9)
```



```dax
OI Oct = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=10)
```



```dax
OI Nov = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=11)
```



```dax
OI Dec = CALCULATE([OrderIncome], FactOrderIncomeByMonth[Month]=12)
```



```dax
Selected Employee = if(HASONEVALUE(DimEmployees[EmployeeID]), min(DimEmployees[Employee (Job)]), "please select single employee or drill through from overview")
```



```dax
dummy space = ""
```



```dax
AP int = CALCULATE(SUMX('Contribution', [AP calc]), 'Contribution'[Type]="International")
```



```dax
DisplayRecord = if("Active" in VALUES(Display[Type]) && SELECTEDVALUE(DimEmployees[ShowDefault ]) == TRUE()
    , 1
    ,if("All" in VALUES(Display[Type]) ==TRUE()
        ,1
        , 0)
)

```



```dax
Measure = USERPRINCIPALNAME()
```



```dax
OI _CC Jan = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=1)
```



```dax
OI _CC Feb = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=2)
```



```dax
OI _CC Mar = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=3)
```



```dax
OI _CC Apr = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=4)
```



```dax
OI _CC May = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=5)
```



```dax
OI _CC Jun = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=6)
```



```dax
OI _CC Jul = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=7)
```



```dax
OI _CC Aug = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=8)
```



```dax
OI _CC Sep = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=9)
```



```dax
OI _CC Oct = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=10)
```



```dax
OI _CC Nov = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=11)
```



```dax
OI _CC Dec = CALCULATE([OrderIncome CC], FactCC_OrderIncomeByMonth[Month]=12)
```



```dax
Target for emp = 8500
```



```dax
Target for emp to date = 
[Target for emp] / 12 *
CALCULATE(max(FactOrderIncomeByMonth[Month]), Filter(All(FactOrderIncomeByMonth), FactOrderIncomeByMonth[Order Income] > 0) )
```



```dax
Icon = SWITCH(true(), 
[Target for emp to date] > [AP], 0, 1) 
```



```dax
assigned to project cc = 
var curProject = min(DimProjectsForGlobalCCs[ProjectNumber])
return if(CONTAINS(CCContribution, CCContribution[ProjectNumber], curProject),1,0)
```



```dax
AP Emp CC = 
if(
    COUNTROWS(VALUES(CCContribution[EmployeeID])) = 1
    , [Paid CC] * [_Multiple Contrib.]
    , Blank())
```


## Table: DimCC

### Measures:


```dax
EmpCount = COUNTROWS(DimEmployees)
```


### Calculated Columns:


```dax
EmployeeCount = CALCULATE(COUNTROWS(DimEmployees))
```


## Table: rls cc permission

### Measures:


```dax
CurrentUserMail = "TEST RLS ONLY"//USERPRINCIPALNAME() 
//"matthias.rueckriegel@rolandberger.com" 
//"andreas.schwilling@rolandberger.com" 
//"cornelia.haenichen@rolandberger.com"
//"alfredo.arpaia@rolandberger.com"
//"maria.mikhaylenko@rolandberger.com"

//"artem.zakomirnyi@rolandberger.com"   //own user

//"per.breuer@rolandberger.com" // all cc
```


## Table: Contribution

### Calculated Columns:


```dax
Type = if(and(not isblank(RELATED(DimProjects[responsible_unit_cou_iso3])), RELATED(DimEmployees[country_code_iso3])<>RELATED(DimProjects[responsible_unit_cou_iso3])),"International","Domestic")
```



```dax
Contribution Percentage = Contribution[Contribution] / 100
```


## Table: DimProjectsForGlobalCCs

### Measures:


```dax
_Multiple Contrib. = 
IF(ISINSCOPE(CCContribution[Employee]), min(CCContribution[Contribution]) / 100,
    if(ISINSCOPE(DimProjectsForGlobalCCs[project name with id])
        , CALCULATE(Sum(CCContribution[Contribution]) / 100,Filter(all(CCContribution), CCContribution[ProjectNumber] = min(DimProjectsForGlobalCCs[ProjectNumber]) && CCContribution[IsPartner] = 1))
        , blank()
    )
) 
```


### Calculated Columns:


```dax
project name with id = CONCATENATE( CONCATENATE(DimProjectsForGlobalCCs[ProjectNumber], " "), DimProjectsForGlobalCCs[Project])
```



```dax
RLS Col = if(LOOKUPVALUE('global cc permission'[User Email],'global cc permission'[Global CC ID], -9999)<> Blank(),1,

if(LOOKUPVALUE('global cc permission'[User Email],'global cc permission'[Global CC ID], DimProjectsForGlobalCCs[function_id], 'global cc permission'[User Email], "patrick.biecheler@rolandberger.com")<> Blank()
    , 2
    , if(LOOKUPVALUE('global cc permission'[User Email],'global cc permission'[Global CC ID], DimProjectsForGlobalCCs[industry_id], 'global cc permission'[User Email], "patrick.biecheler@rolandberger.com")<> Blank()
        , 3
                //,if(LOOKUPVALUE('DimProjects'[project_number],'DimProjects'[project_number], DimProjectsForGlobalCCs[project_number])<> Blank(),4
        , 99
//)
    )
)

)
```


## Table: FactCC_OrderIncomeByMonth

### Measures:


```dax
OrderIncome CC = if(sum(FactCC_OrderIncomeByMonth[Order Income])<>0,sum(FactCC_OrderIncomeByMonth[Order Income]) ,blank())
```


## Table: FactCC_PaidByYear

### Measures:


```dax
Paid CC = Sum(FactCC_PaidByYear[Paid Year])
```


## Table: FactCC_InvoicedByYear

### Measures:


```dax
Invoiced CC = sum(FactCC_InvoicedByYear[Invoiced Year] ) 
```


## Table: CCContribution

### Calculated Columns:


```dax
Employee = LOOKUPVALUE(DimEmployees[Employee (Job)], DimEmployees[EmployeeID], CCContribution[EmployeeID])
```



```dax
IsPartner = LOOKUPVALUE(DimEmployees[IsPartner], DimEmployees[EmployeeID], CCContribution[EmployeeID])
```

