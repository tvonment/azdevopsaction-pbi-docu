



# DAX

|Dataset|[Napta Report V1](./../Napta-Report-V1.md)|
| :--- | :--- |
|Workspace|[Napta [Prod]](../../Workspaces/Napta-[Prod].md)|

## Table: CategorySort


```dax
{
    ("Project", 1),
    ("Reservation", 2),
    ("Holiday and training", 3),
    ("Sickness and leave", 4),
    ("Acquisition, free and internal activity", 5),
    ("other", 6)
}
```


## Table: CalendarWeeks


```dax
{ [Week-2], [Week-1], [WeekCurrent], [Week+1], [Week+2], [Week+3]}
```


### Measures:


```dax
Week-1 = 
    VAR week_t = WEEKNUM(TODAY()-7)
    VAR year_t = YEAR(TODAY()-7)
Return year_t & "-W" & week_t
```



```dax
Week-2 = 
    VAR week_t = WEEKNUM(TODAY()-14)
    VAR year_t = YEAR(TODAY()-14)
Return year_t & "-W" & week_t
```



```dax
Week+1 = 
    VAR week_t = WEEKNUM(TODAY()+7)
    VAR year_t = YEAR(TODAY()+7)
Return year_t & "-W" & week_t
```



```dax
Week+2 = 
    VAR week_t = WEEKNUM(TODAY()+14)
    VAR year_t = YEAR(TODAY()+14)
Return year_t & "-W" & week_t
```



```dax
Week+3 = 
    VAR week_t = WEEKNUM(TODAY()+21)
    VAR year_t = YEAR(TODAY()+21)
Return year_t & "-W" & week_t
```



```dax
WeekCurrent = 
    VAR week_t = WEEKNUM(TODAY())
    VAR year_t = YEAR(TODAY())
Return year_t & "-W" & week_t
```


## Table: v_napta_staffing_days_per_week

### Measures:


```dax
StaffedHours = SUM(v_napta_staffing_days_per_week[staffed_days]) * 8
```



```dax
TargetHoursWeek = SUM(v_napta_employee_target_hours_week[target_hours_week])
```



```dax
TargetHoursWeek (without leaves) = [TargetHoursWeek] - [HoursOnSicknessAndLeave]
```



```dax
HoursOnSicknessAndLeave = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Sickness and leave")
```



```dax
HoursOnSicknessAndLeave_% = IF([TargetHoursWeek (without leaves)] = 0, "", [HoursOnSicknessAndLeave] / [TargetHoursWeek (without leaves)])
```



```dax
HoursOnAcquisitoFreeInternal_old = 
    VAR target_hours = [TargetHoursWeek (without leaves)]
    VAR staffed_hours = [HoursOnProject] + [HoursOnReservation] + [HoursOnTrainingAndHoliday]
    VAR acquisition_free_internal_hours = CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, v_napta_staffing_days_per_week[staffing_category] = "Acquisition or internal activity")
    VAR total_hours = staffed_hours + acquisition_free_internal_hours
    VAR missing_hours = IF(total_hours < target_hours, target_hours - total_hours, 0)
RETURN
    acquisition_free_internal_hours + missing_hours
```



```dax
HoursOnAcquisitonFreeInternal_%_old = IF([TargetHoursWeek] = 0, "", [HoursOnAcquisitoFreeInternal_old] / [TargetHoursWeek (without leaves)])
```



```dax
HoursOnProject = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Project")
```



```dax
HoursOnProject_% = IF([TargetHoursWeek (without leaves)] = 0, "", [HoursOnProject] / [TargetHoursWeek (without leaves)])
```



```dax
HoursOnReservation = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Reservation")
```



```dax
HoursOnReservation_% = IF([TargetHoursWeek (without leaves)] = 0, "", [HoursOnReservation] / [TargetHoursWeek (without leaves)])
```



```dax
HoursOnTrainingAndHoliday = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Holiday and training")
```



```dax
HoursOnTrainingAndHoliday_% = IF([TargetHoursWeek (without leaves)] = 0, "", [HoursOnTrainingAndHoliday] / [TargetHoursWeek (without leaves)])
```



```dax
HoursOnAcquisitoFreeInternal = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Acquisition, free and internal activity")
```



```dax
HoursOnAcquisitonFreeInternal_% = IF([TargetHoursWeek (without leaves)] = 0, "", [HoursOnAcquisitoFreeInternal] / [TargetHoursWeek (without leaves)])
```



```dax
StaffedHours_% = DIVIDE([StaffedHours], [TargetHoursWeek])
```



```dax
HoursOnProBono = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Project", v_napta_staffing_days_per_week[napta_staffing_status] = "Pro Bono")
```



```dax
HoursOnProjectWithoutProBono = 
    CALCULATE(SUM(v_napta_staffing_days_per_week[staffed_days]) * 8, 
        v_napta_staffing_days_per_week[staffing_category] = "Project", v_napta_staffing_days_per_week[napta_staffing_status] <> "Pro Bono")
```



```dax
HoursOnProjectWithoutProBono_% = IF([TargetHoursWeek (without leaves)] = 0, "", [HoursOnProjectWithoutProBono] / [TargetHoursWeek (without leaves)])
```


### Calculated Columns:


```dax
Sorting = RELATED(CategorySort[sort_order])
```

