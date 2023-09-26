



# DAX

|Dataset|[Cash Dispo](./../Cash-Dispo.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: RB_COMPANIES

### Calculated Columns:


```dax
Abbreveation = LOOKUPVALUE(MD_PARTNERS[INTERNET_ADDRESS], MD_PARTNERS[PARTNER_SHORT_NAME], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID])
```


## Table: ACTUAL_BALANCES

### Calculated Columns:


```dax
ACCOUNT_TYPE = LOOKUPVALUE('MD_BANK ACCOUNTS'[ACCOUNT_TYPE_NAME], 'MD_BANK ACCOUNTS'[SHORT_NAME], ACTUAL_BALANCES[SHORT_NAME])
```



```dax
PriviousDaySum = 
LOOKUPVALUE(ACTUAL_BALANCES[TOTAL_SUM], ACTUAL_BALANCES[Unique_Name_Datum], ACTUAL_BALANCES[Unique_Name&priviousDay])

```



```dax
Delta_Actual Balance between days = ACTUAL_BALANCES[TOTAL_SUM] - ACTUAL_BALANCES[PriviousDaySum]
```



```dax
CashPooling_RB_Total_Sum_EUR_NEG = 
SWITCH(
    True(),

    'MD_BANK ACCOUNTS'[Bank_Account_Selection] = "DB RBH EUR", LOOKUPVALUE(ACTUAL_BALANCES[TOTAL_SUM_EUR], ACTUAL_BALANCES[SHORT_NAME],"DB RB EUR", ACTUAL_BALANCES[DATUM],ACTUAL_BALANCES[DATUM]),
    'MD_BANK ACCOUNTS'[Bank_Account_Selection] = "UCB RBH EUR", LOOKUPVALUE(ACTUAL_BALANCES[TOTAL_SUM_EUR], ACTUAL_BALANCES[SHORT_NAME],"UCB RB EUR",ACTUAL_BALANCES[DATUM],ACTUAL_BALANCES[DATUM]),
0
)
```


## Table: MD_BANK ACCOUNTS

### Measures:


```dax
Bank_Account_Selection = SELECTEDVALUE('MD_BANK ACCOUNTS'[SHORT_NAME])
```


### Calculated Columns:


```dax
Entity_Country = LOOKUPVALUE(RB_COMPANIES[COUNTRY_ISO3], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID], 'MD_BANK ACCOUNTS'[TIS_CLIENT])
```


## Table: ACTUAl_CASH_FLOWS

### Calculated Columns:


```dax
Current_Month = if( MONTH(ACTUAl_CASH_FLOWS[VALUE_DATE]) = month(TODAY()-1), 1, 0)
```



```dax
Last_Workday = LOOKUPVALUE(ZZ_RollingCalender_Workdays[Last_Workday_Id], ZZ_RollingCalender[Date], ACTUAl_CASH_FLOWS[VALUE_DATE])
```



```dax
Current_Workday_Id = LOOKUPVALUE(ZZ_RollingCalender_Workdays[Current_Workday_Id], ZZ_RollingCalender[Date], ACTUAl_CASH_FLOWS[VALUE_DATE])
```



```dax
Is Latest CF_Date = 
VAR LatestDate = MAXX(FILTER(ACTUAl_CASH_FLOWS,ACTUAl_CASH_FLOWS[SHORT_NAME] = EARLIER(ACTUAl_CASH_FLOWS[SHORT_NAME])),ACTUAl_CASH_FLOWS[VALUE_DATE])

RETURN 
IF(AND(ACTUAl_CASH_FLOWS[VALUE_DATE]=LatestDate ,ACTUAl_CASH_FLOWS[STATUS] = 1),1,0)
```


## Table: ZZ_RollingCalender_Workdays

### Calculated Columns:


```dax
Date_Historicals = if(ZZ_RollingCalender_Workdays[Date] < today(), ZZ_RollingCalender_Workdays[Date], 0)
```



```dax
Last_Workday_Id = if(ZZ_RollingCalender_Workdays[Date_Historicals] = max(ZZ_RollingCalender_Workdays[Date_Historicals]), 1, 0)
```



```dax
Date_Today = if(ZZ_RollingCalender_Workdays[Date] < today()+1, ZZ_RollingCalender_Workdays[Date], 0)
```



```dax
Current_Workday_Id = if(ZZ_RollingCalender_Workdays[Date_Today] = max(ZZ_RollingCalender_Workdays[Date_Today]), 1, 0)
```


## Table: ZZ_DateLastRefresh

### Measures:


```dax
Last refersh PBi = SELECTEDVALUE(ZZ_DateLastRefresh[ZZ_DateLastRefresh])
```



```dax
Measure 2 = Now()-(8/24)
```


## Table: _LQ_Measure

### Measures:


```dax
CIB_EUR = 
        calculate(sum(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[TOTAL_SUM_EUR] > 0) +
        -CALCULATE(SUM(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[ACCOUNT_TYPE] = {"Blocked_Cash_included"})
```



```dax
CIB_LC = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]), ACTUAL_BALANCES[TOTAL_SUM] > 0)
```



```dax
CIB_EUR_k = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[TOTAL_SUM_EUR] > 0) / 1000
```



```dax
CF_EUR_k = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]))/1000
```



```dax
CF_EUR_NEG_k = - [CF_EUR_k]
```



```dax
CF_k = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT]))/1000
```



```dax
CF_MTD_EUR = 

Var PreviusWorkDay =   CALCULATE(MAX(ZZ_RollingCalender_Workdays[Date]),FILTER(ZZ_RollingCalender_Workdays,ZZ_RollingCalender_Workdays[Date] < TODAY()))
return
Calculate(SUM(ACTUAl_CASH_FLOWS[AMOUNT_EUR]),  DATESBETWEEN(ZZ_RollingCalender_Workdays[Date], DATE(YEAR(PreviusWorkDay),MONTH(PreviusWorkDay),1), PreviusWorkDay) )

/*CF_MTD_EUR = 

Var PreviusWorkDay =  CALCULATE(MAX(ZZ_RollingCalender_Workdays[Date]),FILTER(ZZ_RollingCalender_Workdays,ZZ_RollingCalender_Workdays[Date] < TODAY()))
return
Calculate(SUM(ACTUAl_CASH_FLOWS[AMOUNT_EUR]),  DATESBETWEEN(ZZ_RollingCalender_Workdays[Date], DATE(YEAR(PreviusWorkDay),MONTH(PreviusWorkDay),1), PreviusWorkDay) )"*/
```



```dax
CIB_Max_Date = max(ZZ_RollingCalender_Workdays[Date_Historicals])
```



```dax
Anc_Line_Usage_EUR = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[TOTAL_SUM_EUR] < 0)
```



```dax
CF_EUR_k_pos = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]), ACTUAl_CASH_FLOWS[AMOUNT_EUR] > {0}, ACTUAl_CASH_FLOWS[STATUS] <> 3, FILTER(ACTUAl_CASH_FLOWS,NOT([PAYMENT_REASON_ID] = 53 && [STATUS] = 5) ) )/ 1000
// Calculate all positive amounts in actual cash flows except : status 3 ( Cancelled ), filter not equal to cash pooling && Pre-reconcilated //

```



```dax
CF_EUR_k_neg = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]), ACTUAl_CASH_FLOWS[AMOUNT_EUR] < {0}, ACTUAl_CASH_FLOWS[STATUS] <> 3, FILTER(ACTUAl_CASH_FLOWS[PAYMENT_REASON_ID] <> 53 &&  ) / 1000
// Calculate all negative amounts in actual cash flows except status 3 (Cancelled ), and payment reason ID not equal to 41( cash pooling)   //)
```



```dax
AvFunds_FC_EUR_k = 
        CALCULATE([CIB_EUR_k], ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1})  + 
        CALCULATE([Anc_Line_Headroom_EUR_k], ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1}) 

        // Jan logic for payoutoverview FC balance
```



```dax
Anc_Line_Usage_EUR_k = [Anc_Line_Usage_EUR]/ 1000
```



```dax
Anc_Line_Available_EUR_k = CALCULATE(sum(Credit_Line_Ancillary[Amount]))/1000
```



```dax
Anc_Line_Headroom_EUR_k = [Anc_Line_Available_EUR_k] + [Anc_Line_Usage_EUR_k] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_Guarantees_IntLines_EUR_k] + [Credit_Line_FXbuffer_EUR_k]
```



```dax
AvL Funds_EUR_k = [CIB_EUR_k] + [Anc_Line_Headroom_EUR_k]
```



```dax
Credit_Line_available_RoW_EUR = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]))
```



```dax
Credit_Line_Usage_RoW_EUR = [Anc_Line_Usage_EUR]
```



```dax
AvLQ_RoW_EUR = [CIB_EUR] + [Restricted_Cash_EUR] + [Credit_Line_Headroom_RoW_EUR] 
```



```dax
Credit_Line_Headroom_RoW_EUR = [Credit_Line_available_RoW_EUR] + [Credit_Line_Usage_RoW_EUR]
```



```dax
AvLQ_RoW_EUR_k = [AvLQ_RoW_EUR] / 1000
```



```dax
CF_MTD_EUR_k = [CF_MTD_EUR]/ 1000
```



```dax
Neg_Interest_Threshold_EUR_k = CALCULATE(sum(LQ_Negative_Interest[Threshold])/1000)
```



```dax
Neg_Interest_Headroom_EUR_k = [Neg_Interest_Threshold_EUR_k] - [CIB_FC_EUR_k]
```



```dax
Credit_Line_Guarantees_EUR_k = -CALCULATE(sum(Credit_Line_Guarantees[Amount]),Credit_Line_Guarantees[Gurantee_Type] = {"Guarantees"}) / 1000
```



```dax
Credit_Line_Guarantees_IntLines_EUR_k = -CALCULATE(sum(Credit_Line_Guarantees[Amount]),Credit_Line_Guarantees[Gurantee_Type] = {"Guarantees for cash line"}) / 1000
```



```dax
Credit_Line_FXbuffer_EUR_k = -CALCULATE(sum(Credit_Line_Guarantees[Amount]),Credit_Line_Guarantees[Gurantee_Type] = {"Fx buffer"}) / 1000
```



```dax
RCF_Usage_EUR_k = -IFERROR(CALCULATE(sum(Credit_Line_RCF[Amount_EUR])),0)/1000
```



```dax
RCF+Anc_Headroom_EUR_k = [RCF+Anc_Line_Available_EUR_k] + [Credit_Line_Guarantees_IntLines_EUR_k] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_FXbuffer_EUR_k] + [RCF_Usage_EUR_k] + [Anc_Line_Usage_EUR_k] + [Cash_Reserve_EUR_k]
```



```dax
RCF+Anc_Line_Available_EUR_k = CALCULATE(sum('Credit_Line_Avl Credit Line'[Amount]), 'Credit_Line_Avl Credit Line'[Description] = {"Total amount RCF + Ancillary"}) / 1000
```



```dax
AvLQ_RBH_GER_EUR_k = [RCF+Anc_Line_Available_EUR_k] + [RCF_Usage_EUR_k] + [Anc_Line_Usage_EUR_k] + [CIB_EUR_k] + [Credit_Line_FXbuffer_EUR_k] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_Guarantees_IntLines_EUR_k] + [Cash_Reserve_EUR_k]
```



```dax
Restricted_Cash_EUR = 
        -CALCULATE(SUM(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[ACCOUNT_TYPE] = {"Blocked_Cash_seperate"}) + 
        -CALCULATE(SUM(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[ACCOUNT_TYPE] = {"Blocked_Cash_included"})
```



```dax
Restricted_Cash_EUR_k = [Restricted_Cash_EUR] / 1000
```



```dax
RCF+Anc+int_Headroom_EUR_k = 
            [RCF+Anc_Line_Available_EUR_k] + 
            [Credit_Line_Guarantees_IntLines_EUR_k] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_FXbuffer_EUR_k] + 
            [RCF_Usage_EUR_k] +
            [Cash_Reserve_EUR_k] +
            [Credit_Line_Headroom_RoW_EUR]/1000
```



```dax
Credit_Line_available_RoW_EUR_k = [Credit_Line_available_RoW_EUR] / 1000
```



```dax
AvLQ_Group_EUR_k = [RCF+Anc_Line_Available_EUR_k] + [RCF_Usage_EUR_k] + [Anc_Line_Usage_EUR_k]+ [CIB_EUR_k] + [Credit_Line_FXbuffer_EUR_k] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_Guarantees_IntLines_EUR_k] + [Credit_Line_available_RoW_EUR_k] + [Cash_Reserve_EUR_k]+0
```



```dax
CIB_FC_EUR_k = 
      CALCULATE([CIB_EUR_k], ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1})  + 
        CALCULATE([Anc_Line_Usage_EUR_k], ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1})  + 
        CALCULATE([CF_EUR_k], ZZ_RollingCalender_Workdays[Current_Workday_Id] = {1})
```



```dax
Account_Balance_EUR_k = [CIB_EUR_k] + [Anc_Line_Usage_EUR_k]
```



```dax
Account_Balance_LC_k = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]), ACTUAL_BALANCES[TOTAL_SUM] <> {0}) / 1000
```



```dax
Cash_Reserve_EUR_k = CALCULATE(sum(Credit_Line_Cash_Reserve[Amount])) / 1000
```



```dax
Mezzanine = -CALCULATE(sum(Credit_Line_Mezzanine_Financing[Amount]))
```



```dax
Mezzanine_EUR_k = [Mezzanine] / 1000
```



```dax
Term_Loan_EUR = -CALCULATE(sum('Credit_Line_Term Loan'[Amount]))
```



```dax
Term_Loan_EUR_k = [Term_Loan_EUR] / 1000
```



```dax
Total_Debt_EUR_k = [Term_Loan_EUR_k] + [Mezzanine_EUR_k] + [Anc_Line_Usage_EUR_k] + [RCF_Usage_EUR_k] + [Cash_Reserve_EUR_k]
```



```dax
Total_Net_Debt_EUR_k = [Total_Debt_EUR_k] + [CIB_EUR_k]
```



```dax
Total_Net_Debt_Chart_EUR_k = -[Total_Net_Debt_EUR_k]
```



```dax
Account_Balance_EUR = [CIB_EUR] + [Anc_Line_Usage_EUR]
```



```dax
Account_Balance_LC = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]), ACTUAL_BALANCES[TOTAL_SUM] <> {0})
```



```dax
CF_acc_EUR_k = CALCULATE( [CF_EUR_k] , FILTER(ALLSELECTED(ACTUAl_CASH_FLOWS), ACTUAl_CASH_FLOWS[VALUE_DATE] <= max(ACTUAl_CASH_FLOWS[VALUE_DATE]) && ACTUAl_CASH_FLOWS[VALUE_DATE] >= today()))

// FILTER(ALLSELECTED(ACTUAl_CASH_FLOWS[VALUE_DATE]), ACTUAl_CASH_FLOWS[VALUE_DATE] < max(ACTUAl_CASH_FLOWS[VALUE_DATE]) && ACTUAl_CASH_FLOWS[VALUE_DATE] > Min(ACTUAl_CASH_FLOWS[VALUE_DATE])))
// FILTER(ALL(ZZ_RollingCalender), ZZ_RollingCalender[Date] >= today() && ZZ_RollingCalender[Date] <= ZZ_RollingCalender[Date])
```



```dax
AvLQ_RCF_FC_EUR = ([AvL Funds_EUR_k] + [CF_acc_EUR_k]) * 1000
```



```dax
AvLQ_RCF_historic_EUR = CALCULATE([AvL Funds_EUR_k], FILTER(ZZ_RollingCalender_Workdays, ZZ_RollingCalender_Workdays[Date] < today())) * 1000
```



```dax
RCF_Target_Headroom = 'RCF Target Headroom'[RCF Target Headroom Value] * 1000000
```



```dax
AvLQ_RCF_2_FC_EUR = 

 
           CALCULATE([AvL Funds_EUR_k] * 1000, 
                  ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1}, 
                 FILTER(ALL(ZZ_RollingCalender_Workdays), ZZ_RollingCalender_Workdays[Date] < TODAY() + 365 ))  +
               ([CF_acc_EUR_k] * 1000)
              



    //    if ( max(ZZ_RollingCalender_Workdays[Date]) < max(ZZ_RollingCalender_Workdays[Date_Historicals]), 
    //            blank(), 
      //          CALCULATE([AvLQ_EUR_k], FILTER(ALLSELECTED(ZZ_RollingCalender_Workdays), ZZ_RollingCalender_Workdays[Date] = today()-1)) * 1000 +
        //        ([CF_acc_EUR_k] * 1000)
          //      ))
```



```dax
AvLQ_RCF_today_EUR = CALCULATE([AvL Funds_EUR_k], filter(ZZ_RollingCalender_Workdays, ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1}),filter(ZZ_RollingCalender_Workdays, ZZ_RollingCalender_Workdays[Date] <= max(ZZ_RollingCalender_Workdays[Date]))) * 1000
```



```dax
RCF_Headroom_EUR_k = [RCF+Anc_Line_Available_EUR_k] - [Anc_Line_Available_EUR_k] + [RCF_Usage_EUR_k]
```



```dax
RCF_Headroom_EUR = [RCF_Headroom_EUR_k] * 1000
```



```dax
External_CF_EUR_k_pos = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]), ACTUAl_CASH_FLOWS[AMOUNT_EUR] > {0}, ACTUAl_CASH_FLOWS[PAYMENT_REASON_ID] <> 53) / 1000
// Calculate all positive amounts in actual cash flows except : status 3 ( Cancelled ), PAyment reason ID 53( Cash pooling) //

```



```dax
Out_CF_EUR_k_neg = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]), ACTUAl_CASH_FLOWS[AMOUNT_EUR] < {0}, ACTUAl_CASH_FLOWS[PAYMENT_REASON_ID] <> 53 ) / 1000
// Calculate all negative amounts in actual cash flows except payment reason ID not equal to 41( cash pooling)   //
```



```dax
CF_EUR_k_neg_new = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]), ACTUAl_CASH_FLOWS[AMOUNT_EUR] < {0}, ACTUAl_CASH_FLOWS[STATUS] <> 3, FILTER(ACTUAl_CASH_FLOWS,NOT([PAYMENT_REASON_ID] = 53 && [STATUS] = 5) ) )/ 1000
// Calculate all negative amounts in actual cash flows except status 3 (Cancelled ), filter only not equal to cash pooling && Pre-reconcilated //))
```



```dax
CF_EUR_Sum = CALCULATE(sum(ACTUAl_CASH_FLOWS[AMOUNT_EUR]))
```



```dax
Delta_CIB_SumCF = [Account_Balance_EUR]- [CF_EUR_Sum]
```



```dax
Delta Delta_ActualBalance & SumCF_K = ABS(CALCULATE(SUM(ACTUAL_BALANCES[Delta_Actual Balance between days]) - CALCULATE(SUM(ACTUAl_CASH_FLOWS[AMOUNT]))))/1000
```



```dax
Delta_ AC Balance & STMNT Balance_K = ABS(CALCULATE(sum(ACTUAL_BALANCES[Delta_Actual Balance between days])- CALCULATE(SUM(DW_CM_STMNT[STMNT_BALANCE_SUM]))))/1000
```



```dax
AvLQ_RCF_2_FC_EUR_K = 

 
          ( CALCULATE([AvL Funds_EUR_k] * 1000, 
                  ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1}, 
                 FILTER(ALL(ZZ_RollingCalender_Workdays), ZZ_RollingCalender_Workdays[Date] < TODAY() + 365 ))  +
               ([CF_acc_EUR_k] * 1000))/ 1000
              



    //    if ( max(ZZ_RollingCalender_Workdays[Date]) < max(ZZ_RollingCalender_Workdays[Date_Historicals]), 
    //            blank(), 
      //          CALCULATE([AvLQ_EUR_k], FILTER(ALLSELECTED(ZZ_RollingCalender_Workdays), ZZ_RollingCalender_Workdays[Date] = today()-1)) * 1000 +
        //        ([CF_acc_EUR_k] * 1000)
          //      ))
```



```dax
AV Funds_k = If ( SELECTEDVALUE(ZZ_RollingCalender_Workdays[Date]) < TODAY(), [AvLQ_RCF_historic_EUR_K], [AvLQ_RCF_Future_EUR_K])
```



```dax
AvLQ_RCF_historic_EUR_K = CALCULATE([AvL Funds_EUR_k], FILTER(ZZ_RollingCalender_Workdays, ZZ_RollingCalender_Workdays[Date] < today()))
```



```dax
AvLQ_RCF_Future_EUR = CALCULATE([AvL Funds_EUR_k], FILTER(ZZ_RollingCalender_Workdays, ZZ_RollingCalender_Workdays[Date] >= today())) * 1000
```



```dax
AvLQ_RCF_Future_EUR_K = [AvLQ_RCF_Future_EUR]/1000
```



```dax
CIB_FC_EUR_k_NewS = 
       CALCULATE([CIB_EUR_k], ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1})  + 
       CALCULATE([Anc_Line_Usage_EUR_k], ZZ_RollingCalender_Workdays[Last_Workday_Id] = {1})  + 
       CALCULATE([CF_EUR_k_neg_new], ZZ_RollingCalender_Workdays[Current_Workday_Id] = {1}) +
       CALCULATE([CF_EUR_k_pos], ZZ_RollingCalender_Workdays[Current_Workday_Id] = {1}) 
      
```



```dax
Neg_Interest_Headroom_EUR_k_NewS = [Neg_Interest_Threshold_EUR_k] - [CIB_FC_EUR_k_NewS]
```



```dax
CIB_LC_last_workday = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]), ACTUAL_BALANCES[TOTAL_SUM] > 0, ZZ_RollingCalender_Workdays[Last_Workday_Id]= 1)
```



```dax
weekly Group LQ Delta = CALCULATE([AvLQ_Group_EUR_k],ZZ_RollingCalender[Date]= TODAY()-1) - CALCULATE([AvLQ_Group_EUR_k],ZZ_RollingCalender[Date]= TODAY()-8) 
```



```dax
weekly RoW LQ Delta = CALCULATE([AvLQ_Group_EUR_k],ZZ_RollingCalender[Date]= TODAY()-1) - CALCULATE([AvLQ_Group_EUR_k],ZZ_RollingCalender[Date]= TODAY()-8) 

// filter RoW entitiies manually 
```



```dax
CF_WTD_EUR = CALCULATE([CF_EUR_k],ZZ_RollingCalender[Date]= TODAY()-3) - CALCULATE([CF_EUR_k],ZZ_RollingCalender[Date]= TODAY()-10) 
```



```dax
CF_External_ Other Cash ins = CALCULATE([CF_EUR_k], ACTUAl_CASH_FLOWS[PAYMENT_REASON] = {"External Clents"})
```



```dax
AvLQ_Group_EUR_2021 = CALCULATE([AvLQ_Group_EUR_k_No Zero], FILTER(ZZ_RollingCalender, ZZ_RollingCalender[Date] >= DATE(2021,01,10) && ZZ_RollingCalender[Date] <= DATE(2022,01,02)), ZZ_RollingCalender[WeekDay_Number] = 7) *1000

// 2019-> 1st start sunday 01.01.2019( CW1)----- year end Sunday 29.12.2019(CW52)
// 2020-> 1st start sunday 05.01.2020( CW1)----- year end Sunday 03.01.2021(CW53)
// 2021-> 1st start sunday 10.01.2021( CW1)----- year end Sunday 02.01.2022(CW52)
```



```dax
AvLQ_Group_EUR_2020 = CALCULATE([AvLQ_Group_EUR_k_No Zero], FILTER(ZZ_RollingCalender, ZZ_RollingCalender[Date] >= DATE(2020,01,05) && ZZ_RollingCalender[Date] <= DATE(2021,01,03)), ZZ_RollingCalender[WeekDay_Number] = 7) *1000
// 2019-> 1st start sunday 01.01.2019( CW1)----- year end Sunday 29.12.2019(CW52)
// 2020-> 1st start sunday 05.01.2020( CW1)----- year end Sunday 03.01.2021(CW53)
// 2021-> 1st start sunday 10.01.2021( CW1)----- year end Sunday 02.01.2022(CW52)
```



```dax
AvLQ_Group_EUR_2019 = CALCULATE([AvLQ_Group_EUR_k_No Zero], FILTER(ZZ_RollingCalender, ZZ_RollingCalender[Date] >= DATE(2019,01,01) && ZZ_RollingCalender[Date] <= DATE(2019,12,29)), ZZ_RollingCalender[WeekDay_Number] = 7) *1000
// 2019-> 1st start sunday 01.01.2019( CW1)----- year end Sunday 29.12.2019(CW52)
// 2020-> 1st start sunday 05.01.2020( CW1)----- year end Sunday 03.01.2021(CW53)
// 2021-> 1st start sunday 10.01.2021( CW1)----- year end Sunday 02.01.2022(CW52)
```



```dax
AvLQ_Group_EUR_k_2018 = CALCULATE([AvLQ_Group_EUR_k], ZZ_RollingCalender[Year]= 2018)
```



```dax
AvLQ_Group_EUR_k_2021_weekly Delta = CALCULATE([AvLQ_Group_EUR_2021], ZZ_RollingCalender[Date] = TODAY()-1) - CALCULATE([AvLQ_Group_EUR_2021], ZZ_RollingCalender[Date] = TODAY()-8) 
```



```dax
Anc_Line_Usage_Local = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]), ACTUAL_BALANCES[TOTAL_SUM] < 0)
```



```dax
CIB_LC_last_workday_test = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]), ZZ_RollingCalender_Workdays[Last_Workday_Id]= 1)
```



```dax
AvLQ_OtherEntities_EUR_K = ([CIB_EUR] + [Restricted_Cash_EUR])/1000
```



```dax
Total_Net_Debt_chartEUR_K Q_ending = CLOSINGBALANCEQUARTER( [Total_Net_Debt_Chart_EUR_k], ZZ_RollingCalender[Date])
```



```dax
AvLQ_Group_EUR_k_Delta = CALCULATE([AvLQ_Group_EUR_k], ZZ_RollingCalender[Date]= TODAY()-2) - CALCULATE([AvLQ_Group_EUR_k],ZZ_RollingCalender[Date] = TODAY()-9)
```



```dax
CF_EUR_k_withZero = if(ISBLANK([CF_EUR_k]),0, [CF_EUR_k])
```



```dax
CP_balance_EUR_K = CALCULATE(SUM(RB_CP_CASH_POOL_BALANCES[VALUE_BALANCE] ) / 1000)
```



```dax
weekly NetDebt Delta = CALCULATE([Total_Net_Debt_EUR_k],ZZ_RollingCalender[Date]= TODAY()-1) - CALCULATE([Total_Net_Debt_EUR_k],ZZ_RollingCalender[Date]= TODAY()-8) 
```



```dax
CF_EUR_k_Weekly_Delta = CALCULATE(
CALCULATE([CP_balance_EUR_K],RB_CP_CASH_POOL_BALANCES[DATE]= (TODAY())-2 )- CALCULATE([CP_balance_EUR_K],RB_CP_CASH_POOL_BALANCES[DATE]= TODAY()-9 ))
```



```dax
RCF_Usage_EUR_k_ReplaceZero = if(ISBLANK([RCF_Usage_EUR_k]),0 , [RCF_Usage_EUR_k])
```



```dax
Anc_Line_Usage_EUR_k( Euro accounts) = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[TOTAL_SUM_EUR] < 0, FILTER('MD_BANK ACCOUNTS', 'MD_BANK ACCOUNTS'[CURRENCY] = "EUR" ))/ 1000
```



```dax
Anc_Line_Usage_EUR_k( Non Euro accounts) = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[TOTAL_SUM_EUR] < 0, ACTUAL_BALANCES[CURRENCY] = "USD" )/ 1000
```



```dax
Credit_Line_Headroom_RoW_EUR_K = [Credit_Line_Headroom_RoW_EUR]/1000
```



```dax
CIB_EUR_MTD_k = CALCULATE(TOTALMTD(SUM(ACTUAL_BALANCES[TOTAL_SUM_EUR]), ACTUAL_BALANCES[DATUM]),ALL(ZZ_RollingCalender[Date]))/1000
```



```dax
Anc_Line_Headroom_EUR_MTD_k = CALCULATE(TOTALMTD([Anc_Line_Headroom_EUR_k], ACTUAL_BALANCES[DATUM]),all(ZZ_RollingCalender[Date]))
```



```dax
AvL Funds_EUR_k_EuroAcount = CALCULATE([AvL Funds_EUR_k], 'MD_BANK ACCOUNTS'[CURRENCY]= "EUR")
```



```dax
AvL Funds_EUR_k_NonEuroAcount = CALCULATE([AvL Funds_EUR_k], 'MD_BANK ACCOUNTS'[CURRENCY] <> "EUR")
```



```dax
AvLQ_Group_EUR_k_No Zero = [RCF+Anc_Line_Available_EUR_k] + [RCF_Usage_EUR_k] + [Anc_Line_Usage_EUR_k]+ [CIB_EUR_k] + [Credit_Line_FXbuffer_EUR_k] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_Guarantees_IntLines_EUR_k] + [Credit_Line_available_RoW_EUR_k] + [Cash_Reserve_EUR_k]
```



```dax
Credit_Line_Guarantees_EUR_k_test = -CALCULATE(sum(Credit_Line_Guarantees[Amount]),Credit_Line_Guarantees[Gurantee_Type] = {"Guarantees"}, FILTER('MD_BANK ACCOUNTS','MD_BANK ACCOUNTS'[Euro and Non Euro] = "EUR AC" &&'MD_BANK ACCOUNTS'[Euro and Non Euro] = "Non EUR AC" )) / 1000
```



```dax
CIB_LC_K = [CIB_LC]/1000
```



```dax
Last Refresh = "Last Refresh- " & "PBi :"& ZZ_DateLastRefresh[Last refersh PBi] +2/24 & "  CIB :" & 'CIB LastRefresh'[Last Refresh CIB] 
```



```dax
AvLQ_Group_EUR_2022 = CALCULATE([AvLQ_Group_EUR_k_No Zero], FILTER(ZZ_RollingCalender, ZZ_RollingCalender[Date] >= DATE(2022,01,09) && ZZ_RollingCalender[Date] <= DATE(2023,01,01)), ZZ_RollingCalender[WeekDay_Number] = 7) *1000

// 2019-> 1st start sunday 01.01.2019( CW1)----- year end Sunday 29.12.2019(CW52)
// 2020-> 1st start sunday 05.01.2020( CW1)----- year end Sunday 03.01.2021(CW53)
// 2021-> 1st start sunday 10.01.2021( CW1)----- year end Sunday 02.01.2022(CW52)
// 2022-> 1st start sunday 09.01.2022( cw1)----- Yaer end Sunday 01.01.2023(CW)
```



```dax
culumn zero = "00000000"
```



```dax
CIB_EUR_k_Without_Value_ilter = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM_EUR])) / 1000
```



```dax
CIB_LC_Without_Value_Filter = calculate(sum(ACTUAL_BALANCES[TOTAL_SUM]))

//both negative and positive value
```



```dax
CIB_LC_K_Without_Value_Filter = [CIB_LC_Without_Value_Filter]/1000
```



```dax
Anc_Line_Usage_EUR__K_CashPoolingRB = 

IF(SELECTEDVALUE('MD_BANK ACCOUNTS'[CashPooling RB AC] )= 1,0,
        If(SELECTEDVALUE('MD_BANK ACCOUNTS'[CashPooing RBH AC])=1 && [CIB_EUR_CashPooling_SumX_k_Use for line usage] <0, [CIB_EUR_CashPooling_SumX_k_Use for line usage],
            [Anc_Line_Usage_EUR_k]
        )
)


```



```dax
CIB_EUR_CashPooling_k = 

SWITCH(
    TRUE(),
      SELECTEDVALUE('MD_BANK ACCOUNTS'[SHORT_NAME]) in
             {
               "DB RBH EUR","COBA RBH EUR","HSBC RBH EUR","LBBW RBH EUR","UCB RBH EUR"
             } ,            
             CALCULATE(If(CALCULATE([CIB_EUR_k] + [CashPooling_RB To RBH_k]) <0,0, CALCULATE([CIB_EUR_k] + [CashPooling_RB To RBH_k]))),
              [CIB_EUR_k]

)
```



```dax
CashPooling_RB To RBH_k = calculate(sum(ACTUAL_BALANCES[CashPooling_RB_Total_Sum_EUR_NEG]))/1000
```



```dax
Anc_Line_Headroom_EUR_CashPooaling_k = [Anc_Line_Available_EUR_k] + [Anc_Line_Usage_EUR__K_CashPoolingRB] + [Credit_Line_Guarantees_EUR_k] + [Credit_Line_Guarantees_IntLines_EUR_k] + [Credit_Line_FXbuffer_EUR_k]
```



```dax
AvL Funds_EUR_CashPooling_k = [CIB_EUR_k] + [Anc_Line_Headroom_EUR_CashPooaling_k]
```



```dax
CIB_EUR_CashPooling_SumX_k_ = 
SUMX(VALUES('MD_BANK ACCOUNTS'[SHORT_NAME]), [CIB_EUR_CashPooling_k])
```



```dax
CIB_EUR_CashPooling_k_use for line usage = 

SWITCH(
    TRUE(),
      SELECTEDVALUE('MD_BANK ACCOUNTS'[SHORT_NAME]) in
             {
               "DB RBH EUR","COBA RBH EUR","HSBC RBH EUR","LBBW RBH EUR","UCB RBH EUR"
             } ,            
             ([CIB_EUR_k] + [CashPooling_RB To RBH_k]),
              [CIB_EUR_k]

)
```



```dax
CIB_EUR_CashPooling_SumX_k_Use for line usage = 
SUMX(VALUES('MD_BANK ACCOUNTS'[SHORT_NAME]), [CIB_EUR_CashPooling_k_use for line usage])
```



```dax
AvLQ_Group_EUR_2023 = CALCULATE([AvLQ_Group_EUR_k_No Zero], FILTER(ZZ_RollingCalender, ZZ_RollingCalender[Date] >= DATE(2023,01,08) && ZZ_RollingCalender[Date] <= DATE(2023,12,31)), ZZ_RollingCalender[WeekDay_Number] = 7) *1000

/* 2019-> 1st start sunday 01.01.2019( CW1)----- year end Sunday 29.12.2019(CW52)
2020-> 1st start sunday 05.01.2020( CW1)----- year end Sunday 03.01.2021(CW53)
2021-> 1st start sunday 10.01.2021( CW1)----- year end Sunday 02.01.2022(CW52)
2022-> 1st start sunday 09.01.2022( cw1)----- Yaer end Sunday 01.01.2023(CW52)
2023-> 1st start sunday 08.01.2023( cw1)----- Yaer end Sunday 31.12.2023(CW52)*/
```



```dax
Date check = TODAY()-8
```



```dax
Last Refresh CIB text = "Last Refresh CIB- " & ": " & 'CIB LastRefresh'[Last Refresh CIB] 
```


## Table: _Title_Measure

### Measures:


```dax
Title_ Current_vs_last_FC_ = "CIB [Account Currency] by Zone, Bank Account and Date" & " : " & SELECTEDVALUE(ACTUAL_BALANCES[SHORT_NAME])
```



```dax
Delta1T = IF([Delta Delta_ActualBalance & SumCF_K] <> 0, _Title_Measure[Measure])
```



```dax
Measure = All('MD_BANK ACCOUNTS'[SHORT_NAME])
```


## Table: ZZ_RollingCalender

### Measures:


```dax
Current day = TODAY()
```



```dax
M.Date = 
VAR _MAX =
    MAX ( ZZ_RollingCalender[Date Hierarchy] )
VAR _MIN =
    MIN ( ZZ_RollingCalender[Date Hierarchy] )
VAR _Select =
    CALCULATE (
        MAX ( ZZ_RollingCalender[Date Hierarchy] ),
        FILTER ( ZZ_RollingCalender, ZZ_RollingCalender[Date Hierarchy]<= _MAX && ZZ_RollingCalender[Date Hierarchy] >= _MIN )
    )
VAR _Default =
    CALCULATE (
        MAX ( ZZ_RollingCalender[Date Hierarchy] ),
        FILTER ( ZZ_RollingCalender, ZZ_RollingCalender[Date Hierarchy] = TODAY () )
    )
RETURN
    IF ( ISFILTERED ( ZZ_RollingCalender[Date Hierarchy] ), _Select, _Default )
```


### Calculated Columns:


```dax
Week of Year_ISO 8601 = WEEKNUM(ZZ_RollingCalender[Date], 21 )
```



```dax
WeekDay_Number = WEEKDAY(ZZ_RollingCalender[Date],2)
```



```dax
Old_date = IF(ZZ_RollingCalender[Date] < ZZ_RollingCalender[Current day], 1, 0) 
```



```dax
Today_ID = if(ZZ_RollingCalender[Date]= TODAY(), 1, 0)
```


## Table: Credit_Line_RCF

### Calculated Columns:


```dax
FX_rate = LOOKUPVALUE(ACTUAL_FX_RATES[RATES_VALUE], ACTUAL_FX_RATES[DATUM], Credit_Line_RCF[Date], ACTUAL_FX_RATES[CURRENCY], Credit_Line_RCF[Currency])
```



```dax
Amount_EUR = Credit_Line_RCF[Amount] / Credit_Line_RCF[FX_rate]
```


## Table: Credit_Line_RoW

### Calculated Columns:


```dax
FX_Rate = LOOKUPVALUE(ACTUAL_FX_RATES[RATES_VALUE], ACTUAL_FX_RATES[DATUM], Credit_Line_RoW[Date], ACTUAL_FX_RATES[CURRENCY], Credit_Line_RoW[Currency])
```



```dax
Amount_EUR = Credit_Line_RoW[Amount] / Credit_Line_RoW[FX_Rate]
```


## Table: ACTUAL_FX_RATES

### Measures:


```dax
Daily Delta = CALCULATE(SUM(ACTUAL_FX_RATES[RATES_VALUE]),ACTUAL_BALANCES[DATUM]= SELECTEDVALUE(ACTUAL_BALANCES[DATUM]))- CALCULATE(SUM(ACTUAL_BALANCES[RATES_VALUE]),ACTUAL_BALANCES[DATUM]= (SELECTEDVALUE(ACTUAL_BALANCES[DATUM])-1))
```


## Table: RCF Target Headroom


```dax
GENERATESERIES(0, 25, 1)
```


### Measures:


```dax
RCF Target Headroom Value = SELECTEDVALUE('RCF Target Headroom'[RCF Target Headroom])
```


## Table: DW_CM_STMNT

### Calculated Columns:


```dax
Is Latest Statement_Date = 
VAR LatestDate = MAXX(FILTER(DW_CM_STMNT,DW_CM_STMNT[SHORT_NAME] = EARLIER(DW_CM_STMNT[SHORT_NAME])),DW_CM_STMNT[STMNT_STATEMENT_DATE])

RETURN 
IF(DW_CM_STMNT[STMNT_STATEMENT_DATE]=LatestDate,1,0)
```



```dax
Days_from_Last_STMNT = DATEDIFF(DW_CM_STMNT[STMNT_STATEMENT_DATE], TODAY(),DAY)
```


## Table: CIB LastRefresh

### Measures:


```dax
Last Refresh CIB = SELECTEDVALUE('CIB LastRefresh'[EXPORTED_ON])
```

