



# DAX

|Dataset|[Working Capital_CM](./../Working-Capital_CM.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: MeasureTable

### Measures:


```dax
External Sales = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"120"})
```



```dax
Internal Sales = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"160"})
```



```dax
Internal Purchases = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"650"})
```



```dax
NR = [External Sales]+[Internal Sales]+[Internal Purchases]+[WIP change]
```



```dax
NR LTM = Calculate([NR],
                    QAP[End of Month] < date(year(today()),month(today()),day(today())), 
                    QAP[End of Month] > date(year(today()),month(today()),day(today()))-365)
```



```dax
NR LTM-1 = Calculate([NR],
                    QAP[End of Month] < date(year(today()),month(today()),day(today()))-365, 
                    QAP[End of Month] > date(year(today()),month(today()),day(today()))-730)
```



```dax
Change in Net Revenue LTM = [NR LTM] / [NR LTM-1] - 1
```



```dax
NR PY = calculate([NR],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
NR Delta abs = [NR] - [NR PY]
```



```dax
NR Delta per = [NR Delta abs] / [NR PY]
```



```dax
NR Delta per rank = rankx(ALLSELECTED(RB_COMPANIES[ZONE]),calculate([NR Delta per]),,DESC)
```



```dax
NR Delta Grouping = IF([NR Delta per rank] < calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[NR Delta per rank]))/3,1,
                IF([NR Delta per rank] > calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[NR Delta per rank]))/3*2,3,2))
```



```dax
Other Income = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"400"})
```



```dax
Personnel Expenses = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"820"}) + CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"850"})
```



```dax
Other operating Expenses = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"1000"})
```



```dax
EBITDA = [External Sales]+[Internal Sales]+[Other Income]+[Internal Purchases]+[Personnel Expenses]+[Other operating Expenses]+[WIP change]
```



```dax
EBITDA PY = calculate([EBITDA],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
Leverage rank = RANKX(ALLSELECTED((RB_COMPANIES[ZONE])),calculate([Leverage]),,ASC)
```



```dax
IC Pay = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"8200"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))
```



```dax
Leverage = if([Net Financial Debt]>0,0,if([EBITDA]<0,"-Infinity",[Net Financial Debt] / [EBITDA]))
```



```dax
IC Rec = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"6000"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))
```



```dax
Bank Liabilities = CALCULATE(SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"8000"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))
```



```dax
Cash = CALCULATE(SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"6350"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))
```



```dax
Net Financial Debt = [IC Loans]+[ICAs AGED net_items]+[CashPool]+[Bank Liabilities]+[Cash]
```



```dax
Leverage Grouping = IF([Leverage rank] < calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[Leverage rank]))/3,1,
                IF([Leverage rank] > calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[Leverage rank]))/3*2,3,2))
```



```dax
Grouping I = ([Leverage Grouping] * 'Weight Leverage'[Weight Leverage Value] + [EBITDA Margin Grouping] * 'Weight EBITDA'[Weight EBITDA Value] + [NR Delta Grouping] * 'Weight NR'[Weight NR Value 2])/100
```



```dax
IC Margin factor = if(round([Grouping II],0)=1,1,if(round([Grouping II],0)=2,1+'Down Nodging'[Down Nodging Value],1+2*'Down Nodging'[Down Nodging Value]))
```



```dax
IC Interest Margin = MROUND('Group Interest Margin'[Group Interest Rate Value] * [IC Margin factor],0.25)/100+'Profit Margin'[Profit Margin Value]/100
```



```dax
EBITDA Margin = [EBITDA] / [NR]
```



```dax
EBITDA Margin rank = rankx(ALLSELECTED((RB_COMPANIES[ZONE])),calculate([EBITDA Margin]))
```



```dax
EBITDA Margin Grouping = IF([EBITDA Margin rank] < calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[EBITDA Margin rank]))/3,1,
                IF([EBITDA Margin rank] > calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[EBITDA Margin rank]))/3*2,3,2))
```



```dax
Grouping Rank Max = calculate(MAXX(ALLSELECTED((RB_COMPANIES[ZONE])),[Grouping I]))
```



```dax
Leverage Summary = if([Leverage]=0.0,"NA",format([Leverage],"#.#x"))
```



```dax
NR Growth Summary = format([NR Delta per],"#.#,0%")
```



```dax
Other Income PY = calculate([Other Income],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
Other operating Expenses PY = calculate([Other operating Expenses],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
Personnel Expenses PY = calculate([Personnel Expenses],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
WIP change = CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[PARENT_GL_ACCOUNT_ID] in {"200"})
```



```dax
Other Income Growth Summary = format([Other Income]/[Other Income PY]-1,"#.#,0%")
```



```dax
Other operating Expenses Growth Summary = format([Other operating Expenses]/[Other operating Expenses PY]-1,"#.#,0%")
```



```dax
Personnel Expenses Growth Summary = format([Personnel Expenses]/[Personnel Expenses PY]-1,"#.#,0%")
```



```dax
EBITDA Growth Summary = format([EBITDA]/[EBITDA PY]-1,"#.#,0%")
```



```dax
NR Detla Grouping fixed threshold = if([NR Delta per]<'NR Threshold Group 3'[NR Group 3 Value]/100,3,if([NR Delta per]>'NR Threshold Group 1'[NR Threshold Group 1 Value]/100,1,2))
```



```dax
EBITDA margin Grouping fixed = if([EBITDA Margin]<'EBITDA Margin Threshold Group 3 [%]'[EBITDA Margin Threshold Group 3 [%]] Value]/100,3,if([EBITDA Margin]>'EBITDA Margin Threshold Group 1'[EBITDA Margin Threshold Group 1 Value]/100,1,2))
```



```dax
Leverage Grouping fixed = if([Leverage]<'Leverage Threshold Group 3'[Leverage Threshold Group 3 Value],3,if([Leverage]="-Infinity",3,if([Leverage]>'Leverage Threshold Group 1'[Leverage Threshold Group 1 Value]-0.001,1,2)))
```



```dax
Grouping II = ROUND(([Leverage Grouping fixed] * 'Weight Leverage'[Weight Leverage Value] + [EBITDA margin Grouping fixed] * 'Weight EBITDA'[Weight EBITDA Value] + [NR Detla Grouping fixed threshold] * 'Weight NR'[Weight NR Value 2])/100,0)
```



```dax
External Sales PY = calculate([External Sales],SAMEPERIODLASTYEAR(RollingCalender[Date]))
```



```dax
External Sales Delta = [External Sales]-[External Sales PY]
```



```dax
Total Sales Delta = [External Sales Delta]+[WIP change] - [WIP Change PY]
```



```dax
WIP Change PY = calculate([WIP change],SAMEPERIODLASTYEAR(RollingCalender[Date]))
```



```dax
Net IC Sales = [Internal Sales]+[Internal Purchases]
```



```dax
Net IC Sales PY = calculate([Net IC Sales],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
Net IC Sales Delta = [Net IC Sales]-[Net IC Sales PY]
```



```dax
Total Sales = [External Sales]+ [WIP change]
```



```dax
Total Sales PY = calculate([Total Sales],SAMEPERIODLASTYEAR(QAP[End of Month]))
```



```dax
IC Rec AGED_items = calculate(sum('IC REC'[BALANCE_EUR]),'IC REC'[AGE ID] in {"1"})
```



```dax
IC Rec_items = calculate(sum('IC REC'[BALANCE_EUR]))
```



```dax
IC Pay AGED_items = calculate(sum('IC PAY'[BALANCE_EUR]),'IC PAY'[AGE_ID] in {"1"})
```



```dax
IC Pay_items = calculate(sum('IC PAY'[BALANCE_EUR]))
```



```dax
ICAs AGED net_items = [IC Rec AGED_items]+[IC Pay AGED_items]
```



```dax
IC Loans = -CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[ALLOC_GL_ACCOUNT] in {"335100"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))-CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[ALLOC_GL_ACCOUNT] in {"125100"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))
```



```dax
CashPool = -CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[ALLOC_GL_ACCOUNT] in {"125200"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))-CALCULATE(-SUM(QAP[AMOUNT_EUR]),QAP[ALLOC_GL_ACCOUNT] in {"335200"}, filter(QAP,QAP[End of Month]=maxx(qap,QAP[End of Month])))
```



```dax
WIP = sum(CARDINAL_ACC[WIP]) - sum(CARDINAL_ACC[ADVANCE_PAYMENTS])
```



```dax
AR = sum(CARDINAL_ACC[TRADE_RECEIVABLES]) - sum(CARDINAL_ACC[BAD_DEBT])
```



```dax
L3M Sales = calculate(sum(CARDINAL_ACC[REVENUE_TOTAL]), DATESINPERIOD(RollingCalender[Date], max(RollingCalender[Date]),-3,MONTH))
```



```dax
DSO Total = sum(CARDINAL_ACC[TOTAL_WORKING_CAPITAL]) / [L3M Sales] *90
```



```dax
DSO_AR = [AR] / [L3M Sales] * 90
```



```dax
DSO_WIP = [WIP] / [L3M Sales] * 90
```



```dax
WC Target = sumx(Targets,[Target_WC_Day]*[L3M Sales]) / 90
```



```dax
WC Target DSO = [WC Target] / [L3M Sales] * 90
```



```dax
AR Delta = calculate([AR],filter(CARDINAL_ACC,CARDINAL_ACC[YEAR_MONTH]=maxx(RollingCalender,RollingCalender[Date]))) - calculate([AR],filter(CARDINAL_ACC,CARDINAL_ACC[YEAR_MONTH]=MINX(RollingCalender,RollingCalender[Date])))
```



```dax
WIP Delta = calculate([WIP],filter(CARDINAL_ACC,CARDINAL_ACC[YEAR_MONTH]=maxx(RollingCalender,RollingCalender[Date]))) - calculate([WIP],filter(CARDINAL_ACC,CARDINAL_ACC[YEAR_MONTH]=MINX(RollingCalender,RollingCalender[Date])))
```



```dax
WC Delta = [AR Delta] + [WIP Delta]
```



```dax
WC_current = CALCULATE([WC total],FILTER(RollingCalender,RollingCalender[Date]=maxx(RollingCalender,RollingCalender[Date])))
```



```dax
WC total = [AR]+ [WIP]
```



```dax
WC target current = calculate([WC Target],filter(RollingCalender,RollingCalender[Date]=maxx(RollingCalender,RollingCalender[Date])))
```



```dax
WC Gauge max = [WC_current] * 1.25
```



```dax
WC Gap to target = calculate([WC total] - [WC Target],FILTER(RollingCalender,RollingCalender[Date]=maxx(RollingCalender,RollingCalender[Date])))
```



```dax
WC total chart = CALCULATE([WC total],FILTER(RollingCalender,RollingCalender[Date]=max(RollingCalender[Date])))
```



```dax
DSO chart = CALCULATE([DSO Total],FILTER(RollingCalender,RollingCalender[Date]=maxx(RollingCalender,RollingCalender[Date])))
```



```dax
DSO Gauge max = [DSO chart] * 1.25
```



```dax
Provisions individual = -CALCULATE(sum(QAP[AMOUNT_EUR]),QAP[ALLOC_GL_ACCOUNT] in {"124600"},filter(CARDINAL_ACC,CARDINAL_ACC[YEAR_MONTH]=MaxX(RollingCalender,RollingCalender[Date])))
```



```dax
Provisions general = -CALCULATE(sum(QAP[AMOUNT_EUR]),QAP[ALLOC_GL_ACCOUNT] in {"124800"},filter(CARDINAL_ACC,CARDINAL_ACC[YEAR_MONTH]=MaxX(RollingCalender,RollingCalender[Date])))
```



```dax
Provision total = [Provisions general] + [Provisions individual]
```



```dax
Provision Gauge = [Theoretical Bad Debt]*1.25
```



```dax
Provision gap = [Provision total] - [Theoretical Bad Debt]
```



```dax
DSO Gap % = [DSO chart] / [WC Target DSO] - 1
```



```dax
Theoretical Bad Debt general = sum(AR[Basis general bad debt]) * 0.025
```



```dax
Theoretical Bad Debt = sum(AR[Provision Amount]) + [Theoretical Bad Debt general]
```



```dax
Theoretical Bad Debt individual = sum(AR[Provision Amount])
```



```dax
Total WC items = sum(AR[OPEN_AMOUNT]) + sum(WIP[OPEN_WIP])
```



```dax
Weighted avg Age AR = sum(AR[Weighted Age]) / sum(AR[OPEN_AMOUNT])


```



```dax
Weighted avg Age WIP = sum(WIP[Weighted Age]) / sum(WIP[OPEN_WIP])
```



```dax
Weighted avg Age WC = ([Weighted avg Age AR] * sum(AR[OPEN_AMOUNT]) + [Weighted avg Age WIP] * sum(WIP[OPEN_WIP]) )/ (sum(WIP[OPEN_WIP])+sum(AR[OPEN_AMOUNT]))
```



```dax
Bad Debt = -sum(CARDINAL_ACC[BAD_DEBT])
```



```dax
Advance Payments = -sum(CARDINAL_ACC[ADVANCE_PAYMENTS])
```



```dax
Delta Date = datediff(maxx(RollingCalender,RollingCalender[Date]),minx(RollingCalender,RollingCalender[Date]),DAY)
```



```dax
WC beginning of period = CALCULATE([WC total],FILTER(RollingCalender,RollingCalender[Date]=minx(RollingCalender,RollingCalender[Date])))
```



```dax
WC Change = [WC_current] - [WC beginning of period]
```



```dax
Min = minx(RollingCalender,RollingCalender[Date])
```



```dax
Total WC items (2) = sum('AR (2)'[OPEN_AMOUNT]) + sum('WIP (2)'[OPEN_WIP])
```



```dax
Weighted avg Age AR (2) = sum('AR (2)'[Weighted Age (2)]) / sum('AR (2)'[OPEN_AMOUNT])
```



```dax
Weighted avg Age WIP (2) = sum('WIP (2)'[Weighted Age]) / sum('WIP (2)'[OPEN_WIP])
```



```dax
Weighted avg Age WC (2) = ([Weighted avg Age AR (2)] * sum('AR (2)'[OPEN_AMOUNT]) + [Weighted avg Age WIP (2)] * sum('WIP (2)'[OPEN_WIP]) )/ (sum('WIP (2)'[OPEN_WIP])+sum('AR (2)'[OPEN_AMOUNT]))
```



```dax
Weighted avg Age AR (3) = sum('AR (3)'[Column_Weighted Age (3)]) / sum('AR (3)'[OPEN_AMOUNT])
```



```dax
Weighted avg Age WIP (3) = sum('WIP (3)'[Weighted Age (3)]) / sum('WIP (3)'[OPEN_WIP])
```



```dax
Weighted avg Age WC (3) = ([Weighted avg Age AR (3)] * sum('AR (3)'[OPEN_AMOUNT]) + [Weighted avg Age WIP (3)] * sum('WIP (3)'[OPEN_WIP]) )/ (sum('WIP (3)'[OPEN_WIP])+sum('AR (3)'[OPEN_AMOUNT]))
```



```dax
Total WC items (3) = sum('AR (3)'[OPEN_AMOUNT]) + sum('WIP (3)'[OPEN_WIP])
```



```dax
Last Refresh = "Last Refresh- " & "PBi :"& ZZ_DateLastRefresh[Last refersh PBi] & "  Cadinal Archived :" & 'Last Refresh_CARDINAL_ACC'[Last refersh Cardinal_ACC]
```



```dax
Provision Gauge_with_logic = if([Provision total] > 1.25 * [Theoretical Bad Debt], [Provision total], [Provision Gauge])

```



```dax
Measure = Not available
```



```dax
Open AR_EUR = sum(AR[OPEN_AMOUNT])
```



```dax
Open AR_EUR_Overdue = CALCULATE(Sum(AR[OPEN_AMOUNT]), AR[DAYS_OVERDUE] >0)
```



```dax
Overdue_AR vs Total_AR_EUR_% = FORMAT([Open AR_EUR_Overdue]/[Open AR_EUR], "0.0%")
```



```dax
Not Overdue_AR = [Open AR_EUR]- [Open AR_EUR_Overdue]
```



```dax
Open AR_EUR_INV = Calculate(sum(AR[OPEN_AMOUNT]) , filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV"))
```



```dax
Total WC vs INV WC_% = FORMAT(MeasureTable[Total WC items_INV]/MeasureTable[Total WC items], "0.00%")
```



```dax
Total WC items_INV = Calculate(sum(AR[OPEN_AMOUNT]) + sum(WIP[OPEN_WIP]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV"))
```



```dax
Open AR_EUR_Not_INV(other) = Calculate(sum(AR[OPEN_AMOUNT]) , filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other"))
```



```dax
Open WIP items_INV = Calculate(sum(WIP[OPEN_WIP]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV"))
```



```dax
Open WIP items_Not INV(other) = Calculate(sum(WIP[OPEN_WIP]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other"))
```



```dax
Overdue_AR = CALCULATE(Sum(AR[OPEN_AMOUNT]),
FILTER(AR, AR[Overdue_ID] = {"Overdue AR"}))
```



```dax
Overdue_AR && INS = CALCULATE(Sum(AR[OPEN_AMOUNT]),
FILTER(AR, AR[Overdue_ID] = {"Overdue AR"} 
&& AR[Function_INV & other]= {"INV"}))
```



```dax
Overdue_AR && Not INS = CALCULATE(Sum(AR[OPEN_AMOUNT]),
FILTER(AR, AR[Overdue_ID] = {"Overdue AR"} 
&& AR[Function_INV & other]<> {"INV"}))
```



```dax
Overdue_AR vs Total_AR_EUR = ([Open AR_EUR_Overdue]/[Open AR_EUR])
```



```dax
Total Overdue AR % (without INV) = FORMAT([Overdue_AR && Not INS]/[Open AR_EUR_Not_INV(other)],"00.0%")
```



```dax
Total Overdue AR(without INV) = ([Overdue_AR && Not INS]/[Overdue_AR])
```



```dax
Measure 2 = Not available
```



```dax
Measure 3 = Not available
```



```dax
Weighted avg Age AR(INV) = Calculate(sum(AR[Weighted Age]),filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV")) / Calculate(sum(AR[OPEN_AMOUNT]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV")
)
```



```dax
Weighted avg Age AR(Non INV) = Calculate(sum(AR[Weighted Age]),filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other")) / Calculate(sum(AR[OPEN_AMOUNT]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other"))
```



```dax
Weighted avg Age WIP(INV) = Calculate(sum(WIP[Weighted Age]),filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV")) / Calculate(sum(WIP[OPEN_WIP]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV")
)
```



```dax
Weighted avg Age WIP(Non INV) = Calculate(sum(WIP[Weighted Age]),filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other")) / Calculate(sum(WIP[OPEN_WIP]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other")
)
```



```dax
Weighted avg Overdue Age AR(Non INV) = Calculate(sum(AR[Weighted Overdue Age]),
    filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other"),FILTER(AR, AR[Overdue_ID] = {"Overdue AR"})) 

/ Calculate(sum(AR[OPEN_AMOUNT]), 
    filter(SAP_Function,SAP_Function[Investor_suportY_S]="Other"), FILTER(AR, AR[Overdue_ID] = {"Overdue AR"})
)
```



```dax
Weighted avg Overdue Age AR(INV) = Calculate(sum(AR[Weighted Overdue Age]),
    filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV"),FILTER(AR, AR[Overdue_ID] = {"Overdue AR"})) 

/ Calculate(sum(AR[OPEN_AMOUNT]), 
    filter(SAP_Function,SAP_Function[Investor_suportY_S]="INV"), FILTER(AR, AR[Overdue_ID] = {"Overdue AR"})
)
```



```dax
Total WC items_Excl. INV = Calculate(sum(AR[OPEN_AMOUNT]) + sum(WIP[OPEN_WIP]), filter(SAP_Function,SAP_Function[Investor_suportY_S]="other"))
```



```dax
Weighted avg Overdue Age AR = Calculate(sum(AR[Weighted Overdue Age]),
    FILTER(AR, AR[Overdue_ID] = {"Overdue AR"})) 

/ Calculate(sum(AR[OPEN_AMOUNT]), 
    FILTER(AR, AR[Overdue_ID] = {"Overdue AR"})
)
```



```dax
WIP INV % = FORMAT([Open WIP items_INV]/([Open WIP items_INV]+ [Open WIP items_Not INV(other)]),"00.0%")
```



```dax
WIP over 30 days = CALCULATE(sum(WIP[OPEN_WIP]), FILTER(WIP,WIP[AGE_OF_WIP] > 30))
```



```dax
# WIP over 30 days = CALCULATE(count(WIP[PROJECT_ID]), FILTER(WIP,WIP[AGE_OF_WIP] > 30))
```



```dax
KPI_Share of Project invoiced = [Last Week # invoiced Project]/[# WIP over 30 days]
```


## Table: RollingCalender

### Calculated Columns:


```dax
Calendar Week(ISO) = WEEKNUM(RollingCalender[Date],21) 
```


## Table: WIP

### Measures:


```dax
KPI_WIP_Unhealthy Share = CALCULATE(sum(WIP[OPEN_WIP]), WIP[AGE_OF_WIP] > 30,FILTER(WIP,WIP[OPEN_WIP]>0) ) / CALCULATE(sum(WIP[OPEN_WIP]),FILTER(WIP,WIP[OPEN_WIP]>0))
```


### Calculated Columns:


```dax
Weighted Age = WIP[AGE_OF_WIP] * WIP[OPEN_WIP]
```



```dax
Function_INV & other = if(WIP[FUNCTION_ID] = "53" || WIP[FUNCTION_ID] = "_P", "INS", "other")
```



```dax
Type = "WIP"
```



```dax
Dummy columns to be delete = ""
```



```dax
Dummy2 columns to be delete = ""
```



```dax
Dummy3 columns to be delete = ""
```


## Table: AR

### Measures:


```dax
Measure 4 = Not available
```


### Calculated Columns:


```dax
Provision % = if(AR[INVOICE_AGE]<180,0.0,if(AR[INVOICE_AGE]<270,0.25,if(AR[INVOICE_AGE]<360,0.5,1)))
```



```dax
Provision Amount = AR[Provision %] * AR[OPEN_AMOUNT]
```



```dax
Basis general bad debt = if(AR[INVOICE_AGE]<180,AR[OPEN_AMOUNT],0)
```



```dax
Weighted Age = AR[OPEN_AMOUNT] * AR[INVOICE_AGE]
```



```dax
Overdue_ID = If(AR[DAYS_OVERDUE] > 0, "Overdue AR", "Not Overdue AR") 
```



```dax
Function_INV & other = if(AR[FUNCTION_ID] = "53" || AR[FUNCTION_ID] = "_P", "INV", "other")
```



```dax
Weighted Overdue Age = AR[OPEN_AMOUNT] * AR[DAYS_OVERDUE]
```



```dax
Type = "AR"
```


## Table: AR (2)

### Calculated Columns:


```dax
Weighted Age (2) = 'AR (2)'[OPEN_AMOUNT] * 'AR (2)'[INVOICE_AGE]
```


## Table: WIP (2)

### Calculated Columns:


```dax
Weighted Age (2) = 'WIP (2)'[AGE_OF_WIP] * 'WIP (2)'[OPEN_WIP]
```



```dax
Weighted Age = 'WIP (2)'[AGE_OF_WIP] * 'WIP (2)'[OPEN_WIP]
```


## Table: AR (3)

### Calculated Columns:


```dax
Column_Weighted Age (3) = 'AR (3)'[OPEN_AMOUNT] * 'AR (3)'[INVOICE_AGE]
```


## Table: WIP (3)

### Calculated Columns:


```dax
Weighted Age (3) = 'WIP (3)'[AGE_OF_WIP] * 'WIP (3)'[OPEN_WIP]
```


## Table: ZZ_DateLastRefresh

### Measures:


```dax
Last refersh PBi = SELECTEDVALUE(ZZ_DateLastRefresh[Date Last Refreshed])
```


## Table: SAP_Function

### Calculated Columns:


```dax
Investor_suportY_S = if(
    SAP_Function[FUNCTION_ID]="53"
    || SAP_Function[FUNCTION_ID]="_P"
    , "INV", "Other")
```


## Table: Last Refresh_CARDINAL_ACC

### Measures:


```dax
Last refersh Cardinal_ACC = SELECTEDVALUE('Last Refresh_CARDINAL_ACC'[ARCHIVED_AT])
```


## Table: RECEIVABLES_ADJUSTED

### Calculated Columns:


```dax
Max_ReportIndexNumber_ID = if(RECEIVABLES_ADJUSTED[ReportIndexNumber] = MAX(RECEIVABLES_ADJUSTED[ReportIndexNumber]), 1,0)
```


## Table: RB_CORIMA_VALUE DATES

### Calculated Columns:


```dax
Current_Week_ID = if('RB_CORIMA_VALUE DATES'[PLAN_VARIANT_ID] = max('RB_CORIMA_VALUE DATES'[PLAN_VARIANT_ID]), 1, 0)
```



```dax
PLAN_VARIANT_ID = LOOKUPVALUE(FC_DATA[PLAN_VARIANT_ID_ADJ],FC_DATA[PLAN_VARIANT_SHORT_NAME], 'RB_CORIMA_VALUE DATES'[PLAN_VARIANT_SHORT_NAME])
```


## Table: FC_DATA

### Calculated Columns:


```dax
PLAN_VARIANT_ID_ADJ = if(FC_DATA[CLIENT_RATE_DATE] < TODAY(), FC_DATA[PLAN_VARIANT_ID], 0 )
```


## Table: Merge_ Project Data_Invoice

### Measures:


```dax
Last Week invoiced amount = CALCULATE(sum('Merge_ Project Data_Invoice'[AMOUNT_EUR]),'Merge_ Project Data_Invoice'[lastWeek_ InvoiceDate_ID]=1)
```



```dax
KPI_WIP to AR = [Last Week invoiced amount]/([WIP over 30 days]+ [Last Week invoiced amount])
```



```dax
KPI_ AR to Cash = [Last week cash collected]/ (CALCULATE(sum('Merge_ Project Data_Invoice'[AMOUNT_EUR]),'Merge_ Project Data_Invoice'[CLEARING_DATE_1] < TODAY()-8, filter('Merge_ Project Data_Invoice','Merge_ Project Data_Invoice'[OverdueDays] > 0 )))
```



```dax
KPI_AR_Unhealthy Share = CALCULATE(SUM(AR[OPEN_AMOUNT]),AR[DAYS_OVERDUE] >0 ) / CALCULATE(SUM(AR[OPEN_AMOUNT]))
```



```dax
Last Week # invoiced Project = CALCULATE(count('Merge_ Project Data_Invoice'[PROJECT_ID]),'Merge_ Project Data_Invoice'[lastWeek_ InvoiceDate_ID]=1,'Merge_ Project Data_Invoice'[INVOICE_LIFECYCLE_STATUS] <> {"Release Canceled"}
)
```



```dax
KPI_share of Projects Invoiced = [Last Week # invoiced Project]/ ([# WIP over 30 days]+[Last Week # invoiced Project])
```



```dax
Last week cash collected = CALCULATE(sum('Merge_ Project Data_Invoice'[AMOUNT_EUR]),'Merge_ Project Data_Invoice'[lastWeek_ ClearingDate_ID]=1,'Merge_ Project Data_Invoice'[STATUS] = {"Cleared"})
```



```dax
Last Week # invoiced canceled = CALCULATE(count('Merge_ Project Data_Invoice'[INVOICE_ID]),'Merge_ Project Data_Invoice'[lastWeek_ ClearingDate_ID]=1,'Merge_ Project Data_Invoice'[INVOICE_LIFECYCLE_STATUS] = {"Release Canceled"}
)
```



```dax
Last Week Amount invoice canceled = CALCULATE(sum('Merge_ Project Data_Invoice'[AMOUNT_EUR]),'Merge_ Project Data_Invoice'[lastWeek_ ClearingDate_ID]=1,'Merge_ Project Data_Invoice'[INVOICE_LIFECYCLE_STATUS] = {"Release Canceled"})
```


### Calculated Columns:


```dax
lastWeek_ InvoiceDate_ID = if(WEEKNUM('Merge_ Project Data_Invoice'[INVOICE_DATE])= 'Merge_ Project Data_Invoice'[Last week ISO],1,0)
```



```dax
current week ISO = WEEKNUM(TODAY(),21) 
```



```dax
Last week ISO = WEEKNUM(TODAY(),21) -1
```



```dax
lastWeek_ ClearingDate_ID = if(WEEKNUM('Merge_ Project Data_Invoice'[CLEARING_DATE_1])= ('Merge_ Project Data_Invoice'[Last week ISO]),1,0)
```

