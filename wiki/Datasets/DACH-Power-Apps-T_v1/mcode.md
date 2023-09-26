



# M Code

|Dataset|[DACH Power Apps T_v1](./../DACH-Power-Apps-T_v1.md)|
| :--- | :--- |
|Workspace|[Samal_Test](../../Workspaces/Samal_Test.md)|

## Table: AR


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M711694\OneDrive - Roland Berger Holding GmbH\cash-management\WC Master Tracking File DACH_test v1.xlsx"), null, true),
    AR_Table = Source{[Item="AR",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(AR_Table,{{"CUSTOMER", type text}, {"PROJECT", type text}, {"FUNCTION", type text}, {"P/PRI", type text}, {"CUSTOMER_INVOICE_ID", type text}, {"INVOICE_DATE", Int64.Type}, {"NET_DUE_DATE_ADJUSTED", Int64.Type}, {"CONTRACTED_PAYMENT_TERMS", Int64.Type}, {"OPEN_AMOUNT", type number}, {"DAYS_OVERDUE", Int64.Type}, {"INVOICE_AGE", Int64.Type}, {"Provision % ", type number}, {"RECEIVABLE_COMPANY", type text}, {"LOCAL_CURRENCY", type text}, {"OPEN_AMOUNT_LC", type number}, {"Exp Date", type date}, {"EMPLOYEE_RESPONSIBLE_ID", type text}, {"EMPLOYEE_RESPONSIBLE", type text}, {"CUSTOMER_ID", Int64.Type}, {"PROJECT_ID", type text}, {"NET_DUE_DATE", type datetime}, {"AGE_CLUSTER", type text}, {"FEE_TOTAL_NET_VALUE", type any}, {"INC_EXP_TOTAL_NET_VALUE", type any}, {"NET_VALUE", type number}, {"TAX", type number}, {"TOTAL", type number}, {"FEE_TOTAL_NET_VALUE_LC", type any}, {"INC_EXP_TOTAL_NET_VALUE_LC", type any}, {"NET_VALUE_LC", type number}, {"TAX_LC", type number}, {"TOTAL_LC", type number}, {"TRANSACTION_CURRENCY", type text}, {"SOURCE", type any}, {"DUNNING_LEVEL", type any}, {"DUNNING_CREATED_ON", type any}, {"DUNNING_CURRENCY", type any}, {"DUNNING_BLOCK", type any}, {"DUNNING_BLOCK_NOTE", type any}, {"DUNNING_BLOCK_EXPIRATION_DATE", type any}, {"DUNNING_BLOCK_REASON_ID", type any}, {"DUNNING_BLOCK_REASON", type any}, {"HIGHEST_DUNNING_LEVEL", type any}, {"DUNNING_DATE", type any}, {"EMPLOYEE_RESPONSIBLE_COUNTRY", type any}, {"EMPLOYEE_RESPONSIBLE_STATUS", type any}, {"NEXT_DUNNING_INTERVAL", type any}, {"APROXIMATE_DUNNING_DATE", type any}, {"EMPLOYEE_RESPONSIBLE_COUNTRY_ISO2", type any}, {"EMPLOYEE_RESPONSIBLE_COUNTRY_ISO3", type any}, {"RECEIVABLE_COMPANY_ID", Int64.Type}, {"CUSTOMER_COUNTRY_ISO2", type any}, {"CUSTOMER_COUNTRY_ISO3", type any}, {"FUNCTIONAL_UNIT_RESPONSIBLE_ID", type any}, {"FUNCTIONAL_UNIT_RESPONSIBLE", type any}, {"EMPLOYEE_RESPONSIBLE_ID_OLD", type any}, {"EMPLOYEE_RESPONSIBLE_OLD", type any}, {"SALES_UNIT_ID", Int64.Type}, {"SALES_UNIT", type text}, {"FUNCTION_ID", type any}, {"INDUSTRY_ID", type any}, {"INDUSTRY", type any}, {"EMP_PLATFORM_ID", Int64.Type}, {"EMP_PLATFORM", type text}, {"TYPE(DP/AR)", type text}, {"CLEARED_AMOUNT_TC", Int64.Type}, {"CLEARED_AMOUNT_CURRENCY", type any}, {"CLEARED_AMOUNT_EUR", type any}, {"SAP_CUSTOMER_DOWN_PAYMENTS_Open.CANCELLATION_INVOICE_INDICATOR_ID", type logical}, {"SAP_CUSTOMER_DOWN_PAYMENTS_Open.PROJECT_ID", type text}, {"Unique_Project&Invoice_ID", type text}, {"Unique_3", type text}, {"Already in Maserlist", type text}})
in
    #"Changed Type"
```


## Table: WORK_IN_PROGRESS


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M711694\OneDrive - Roland Berger Holding GmbH\cash-management\WC Master Tracking File DACH_test v1.xlsx"), null, true),
    WORK_IN_PROGRESS_Table = Source{[Item="WORK_IN_PROGRESS",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(WORK_IN_PROGRESS_Table,{{"CUSTOMER", type text}, {"PROJECT", type text}, {"FUNCTION", type text}, {"P/PRI", type text}, {"PROJECT_ID", type text}, {"Adjusted(DP) Open WIP", Int64.Type}, {"PROJECT_STATUS", type text}, {"PROJECT_START", type date}, {"AGE_OF_WIP", Int64.Type}, {"PROJECT_FINISH", type date}, {"LAST_INVOICE_DATE", type date}, {"PROJECT_COMPANY", type text}, {"F&C Reponsible", type text}, {"LOCAL_CURRENCY", type text}, {"OPEN_WIP_LC", type number}, {"INVOICING_SUGGESTED", type text}, {"OPEN_WIP [EUR]", type number}, {"Total DOWNPAYMENTS (Open & Paid)", Int64.Type}, {"Already in Maserlist", type text}})
in
    #"Changed Type"
```

