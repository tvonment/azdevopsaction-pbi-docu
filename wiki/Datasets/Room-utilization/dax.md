



# DAX

|Dataset|[Room utilization](./../Room-utilization.md)|
| :--- | :--- |
|Workspace|[MUC Office utilization](../../Workspaces/MUC-Office-utilization.md)|

## Table: RoomBookings

### Measures:


```dax
%Utilization = 
if(
    ISINSCOPE(RoomBookings[Room]),
    DIVIDE(SUM(RoomBookings[Duration]),SUM(WorkdayDuration[Duration])),
    "‎"
)
```


## Table: Calendar


```dax
CALENDAR(FIRSTDATE(RoomBookings[Start Date]),LASTDATE(RoomBookings[End Date]))
```


### Calculated Columns:


```dax
IsWorkingDay = if(or('Calendar'[Date] in DISTINCT(PublicHolidays[calendar_date]),WEEKDAY('Calendar'[Date]) in {1,7}),0,1)
```



```dax
Weekday = format('Calendar'[Date],"dddd")
```


## Table: DeskBookings

### Measures:


```dax
%DeskUtilization = 
    DIVIDE(COUNT(DeskBookings[Desk Name]),SUM(AvailableDesks[TotalDesks]))
```


## Table: CalendarDesks


```dax
CALENDAR(FIRSTDATE(DeskBookings[Start Date]),LASTDATE(DeskBookings[Start Date]))
```


### Calculated Columns:


```dax
IsWorkingDay = if(or('CalendarDesks'[Date] in DISTINCT(PublicHolidays[calendar_date]),WEEKDAY('CalendarDesks'[Date]) in {1,7}),0,1)
```


## Table: DeskBookingsCorona

### Measures:


```dax
%DeskUtilizationCorona = 
    DIVIDE(COUNT(DeskBookingsCorona[Desk Name]),SUM(AvailableDesksCorona[TotalDesks]))
```

