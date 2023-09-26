



# M Code

|Dataset|[BCD Entry Exit last Month](./../BCD-Entry-Exit-last-Month.md)|
| :--- | :--- |
|Workspace|[Travel_Operations](../../Workspaces/Travel_Operations.md)|

## Table: Query_exit_entry


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="/****** Script for SelectTopNRows command from SSMS  ******/#(lf)SELECT 'exit' as info,#(lf)      [emp_id]#(lf)      ,[last_name]#(lf)      ,[first_name]#(lf)#(lf)      ,[jobcode]#(lf),[last_hire_date],[termination_date]#(lf)      ,[work_location]#(lf)#(lf)      ,[company]#(lf)      #(lf)  FROM [datahub].[rep].[v_hr_entry_exit_new] where year( termination_max_date) =  year(dateadd(MONTH, -1,getdate())) and#(lf)  month(termination_max_date) = month(dateadd(MONTH, -1,getdate()))#(lf)   and company_id in ('86', '12','01', '65','77','47','49', '48') and per_org = 'EMP' #(lf)#(lf)   union all #(lf)  /****** Script for SelectTopNRows command from SSMS  ******/#(lf)SELECT 'new entry ' as info,#(lf)      [emp_id]#(lf)      [emp_id]#(lf)      ,[last_name]#(lf)      ,[first_name]#(lf)#(lf)      ,[jobcode]#(lf),[last_hire_date],[termination_date]#(lf)      ,[work_location]#(lf)#(lf)      ,[company]#(lf)      #(lf)  FROM [datahub].[rep].[v_hr_entry_exit_new] where year( [last_hire_date]) =  year(dateadd(MONTH, -1,getdate())) and#(lf)  month([last_hire_date]) = month(dateadd(MONTH, -1,getdate()))#(lf)   #(lf)  and company_id in ('86', '12','01', '65','77','47','49', '48')   and per_org = 'EMP'  #(lf)#(lf)  "])
in
    Source
```

