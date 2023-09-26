



# M Code

|Dataset|[Demo4HR](./../Demo4HR.md)|
| :--- | :--- |
|Workspace|[Demo4HR](../../Workspaces/Demo4HR.md)|

## Table: rep v_hr_employee


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Quelle{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Entfernte Spalten" = Table.RemoveColumns(rep_v_hr_employee,{"last_hire_date", "ter_max_date"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Entfernte Spalten", each ([work_location] = "BER" or [work_location] = "FRA" or [work_location] = "MUC")),
    #"Entfernte Spalten1" = Table.RemoveColumns(#"Gefilterte Zeilen",{"per_org", "cost_center_id", "platform_1_id", "platform_1_name", "platform_2_id", "platform_2_name", "fte", "platform_DACH_name", "cost_center", "phone", "supervisor_emp_id", "supervisor_full_name", "approver_emp_id", "approver_full_name", "phone_mobile", "name_prefix", "office", "title", "org_unit_id", "full_name_display", "nickname", "last_name_ad", "first_name_ad", "full_name_ad", "job_display_name", "jobcode_manager_level", "accounting_category", "country_code_iso2", "country_code_iso3", "work_location_name", "office_location_name", "gender", "empl_class_descr", "toe_id", "national_name", "middle_name", "maiden_name", "modify_date", "mentor_first_name", "job_category", "toe_description", "mentor_full_name", "fax", "region", "toe_id_ps", "accounting_cat", "email", "country_code", "job_start_date", "cc_id", "cc_name", "mentor_last_name", "pa_emp_id", "pa_emp_last_name"})
in
    #"Entfernte Spalten1"
```

