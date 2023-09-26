



# DAX

|Dataset|[LQ FC Dashboard_CM](./../LQ-FC-Dashboard_CM.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: FC_DATA

### Measures:


```dax
Current_Actual_Week = LOOKUPVALUE(FC_DATA[Week of Year], FC_DATA[ID_Current_FC], {1})
```


### Calculated Columns:


```dax
ID_Current_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ]), 1, 0)
```



```dax
ID_Last_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ])-1, 1, 0)
```



```dax
ID_2ndLast_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ])-2, 1, 0)
```



```dax
CONCERN_AMOUNT_K = FC_DATA[CONCERN_AMOUNT] / 1000
```



```dax
PLAN_VARIANT_ID_ADJ = if(FC_DATA[CLIENT_RATE_DATE] < TODAY(), FC_DATA[PLAN_VARIANT_ID], 0 )
```



```dax
FIRST_WEEK_FC_ID = if(FC_DATA[FC_START_DATE] = FC_DATA[PERIODE_DATE], 1, 0)
```



```dax
FC_START_DATE = LOOKUPVALUE(FC_PLANS[PLAN_START], FC_PLANS[PLAN_ID], FC_DATA[PLAN_VARIANT_ID])
```



```dax
DAYS_SINCE_FC_START = FC_DATA[PERIODE_DATE] - FC_DATA[FC_START_DATE]
```



```dax
ID_Last_FC_Overlapping_Period = if([ID_Last_FC] = 1 && FC_DATA[PERIODE_DATE] - FC_DATA[FC_START_DATE] > 6, 1, 0)
```



```dax
CW = LOOKUPVALUE(ZZ_RollingCalender[Year/calandarWeek(ISO)], ZZ_RollingCalender[Date], FC_DATA[PERIODE_DATE])
```



```dax
ID_3rdLast_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ])-3, 1, 0)
```



```dax
ID_4thLast_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ])-4, 1, 0)
```



```dax
ID_5thLast_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ])-5, 1, 0)
```



```dax
ID_6thLast_FC = IF(FC_DATA[PLAN_VARIANT_ID_ADJ] = max(FC_DATA[PLAN_VARIANT_ID_ADJ])-6, 1, 0)
```



```dax
Calander Week(ISO)_leadingZero = right("00" & LOOKUPVALUE(ZZ_RollingCalender[Calendar Week(ISO)], ZZ_RollingCalender[Date], FC_DATA[PERIODE_DATE]),2)
```



```dax
Year(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Year(ISO)], ZZ_RollingCalender[Date], FC_DATA[PERIODE_DATE])
```



```dax
YearWeekOfYear(leadingZero) = LOOKUPVALUE(ZZ_RollingCalender[YearCalandarWeek(ISO)_LeadingZero], ZZ_RollingCalender[Date], FC_DATA[PERIODE_DATE])
```


## Table: RB_COMPANIES

### Calculated Columns:


```dax
Title Column v1 = CONCATENATE("Cash out overview per Category : ", RB_COMPANIES[COUNTRY])
```


## Table: 1_Measure_FC

### Measures:


```dax
Cash-ins from clients_RFC_Total = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"receivables"},FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}) + calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"projects order"},FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}) + calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"new projects"},FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1})
```



```dax
CFI_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cfi"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] > {0})
```



```dax
CFF_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cff"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
FC_AvLQ_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID_2] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
CFOin_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash In"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
CFOout_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Out"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Total_CF_RFC = [CFOin_RFC] + [CFOout_RFC] + [CFF_RFC] + [CFI_RFC]
```



```dax
AvLQ_Start_RFC_Y1_2022 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {0}, FC_DATA[Year] = {2022}, FC_DATA[ID_Current_FC] = {1})
```



```dax
AvLQ_End_RFC = [AvLQ_Start_RFC_Y1_2022] + [Total_CF_RFC]
```



```dax
ARs = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"receivables"},FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {19})
```



```dax
Order books = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"order book"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
New Projects = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"new projects"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Salaries_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"from salaries"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Rent_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"rent"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Bonus_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"bonus (Total)"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Supplier_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Supplier_total"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Social Security_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"incidental wage"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
Tax_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"tax"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
IC rec_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Total IC receivables"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {19})
```



```dax
IC pay_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Total IC payables"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {19})
```



```dax
IC Dividends_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"IC Dividends"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, ABS(FC_DATA[ID_Current_FC] = {1}))
```



```dax
ID_Last_FC = MAXx(FC_DATA, FC_DATA[PLAN_VARIANT_ID]) -1
```



```dax
Bonus_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"bonus (Total)"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Bonus_Delta_FC = [Bonus_RFC] - [Bonus_RFC_LFC]
```



```dax
Cash-ins from clients_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"receivables"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Cash-ins from clients_RFC_Delta_FC = [ARs] - [Cash-ins from clients_RFC_LFC]
```



```dax
Cash-ins from order book_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"order book"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Cash-ins from order book_RFC_Delta_FC = [Order books] - [Cash-ins from order book_RFC_LFC]
```



```dax
Cash-ins from new projects_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"new projects"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Cash-ins from new projects_RFC_Delta = [New Projects] -[Cash-ins from new projects_RFC_LFC]
```



```dax
Rent_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"rent"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Rent_RFC_Delta = [Rent_RFC] - [Rent_RFC_LFC]
```



```dax
Salaries_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"from salaries"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Salaries_RFC_Delta = [Salaries_RFC]- [Salaries_RFC_LFC]
```



```dax
Social Security_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"incidental wage"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2021}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Social_Security_RFC_Delta = [Social Security_RFC] - [Social Security_RFC_LFC]
```



```dax
Supplier_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"supplier"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Supplier_RFC_Delta = [Supplier_RFC] - [Supplier_RFC_LFC]
```



```dax
Tax_2021_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"tax"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2021}, FC_DATA[ID_Last_FC] = {1})
```



```dax
Tax_RFC_Delta = [Tax_RFC] -[Tax_2021_LFC]
```



```dax
IC pay_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Total IC payables"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
IC pay_RFC_Delta = [IC pay_RFC] - [IC pay_RFC_LFC]
```



```dax
IC rec_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Total IC receivables"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
IC rec_RFC_Delta = [IC rec_RFC] - [IC rec_RFC_LFC]
```



```dax
CFF_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cff"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1})
```



```dax
CFF_RFC_Delta = [CFF_RFC] - [CFF_RFC_LFC]
```



```dax
FC_AvLQ_Y1_2021_2ndLFC = 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2021}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[ID_2ndLast_FC] = {1})
```



```dax
IC Loans_2021 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Loans to RBH"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2021}) + calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Loans from RBH"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2021})
```



```dax
IC Investments_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Investments RBH"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1})
```



```dax
FC_Amount_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {18}) 
```



```dax
FC_Amount_RFC_LFC_Overlapping = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1},FC_DATA[ID_Last_FC_Overlapping_Period] = {1}, FC_DATA[PERIOD_NR] < {19})
```



```dax
FC_Amount_RFC_Delta = [FC_Amount_RFC] - [FC_Amount_RFC_LFC_Overlapping]
```



```dax
FC_Amount_acc_RFC = calculate( 
                    [FC_Amount_RFC], 
                            filter (    ALLSELECTED(FC_DATA), 
                            FC_DATA[YearWeekOfYear(leadingZero)] <= max(FC_DATA[YearWeekOfYear(leadingZero)]) && 
                            FC_DATA[PLAN_VARIANT_ID] = max(FC_DATA[PLAN_VARIANT_ID])
                                    )
                            ) 
```



```dax
FC_Amount_acc_RFC_LFC = calculate( 
                    [FC_Amount_RFC_LFC_Overlapping],
                            filter (ALLSELECTED(FC_DATA), FC_DATA[YearWeekOfYear(leadingZero)] <= max(FC_DATA[YearWeekOfYear(leadingZero)]) && FC_DATA[PLAN_VARIANT_ID] = max(FC_DATA[PLAN_VARIANT_ID])-1)
                        )
```



```dax
FC_Amount_acc_RFC_Delta = [FC_Amount_acc_RFC] - [FC_Amount_acc_RFC_LFC]
```



```dax
AvLQ_Period_End_RFC = 
            if(
                isblank(calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {17}, FC_DATA[ID_Current_FC] = {1})), 
                
                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {0}, FC_DATA[PERIOD_NR] = {17}, FC_DATA[ID_Current_FC] = {1}),
                
                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {17}, FC_DATA[ID_Current_FC] = {1}))
```



```dax
AvLQ_Period_End_RFC_LFC = 

            if(
                isblank(calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {18}, FC_DATA[ID_Last_FC] = {1})), 

                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {0}, FC_DATA[PERIOD_NR] = {18}, FC_DATA[ID_Last_FC] = {1}), 

                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {18}, FC_DATA[ID_Last_FC] = {1}))
```



```dax
AvLQ_Period_End_RFC_Delta = [AvLQ_Period_End_RFC] - [AvLQ_Period_End_RFC_LFC]
```



```dax
AvLQ_Start_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1}, FC_DATA[FIRST_WEEK_FC_ID] = {1})
```



```dax
AvLQ_Start_RFC_Delta = [AvLQ_Start_RFC_Y1_2022] - [AvLQ_Start_RFC_LFC]
```



```dax
Cash-ins Other_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"other receivables"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
CFO_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cfo"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0})
```



```dax
CURRENT_FC_SHOR_NAME = LOOKUPVALUE(FC_DATA[PLAN_VARIANT_SHORT_NAME], FC_DATA[PLAN_VARIANT_ID_ADJ], max(FC_DATA[PLAN_VARIANT_ID_ADJ]))
```



```dax
FC_CP_Balance_RFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Weekbreak_ID_2] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
FC_CP_Balance_RFC_LFC_2022 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Last_FC] = {1}, FC_DATA[Year(ISO)] = {2022})
```



```dax
FC_CP_Balance_Y1_2021_2ndLFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"},FC_DATA[Year] = {2021},  FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_2ndLast_FC] = {1})
```



```dax
CP_Start_RFC = CALCULATE(sum(RB_CP_CASH_POOL_BALANCES[VALUE_BALANCE]), WEEKNUM(TODAY()) = RB_CP_CASH_POOL_BALANCES[CW], year(TODAY()) = RB_CP_CASH_POOL_BALANCES[Year],RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
CP_Start_Corima_RFC_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool Balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[FIRST_WEEK_FC_ID] = {1}, FC_DATA[ID_Last_FC] = {1})
```



```dax
CP_Period_End_Corima_RFC = 

                if(isblank(calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cash pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {17}, FC_DATA[ID_Current_FC] = {1})), 

                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cash pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {0}, FC_DATA[PERIOD_NR] = {17}, FC_DATA[ID_Current_FC] = {1}), 
                
                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cash pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {17}, FC_DATA[ID_Current_FC] = {1}))
```



```dax
CP_Period_End_Corima_RFC_LFC = 

               if( 
                   isblank(calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cash pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {18}, FC_DATA[ID_Last_FC] = {1})), 

                                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cash pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {0}, FC_DATA[PERIOD_NR] = {18}, FC_DATA[ID_Last_FC] = {1}), 

                                calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cash pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {18}, FC_DATA[ID_Last_FC] = {1})
                    )                                
```



```dax
CP_Period_End_Corima_RFC_2 = lookupvalue(FC_DATA[CONCERN_AMOUNT], FC_DATA[ID_Current_FC], {1}, FC_DATA[CATEGORY_SHORT_NAME], {"cash pool balance"}, FC_DATA[PERIOD_NR], max(FC_DATA[PERIOD_NR]))
```



```dax
CP_movement = calculate(sum(FC_DATA[CONCERN_AMOUNT]), FC_DATA[CATEGORY_SHORT_NAME] = {"CP_movement"},FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0},FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[PERIOD_NR] < {19})
```



```dax
CP_movement_acc = calculate([CP_movement], filter (ALLSELECTED(FC_DATA), FC_DATA[Week of Year] <= max(FC_DATA[Week of Year])&& FC_DATA[PLAN_VARIANT_ID] = max(FC_DATA[PLAN_VARIANT_ID])))
```



```dax
CP_End_RFC = [CP_Start_RFC] - [CP_movement_acc]
```



```dax
FC_ACTUAL_DELTA_RFC = 
   [Actual_Last_week] - [FC_AmountLastweek_LFC]
```



```dax
FC_Amount_RFC_Delta_m = ( [FC_Amount_RFC]  - [FC_Amount_RFC_LFC_Overlapping] ) / 1000000 
```



```dax
FC_ACTUAL_DELTA_RFC_m = 
        ([FC_ACTUAL_DELTA_RFC]) 
        / 1000000
```



```dax
FC_Incremental = [FC_Amount_RFC_Delta_m] + [FC_ACTUAL_DELTA_RFC_m]
```



```dax
FC_Amount_RFC_Delta_m_Table = if ( [FC_Amount_RFC_Delta_m] = 0, "-", FORMAT([FC_Amount_RFC_Delta_m],"0.0"))
```



```dax
FC_Amount_RFC_k = [FC_Amount_RFC]/1000
```



```dax
CP_AvLQ_2020_S = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Balance_2020],
    [User Selection] = "FRA (45000000)", [CP_Balance_2020],
    [User Selection] = "BEL (35000000)", [CP_Balance_2020],
    [User Selection] = "ITA (55000000)", [CP_Balance_2020], 
    [User Selection] = "AUT (65000000)", [CP_Balance_2020],
    [User Selection] = "ESP (80000000)", [CP_Balance_2020],
    [User Selection] = "PRT (70000000)", [CP_Balance_2020],
    [AvLQ_2020]
    )
```



```dax
User Selection = SELECTEDVALUE(RB_COMPANIES[Company_Slicer])
```



```dax
CP_AvLQ_2021_S = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Balance_2021],
    [User Selection] = "FRA (45000000)", [CP_Balance_2021],
    [User Selection] = "BEL (35000000)", [CP_Balance_2021],
    [User Selection] = "ITA (55000000)", [CP_Balance_2021], 
    [User Selection] = "AUT (65000000)", [CP_Balance_2021],
    [User Selection] = "ESP (80000000)", [CP_Balance_2021],
    [User Selection] = "PRT (70000000)", [CP_Balance_2021],
    [AvLQ_2021]
    )
```



```dax
CP_AvLQ_End_RFC_S = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [CP_End_RFC],
    [User Selection] = "FRA (45000000)", [CP_End_RFC],
    [User Selection] = "BEL (35000000)", [CP_End_RFC],
    [User Selection] = "ITA (55000000)", [CP_End_RFC], 
    [User Selection] = "AUT (65000000)", [CP_End_RFC],
    [User Selection] = "ESP (80000000)", [CP_End_RFC],
    [User Selection] = "PRT (70000000)", [CP_End_RFC],
    [AvLQ_End_RFC]
    )
```



```dax
FC_CP_AvLQ_RFC_2ndLFC_S = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_Y1_2021_2ndLFC], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [FC_AvLQ_Y1_2021_2ndLFC]
    )
```



```dax
CP_FC_AvLQ_RFC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_RFC],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_RFC],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_RFC],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_RFC], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_RFC],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_RFC],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_RFC],
    [FC_AvLQ_RFC]
    )
```



```dax
CP_FC_AvLQ_RFC_2ndLFC_S_Y2_2021 = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_Y1_2021_2ndLFC], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_Y1_2021_2ndLFC],
    [FC_AvLQ_Y1_2021_2ndLFC]
    )
```



```dax
CP_AvLQ_Start_RFC = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [CP_LQ_START],
    [User Selection] = "FRA (45000000)", [CP_LQ_START],
    [User Selection] = "BEL (35000000)", [CP_LQ_START],
    [User Selection] = "ITA (55000000)", [CP_LQ_START], 
    [User Selection] = "AUT (65000000)", [CP_LQ_START],
    [User Selection] = "ESP (80000000)", [CP_LQ_START],
    [User Selection] = "PRT (70000000)", [CP_LQ_START],
    ([AvLQ_Start_RFC_KPI] )
    )
```



```dax
CP_LQ_START = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Start_RFC],
    [User Selection] = "FRA (45000000)", [CP_Start_RFC],
    [User Selection] = "BEL (35000000)", [CP_Start_RFC],
    [User Selection] = "ITA (55000000)", [CP_Start_RFC], 
    [User Selection] = "AUT (65000000)", [CP_Start_RFC],
    [User Selection] = "ESP (80000000)", [CP_Start_RFC],
    [User Selection] = "PRT (70000000)", [CP_Start_RFC],
    [AvLQ_Start_RFC_Y1_2022]
    )
```



```dax
CP_LQ_END = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Period_End_Corima_RFC],
    [User Selection] = "FRA (45000000)", [CP_Period_End_Corima_RFC],
    [User Selection] = "BEL (35000000)", [CP_Period_End_Corima_RFC],
    [User Selection] = "ITA (55000000)", [CP_Period_End_Corima_RFC], 
    [User Selection] = "AUT (65000000)", [CP_Period_End_Corima_RFC],
    [User Selection] = "ESP (80000000)", [CP_Period_End_Corima_RFC],
    [User Selection] = "PRT (70000000)", [CP_Period_End_Corima_RFC],
    [AvLQ_Period_End_RFC]
    )
```



```dax
CP_LQ_START_LFC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Start_Corima_RFC_LFC],
    [User Selection] = "FRA (45000000)", [CP_Start_Corima_RFC_LFC],
    [User Selection] = "BEL (35000000)", [CP_Start_Corima_RFC_LFC],
    [User Selection] = "ITA (55000000)", [CP_Start_Corima_RFC_LFC], 
    [User Selection] = "AUT (65000000)", [CP_Start_Corima_RFC_LFC],
    [User Selection] = "ESP (80000000)", [CP_Start_Corima_RFC_LFC],
    [User Selection] = "PRT (70000000)", [CP_Start_Corima_RFC_LFC],
    [AvLQ_Start_RFC_LFC]
    )
```



```dax
CP_LQ_END_LFC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Period_End_Corima_RFC_LFC],
    [User Selection] = "FRA (45000000)", [CP_Period_End_Corima_RFC_LFC],
    [User Selection] = "BEL (35000000)", [CP_Period_End_Corima_RFC_LFC],
    [User Selection] = "ITA (55000000)", [CP_Period_End_Corima_RFC_LFC], 
    [User Selection] = "AUT (65000000)", [CP_Period_End_Corima_RFC_LFC],
    [User Selection] = "ESP (80000000)", [CP_Period_End_Corima_RFC_LFC],
    [User Selection] = "PRT (70000000)", [CP_Period_End_Corima_RFC_LFC],
    [AvLQ_Period_End_RFC_LFC]
    )
```



```dax
FC_Amount_acc_RFC_2ndLFC = calculate( 
                    [FC_Amount_RFC_2ndLFC], 
                            filter (ALLSELECTED(FC_DATA), FC_DATA[Week of Year] <= max(FC_DATA[Week of Year]) && FC_DATA[PLAN_VARIANT_ID] = max(FC_DATA[PLAN_VARIANT_ID])-2)
                        )
```



```dax
FC_Amount_RFC_2ndLFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_2ndLast_FC] = {1},FC_DATA[PERIOD_NR] > {1}, FC_DATA[PERIOD_NR] < {19})
```



```dax
FC_Amount_RFC_Last_Delta_m = ([FC_Amount_RFC_LFC_Overlapping] - [FC_Amount_RFC_2ndLFC]) / 1000000 
```



```dax
FC_ACTUAL_2ndLAST_DELTA_RFC_m = 
        (
            calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[2nd_last_Actuals_ID]=1) 
            -
            calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_2ndLast_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1})
        ) 
        / 1000000
```



```dax
FC_Incremental_Last = [FC_Amount_RFC_Last_Delta_m] + [FC_ACTUAL_2ndLAST_DELTA_RFC_m]
```



```dax
FC_Amount_Details_RFC_k = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {19}) / 1000
```



```dax
End_of_FC = LOOKUPVALUE(FC_DATA[Week of Year], FC_DATA[ID_Last_FC_Overlapping_Period], {1})
```



```dax
FC_Amount_RFC_LFC_k = [FC_Amount_RFC_LFC_Overlapping]/1000
```



```dax
FC_Amount_RFC_LFC_Full_K = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1}, FC_DATA[PERIOD_NR] <= {18})/1000
```



```dax
FC_CP_Balance_RFC_LFC_2023 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Last_FC] = {1}, FC_DATA[Year(ISO)] = {2023})
```



```dax
FC_Amount_Y2_2022 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year] = {2022}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {18})
```



```dax
FC_CP_Balance_RFC_LFC_test = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID_2] = {1},FC_DATA[ID_Last_FC] = {1})
```



```dax
FC_AvLQ_RFC_LFC = 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true} ,FC_DATA[Weekbreak_ID_2] = {1}, FC_DATA[ID_Last_FC] = {1})

// weekbreak_ID chenged to weekbreak_ID_2 to avoid 27.12.2021 missing date. Later it can change or also can use weekbreak_ID_2 
```



```dax
CP_FC_AvLQ_RFC_LFC_S = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_RFC_LFC_test],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_RFC_LFC_test],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_RFC_LFC_test],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_RFC_LFC_test], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_RFC_LFC_test],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_RFC_LFC_test],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_RFC_LFC_test],
    [FC_AvLQ_RFC_LFC]
    )
```



```dax
CP_FC_AvLQ_Y1_2023 = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_2023],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_2023],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_2023],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_2023], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_2023],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_2023],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_2023],
    [FC_AvLQ_Y1_2023]
    )
```



```dax
CP_FC_AvLQ_Y2_2022 = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_2022],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_2022],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_2022],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_2022], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_2022],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_2022],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_2022],
    [FC_AvLQ_Y2_2022]
    )
```



```dax
CP_FC_AvLQ_RFC_LFC_S_Y2_2022 = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_RFC_LFC_2022],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_RFC_LFC_2022],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_RFC_LFC_2022],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_RFC_LFC_2022], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_RFC_LFC_2022],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_RFC_LFC_2022],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_RFC_LFC_2022],
    [FC_AvLQ_RFC_LFC_2022]
    )
```



```dax
FC_AvLQ_RFC_LFC_2022 = 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year(ISO)] = {2022}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[ID_Last_FC] = {1})
```



```dax
FC_AvLQ_Y2_2022 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year(ISO)] = {2022}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
FC_CP_Balance_2022 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Current_FC] = {1},FC_DATA[Year(ISO)] = {2022})
```



```dax
FC_AvLQ_Y1_2023 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year(ISO)] = {2023}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
FC_CP_Balance_2023 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year(ISO)] = {2023},FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
CP_FC_AvLQ_RFC_LFC_S_Y1_2023 = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_RFC_LFC_2023],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_RFC_LFC_2023],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_RFC_LFC_2023],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_RFC_LFC_2023], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_RFC_LFC_2023],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_RFC_LFC_2023],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_RFC_LFC_2023],
    [FC_AvLQ_RFC_LFC_2023]
    )
```



```dax
FC_AvLQ_RFC_LFC_2023 = 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year(ISO)] = {2023}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[ID_Last_FC] = {1})
```



```dax
CP_FC_AvLQ_2021 = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_2023],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_2023],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_2023],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_2023], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_2023],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_2023],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_2023],
    [AvLQ_2021]
    )
```



```dax
LQ Delta = ABS([CP_AvLQ_2021_S]-[CP_FC_AvLQ_Y1_2023])
```



```dax
FC_CP_Balance_Y2_2022_2ndLFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"Cash Pool balance"},FC_DATA[Year] = {2022},  FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_2ndLast_FC] = {1})
```



```dax
FC_AvLQ_Y2_2022_2ndLFC = 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2022}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[ID_2ndLast_FC] = {1})
```



```dax
CP_FC_AvLQ_RFC_2ndLFC_S_Y2_2022 = 
SWITCH(
    	TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_Y2_2022_2ndLFC],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_Y2_2022_2ndLFC],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_Y2_2022_2ndLFC],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_Y2_2022_2ndLFC], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_Y2_2022_2ndLFC],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_Y2_2022_2ndLFC],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_Y2_2022_2ndLFC],
    [FC_AvLQ_Y2_2022_2ndLFC]
    )
```



```dax
AvLQ_Start_RFC_KPI = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PERIOD_NR] = {0}, FC_DATA[ID_Current_FC] = {1})
```



```dax
Delta_LQ_Actual_FC Start = ABS([CP_AvLQ_2023_S]- [CP_FC_AvLQ_Y1_2023])
```



```dax
CP_AvLQ_2021_S_LC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Balance_2021],
    [User Selection] = "FRA (45000000)", [CP_Balance_2021],
    [User Selection] = "BEL (35000000)", [CP_Balance_2021],
    [User Selection] = "ITA (55000000)", [CP_Balance_2021], 
    [User Selection] = "AUT (65000000)", [CP_Balance_2021],
    [User Selection] = "ESP (80000000)", [CP_Balance_2021],
    [User Selection] = "PRT (70000000)", [CP_Balance_2021],
    [AvLQ_2021_LC]
    )
```



```dax
FC_AvLQ_Y1_2021_LC = calculate(sum(FC_DATA[AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year] = {2021}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
CP_FC_AvLQ_Y1_2021_LC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_2023],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_2023],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_2023],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_2023], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_2023],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_2023],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_2023],
    [FC_AvLQ_Y1_2021_LC]
    )
```



```dax
Delta_LQ_Actual_FC Start_LC = ABS([CP_AvLQ_2023_S_LC]- [CP_FC_AvLQ_Y1_2023_LC])
```



```dax
CP_AvLQ_2022_S = CALCULATE(
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Balance_2022],
    [User Selection] = "FRA (45000000)", [CP_Balance_2022],
    [User Selection] = "BEL (35000000)", [CP_Balance_2022],
    [User Selection] = "ITA (55000000)", [CP_Balance_2022], 
    [User Selection] = "AUT (65000000)", [CP_Balance_2022],
    [User Selection] = "ESP (80000000)", [CP_Balance_2022],
    [User Selection] = "PRT (70000000)", [CP_Balance_2022],
    [AvLQ_2022]
     
    ), FILTER(ZZ_RollingCalender,ZZ_RollingCalender[Date] <> DATE(2022,01,01) && ZZ_RollingCalender[Date] <> DATE(2022,01,02)  ))
```



```dax
CP_AvLQ_2023_S_LC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Balance_2023],
    [User Selection] = "FRA (45000000)", [CP_Balance_2023],
    [User Selection] = "BEL (35000000)", [CP_Balance_2023],
    [User Selection] = "ITA (55000000)", [CP_Balance_2023], 
    [User Selection] = "AUT (65000000)", [CP_Balance_2023],
    [User Selection] = "ESP (80000000)", [CP_Balance_2023],
    [User Selection] = "PRT (70000000)", [CP_Balance_2023],
    [AvLQ_2023_LC]
    )
```



```dax
FC_AvLQ_Y1_2023_LC = calculate(sum(FC_DATA[AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true},FC_DATA[Year] = {2023}, FC_DATA[Weekbreak_ID] = {1},FC_DATA[ID_Current_FC] = {1})
```



```dax
CP_FC_AvLQ_Y1_2023_LC = 
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [FC_CP_Balance_2023],
    [User Selection] = "FRA (45000000)", [FC_CP_Balance_2023],
    [User Selection] = "BEL (35000000)", [FC_CP_Balance_2023],
    [User Selection] = "ITA (55000000)", [FC_CP_Balance_2023], 
    [User Selection] = "AUT (65000000)", [FC_CP_Balance_2023],
    [User Selection] = "ESP (80000000)", [FC_CP_Balance_2023],
    [User Selection] = "PRT (70000000)", [FC_CP_Balance_2023],
    [FC_AvLQ_Y1_2023_LC]
    )
```



```dax
Negative AVLQ Risk RFC = If([CP_FC_AvLQ_RFC] > 100000, Blank(), [CP_FC_AvLQ_RFC])  
```



```dax
Column width CF = "00000000" 
```



```dax
Columns_Zero = "00.0" 
```



```dax
FC_Amount_RFC_Delta_forSorting = ABS([FC_Amount_RFC] - [FC_Amount_RFC_LFC_Overlapping])
```



```dax
FC_AmountLastweek_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1})
```



```dax
FC_ACTUAL_DELTA_RFC_sort_ABS = ABS(

    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[Current_Actuals_ID]) - 

calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Last_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1}))
```



```dax
FC_Amount_LFC_for_FC over FC = If(SELECTEDVALUE('ZZ_RollingCalendar for FC over FC with Last Actual week'[CW_ISO]) = WEEKNUM(TODAY(),21)-1,[FC_AmountLastweek_LFC], [FC_Amount_RFC_LFC_Overlapping])
```



```dax
FC_Amount_Rolling_FC Over FC_Last actual+CurrentFC = 

If( SELECTEDVALUE('ZZ_RollingCalendar for FC over FC with Last Actual week'[CW_ISO] )= WEEKNUM(TODAY(),21)-1,[Actual_Last_week], [FC_Amount_RFC])

```



```dax
FC_Amount_RFC_Last_Delta = ([FC_Amount_RFC_LFC_Overlapping] - [FC_Amount_RFC_2ndLFC])
```



```dax
FC_ACTUAL_3ndLAST_DELTA_RFC_m = 
        (
            calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[3rd_Last_Actuals_ID]=1) 
            -
            calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_3rdLast_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1})
        ) 
        / 1000000
```



```dax
FC_ACTUAL_4ndLAST_DELTA_RFC_m = 
        (
            calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[4th_Last_Actuals_ID]=1) 
            -
            calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_4thLast_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1})
        ) 
        / 1000000
```



```dax
FC_ACTUAL_5thLAST_DELTA_RFC_m = 
        (
            calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[5th_Last_Actuals_ID]=1) 
            -
            calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_5thLast_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1})
        ) 
        / 1000000
```



```dax
FC_ACTUAL_6thLAST_DELTA_RFC_m = 
        (
            calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[6th_Last_Actuals_ID]= 1) 
            -
            calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_6thLast_FC] = {1}, FC_DATA[DAYS_SINCE_FC_START]< {7},FC_DATA[DAYS_SINCE_FC_START] > {-1})
        ) 
        / 1000000
```



```dax
CP_avLQ_Start_RFC_k = '1_Measure_FC'[CP_AvLQ_Start_RFC]/1000
```



```dax
Company_name_Card = IF(ISFILTERED(RB_COMPANIES[Company_Slicer]),FIRSTNONBLANK(RB_COMPANIES[ACCOUNT],RB_COMPANIES[ACCOUNT]),"RBH")
```



```dax
FC_Amount_RFC_ExternalCash-ins = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {18}, FC_DATA[CATEGORY_SHORT_NAME]= {"External Cash-ins"}
) 
```



```dax
CIB last monday_Cash out = ([CIB as of Current week Monday]+ '1_Measure_FC'[FC_Amount_RFC_Cash Out])/1000000
```



```dax
FC_Amount_RFC_Cash Out = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[ID_Current_FC] = {1}, FC_DATA[PERIOD_NR] > {0}, FC_DATA[PERIOD_NR] < {18}, FC_DATA[CATEGORY_SHORT_NAME]= {"Cash out"})
```



```dax
CP_AvLQ_2023_S = CALCULATE(
SWITCH(
    TRUE(),
    [User Selection] = "NLD (64000000)", [CP_Balance_2023],
    [User Selection] = "FRA (45000000)", [CP_Balance_2023],
    [User Selection] = "BEL (35000000)", [CP_Balance_2023],
    [User Selection] = "ITA (55000000)", [CP_Balance_2023], 
    [User Selection] = "AUT (65000000)", [CP_Balance_2023],
    [User Selection] = "ESP (80000000)", [CP_Balance_2023],
    [User Selection] = "PRT (70000000)", [CP_Balance_2023],
    [AvLQ_2023]
     
    ), FILTER(ZZ_RollingCalender,ZZ_RollingCalender[Date] <> DATE(2023,01,01) ))
```



```dax
FC_AvLQ_FC over FC = If(SELECTEDVALUE('ZZ_RollingCalendar for FC over FC with Last Actual week'[CW_ISO]) = WEEKNUM(TODAY(),21)-1,[CP_FC_AvLQ_Y1_2023],[CP_FC_AvLQ_RFC])
```



```dax
FC_AVLQ_LFC_for_FC over FC = If(SELECTEDVALUE('ZZ_RollingCalendar for FC over FC with Last Actual week'[CW_ISO]) = WEEKNUM(TODAY(),21)-1,[CP_FC_AvLQ_RFC_LFC_S], [CP_FC_AvLQ_RFC_LFC_S])
```



```dax
FC month start AvLQ = CALCULATE([CP_FC_AvLQ_RFC],
                    Filter(STARTOFMONTH(ZZ_RollingCalender[Date])))
```



```dax
Month start CP_FC_AvLQ_RFC = CALCULATE([CP_FC_AvLQ_RFC], FILTER(ZZ_RollingCalender,ZZ_RollingCalender[first day of month_ID]=1))
```



```dax
Montly Average CP_FC_AvLQ_RFC = AVERAGEX(VALUES(ZZ_RollingCalender[Date_short]), [CP_FC_AvLQ_RFC])
```



```dax
FC_Cash out OP (Salary,Rent,Suppler,Tax) = CALCULATE([FC_Amount_RFC],ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_DATA,FC_DATA[CATEGORY_SHORT_NAME] in {
"from salaries",
"incidental wage",
"Rent",
"Supplier_total",
"Tax"
}


    ))
```



```dax
FC_Cash out OP+INV (Exlu Bonus,IC) = CALCULATE([FC_Amount_RFC],ALLSELECTED(ZZ_RollingCalender[Date]),  

filter(FC_DATA,FC_DATA[CATEGORY_SHORT_NAME] in { 

"from salaries", 

"incidental wage", 

"Rent", 

"Supplier_total", 

"Tax", 

"CFI" 

} 

 
 
 

)) 

 
```



```dax
FC_Cash out OP+INV(incl Bonus, Excl IC) = CALCULATE([FC_Amount_RFC],ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_DATA,FC_DATA[CATEGORY_SHORT_NAME] in {
"from salaries",
"incidental wage",
"Rent",
"Supplier_total",
"Tax",
"Bonus (Total)",
"CFI"
}


    ))
```



```dax
FC_Cash out OP+INV (all CF) = CALCULATE([FC_Amount_RFC],ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_DATA,FC_DATA[CATEGORY_SHORT_NAME] in {
"Cash out",
"CFI"
}


    ))
```



```dax
Historical Actual Measure = CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]))
```



```dax
Historical Actual & FC = 
switch(
    true(),
   [Month Selection] < Month(TODAY()), [Historical Actual Measure],
   ([Historical Actual Measure] + [FC_Amount_RFC])
   
   )
```



```dax
Month Selection = SELECTEDVALUE(ZZ_RollingCalender[Month])
```


## Table: ACTUAL_BALANCES_Monday

### Calculated Columns:


```dax
current week Monday_ID = if(ACTUAL_BALANCES_Monday[DATUM]= ACTUAL_BALANCES_Monday[Current week Monday], 1,0)
```



```dax
Amount 7 days before = LOOKUPVALUE(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR], ACTUAL_BALANCES_Monday[DATUM], ACTUAL_BALANCES_Monday[Date 7 days before], ACTUAL_BALANCES_Monday[ACCOUNT_ID], ACTUAL_BALANCES_Monday[ACCOUNT_ID])
```



```dax
Date 7 days before = ACTUAL_BALANCES_Monday[DATUM]-7
```



```dax
Amount EUR different 7 days = ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]-  ACTUAL_BALANCES_Monday[Amount 7 days before] 
```


## Table: ZZ_RollingCalender

### Calculated Columns:


```dax
CW = if(WEEKNUM(ZZ_RollingCalender[Date],2) - 1 = {0}, blank(), WEEKNUM(ZZ_RollingCalender[Date],2) - 1)
```



```dax
Year_CW_long = ZZ_RollingCalender[Year] & "/" & ZZ_RollingCalender[CW]
```



```dax
Calendar Week(ISO) = WEEKNUM(ZZ_RollingCalender[Date],21) 
```



```dax
Year/calandarWeek(ISO) = CONCATENATE(
    ZZ_RollingCalender[Year(ISO)] &"/",
    ZZ_RollingCalender[Calendar Week(ISO)]
)
```



```dax
Year(ISO) = Year( ZZ_RollingCalender[Date] + 26- ZZ_RollingCalender[Calendar Week(ISO)])
```



```dax
Calander Week(ISO)_leadingZero = right("00" & ZZ_RollingCalender[Calendar Week(ISO)],2)
```



```dax
YearCalandarWeek(ISO)_LeadingZero = CONCATENATE(
                                                 ZZ_RollingCalender[Year(ISO)] &"",
                                                    ZZ_RollingCalender[Calander Week(ISO)_leadingZero]
                                                )
```



```dax
first day of month_ID = if(ZZ_RollingCalender[Date]= STARTOFMONTH(ZZ_RollingCalender[Date]),1,0)
```


## Table: 1_Measure_LQ

### Measures:


```dax
CIB 2020 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2020}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
CIB 2019 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2019}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
CIB 2021 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0, FILTER(ACTUAL_BALANCES_Monday,ACTUAL_BALANCES_Monday[DATUM] >= Date(2021,01,04) && ACTUAL_BALANCES_Monday[DATUM] <= Date(2022,01,02 )))
```



```dax
CIB = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
Credit_Line_Usage 2021 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] < 0, FILTER(ACTUAL_BALANCES_Monday,ACTUAL_BALANCES_Monday[DATUM] >= Date(2021,01,04) && ACTUAL_BALANCES_Monday[DATUM] <= Date(2022,01,02 )))
```



```dax
Credit_Line_Usage 2020 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2020}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] < 0)
```



```dax
Credit_Line_Usage 2019 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2019}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] < 0)
```



```dax
Credit line usage = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] < 0)
```



```dax
CIB_LC = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM]), ACTUAL_BALANCES_Monday[TOTAL_SUM] > 0)
```



```dax
CIB_Graph = if( isblank(calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)), 0, calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0))
```



```dax
CP_Balance_2018 = calculate(sum(RB_CP_CASH_POOL_BALANCES[BOOK_BALANCE]), RB_CP_CASH_POOL_BALANCES[Year] = {2018}, RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
CP_Balance_2019 = calculate(sum(RB_CP_CASH_POOL_BALANCES[BOOK_BALANCE]), RB_CP_CASH_POOL_BALANCES[Year] = {2019}, RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
CP_Balance_2020 = calculate(sum(RB_CP_CASH_POOL_BALANCES[BOOK_BALANCE]), RB_CP_CASH_POOL_BALANCES[Year] = {2020}, RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
CP_Balance_2021 = calculate(sum(RB_CP_CASH_POOL_BALANCES[BOOK_BALANCE]),RB_CP_CASH_POOL_BALANCES[Year] = {2021}, RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
Credit Line = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]))
```



```dax
Headrooom = [Credit Line] + [Credit line usage]
```



```dax
Credit Line_2019 = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]),'Credit_Line_RoW'[Year] = {2019}, 'Credit_Line_RoW'[Day of Week] = {6})
```



```dax
Credit Line_2020 = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]),'Credit_Line_RoW'[Year] = {2020}, 'Credit_Line_RoW'[Day of Week] = {6})
```



```dax
Credit Line_2021 = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]), 'Credit_Line_RoW'[Day of Week] = {6}, FILTER('Credit_Line_RoW','Credit_Line_RoW'[Date] >= Date(2021,01,04) && 'Credit_Line_RoW'[Date] <= Date(2022,01,02 )))
```



```dax
AvLQ_2019 = [CIB 2019] + [Credit Line_2019] + [Credit_Line_Usage 2019]
```



```dax
AvLQ_2020 = [CIB 2020] + [Credit Line_2020] + [Credit_Line_Usage 2020]
```



```dax
AvLQ_2021 = [CIB 2021] + [Credit Line_2021] + [Credit_Line_Usage 2021]
```



```dax
AvLQ = [CIB] + [Headrooom]
```



```dax
CIB 2022 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2022}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
Credit Line_2022 = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]),'Credit_Line_RoW'[Year] = {2022}, 'Credit_Line_RoW'[Day of Week] = {6})
```



```dax
Credit_Line_Usage 2022 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2022}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] < 0)
```



```dax
AvLQ_2022 = [CIB 2022] + [Credit Line_2022] + [Credit_Line_Usage 2022]
```



```dax
AvLQ_RFC = [AvLQ_2021]+ [AvLQ_2022] 
```



```dax
CP_Balance_2022 = calculate(sum(RB_CP_CASH_POOL_BALANCES[BOOK_BALANCE]),RB_CP_CASH_POOL_BALANCES[Year] = {2022}, RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
CIB 2021_LC = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM]),ACTUAL_BALANCES_Monday[Year] = {2021}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
Measure = Not available
```



```dax
Credit Line_2021_LC = CALCULATE(sum('Credit_Line_RoW'[Amount]),'Credit_Line_RoW'[Year] = {2021}, 'Credit_Line_RoW'[Day of Week] = {6})
```



```dax
Credit_Line_Usage 2021_LC = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM]),ACTUAL_BALANCES_Monday[Year] = {2021}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM] < 0)
```



```dax
AvLQ_2021_LC = [CIB 2021_LC] + [Credit Line_2021_LC] + [Credit_Line_Usage 2021_LC]
```



```dax
CIB 2023_LC = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM]),ACTUAL_BALANCES_Monday[Year] = {2023}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
Credit Line_2023_LC = CALCULATE(sum('Credit_Line_RoW'[Amount]),'Credit_Line_RoW'[Year] = {2023}, 'Credit_Line_RoW'[Day of Week] = {6})
```



```dax
Credit_Line_Usage 2023_LC = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM]),ACTUAL_BALANCES_Monday[Year] = {2023}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM] < 0)
```



```dax
AvLQ_2023_LC = [CIB 2023_LC] + [Credit Line_2023_LC] + [Credit_Line_Usage 2023_LC]
```



```dax
Overdue_IC_Payables = CALCULATE(sum('RB_IC PAY'[Amount_EURk]),FILTER('RB_IC PAY','RB_IC PAY'[Overdue_ID]=1))
```



```dax
Overdue_IC_payables_prt = Format(([Overdue_IC_Payables]/ CALCULATE(sum('RB_IC PAY'[Amount_EURk]))),"0.0%")
```



```dax
Overdue_IC_Receivales = CALCULATE(sum('RB_IC REC'[Amount_EURk]),FILTER ('RB_IC REC', 'RB_IC REC'[overdue_ID]=1))

```



```dax
Overdue_IC_Receivales_prt = Format(([Overdue_IC_Receivales]/ CALCULATE(sum('RB_IC REC'[Amount_EURk]))),"0.0%")
```



```dax
Overdue_IC_payables_/Total = [Overdue_IC_Payables]/ CALCULATE(sum('RB_IC PAY'[Amount_EURk]))
```



```dax
Overdue_IC_Receivales_/total = ([Overdue_IC_Receivales]/ CALCULATE(sum('RB_IC REC'[Amount_EURk])))
```



```dax
CIB as of Current week Monday = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]), ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0, ACTUAL_BALANCES_Monday[current week Monday_ID]=1)
```



```dax
CP_Balance_2023 = calculate(sum(RB_CP_CASH_POOL_BALANCES[BOOK_BALANCE]),RB_CP_CASH_POOL_BALANCES[Year] = {2023}, RB_CP_CASH_POOL_BALANCES[Weekday] = {1})
```



```dax
CIB 2023 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2023}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] > 0)
```



```dax
Credit Line_2023 = CALCULATE(sum('Credit_Line_RoW'[Amount_EUR]),'Credit_Line_RoW'[Year] = {2023}, 'Credit_Line_RoW'[Day of Week] = {6})
```



```dax
Credit_Line_Usage 2023 = calculate(sum(ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR]),ACTUAL_BALANCES_Monday[Year] = {2023}, ACTUAL_BALANCES_Monday[Day of Week] = {1}, ACTUAL_BALANCES_Monday[TOTAL_SUM_EUR] < 0)
```



```dax
AvLQ_2023 = [CIB 2023] + [Credit Line_2023] + [Credit_Line_Usage 2023]
```


## Table: RB_CORIMA_VALUE DATES

### Calculated Columns:


```dax
PLAN_VARIANT_ID = LOOKUPVALUE(FC_DATA[PLAN_VARIANT_ID_ADJ],FC_DATA[PLAN_VARIANT_SHORT_NAME], 'RB_CORIMA_VALUE DATES'[PLAN_VARIANT_SHORT_NAME])
```



```dax
Current_Week_ID = if('RB_CORIMA_VALUE DATES'[PLAN_VARIANT_ID] = max('RB_CORIMA_VALUE DATES'[PLAN_VARIANT_ID]), 1, 0)
```



```dax
INVOICE_DATE = LOOKUPVALUE(RB_RECEIVABLES[INVOICE_DATE], RB_RECEIVABLES[CUSTOMER_INVOICE_ID], 'RB_CORIMA_VALUE DATES'[CUSTOMER_INVOICE_ID], RB_RECEIVABLES[OPEN_AMOUNT_LC], 'RB_CORIMA_VALUE DATES'[AMOUNT_LC])
```



```dax
AGE = if ('RB_CORIMA_VALUE DATES'[VALUE_DATE] - 'RB_CORIMA_VALUE DATES'[INVOICE_DATE] > 1000, blank(), 'RB_CORIMA_VALUE DATES'[VALUE_DATE] - 'RB_CORIMA_VALUE DATES'[INVOICE_DATE])
```



```dax
Exclusion_Id = if('RB_CORIMA_VALUE DATES'[VALUE_DATE] > TODAY() + 180, 1, 0)
```



```dax
CW = if('RB_CORIMA_VALUE DATES'[VALUE_DATE] < today() +110, WEEKNUM('RB_CORIMA_VALUE DATES'[VALUE_DATE],2), 0)
```



```dax
Last_Week_ID = if('RB_CORIMA_VALUE DATES'[PLAN_VARIANT_ID] = max('RB_CORIMA_VALUE DATES'[PLAN_VARIANT_ID])-1, 1, 0)
```



```dax
VALUE_DATE_LAST_FC = LOOKUPVALUE('RB_CORIMA_VALUE DATES'[VALUE_DATE], 'RB_CORIMA_VALUE DATES'[Last_Week_ID], {1}, 'RB_CORIMA_VALUE DATES'[UNIQUE_IDENTIFIER], 'RB_CORIMA_VALUE DATES'[UNIQUE_IDENTIFIER])
```



```dax
Delay to last FC = if(ISBLANK('RB_CORIMA_VALUE DATES'[VALUE_DATE_LAST_FC]), BLANK(), 'RB_CORIMA_VALUE DATES'[VALUE_DATE] - 'RB_CORIMA_VALUE DATES'[VALUE_DATE_LAST_FC])
```



```dax
Delay to Last FC( text) = IF(ISBLANK('RB_CORIMA_VALUE DATES'[Delay to last FC]), "New AR", CONVERT('RB_CORIMA_VALUE DATES'[Delay to last FC], STRING))
```



```dax
UNiqueCheck = 
CALCULATE ( COUNT ( 'RB_CORIMA_VALUE DATES'[UNIQUE_IDENTIFIER] ), ALLEXCEPT ( 'RB_CORIMA_VALUE DATES', 'RB_CORIMA_VALUE DATES'[UNIQUE_IDENTIFIER] ), 'RB_CORIMA_VALUE DATES'[Last_Week_ID] = 1)
```


## Table: ZZ_Measure_FC_Legacy

### Measures:


```dax
FC_AvLQ_RFC_LFC_4 = 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PLAN_VARIANT_ID] = {26})
```



```dax
FC_AvLQ_RFC_LFC_2 = 
VAR m = [ID_Last_FC]
RETURN 
calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1}, FC_DATA[PLAN_VARIANT_ID] = m)
```



```dax
FC_AvLQ_RFC_LFC_3 = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"available liquidity"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Weekbreak_ID] = {1},filter(FC_DATA, FC_DATA[PLAN_VARIANT_ID] = MAX(FC_DATA[PLAN_VARIANT_ID])-1))
```



```dax
CFO_2021_Delta = [CFO_RFC] - [CFO_2021_LFC]
```



```dax
CFO_2021_LFC = calculate(sum(FC_DATA[CONCERN_AMOUNT]),FC_DATA[CATEGORY_SHORT_NAME] = {"cfo"}, FC_DATA[IS_CURRENCY_DETAIL_SUM] = {true}, FC_DATA[Year] = {2021}, FC_DATA[ID_Last_FC] = {1}, FC_DATA[PERIOD_NR] > {1})
```



```dax
CFO_acc_2021 = calculate( 
                    [CFO_RFC], 
                            filter (ALLSELECTED(FC_DATA), FC_DATA[Week of Year] <= max(FC_DATA[Week of Year]) && FC_DATA[PLAN_VARIANT_ID] = max(FC_DATA[PLAN_VARIANT_ID]))
                        )
```



```dax
CFO_acc_2021_Delta = [CFO_acc_2021] - [CFO_acc_2021_LFC]
```



```dax
CFO_acc_2021_LFC = calculate( 
                    [CFO_2021_LFC], 
                            filter (ALLSELECTED(FC_DATA), FC_DATA[Week of Year] <= max(FC_DATA[Week of Year])&& FC_DATA[PLAN_VARIANT_ID] = max(FC_DATA[PLAN_VARIANT_ID])-1)
                        )
```


## Table: FC_IC_MATCHING

### Calculated Columns:


```dax
Amount_TC_k = FC_IC_MATCHING[AMOUNT] / 1000
```



```dax
Company (2) = LOOKUPVALUE(RB_COMPANIES[COMPANY_NAME], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID], FC_IC_MATCHING[Gesellschaft_2])
```



```dax
ID_Current_FC = IF(FC_IC_MATCHING[PLANVARIANTEN_ID] = max(FC_IC_MATCHING[PLANVARIANTEN_ID]), 1, 0)
```



```dax
Company (1) = LOOKUPVALUE(RB_COMPANIES[COMPANY_NAME], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID], FC_IC_MATCHING[Gesellschaft_1])
```



```dax
Status (1) = IF(FC_IC_MATCHING[IC_Status_Gesellschaft_1] = {0}, "New", if(FC_IC_MATCHING[IC_Status_Gesellschaft_1] = {1}, "Approved", if(FC_IC_MATCHING[IC_Status_Gesellschaft_1] = {2}, "Canceled", if(FC_IC_MATCHING[IC_Status_Gesellschaft_1] = {3}, "Draft", "Canceled"))))
```



```dax
Status (2) = IF(FC_IC_MATCHING[IC_Status_Gesellschaft_2] = {0}, "New", if(FC_IC_MATCHING[IC_Status_Gesellschaft_2] = {1}, "Approved", if(FC_IC_MATCHING[IC_Status_Gesellschaft_2] = {2}, "Canceled", if(FC_IC_MATCHING[IC_STATUS_GESELLSCHAFT_2] = {3}, "Draft", "Canceled"))))
```



```dax
Display_Selection = FC_IC_MATCHING[Status (1)] & "_" & FC_IC_MATCHING[Status (2)]
```


## Table: RB_CP_CASH_POOL_BALANCES

### Calculated Columns:


```dax
Year = year(RB_CP_CASH_POOL_BALANCES[DATE])
```



```dax
CW = WEEKNUM(RB_CP_CASH_POOL_BALANCES[DATE])
```



```dax
Weekday = WEEKDAY(RB_CP_CASH_POOL_BALANCES[DATE])
```


## Table: RB_IC PAY

### Calculated Columns:


```dax
Amount_EURk = 'RB_IC PAY'[BALANCE_EUR] / 1000
```



```dax
Amount_EURk_abs = abs('RB_IC PAY'[Amount_EURk])
```



```dax
COMPANY_ISO = LOOKUPVALUE(RB_COMPANIES[COUNTRY_ISO3], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID], 'RB_IC PAY'[COMPANY_ID])
```



```dax
Is_receiving_Compamy_Netting = if((CALCULATE(COUNTROWS(MD_Netting_Countries), FILTER(MD_Netting_Countries, MD_Netting_Countries[PARTNER_SHORT_NAME]='RB_IC pay'[COMPANY_ID]))) = BLANK(),0, CALCULATE(COUNTROWS(MD_Netting_Countries), FILTER(MD_Netting_Countries, MD_Netting_Countries[PARTNER_SHORT_NAME]='RB_IC pay'[COMPANY_ID])))
```



```dax
Is_Payment_Company_Netting = if((CALCULATE(COUNTROWS(MD_Netting_Countries), FILTER(MD_Netting_Countries, MD_Netting_Countries[PARTNER_SHORT_NAME]='RB_IC PAY'[PARTNER_COMPANY_ID])))=BLANK(), 0, CALCULATE(COUNTROWS(MD_Netting_Countries), FILTER(MD_Netting_Countries, MD_Netting_Countries[PARTNER_SHORT_NAME]='RB_IC PAY'[PARTNER_COMPANY_ID])))
```



```dax
Both_Netting_Countries = 'RB_IC PAY'[Is_Payment_Company_Netting] + 'RB_IC PAY'[Is_receiving_Compamy_Netting]
```



```dax
Open_Amount_TC_k = ('RB_IC PAY'[Open_Amount_TC])/1000
```



```dax
OverDue_days = TODAY()-'RB_IC PAY'[DUE_DATE]
```



```dax
Payment_company_Netting = if('RB_IC PAY'[Is_Payment_Company_Netting] = BLANK(), "Not Netting", "Netting")
```



```dax
Receiving_Company_Netting = if('RB_IC PAY'[Is_receiving_Compamy_Netting]= BLANK(), "Not Netting", "Netting")
```



```dax
Overdue_ID = if('RB_IC PAY'[DUE_DATE] < TODAY(), 1,0)
```


## Table: RB_IC REC

### Calculated Columns:


```dax
Amount_EURk = 'RB_IC REC'[BALANCE_EUR] / 1000
```



```dax
PARTNER_COMPANY_ISO = LOOKUPVALUE(RB_COMPANIES[COUNTRY_ISO3], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID], 'RB_IC REC'[PARTNER_COMPANY_ID])
```



```dax
Is_receiving_Compamy_Netting = CALCULATE(COUNTROWS(MD_Netting_Countries), FILTER(MD_Netting_Countries, MD_Netting_Countries[PARTNER_SHORT_NAME]='RB_IC REC'[COMPANY_ID]))
```



```dax
Is_Payment_Company_Netting = CALCULATE(COUNTROWS(MD_Netting_Countries), FILTER(MD_Netting_Countries, MD_Netting_Countries[PARTNER_SHORT_NAME]='RB_IC REC'[PARTNER_COMPANY_ID]))
```



```dax
Both_Netting_Countries = 'RB_IC REC'[Is_Payment_Company_Netting] + 'RB_IC REC'[Is_receiving_Compamy_Netting]
```



```dax
Open_Amount_TC_k = ('RB_IC REC'[Open_Amount_TC])/1000
```



```dax
overdue_ID = if('RB_IC REC'[DUE_DATE]< TODAY(),1,0)
```


## Table: RB_WIP

### Calculated Columns:


```dax
OPEN_WIP_EURk = RB_WIP[OPEN_WIP] / 1000
```



```dax
FEES_TO_BE_INVOCIED_EURK = RB_WIP[FEES_TO_BE_INVOICED_EUR] / 1000
```



```dax
OPEN_BUDGET_FEE_EURk = ( RB_WIP[BUDGET_FEE] - RB_WIP[INVOICED_FEE] ) / 1000
```



```dax
OPEN_BUDGET_IE_EURk = ( RB_WIP[BUDGET_IE] - RB_WIP[INVOICED_IE] ) / 1000
```



```dax
Open Budget = RB_WIP[OPEN_BUDGET_FEE_EURk] + RB_WIP[OPEN_BUDGET_IE_EURk]
```


## Table: FC_ACTUALS

### Calculated Columns:


```dax
CONCERN_AMOUNT_EURk = FC_ACTUALS[CONCERN_AMOUNT] / 1000
```



```dax
Current_Actuals_ID = if (max(FC_ACTUALS[VALUE_DATE]) - 7 < FC_ACTUALS[VALUE_DATE] , 1, 0)
```



```dax
2nd_last_Actuals_ID = if ( max(FC_ACTUALS[VALUE_DATE]) -14 < FC_ACTUALS[VALUE_DATE] && max(FC_ACTUALS[VALUE_DATE]) - 7 > FC_ACTUALS[VALUE_DATE], 1, 0)
```



```dax
3rd_Last_Actuals_ID = if ( max(FC_ACTUALS[VALUE_DATE]) -21 < FC_ACTUALS[VALUE_DATE] && max(FC_ACTUALS[VALUE_DATE]) - 14 > FC_ACTUALS[VALUE_DATE], 1, 0)
```



```dax
4th_Last_Actuals_ID = if ( max(FC_ACTUALS[VALUE_DATE]) -28 < FC_ACTUALS[VALUE_DATE] && max(FC_ACTUALS[VALUE_DATE]) - 21 > FC_ACTUALS[VALUE_DATE], 1, 0)
```



```dax
5th_Last_Actuals_ID = if ( max(FC_ACTUALS[VALUE_DATE]) -35 < FC_ACTUALS[VALUE_DATE] && max(FC_ACTUALS[VALUE_DATE]) - 28 > FC_ACTUALS[VALUE_DATE], 1, 0)
```



```dax
6th_Last_Actuals_ID = if ( max(FC_ACTUALS[VALUE_DATE]) -42 < FC_ACTUALS[VALUE_DATE] && max(FC_ACTUALS[VALUE_DATE]) - 35 > FC_ACTUALS[VALUE_DATE], 1, 0)
```


## Table: Credit_Line_RoW

### Calculated Columns:


```dax
FX Rate = LOOKUPVALUE(ACTUAL_FX_RATES[RATES_VALUE], ACTUAL_FX_RATES[DATUM], 'Credit_Line_RoW'[Date], ACTUAL_FX_RATES[CURRENCY], 'Credit_Line_RoW'[Currency])
```



```dax
Amount_EUR = if('Credit_Line_RoW'[Date] < TODAY()+1, 'Credit_Line_RoW'[Amount] / 'Credit_Line_RoW'[FX Rate], BLANK())
```


## Table: 1_Measure_Actuals

### Measures:


```dax
Bonus = CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Bonus Consultants"}) +
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] =  {"Bonus Partner"}) + 
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Bonus Principals"}) + 
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Bonus Services"}) + 
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Soc. Sec. on Bonus C"}) + 
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Soc. Sec. on Bonus P"}) + 
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Soc. Sec. on Bonus PRI"}) + 
        CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]),FC_ACTUALS[CATEGORY_SHORT_NAME] = {"Soc. Sec. on Bonus S"})
```



```dax
External Cash-ins = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "receivables") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "receivables ACT") +                    
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "projects order") +
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "projects order_up") +
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "new projects") +
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "Other receivables") 
```



```dax
Tax = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "VAT") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "Corporate Income Tax") +                    
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "Other taxes")
```



```dax
Salaries (incl soc sec) = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "Incidental wage") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "from salaries")
```



```dax
Supplier = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] in {"Supplier_other","Travel","Subcontractor"}
 )
```



```dax
Rent = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "rent")
```



```dax
Net ICA = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "IC receivables") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "IC receivables act") +
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "IC payable") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "IC payables act") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "Netting rec") + 
                    calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[CATEGORY_SHORT_NAME] = "Netting pay")
```



```dax
CFO = [Bonus] + [External Cash-ins] + [Net ICA] + [Rent] + [Salaries (incl soc sec)] + [Supplier] + [Tax]
```



```dax
Actual_Last_week = CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]), FC_ACTUALS[Current_Actuals_ID] = {1})
```



```dax
Cash out(Salary,Bonus,Rent,Suppler, Tax) = ([Salaries (incl soc sec)]+ [Bonus]+ [rent]+[Supplier]+[Tax])
```



```dax
Cash out Monthly Av(Salary,Bonus,Rent,Suppler, Tax) = CALCULATE(Sum(FC_ACTUALS[CONCERN_AMOUNT_EURk]),ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_ACTUALS, FC_ACTUALS[CATEGORY_SHORT_NAME] in {
"Bonus Consultants",
"Bonus Partner",
"Bonus Principals",
"Bonus Services",
"from salaries",
"incidental wage",
"Rent",
"Soc. Sec. on Bon Pri",
"Soc. Sec. on Bonus C",
"Soc. Sec. on Bonus P",
"Soc. sec. on Bonus S",
"Subcontractor",
"Supplier_other",
"Travel",
"VAT",
"Corporate income tax",
"Other taxes"
}


    ))/'1_Measure_Actuals'[count Months]
```



```dax
count Months = (COUNTROWS(SUMMARIZE(ZZ_RollingCalender,ZZ_RollingCalender[Date].[Month])))
```



```dax
Cash out Monthly Av(Salary,Rent,Suppler, Tax) = CALCULATE(Sum(FC_ACTUALS[CONCERN_AMOUNT_EURk]),ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_ACTUALS, FC_ACTUALS[CATEGORY_SHORT_NAME] in {
"from salaries",
"incidental wage",
"Rent",
"Subcontractor",
"Supplier_other",
"Travel",
"VAT",
"Corporate income tax",
"Other taxes"
}


    ))/'1_Measure_Actuals'[count Months]
```



```dax
Cash out Monthly Av(Salary,Bonus,Rent,Suppler,Tax,IC payable, Netting) = CALCULATE(Sum(FC_ACTUALS[CONCERN_AMOUNT_EURk]),ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_ACTUALS, FC_ACTUALS[CATEGORY_SHORT_NAME] in {
"Bonus Consultants",
"Bonus Partner",
"Bonus Principals",
"Bonus Services",
"from salaries",
"incidental wage",
"Rent",
"Soc. Sec. on Bon Pri",
"Soc. Sec. on Bonus C",
"Soc. Sec. on Bonus P",
"Soc. sec. on Bonus S",
"Subcontractor",
"Supplier_other",
"Travel",
"VAT",
"Corporate income tax",
"Other taxes",
"IC payable",
"IC payables ACT",
"Netting pay"

}


    ))/'1_Measure_Actuals'[count Months]
```



```dax
Cash in Monthly Av(External) = CALCULATE(Sum(FC_ACTUALS[CONCERN_AMOUNT_EURk]),ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_ACTUALS, FC_ACTUALS[CATEGORY_SHORT_NAME] in {
"new projects",
"Other receivables",
"projects order",
"projects order_up",
"receivables",
"receivables ACT",
"receivables_GER"
}


    ))/'1_Measure_Actuals'[count Months]
```



```dax
Cash in Monthly Av(External, IC;Netting) = CALCULATE(Sum(FC_ACTUALS[CONCERN_AMOUNT_EURk]),ALLSELECTED(ZZ_RollingCalender[Date]), 
filter(FC_ACTUALS, FC_ACTUALS[CATEGORY_SHORT_NAME] in {
"new projects",
"Other receivables",
"projects order",
"projects order_up",
"receivables",
"receivables ACT",
"receivables_GER",
"Netting rec",
"IC receivables ACT",
"IC receiveables"

}


    ))/'1_Measure_Actuals'[count Months]
```



```dax
Operating CF margin = Format(('1_Measure_Actuals'[CFO]/ '1_Measure_Actuals'[External Cash-ins])*100, "0.0%")
```



```dax
count Days = (COUNTROWS(SUMMARIZE(ZZ_RollingCalender,ZZ_RollingCalender[Date])))
```



```dax
Average available LQ = CALCULATE('1_Measure_FC'[CP_AvLQ_2022_S],ALLSELECTED(ZZ_RollingCalender[Date])
)/'1_Measure_Actuals'[Number of Sundays]
```



```dax
Number of Sundays = CALCULATE(count(ZZ_RollingCalender[Date]), filter(ZZ_RollingCalender,ZZ_RollingCalender[Day of Week]=1))
```



```dax
CF rule = CALCULATE(sum(ACTUAL_BALANCES_Monday[Amount EUR different 7 days]), ACTUAL_BALANCES_Monday[Day of Week] = 2) 
- 
CALCULATE(sum(FC_ACTUALS[CONCERN_AMOUNT]), filter(FC_ACTUALS, FC_ACTUALS[CATEGORY_SHORT_NAME] in {
"CFF",
"CFI",
"CFO"

}
)
)
```



```dax
Actual all CFs = calculate(sum(FC_ACTUALS[CONCERN_AMOUNT]))
```


## Table: FC_RESPONSE_A

### Measures:


```dax
Response_A_Row_Count = COUNTROWS(FC_RESPONSE_A)
```


### Calculated Columns:


```dax
Current_Actual_ID = if ( FC_RESPONSE_A[PERIOD_NR] = max(FC_RESPONSE_A[PERIOD_NR]), 1, 0)
```



```dax
Current_Actual_Approved = FC_RESPONSE_A[Current_Actual_ID] * FC_RESPONSE_A[APPROVED1]
```


## Table: FC_RESPONSE_FC

### Measures:


```dax
Cross Filter_only approved FC = INT( NOT( ISEMPTY(FC_RESPONSE_FC)))
```


### Calculated Columns:


```dax
Current_FC_ID = if( max(FC_RESPONSE_FC[PLAN_VARIANT_ID]) = FC_RESPONSE_FC[PLAN_VARIANT_ID], 1, 0)
```



```dax
Current_FC_Approved = FC_RESPONSE_FC[Current_FC_ID] * FC_RESPONSE_FC[APPROVED1]
```


## Table: ZZ_RollingCalendar_From_FC_Plans

### Measures:


```dax
Actual_Week = LOOKUPVALUE(ZZ_RollingCalendar_From_FC_Plans[Y-CW_long],ZZ_RollingCalendar_From_FC_Plans[CW], MIN(ZZ_RollingCalendar_From_FC_Plans[CW]))
```


### Calculated Columns:


```dax
Calander Week(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Calendar Week(ISO)], ZZ_RollingCalender[Date], ZZ_RollingCalendar_From_FC_Plans[Plan_Date])
```



```dax
Year(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Year(ISO)], ZZ_RollingCalender[Date], ZZ_RollingCalendar_From_FC_Plans[Plan_Date])
```



```dax
Year/calandarWeek(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Year/calandarWeek(ISO)], ZZ_RollingCalender[Date], ZZ_RollingCalendar_From_FC_Plans[Plan_Date])
```


## Table: ZZ_RollingCalendar_From_FC_Plans- For rolling CW

### Calculated Columns:


```dax
Year_select = if('ZZ_RollingCalendar_From_FC_Plans- For rolling CW'[Plan_Date] <= DATE(2021,12,31), 2021, 2022)
```



```dax
Actual_Week_test = LOOKUPVALUE(ZZ_RollingCalendar_From_FC_Plans[Y-CW_long],ZZ_RollingCalendar_From_FC_Plans[CW], MIN(ZZ_RollingCalendar_From_FC_Plans[CW]))
```



```dax
Calander Week(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Calendar Week(ISO)], ZZ_RollingCalender[Date], 'ZZ_RollingCalendar_From_FC_Plans- For rolling CW'[Plan_Date])
```



```dax
Year(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Year(ISO)], ZZ_RollingCalender[Date], 'ZZ_RollingCalendar_From_FC_Plans- For rolling CW'[Plan_Date])
```



```dax
Year/calandarWeek(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Year/calandarWeek(ISO)], ZZ_RollingCalender[Date], 'ZZ_RollingCalendar_From_FC_Plans- For rolling CW'[Plan_Date])
```



```dax
Year/calandarWeek(ISO)_LeadingZero = LOOKUPVALUE(ZZ_RollingCalender[YearCalandarWeek(ISO)_LeadingZero], ZZ_RollingCalender[Date], 'ZZ_RollingCalendar_From_FC_Plans- For rolling CW'[Plan_Date])
```


## Table: FC_IC_MATCHING_NEW

### Calculated Columns:


```dax
Company (1) = LOOKUPVALUE(RB_COMPANIES[COMPANY_NAME], RB_COMPANIES[ORGANIZATIONAL_CCENTER_ID], FC_IC_MATCHING_NEW[Gesellschaft_1])
```


## Table: ZZ_RollingCalendar for FC over FC with Last Actual week

### Calculated Columns:


```dax
CW_ISO = WEEKNUM('ZZ_RollingCalendar for FC over FC with Last Actual week'[Days],21)
```



```dax
CW_ISO_(text) = WEEKNUM('ZZ_RollingCalendar for FC over FC with Last Actual week'[Days],21)
```



```dax
Current_Actual_week_ID = IF('ZZ_RollingCalendar for FC over FC with Last Actual week'[LastActualWeekStartDate]='ZZ_RollingCalendar for FC over FC with Last Actual week'[Days],1,0)
```



```dax
CW_ISO_(text)/Year = CONCATENATE(
    'ZZ_RollingCalendar for FC over FC with Last Actual week'[Year(ISO)] &"/",
    'ZZ_RollingCalendar for FC over FC with Last Actual week'[CW_ISO_(text)]
)
```



```dax
Year(ISO) = LOOKUPVALUE(ZZ_RollingCalender[Year(ISO)], ZZ_RollingCalender[Date], 'ZZ_RollingCalendar for FC over FC with Last Actual week'[Days])
```

