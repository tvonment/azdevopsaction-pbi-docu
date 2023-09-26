



# DAX

|Dataset|[Capacity Metrics Analysis](./../Capacity-Metrics-Analysis.md)|
| :--- | :--- |
|Workspace|[Premium Capacity Utilization And Metrics 22.12.2022 15:51:11](../../Workspaces/Premium-Capacity-Utilization-And-Metrics-22.12.2022-15:51:11.md)|

## Table: Performance_by_Artifact_and_Hour

### Measures:


```dax
Count of Performance by Artifact and hour = COUNTROWS('Performance_by_Artifact_and_Hour')
```


## Table: All Measures

### Measures:


```dax
Artifact KPI1 - Count of Throttled users by Total Active Users = 
AVERAGEX(
    VALUES('Date and Time'[Hour Start]),
    DIVIDE(
        [Count of Throttled Users (Artifact)],
        SUM('Throttled_by_Artifact_and_Hour'[active_users]),
        0
        )
    )
```



```dax
Artifact KPI2 - Seconds of throttle time by user = 
    AVERAGEX(
        VALUES('Date and Time'[Hour Start]) ,
        DIVIDE(
            [Sum of Throttled Time (Artifact)], 
            //[Sum of Throttled Operations (Artifact)]//
            [Count of Throttled Users (Artifact)]
            )
        )
```



```dax
Artifact KPI3 - throttle time % = 
    MAXX(
        VALUES('Date and Time'[Hour Start]) ,
        DIVIDE(
            [Sum of Throttled Time (Artifact)], 
            // SUM('Metrics by Artifact and Operation and Hour'[sum_duration]) / 1000 ,
            [Sum of Duration by Operation and Hour]
            ) 
        )
```



```dax
Artifact Users Busy % = 
VAR MAXUsers = CALCULATE(MAX('Artifacts'[dcount_Identity]),ALL('Artifacts'))
VAR MyUsers = 
    MAXX(
        FILTER('Artifacts',[ArtifactId]=SELECTEDVALUE('MAX_Memory_by_Artifact'[ArtifactId])),[dcount_Identity])
RETURN MyUsers / MAXUsers


```



```dax
Count of Refresh Failures = CALCULATE([Count of Refresh Operations],'Refresh_by_Hour'[Status]<>"Success")
```



```dax
Count of Refresh Operations = SUM('Refresh_by_Hour'[count_])
```



```dax
Count of Throttled Users (Artifact) = 
VAR Artifact = SELECTEDVALUE('Artifacts'[Artifact])
RETURN 
CALCULATE(SUM('Throttled_by_Artifact_and_Hour'[active_users]), TREATAS({Artifact},'Artifacts (Throttled)'[Artifact]))
```



```dax
Dynamic M1 CPU = 

        VAR isFiltered_Hour =
            ISFILTERED ( 'Date and Time'[Hour Start] )
        VAR isFiltered_Op =
            ISFILTERED ( 'Operation Names'[OperationName])
            
        VAR isFiltered_Day = ISFILTERED(Dates[Date])   
        VAR hasOneFilter_Day = HASONEFILTER(Dates[Date])
        VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")

        VAR myMetric = SELECTEDVALUE('Metrics'[Metric])
        RETURN 
            SWITCH (
                TRUE (),
			    not isFiltered_Hour && not isFiltered_Op && isFiltered_Day,SUM ( 		'Metrics_by_Artifact_and_Day'[sum_cpu] )  ,
                not isFiltered_Hour && not isFiltered_Op,SUM ( 		'Metrics_by_Artifact_and_Day'[sum_cpu] ),
                isFiltered_Op && not isFiltered_Day,SUM ( 		'Metrics_by_Artifact_and_Operation'[sum_cpu] ),
                not isFiltered_Hour &&  isFiltered_Op,SUM ( 		'Metrics_by_Artifact_and_Operation_and_Day'[sum_cpu] ),
                SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[sum_cpu] )               

                ) / 1000


//         RETURN 
//   SWITCH (
//                 TRUE (),
// 			    not isFiltered_Hour && not isFiltered_Op && isFiltered_Day,SUM ( 		'Metrics by Artifact and Day'[sum_cpu] )/1000
//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Day'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Day'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Day'[count_operations] ),
//                     //     "Users", SUM ( 		'Metrics by Artifact and Day'[count_users] ) ,
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2] ,
//                     //     "Memory" , [MAX Memory (GB)] ,
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     //     //"Users", SUMX ( 	VALUES('Operation Names'[OperationName]),	CALCULATE(SUM('Capacity Overview Scenario 6 - AGG - Op, No day'[count_users])) )
//                     // )
//                     ,



//                 not isFiltered_Hour && not isFiltered_Op,SUM ( 		'Metrics by Artifact and Day'[sum_cpu] )/1000,
//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Day'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Day'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Day'[count_operations] ),
//                     //     //"Users", SUM ( 		'Capacity Overview Scenario 6 - AGG - day'[count_users] )
//                     //     "Users", SUMX ( 	VALUES('Operation Names'[OperationName]),	CALCULATE(SUM('Metrics by Artifact and Operation'[count_users])) ),
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2],
//                     //     "Memory" , [MAX Memory (GB)],
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     // ),
//                 isFiltered_Op && not isFiltered_Day,SUM ( 		'Metrics by Artifact and Operation'[sum_cpu] )/1000,

//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Operation'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Operation'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Operation'[count_operations] ),
//                     //     "Users", SUM ( 		'Metrics by Artifact and Operation'[count_users] ),
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2],
//                     //     "Memory" , [MAX Memory (GB)],
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     // ),
//                 not isFiltered_Hour &&  isFiltered_Op,SUM ( 		'Metrics_by_Artifact_and_Operation_and_Day'[sum_cpu] )/1000,
//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Operation and Day'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Operation and Day'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Operation and Day'[count_operations] ),
//                     //     "Users", SUM ( 		'Metrics by Artifact and Operation and Day'[count_users] ),
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2],
//                     //     "Memory" , [MAX Memory (GB)],
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     // )
//                      SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[sum_cpu] )/1000               
//                 // SWITCH (
//                 //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                 //     "Duration", SUM ( 'Metrics by Artifact and Operation and Hour'[sum_duration] )/1000,
//                 //     "CPU", SUM ( 'Metrics by Artifact and Operation and Hour'[sum_cpu] )/1000,
//                 //     "Operations", SUM ( 'Metrics by Artifact and Operation and Hour'[count_operations] ),
//                 //     "Users", SUM ( 'Metrics by Artifact and Operation and Hour'[count_users] ),
//                 //         "Perf 1" , [Perf Metric 1] ,
//                 //         "Perf 2" , [Perf Metric 2],
//                 //         "Memory" , [MAX Memory (GB)],
//                 //         "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                 )
```



```dax
Dynamic M1 Duration = 

        VAR isFiltered_Hour =
            ISFILTERED ( 'Date and Time'[Hour Start] )
        VAR isFiltered_Op =
            ISFILTERED ( 'Operation Names'[OperationName])
            
        VAR isFiltered_Day = ISFILTERED(Dates[Date])   
        VAR hasOneFilter_Day = HASONEFILTER(Dates[Date])
        VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")

        VAR myMetric = SELECTEDVALUE('Metrics'[Metric])
        RETURN 
            SWITCH (
                TRUE (),
			    not isFiltered_Hour && not isFiltered_Op && isFiltered_Day,SUM ( 		'Metrics_by_Artifact_and_Day'[sum_duration] )  ,
                not isFiltered_Hour && not isFiltered_Op,SUM ( 		'Metrics_by_Artifact_and_Day'[sum_duration] ),
                isFiltered_Op && not isFiltered_Day,SUM ( 		'Metrics_by_Artifact_and_Operation'[sum_duration] ),
                not isFiltered_Hour &&  isFiltered_Op,SUM ( 		'Metrics_by_Artifact_and_Operation_and_Day'[sum_duration] ),
                SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[sum_duration] )               

                ) / 1000



//         RETURN 
//   SWITCH (
//                 TRUE (),
// 			    not isFiltered_Hour && not isFiltered_Op && isFiltered_Day,SUM ( 		'Metrics by Artifact and Day'[sum_duration] )/1000
//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Day'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Day'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Day'[count_operations] ),
//                     //     "Users", SUM ( 		'Metrics by Artifact and Day'[count_users] ) ,
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2] ,
//                     //     "Memory" , [MAX Memory (GB)] ,
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     //     //"Users", SUMX ( 	VALUES('Operation Names'[OperationName]),	CALCULATE(SUM('Capacity Overview Scenario 6 - AGG - Op, No day'[count_users])) )
//                     // )
//                     ,



//                 not isFiltered_Hour && not isFiltered_Op,SUM ( 		'Metrics by Artifact and Day'[sum_duration] )/1000,
//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Day'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Day'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Day'[count_operations] ),
//                     //     //"Users", SUM ( 		'Capacity Overview Scenario 6 - AGG - day'[count_users] )
//                     //     "Users", SUMX ( 	VALUES('Operation Names'[OperationName]),	CALCULATE(SUM('Metrics by Artifact and Operation'[count_users])) ),
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2],
//                     //     "Memory" , [MAX Memory (GB)],
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     // ),
//                 isFiltered_Op && not isFiltered_Day,SUM ( 		'Metrics by Artifact and Operation'[sum_duration] )/1000,

//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Operation'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Operation'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Operation'[count_operations] ),
//                     //     "Users", SUM ( 		'Metrics by Artifact and Operation'[count_users] ),
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2],
//                     //     "Memory" , [MAX Memory (GB)],
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     // ),
//                 not isFiltered_Hour &&  isFiltered_Op,SUM ( 		'Metrics_by_Artifact_and_Operation_and_Day'[sum_duration] )/1000,
//                     // SWITCH (
//                     //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                     //     "Duration", SUM ( 	'Metrics by Artifact and Operation and Day'[sum_duration] )/1000,
//                     //     "CPU", SUM ( 		'Metrics by Artifact and Operation and Day'[sum_cpu] )/1000,
//                     //     "Operations", SUM ( 'Metrics by Artifact and Operation and Day'[count_operations] ),
//                     //     "Users", SUM ( 		'Metrics by Artifact and Operation and Day'[count_users] ),
//                     //     "Perf 1" , [Perf Metric 1] ,
//                     //     "Perf 2" , [Perf Metric 2],
//                     //     "Memory" , [MAX Memory (GB)],
//                     //     "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                     // )
//                      SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[sum_duration] )/1000               
//                 // SWITCH (
//                 //     SELECTEDVALUE ( 'Metrics'[Metric] ),
//                 //     "Duration", SUM ( 'Metrics by Artifact and Operation and Hour'[sum_duration] )/1000,
//                 //     "CPU", SUM ( 'Metrics by Artifact and Operation and Hour'[sum_cpu] )/1000,
//                 //     "Operations", SUM ( 'Metrics by Artifact and Operation and Hour'[count_operations] ),
//                 //     "Users", SUM ( 'Metrics by Artifact and Operation and Hour'[count_users] ),
//                 //         "Perf 1" , [Perf Metric 1] ,
//                 //         "Perf 2" , [Perf Metric 2],
//                 //         "Memory" , [MAX Memory (GB)],
//                 //         "Throttling" , [Artifact KPI3 - throttle time %] * 100
//                 )
```



```dax
Dynamic M1 Memory = 
VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")
VAR myArtifactKind = SELECTEDVALUE('Artifacts'[ArtifactKind],"")
RETURN 
    SWITCH(
        TRUE(),
        myArtifactKind <> "Dataset" && myOperationName="" , blank(), // "------",
        myOperationName="" , [MAX Memory (GB)]
        )
```



```dax
Dynamic M1 Perf = 
VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")
VAR myArtifactKind = SELECTEDVALUE('Artifacts'[ArtifactKind],"")
RETURN 
    // IF(
    //     myOperationName="" ,
    //      [Perf Metric 1]
    //     )
    SWITCH(
        TRUE(),
        myArtifactKind <> "Dataset" && myOperationName="" , blank() ,// "------",
        myOperationName="" ,  [Perf Metric 1]
        )

```



```dax
Dynamic M1 Throttling = 
VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")
RETURN 
    IF(
        myOperationName="" ,
        [Artifact KPI4 - throttle time % * Multiplier]
        )
```



```dax
Dynamic M1 Users = 

        VAR isFiltered_Hour =
            ISFILTERED ( 'Date and Time'[Hour Start] )
        VAR isFiltered_Op =
            ISFILTERED ( 'Operation Names'[OperationName])
            
        VAR isFiltered_Day = ISFILTERED(Dates[Date])   
        VAR hasOneFilter_Day = HASONEFILTER(Dates[Date])
        VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")

        VAR myMetric = SELECTEDVALUE('Metrics'[Metric])
        RETURN 


            SWITCH (
                TRUE (),
                not isFiltered_Hour && not isFiltered_Op && not isFiltered_Day,               MAX ( 		'Metrics_by_Artifact'[count_users] ), // NEEDS TO BE Metrics_by_Artifact'[count_users]
                not isFiltered_Hour &&    isFiltered_Op && not isFiltered_Day ,                MAX ( 'Metrics_by_Artifact_and_Operation'[count_users] ),
			    not isFiltered_Hour && not isFiltered_Op && isFiltered_Day, MAX ( 'Metrics_by_Artifact_and_Day'[count_users] )  ,
                not isFiltered_Hour && not isFiltered_Op,                   MAX ( 'Metrics_by_Artifact_and_Day'[count_users] ),
                isFiltered_Op && not isFiltered_Day ,                        MAX ( 'Metrics_by_Artifact_and_Operation'[count_users] ),
                not isFiltered_Hour &&  isFiltered_Op,                      MAX ( 'Metrics_by_Artifact_and_Operation_and_Day'[count_users] ),
                MAX ( 'Metrics_by_Artifact_and_Operation_and_Hour'[count_users] )               

                )


            // SWITCH (
            //     TRUE (),
            //     //ISFILTERED('Artifacts'[Full ID]) && not isFiltered_Op , MAX('Metrics_by_Artifact'[count_users]) ,
            //     Not ISFILTERED('Artifacts'[Artifact]), Blank() ,
			//     not isFiltered_Hour && not isFiltered_Op && hasOneFilter_Day,MAX ( 		'Metrics_by_Artifact_and_Day'[count_users] )  ,
            //     not isFiltered_Hour && not isFiltered_Op,MAX ( 		'Metrics_by_Artifact'[count_users] ), // NEEDS TO BE Metrics_by_Artifact'[count_users]
            //     isFiltered_Op && not isFiltered_Day,MAX ( 		'Metrics_by_Artifact_and_Operation'[count_users] ),
            //     not isFiltered_Hour &&  isFiltered_Op,MAX ( 		'Metrics_by_Artifact_and_Operation'[count_users] ),
                
            //     MAX ( 'Metrics_by_Artifact_and_Operation_and_Hour'[count_users] )               

            //     )
```



```dax
Dynamic Metric Artifact 1 = 

        VAR isFiltered_Hour =
            ISFILTERED ( 'Date and Time'[Hour Start] )
        VAR isFiltered_Op =
            ISFILTERED ( 'Operation Names'[OperationName])
            
        VAR isFiltered_Day = ISFILTERED(Dates[Date])   
        VAR hasOneFilter_Day = HASONEFILTER(Dates[Date])
        VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")

        VAR myMetric = SELECTEDVALUE('Metrics'[Metric])

        VAR DynamicCalc =  int(
            SWITCH (
                TRUE (),
			    not isFiltered_Hour && not isFiltered_Op && isFiltered_Day,
                    SWITCH (
                        SELECTEDVALUE ( 'Metrics'[Metric] ),
                        "Duration", SUM ( 	'Metrics_by_Artifact_and_Day'[sum_duration] )/1000,
                        "CPU", SUM ( 		'Metrics_by_Artifact_and_Day'[sum_cpu] )/1000,
                        "Operations", SUM ( 'Metrics_by_Artifact_and_Day'[count_operations] ),
                        "Users", SUM ( 		'Metrics_by_Artifact_and_Day'[count_users] ) ,
                        // "Perf 1" , [Perf Metric 1] ,
                        // "Perf 2" , [Perf Metric 2] ,
                        "Memory" , [MAX Memory (GB)] ,
                        "Throttling" , [Artifact KPI3 - throttle time %] * 100
                        //"Users", SUMX ( 	VALUES('Operation Names'[OperationName]),	CALCULATE(SUM('Capacity Overview Scenario 6 - AGG - Op, No day'[count_users])) )
                    ),



                not isFiltered_Hour && not isFiltered_Op,
                    SWITCH (
                        SELECTEDVALUE ( 'Metrics'[Metric] ),
                        "Duration", SUM ( 	'Metrics_by_Artifact_and_Day'[sum_duration] )/1000,
                        "CPU", SUM ( 		'Metrics_by_Artifact_and_Day'[sum_cpu] )/1000,
                        "Operations", SUM ( 'Metrics_by_Artifact_and_Day'[count_operations] ),
                        //"Users", SUM ( 		'Capacity Overview Scenario 6 - AGG - day'[count_users] )
                        "Users", SUMX ( 	VALUES('Operation Names'[OperationName]),	CALCULATE(SUM('Metrics_by_Artifact_and_Operation'[count_users])) ),
                        // "Perf 1" , [Perf Metric 1] ,
                        // "Perf 2" , [Perf Metric 2],
                        "Memory" , [MAX Memory (GB)],
                        "Throttling" , [Artifact KPI3 - throttle time %] * 100
                    ),
                isFiltered_Op && not isFiltered_Day,

                    SWITCH (
                        SELECTEDVALUE ( 'Metrics'[Metric] ),
                        "Duration", SUM ( 	'Metrics_by_Artifact_and_Operation'[sum_duration] )/1000,
                        "CPU", SUM ( 		'Metrics_by_Artifact_and_Operation'[sum_cpu] )/1000,
                        "Operations", SUM ( 'Metrics_by_Artifact_and_Operation'[count_operations] ),
                        "Users", SUM ( 		'Metrics_by_Artifact_and_Operation'[count_users] ),
                        // "Perf 1" , [Perf Metric 1] ,
                        // "Perf 2" , [Perf Metric 2],
                        "Memory" , [MAX Memory (GB)],
                        "Throttling" , [Artifact KPI3 - throttle time %] * 100
                    ),
                not isFiltered_Hour &&  isFiltered_Op,
                    SWITCH (
                        SELECTEDVALUE ( 'Metrics'[Metric] ),
                        "Duration", SUM ( 	'Metrics_by_Artifact_and_Operation_and_Day'[sum_duration] )/1000,
                        "CPU", SUM ( 		'Metrics_by_Artifact_and_Operation_and_Day'[sum_cpu] )/1000,
                        "Operations", SUM ( 'Metrics_by_Artifact_and_Operation_and_Day'[count_operations] ),
                        "Users", SUM ( 		'Metrics_by_Artifact_and_Operation_and_Day'[count_users] ),
                        // "Perf 1" , [Perf Metric 1] ,
                        // "Perf 2" , [Perf Metric 2],
                        "Memory" , [MAX Memory (GB)],
                        "Throttling" , [Artifact KPI3 - throttle time %] * 100
                    )
                    ,                
                    isFiltered_Hour && not isFiltered_Op ,
                    SWITCH (
                        SELECTEDVALUE ( 'Metrics'[Metric] ),
                        "Duration", SUM (   'Metrics_by_Artifact_and_Hour'[sum_duration] )/1000,
                        "CPU", SUM (        'Metrics_by_Artifact_and_Hour'[sum_cpu] )/1000,
                        "Operations", SUM ( 'Metrics_by_Artifact_and_Hour'[count_operations] ),
                        "Users",  SUM (         'Metrics_by_Artifact_and_Hour'[count_users] ),
                        // "Perf 1" , [Perf Metric 1] ,
                        // "Perf 2" , [Perf Metric 2],
                        "Memory" , [MAX Memory (GB)],
                        "Throttling" , [Artifact KPI3 - throttle time %] * 100
                    )
                    ,              


                SWITCH (
                    SELECTEDVALUE ( 'Metrics'[Metric] ),
                    "Duration", SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[sum_duration] )/1000,
                    "CPU", SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[sum_cpu] )/1000,
                    "Operations", SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[count_operations] ),
                    "Users", SUM ( 'Metrics_by_Artifact_and_Operation_and_Hour'[count_users] ),
                        // "Perf 1" , [Perf Metric 1] ,
                        // "Perf 2" , [Perf Metric 2],
                        "Memory" , [MAX Memory (GB)],
                        "Throttling" , [Artifact KPI3 - throttle time %] * 100
                )

            ))

    RETURN 
        SWITCH( 
            TRUE(), 
            myMetric in {"Perf 1","Perf 2","Memory","Throttling"} && myOperationName<>"" , blank(),
            //myMetric="Perf 2" && myOperationName<>"", blank(),
            myMetric in {"Perf 1","Perf 2","Memory","Throttling"}&& hasOneFilter_Day , blank(),
            //myMetric="Perf 2" && hasOneFilter_Day , blank(),
            DynamicCalc)
```



```dax
Dynamic Refresh Metric = 
SWITCH(
        SELECTEDVALUE('Metrics'[Metric],""),
        "CPU",      [Sum of refresh CPU],
        "Duration", [Sum of Refresh Duration (s)],
        SUM('Refresh_by_Hour'[count_])
        )
```



```dax
Failure Ratio = DIVIDE(SUM('Failures_By_Utilization_Type'[Failures]) , SUM('Failures_By_Utilization_Type'[count_]))
```



```dax
Magars Magic Measure = 
    (
        DIVIDE(SUM('Throttler_by_Artifact_and_Hour'[detailCpuTimeMs]),1000) * 
        COUNTROWS('Throttler_by_Artifact_and_Hour')
    )
```



```dax
MAX Memory (GB) = MAX('MAX_Memory_by_Artifact_and_3-Hour'[MaxMemoryInBytes]) / (1024 * 1024 * 1024)
```



```dax
MAX of Throttled User = 
CALCULATE(
    MAX('Throttled_by_Artifact_and_Hour'[active_users])
    )
```



```dax
MAX of Throttled User KPI = 
CALCULATE(
    MAX('Throttled_by_Artifact_and_Hour'[active_users]), 
    ALL('Artifacts (Throttled)'[Artifact]
        )
    )
```



```dax
MAX Throttle Time + buffer = MAXX(VALUES('Date and Time'[Date]),[Sum of Throttled Time] * 1.05)
```



```dax
MAX Throttle User + buffer = MAXX(VALUES('Date and Time'[Date]),[MAX of Throttled User] * 1.05)
```



```dax
Measure = 
IF(
    ISFILTERED('MAX_Memory_by_Artifact_and_3-Hour'[ArtifactId]),
    SUM('Performance_by_Artifact_and_Hour'[slow_running_average]),
    [Moving Average (fast queries)]
    )
```



```dax
Memory SKU Limit (GB) = MAX('MAX_Memory_by_Artifact_and_3-Hour'[SkuMemory]) / (1000*1000*1000) * 1.0
```



```dax
MIN Throttle Time + buffer = 
VAR myValue = MINX(VALUES('Date and Time'[Date]),[Sum of Throttled Time]) * .1
RETURN if(myValue<100,-10000,myValue)
```



```dax
MIN Throttle User + buffer = 
VAR myValue = MINX(VALUES('Date and Time'[Date]),[MAX of Throttled User]) * .95
RETURN if(myValue<100,-2,myValue)
```



```dax
Moving Average (fast queries) = 
VAR CurrentTimeBucket = 
    SELECTEDVALUE('Date and Time'[Hour Start])
RETURN 
CALCULATE(
        AVERAGEX(
                VALUES('Date and Time'[Hour Start]),
                CALCULATE(SUM('Performance_by_Hour'[Fast]))
        ),
        FILTER(
            ALL('Date and Time'[Hour Start]),[Hour Start] <= CurrentTimeBucket && [Hour Start] > CurrentTimeBucket - 7 ))
```



```dax
Moving Average (fast queries) DQ = 
VAR CurrentTimeBucket = 
    SELECTEDVALUE('Performance_by_Artifact_and_Hour'[Timestamp])
RETURN 
CALCULATE(
        AVERAGEX(
                VALUES('Performance_by_Artifact_and_Hour'[Timestamp]),
                CALCULATE(SUM('Performance_by_Artifact_and_Hour'[fast_running_average]))
        ),
        FILTER(
            ALL('Performance_by_Artifact_and_Hour'[Timestamp]),[Timestamp] <= CurrentTimeBucket && [Timestamp] > CurrentTimeBucket - 7 ))
```



```dax
Moving Average (medium queries) = 
VAR CurrentTimeBucket = 
    SELECTEDVALUE('Date and Time'[Hour Start])
RETURN 
CALCULATE(
        AVERAGEX(
                VALUES('Date and Time'[Hour Start]),
                CALCULATE(SUM('Performance_by_Hour'[Medium]))
        ),
        FILTER(
            ALL('Date and Time'[Hour Start]),[Hour Start] <= CurrentTimeBucket && [Hour Start] > CurrentTimeBucket - 7 ))
```



```dax
Moving Average (Slow queries) = 
VAR CurrentTimeBucket = 
    SELECTEDVALUE('Date and Time'[Hour Start])
RETURN 
CALCULATE(
        AVERAGEX(
                VALUES('Date and Time'[Hour Start]),
                CALCULATE(SUM('Performance_by_Hour'[Slow]))
        ),
        FILTER(
            ALL('Date and Time'[Hour Start]),[Hour Start] <= CurrentTimeBucket && [Hour Start] > CurrentTimeBucket - 7 ))
```



```dax
Perf Metric 1 = 
VAR old = 
    DIVIDE(
        FIRSTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX(Performance_2day_Snapshot[fast_running_average])) ,        
        FIRSTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX(Performance_2day_Snapshot[total_average])) 
        )
VAR new = 
    DIVIDE(
        LASTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX(Performance_2day_Snapshot[fast_running_average])),
        LASTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX(Performance_2day_Snapshot[total_average]))
    )
RETURN SWITCH( 
            TRUE() , 
            ISBLANK(old) || ISBLANK(new) , BLANK(),
            new<>old,int( divide( (new-old) , new) * 100))

```



```dax
Perf Metric 1a = 
VAR old = FIRSTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX(Performance_2day_Snapshot[Fast]))
VAR new = LASTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX(Performance_2day_Snapshot[Fast]))
RETURN format(old ,"###.####")  & " / " & format(new,"###.####")
```



```dax
Perf Metric 2 = 
VAR old = FIRSTNONBLANKVALUE(Performance_2day_Snapshot[TIMESTAMP],MAX('Performance_2day_Snapshot'[Fast]))
VAR new = LASTNONBLANKVALUE('Performance_2day_Snapshot'[TIMESTAMP],MAX('Performance_2day_Snapshot'[fast_running_average]))
RETURN DIVIDE(new  , LASTNONBLANKVALUE('Performance_2day_Snapshot'[TIMESTAMP],MAX('Performance_2day_Snapshot'[total_average]))) * 100

```



```dax
Seconds of Throttling = SUM('Throttling_by_Artifact'[count_throlltletime]) / 1000
```



```dax
Sum of CPU by Operation and Hour = SUM('Metrics_by_Artifact_and_Operation_and_Hour'[sum_cpu]) / 1000
```



```dax
Sum of Duration by Operation and Hour = SUM('Metrics_by_Artifact_and_Operation_and_Hour'[sum_duration]) / 1000
```



```dax
Sum of refresh CPU = SUM('Refresh_by_Hour'[CpuTimeMs]) / 1000
```



```dax
Sum of Refresh Duration (s) = SUM('Refresh_by_Hour'[sum_duration]) /1000
```



```dax
Sum of Throttled Operations (Artifact) = 
VAR Artifact = SELECTEDVALUE('Artifacts'[Artifact])
RETURN 
    CALCULATE(
        SUM('Throttled_by_Artifact_and_Hour'[ThrottledOperations]), 
        TREATAS({Artifact},'Artifacts (Throttled)'[Artifact])
        ) 
```



```dax
Sum of Throttled Time = CALCULATE(SUM('Throttled_by_Artifact_and_Hour'[ThrottleTime]), ALL('Artifacts'[Artifact])) 
```



```dax
Sum of Throttled Time (Artifact) = 
VAR Artifact = SELECTEDVALUE('Artifacts'[Artifact])
RETURN 
    CALCULATE(
        SUM('Throttled_by_Artifact_and_Hour'[ThrottleTime]), 
        TREATAS({Artifact},'Artifacts (Throttled)'[Artifact])
        ) 
```



```dax
Sum of Throttled Users = 
    CALCULATE(
        MAX('Throttled_by_Artifact_and_Hour'[active_users])
        //, 
        // ALL('Artifacts'[Artifact]), 
        // 'Throttled_by_Artifact_and_Hour'[active_users] > 0
        )
```



```dax
Sum of Throttled Users 2 = sum('Throttled_by_Artifact_and_Hour'[active_users])
```



```dax
MAX Artifacts + buffer = CALCULATE(MAXX('Metrics_by_7_day',[Metric 7-day Sum of Artifacts]),ALL('Metrics_by_7_day')) * 1.05
```



```dax
MAX Cores + buffer = MAXX('Metrics_by_7_day',[max_cores]) * 1.01
```



```dax
MAX CPU + buffer = CALCULATE(MAXX('Metrics_by_7_day',[Metric 7-day Sum of CPU]),ALL('Metrics_by_7_day')) * 1.05
```



```dax
MAX Users + buffer = CALCULATE(MAXX('Metrics_by_7_day',[active_users]),ALL('Metrics_by_7_day')) * 1.05
```



```dax
MIN Artifacts + buffer = CALCULATE(MINX('Metrics_by_7_day',[Metric 7-day Sum of Artifacts]),ALL('Metrics_by_7_day')) * 0.90
```



```dax
MIN Cores + buffer = MINX('Metrics_by_7_day',[max_cores]) * .99
```



```dax
MIN CPU + buffer = CALCULATE(MINX('Metrics_by_7_day',[Metric 7-day Sum of CPU]),ALL('Metrics_by_7_day')) * 0.90
```



```dax
MIN Users + buffer = CALCULATE(MINX('Metrics_by_7_day',[active_users]),ALL('Metrics_by_7_day')) * 0.90
```



```dax
Dynamic Text for Memory Visual = IF(SELECTEDVALUE('Artifacts'[ArtifactKind],"Dataset")<>"Dataset","This artifact type does not record memory at this time")
```



```dax
Degradation Visual Fast = IF(SELECTEDVALUE('Artifacts'[ArtifactKind],"Dataset")="Dataset",SUM('Performance_by_Artifact_and_Hour'[fast_running_average]))
```



```dax
Degradation Visual Medium = IF(SELECTEDVALUE('Artifacts'[ArtifactKind],"Dataset")="Dataset",SUM('Performance_by_Artifact_and_Hour'[medium_running_average]))
```



```dax
Degradation Visual Slow = IF(SELECTEDVALUE('Artifacts'[ArtifactKind],"Dataset")="Dataset",SUM('Performance_by_Artifact_and_Hour'[slow_running_average]))
```



```dax
Dynamic Text for Degradation Visual = IF(SELECTEDVALUE('Artifacts'[ArtifactKind],"Dataset")<>"Dataset","This artifact type does not record degradation performance at this time")
```



```dax
Memory SKU Limit (GB)  AS = MAX('MAX_Memory_by_Artifact_and_3-Hour'[SkuMemory]) / (1000*1000*1000) /2.0
```



```dax
Artifact KPI4 - throttle time % * Multiplier = 
[Artifact KPI3 - throttle time %] * [Count of Throttled Users (Artifact)]
```



```dax
Metric 7-day Sum of Artifacts = SUM('Metrics_by_7_day'[active_artifacts])
```



```dax
Metric 7-day Sum of CPU = SUM('Metrics_by_7_day'[cpu]) / 1000
```



```dax
Sum of refresh detail CPU = SUM('Refresh_Detail'[CpuTimeMs]) / 1000
```



```dax
Sum of Refresh detail Duration (s) = SUM('Refresh_Detail'[DurationMs]) /1000
```



```dax
Refresh Detail Ratio = DIVIDE([Sum of refresh detail CPU] ,[Sum of Refresh detail Duration (s)])
```



```dax
Count of Refresh Detail Operations = COUNTROWS('Refresh_Detail')
```



```dax
Degradation Visual Slowest = IF(SELECTEDVALUE('Artifacts'[ArtifactKind],"Dataset")="Dataset",SUM('Performance_by_Artifact_and_Hour'[slowest_running_average]))
```



```dax
Count of throttled windows (Matrix) = 
VAR countOfWindows = CALCULATE( COUNTROWS('Throttled_by_Artifact_and_Hour'), TREATAS({SELECTEDVALUE('Artifacts'[ArtifactId])},'Artifacts (Throttled)'[ArtifactId]))
// RETURN 
//     if(not ISBLANK(countOfWindows), countOfWindows/2 ) //format(countOfWindows/2 ,  "0.0 mins" ))

// //Dynamic M1 Memory = 
VAR myOperationName = SELECTEDVALUE('Operation Names'[OperationName],"")
VAR myArtifactKind = SELECTEDVALUE('Artifacts'[ArtifactKind],"")
RETURN 
    SWITCH(
        TRUE(),
        myArtifactKind <> "Dataset" && myOperationName="" , blank(), // "------",
        myOperationName="" ,  divide(countOfWindows,2) 
        )


```



```dax
Count of throttled windows = 
VAR x = SELECTEDVALUE('Artifacts'[Artifact],"")
RETURN 
    IF(   
        x<>"",
        //CALCULATE(COUNTROWS('Throttled_by_Artifact_and_Hour') / 2,
        CALCULATE(
            COUNTROWS(
                    DISTINCT(
                        'Throttler_by_Artifact_and_Hour'[OperationStartTime]
                        )
                    ) / 2,
                TREATAS(FILTERS('Artifacts'[Artifact]),'Artifacts (Throttled)'[Artifact])
            ),

        COUNTROWS(DISTINCT(
                        'Throttler_by_Artifact_and_Hour'[OperationStartTime]
                        )) / 2
        
        )
```



```dax
Metric description = 
VAR selectedMetric = SELECTEDVALUE('Metrics'[Metric],"")
RETURN 
    SWITCH
        (
            selectedMetric ,
            "CPU" , "CPU shows the combined value in CPU seconds for any given operation." ,
            "Duration" , "The actual time taken to complete the operation." ,
            "Operations" , "The count of individual operations that took place" ,
            "Users" , "The distinct number of users who performed the operation." ,
            "This is a test"
            )
```



```dax
Dynamic Text for Matrix Title = "Artifacts (" & COUNTROWS(VALUES('Date and Time'[Date])) & " days)"
```



```dax
Dynamic Label Colour = 
VAR myTimeSpan = SELECTEDVALUE(Metrics_by_7_day[Time Span],"")
RETURN 
IF(myTimeSpan = "Last 7 days" ,"Red" , "Blue")
```



```dax
Autoscale Core Count = 
VAR m = MAX('Throttler_by_Artifact_and_Hour'[AutoScaleCoreCount])
RETURN 
    IF(m<0,0,m)
```



```dax
V-Cores = 
VAR CapacityCores = MIN('Capacities'[capacityNumberOfVCores])
VAR BackendCores = CapacityCores / 2
VAR CurrentMetric = MAX('Metrics_by_7_day'[max_cores])
VAR AutoScale = if(CurrentMetric <> BackendCores,(CurrentMetric - BackendCores) *  2 , 0) 
RETURN 
    CapacityCores + AutoScale
```



```dax
Count of Background Operations = COUNTROWS('TimePointBackgroundDetail')
```



```dax
Count of Interactive Operations = COUNTROWS('TimePointInteractiveDetail')
```



```dax
SKU CPU by TimePoint = 
VAR TimePoint = SELECTEDVALUE('TimePoints'[TimePoint])
VAR x = [xInteractive]
var y = [xBackground]
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail2'[BaseCoreCount]) 
    VAR AutoScaleCoreCount = MAX(TimePointCPUDetail2[AutoScaleCoreCount])
    RETURN (BaseCoreCount * 30) + IF(AutoScaleCoreCount>0,AutoScaleCoreCount*30)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN if(not isblank(x) || not isblank(y),CPU) 

```



```dax
SKU CPU by TimePoint short = 
VAR TimePoint = SELECTEDVALUE('TimePointCPUDetail'[WindowStartTime])
// VAR x = [xInteractive]
// var y = [xBackground]
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail'[BaseCoreCount]) 
    VAR AutoScaleCoreCount = MAX(TimePointCPUDetail[AutoScaleCoreCount])
    RETURN (BaseCoreCount * 30) + IF(AutoScaleCoreCount>0,AutoScaleCoreCount*30)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN CPU //if(not isblank(x) || not isblank(y),CPU) 

```



```dax
SKU CPU by TimePoint Timepoint Card = 
VAR TimePoint = SELECTEDVALUE('TimePoints'[TimePoint])
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail2'[BaseCoreCount]) 
    VAR AutoScaleCoreCount = MAX(TimePointCPUDetail2[AutoScaleCoreCount])
    RETURN (BaseCoreCount * 30) + IF(AutoScaleCoreCount>0,AutoScaleCoreCount*30)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN CPU

```



```dax
Count of Interactive Operations 2 = COUNTROWS('TimePointInteractiveDetail (2)')
```



```dax
Count of Background Operations 2 = COUNTROWS('TimePointBackgroundDetail (2)')
```



```dax
SKU CPU by TimePoint short 2 = 
VAR TimePoint = SELECTEDVALUE('TimePointCPUDetail (2)'[WindowStartTime])
// VAR x = [xInteractive]
// var y = [xBackground]
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail (2)'[BaseCoreCount]) 
    VAR AutoScaleCoreCount = MAX('TimePointCPUDetail (2)'[AutoScaleCoreCount])
    RETURN (BaseCoreCount * 30) + IF(AutoScaleCoreCount>0,AutoScaleCoreCount*30)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN CPU //if(not isblank(x) || not isblank(y),CPU) 
```



```dax
Count of throttler windows = 
VAR x = SELECTEDVALUE('Artifacts'[Artifact],"")
RETURN 
    IF(   
        x<>"",
            COUNTROWS(DISTINCT('Throttler_by_Artifact_and_Hour'[OperationStartTime])) / 2,
        
        // CALCULATE(
        //     COUNTROWS('Throttler_by_Artifact_and_Hour') / 2,
        //     TREATAS(FILTERS('Artifacts'[Artifact]),'Artifacts (Throttled)'[Artifact])
        //     ),
       COUNTROWS(DISTINCT('Throttler_by_Artifact_and_Hour'[OperationStartTime])) / 2
        )
```



```dax
SKU CPU by TimePoint % = 
VAR denominator = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail2'[BaseCoreCount]) 
    RETURN (BaseCoreCount * 30) 
VAR Numerator = 'All Measures'[SKU CPU by TimePoint]
RETURN Divide(Numerator, denominator)
```



```dax
xBackground % = 

VAR Numerator = TimePointCPUDetail2[xBackground]
VAR denominator = 'All Measures'[SKU CPU by TimePoint Basecore Only]
RETURN DIVIDE(Numerator,denominator)
```



```dax
xInteractive % = 
VAR Numerator = TimePointCPUDetail2[xInteractive]
VAR denominator = 'All Measures'[SKU CPU by TimePoint Basecore Only]
RETURN DIVIDE(Numerator,denominator)
```



```dax
SKU CPU by TimePoint short 2 % = 
VAR TimePoint = SELECTEDVALUE('TimePointCPUDetail (2)'[WindowStartTime])
// VAR x = [xInteractive]
// var y = [xBackground]
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail (2)'[BaseCoreCount]) * 30
    VAR AutoScaleCoreCount = MAX('TimePointCPUDetail (2)'[AutoScaleCoreCount])
    VAR ResultASSeconds = BaseCoreCount + IF(AutoScaleCoreCount>0,AutoScaleCoreCount*30)
    RETURN DIVIDE(ResultASSeconds,BaseCoreCount)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN CPU //if(not isblank(x) || not isblank(y),CPU) 
```



```dax
Sum of Timepoint Detail (2) CPU % = 
VAR nominator = SUM('TimePointCPUDetail (2)'[CpuTimeMs])
VAR denominator = [SKU CPU by TimePoint short 2]
RETURN divide(nominator,denominator)
```



```dax
SKU CPU by TimePoint short % = 
VAR TimePoint = SELECTEDVALUE('TimePointCPUDetail'[WindowStartTime])
// VAR x = [xInteractive]
// var y = [xBackground]
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail'[BaseCoreCount]) * 30
    VAR AutoScaleCoreCount = MAX('TimePointCPUDetail'[AutoScaleCoreCount])
    VAR ResultASSeconds = BaseCoreCount + IF(AutoScaleCoreCount>0,AutoScaleCoreCount*30)
    RETURN DIVIDE(ResultASSeconds,BaseCoreCount)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN CPU //if(not isblank(x) || not isblank(y),CPU) 
```



```dax
Sum of Timepoint Detail CPU % = 
VAR nominator = SUM('TimePointCPUDetail'[CpuTimeMs])
VAR denominator = [SKU CPU by TimePoint short]
RETURN divide(nominator,denominator)
```



```dax
SKU CPU by TimePoint Basecore Only = 
VAR TimePoint = SELECTEDVALUE('TimePoints'[TimePoint])
VAR x = [xInteractive]
var y = [xBackground]
VAR CPU = 
    VAR BaseCoreCount = MAX('TimePointCPUDetail2'[BaseCoreCount]) 
    VAR AutoScaleCoreCount = MAX(TimePointCPUDetail2[AutoScaleCoreCount])
    RETURN (BaseCoreCount * 30)

//MINX(ALL(Throttler_by_Artifact_and_Hour),MAX([MaxCpuMS]))
RETURN if(not isblank(x) || not isblank(y),CPU) 

```


## Table: Dates


```dax
CALENDAR(TODAY()-30, TODAY()+1)
```


## Table: Date and Time


```dax

	SELECTCOLUMNS(
		GENERATE(
			'Dates',
			GENERATESERIES(0,23)
			) ,
		"Date" 		 , [Date] ,
		"Hour Start" , [Date] + TIME([Value],	 0,0) ,
		"Hour End" 	 , [Date] + TIME([Value]   +1,0,0),
        "Hour Start Long" , [Date] + TIME([Value],	 0,0)
		)
```


## Table: Artifacts (Throttled)


```dax
Artifacts
```


## Table: Artifacts

### Measures:


```dax
Count of Artifacts = COUNTROWS('Artifacts')
```


## Table: 30_Second_Windows


```dax

VAR Seconds = SELECTCOLUMNS(GENERATESERIES(0,(60 * 60 * 24)-30 ,30),"Seconds",[Value])
RETURN 
    SELECTCOLUMNS(
        GENERATE(
            GENERATESERIES(TODAY()-21 , TODAY()) ,
            Seconds
        ),
    "OperationWindow" , [Value] + TIME(
                        int([Seconds]/3600), 
                        mod(int([Seconds]/60),60),
                        mod([Seconds],60)
                        ) ,
      "HourStart" , [Value] + TIME(
                        int([Seconds]/3600), 
                        mod(int([Seconds]/60),60),
                        0 //mod([Seconds],60)
                        )                      
    // "A" , [Value] ,
    // "X" , [seconds] ,

    // "S" , mod([Seconds],60) ,
    // "M" , mod(int([Seconds]/60),60) ,
    // "H" , int([Seconds]/3600)
    // )
    )
```


## Table: TimePoints

### Measures:


```dax
Filter Next = 
VAR OtherSlicerTimePoint = SELECTEDVALUE('timepoints'[timepoint])
VAR ThisSlicerTimePoint = SELECTEDVALUE('TimePoints2'[TimePoint])
RETURN 
//if(ThisSlicerTimePoint = OtherSlicerTimePoint + Time(0,0,30)   ,1)
IF(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,SECOND) = -30 , 1)
```



```dax
Filter Previous = 
VAR OtherSlicerTimePoint = SELECTEDVALUE('timepoints'[timepoint])
VAR ThisSlicerTimePoint = SELECTEDVALUE('TimePoints2'[TimePoint])
RETURN 
//if(ThisSlicerTimePoint = OtherSlicerTimePoint - Time(0,0,30)   ,1)
//IF(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,SECOND) = -30 , 1)
IF(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,SECOND) = 30 , 1)
```



```dax
Filter 60m = 
VAR OtherSlicerTimePoint = SELECTEDVALUE('timepoints'[timepoint])
VAR ThisSlicerTimePoint = SELECTEDVALUE('TimePoints2'[TimePoint])
RETURN 
//if(ThisSlicerTimePoint = OtherSlicerTimePoint - Time(0,0,30)   ,1)
//IF(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,SECOND) = -30 , 1)
IF(ABS(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,MINUTE)) <= 30 , 1)
```


## Table: TimePointBackgroundDetail

### Measures:


```dax
Background CPU Ratio = SUMX('TimePointBackgroundDetail',
    DIVIDE(CALCULATE(MIN(TimePointBackgroundDetail[Cpu (s)])) ,
    DATEDIFF(
        MIN('TimePointBackgroundDetail'[WindowStartTime]),
        MIN('TimePointBackgroundDetail'[WindowEndTime]),
        SECOND) / 30))
```



```dax
Background Pro Rata % = DIVIDE([Background CPU Ratio],[SKU CPU by TimePoint Timepoint Card])
```


## Table: TimePointInteractiveDetail

### Measures:


```dax
Interactive CPU Ratio = 
     SUMX(
         'TimePointInteractiveDetail',
            CALCULATE(
                MIN(TimePointInteractiveDetail[New Cpu (s)])
                )
            )
```



```dax
Interactive CPU Ratio % = DIVIDE([interactive CPU ratio],[SKU CPU by TimePoint Timepoint Card])
```


## Table: TimePointCPUDetail2

### Measures:


```dax
xBackground = 
VAR y = MAX('TimePointCPUDetail2'[Background])
VAR tp = SELECTEDVALUE('TimePoints'[TimePoint])
VAR df = HASONEVALUE('Dates'[Date])

VAR z =  MAX('TimePointCPUDetail2'[PeakHourBackground]) / 1000
RETURN 
    SWITCH(
        TRUE(),
        df, y ,
        z
        )
```



```dax
xInteractive = 
VAR x =[xBackground]
VAR y = MAX('TimePointCPUDetail2'[Interactive]) + IF(NOT ISBLANK(x) , 0)
VAR tp = SELECTEDVALUE('TimePoints'[TimePoint])
VAR df = HASONEVALUE('Dates'[Date])

VAR z =  MAX('TimePointCPUDetail2'[PeakHourInteractive]) / 1000

RETURN 
    SWITCH(
        TRUE(),
        df, y ,
        z
        )


```


## Table: Metrics_by_7_day

### Calculated Columns:


```dax
Time Span = 
SWITCH(
    Metrics_by_7_day[Weekly_Bucket] ,
    -7 ,  "Last 7 days" ,
    -14 , "Last 7 to 14 days" ,
    -21 , "Last 14 to 21 days" ,
          "Last 21 to 28 days"
)
```


## Table: TimePointBackgroundDetail (2)

### Measures:


```dax
Background CPU Ratio 2 = SUMX('TimePointBackgroundDetail (2)',
    DIVIDE(CALCULATE(MIN('TimePointBackgroundDetail (2)'[Cpu (s)])) ,
    DATEDIFF(
        MIN('TimePointBackgroundDetail (2)'[WindowStartTime]),
        MIN('TimePointBackgroundDetail (2)'[WindowEndTime]),
        SECOND) / 30))
```



```dax
Background Pro Rata % 2 = DIVIDE([Background CPU Ratio 2],[SKU CPU by TimePoint Timepoint Card])
```


## Table: TimePointInteractiveDetail (2)

### Measures:


```dax
Interactive CPU Ratio (2) = 
     SUMX(
         'TimePointInteractiveDetail (2)',
            CALCULATE(
                MIN('TimePointInteractiveDetail (2)'[New Cpu (s)])
                )
            )
```



```dax
Interactive CPU Ratio % 2 = DIVIDE([interactive CPU ratio (2)],[SKU CPU by TimePoint Timepoint Card])
```


## Table: TimePoints2

### Measures:


```dax
Filter Next 2 = 
VAR OtherSlicerTimePoint = SELECTEDVALUE('timepoints2'[timepoint])
VAR ThisSlicerTimePoint = SELECTEDVALUE('TimePoints'[TimePoint])
RETURN 
//if(ThisSlicerTimePoint = OtherSlicerTimePoint + Time(0,0,30)   ,1)
IF(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,SECOND) = -30 , 1)
```



```dax
Filter Prev 2 = 
VAR OtherSlicerTimePoint = SELECTEDVALUE('timepoints2'[timepoint])
VAR ThisSlicerTimePoint = SELECTEDVALUE('TimePoints'[TimePoint])
RETURN 
//if(ThisSlicerTimePoint = OtherSlicerTimePoint - Time(0,0,30)   ,1)
IF(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,SECOND) = 30 , 1)
```



```dax
Measure 2 = Not available
```



```dax
Filter 60min 2 = 
VAR OtherSlicerTimePoint = SELECTEDVALUE('timepoints2'[timepoint])
VAR ThisSlicerTimePoint = SELECTEDVALUE('TimePoints'[TimePoint])
RETURN 
//if(ThisSlicerTimePoint = OtherSlicerTimePoint - Time(0,0,30)   ,1)
IF(ABS(DATEDIFF(ThisSlicerTimePoint,OtherSlicerTimePoint,MINUTE)) <= 30 , 1)
```

