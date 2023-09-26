



# DAX

|Dataset|[FTE CSS](./../FTE-CSS.md)|
| :--- | :--- |
|Workspace|[CSS](../../Workspaces/CSS.md)|

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


## Table: rep v_hr_employee_ps_job_matrix

### Measures:


```dax
avg. FTE = AVERAGE('rep v_hr_employee_ps_job_matrix'[fte])
```



```dax
number of visible employees = COUNT('rep v_hr_employee'[emp_id])
```



```dax
h-cnt (old) = DISTINCTCOUNT('rep v_hr_employee_ps_job_matrix'[emp_id])
```



```dax
sum FTE = sumx('rep v_hr_employee', [avg. FTE])
```


## Table: DimDate


```dax
CALENDAR(min('rep v_hr_employee_ps_job_matrix'[key_date]), max('rep v_hr_employee_ps_job_matrix'[key_date]))
```


### Calculated Columns:


```dax
Year = year(DimDate[Date]) 
```



```dax
Month = Month(DimDate[Date]) 
```


## Table: rep v_hr_employee_costcenter_fte_per_MONTH

### Measures:


```dax
HCnt = DISTINCTCOUNT('rep v_hr_employee_costcenter_fte_per_MONTH'[emp_id])
```



```dax
FTE = 
DIVIDE([Target Hours], [Target Hours FTE])
```



```dax
Target Hours = Sumx('rep v_hr_employee_costcenter_fte_per_MONTH', 'rep v_hr_employee_costcenter_fte_per_MONTH'[target_hours])
```



```dax
Target Hours FTE = Sumx('rep v_hr_employee_costcenter_fte_per_MONTH', 'rep v_hr_employee_costcenter_fte_per_MONTH'[target_hours_fte])
```



```dax
agg. FTE = Sumx(values('rep v_hr_employee_costcenter_fte_per_MONTH'[emp_id]), [FTE])
```



```dax
dsp tree = 
var lVal = if(ISINSCOPE('Hierarchy'[L7]),  SELECTEDVALUE('Hierarchy'[L7])
, if(ISINSCOPE('Hierarchy'[L6]),  SELECTEDVALUE('Hierarchy'[L6]),
    if(ISINSCOPE('Hierarchy'[L5]),  SELECTEDVALUE('Hierarchy'[L5]),
        if(ISINSCOPE('Hierarchy'[L4]),  SELECTEDVALUE('Hierarchy'[L4]),
            if(ISINSCOPE('Hierarchy'[L3]),  SELECTEDVALUE('Hierarchy'[L3]),
                if(ISINSCOPE('Hierarchy'[L2]),  SELECTEDVALUE('Hierarchy'[L2]),
                    if(ISINSCOPE('Hierarchy'[L1]),  SELECTEDVALUE('Hierarchy'[L1])
, blank())))))))

return if(lVal = blank(), blank(), [agg. FTE])

```



```dax
IsVisibleToSelectedUser = 
var currentUser = SELECTEDVALUE(OrgResponsible[org_unit_responsible_id])
var orgid = min(Org[org_unit_id])

var result =  calculate(countrows(PermissionPerUserToCostCenterValues)
                    , Filter(PermissionPerUserToCostCenterValues
                                , PermissionPerUserToCostCenterValues[org_unit_responsible_id] = currentUser 
                                    && CONTAINSSTRING(PermissionPerUserToCostCenterValues[AssociatedAndChildren],orgid)
                    )
                    )

                    return result
```



```dax
agg. FTE Permission = 
calculate(
     Sumx('rep v_hr_employee', [FTE])
     , Filter('rep v_hr_employee_costcenter_fte_per_MONTH', [IsVisibleToSelectedUser] > 0) 
)
```



```dax
agg. FTE (by day) = AVERAGEX(DimDate,  Sumx(values('rep v_hr_employee_costcenter_fte_per_MONTH'[emp_id]), [FTE]))
```


### Calculated Columns:


```dax
Empl = CONCATENATE( coalesce( RELATED('rep v_hr_employee'[full_name]), "") , CONCATENATE( " - ", 'rep v_hr_employee_costcenter_fte_per_MONTH'[emp_id]))
```



```dax
ToeId = LOOKUPVALUE('employee toe by month'[ToeId]
                , 'employee toe by month'[emp_id], 'rep v_hr_employee_costcenter_fte_per_MONTH'[emp_id]
                , 'employee toe by month'[validfrom_date], 'rep v_hr_employee_costcenter_fte_per_MONTH'[StartOfMonth])
```


## Table: Org

### Measures:


```dax
tree display agg FTE = 
var lVal = if(ISINSCOPE('Org'[L5Name]),  SELECTEDVALUE('Org'[L5Name])
, if(ISINSCOPE('Org'[L4Name]),  SELECTEDVALUE('Org'[L4Name]),
    if(ISINSCOPE('Org'[L3Name]),  SELECTEDVALUE('Org'[L3Name]),
        if(ISINSCOPE('Org'[L2Name]),  SELECTEDVALUE('Org'[L2Name]),
            if(ISINSCOPE('Org'[L1Name]),  SELECTEDVALUE('Org'[L1Name])
            --,
                --if(ISINSCOPE('Hierarchy'[L2]),  SELECTEDVALUE('Hierarchy'[L2]),
                  --  if(ISINSCOPE('Hierarchy'[L1]),  SELECTEDVALUE('Hierarchy'[L1])
, blank())))))
--))

return if(lVal = blank(), blank(),
 
 [agg. FTE (by day)]
 )
```



```dax
# cost centers visible for selected user = 
var curUser = SELECTEDVALUE(OrgResponsible[org_unit_responsible_id])
var curOrg = SELECTEDVALUE(Org[org_unit_id])

var curPath = SELECTEDVALUE(Org[Hierarchy])

var linesForUser = CALCULATETABLE(Permission, Permission[org_unit_responsible_id] = curUser)

var allIds = CONCATENATEX(linesForUser, Permission[Children], ";")

return if(curOrg<> blank() && CONTAINSSTRING(allIds, curOrg)
, 1
)
```



```dax
agg. FTE (one cost center) = 
if(COUNTROWS(ALLSELECTED(org)) > 1, blank(), [agg. FTE])
```


### Calculated Columns:


```dax
Hierarchy = path(Org[org_unit_id], Org[parent_id])
```



```dax
Level = PATHLENGTH( Org[Hierarchy])
```



```dax
L1 = PATHITEM(Org[Hierarchy], 1)
```



```dax
L2 = PATHITEM(Org[Hierarchy], 2)
```



```dax
L3 = PATHITEM(Org[Hierarchy], 3)
```



```dax
L4 = PATHITEM(Org[Hierarchy], 4)
```



```dax
L5 = PATHITEM(Org[Hierarchy], 5)
```



```dax
L1Name = LOOKUPVALUE(Org[org_unit], Org[org_unit_id], Org[L1])
```



```dax
L2Name = LOOKUPVALUE(Org[org_unit], Org[org_unit_id], Org[L2])
```



```dax
L3Name = LOOKUPVALUE(Org[org_unit], Org[org_unit_id], Org[L3])
```



```dax
L4Name = LOOKUPVALUE(Org[org_unit], Org[org_unit_id], Org[L4])
```



```dax
L5Name = LOOKUPVALUE(Org[org_unit], Org[org_unit_id], Org[L5])
```



```dax
Children = 
    var curPath = Org[Hierarchy]
    var length = len(curPath)
    var allChildrenAndSelf  = CALCULATETABLE(Org, Left( Org[Hierarchy], length) = curPath, all(org))
    return CONCATENATEX(allChildrenAndSelf, Org[org_unit_id], ";")
```


## Table: Permission


```dax


var _orgs = CALCULATETABLE(
    summarize (org, Org[org_unit_responsible_id], Org[Children])
    , Org[org_unit_responsible_id] <> blank())
return _orgs

//var xx = ADDCOLUMNS(_orgs, "Child",
    //var curPath = SELECTEDVALUE(Org[Hierarchy])
    //var length = len(curPath)
  //  var allChildrenAndSelf  = CALCULATETABLE(Org, Left( Org[Hierarchy], length) = curPath, all(org))
    
    //return curPath
    //)

//return xx
```


## Table: PermissionPerUserToCostCenterValues


```dax

    //group by user, add all children ...
    VAR Result =
    Addcolumns(
    distinct(
        SELECTCOLUMNS (
        Permission,
        "org_unit_responsible_id", Permission[org_unit_responsible_id]
        )
    )
        
        , "AssociatedAndChildren", 
        	
    	calculate
    	(
    		var curUser = min(Permission[org_unit_responsible_id])
    		var linesForUser = CALCULATETABLE(Permission, Permission[org_unit_responsible_id] = curUser)
    		var allIds = CONCATENATEX(linesForUser, Permission[Children], ";")
    		return allIds
    	)
    )
    
    
RETURN
    Result
```

