



# DAX

|Dataset|[MVP_CostIQ_Dashboard_updated_v4](./../MVP_CostIQ_Dashboard_updated_v4.md)|
| :--- | :--- |
|Workspace|[Purchase Optimization](../../Workspaces/Purchase-Optimization.md)|

## Table: flat_table

### Measures:


```dax
calc_delta_to_reopt_bought = MAX(Evaluation[rel_delta_to_Reoptimization_bought])
```



```dax
calc_average_of_unit_price_with_unit = FORMAT(ROUND([calc_average_of_unit_price],2), "#,##0.00") & " " &  MIN(flat_table[currency_unit])
```



```dax
calc_Total Volume = sum(flat_table[demand_bought]) & " " & MIN(flat_table[unit])
```



```dax
calc_average_of_unit_price_perfect_foresight = CALCULATE([calc_average_of_unit_price_with_unit], flat_table[strategy] == "Perfect Foresight")
```



```dax
calc_average_of_unit_price = AVERAGE(flat_table[unit_price_planned])
```



```dax
calc_Total Purchase costs = FORMAT(ROUND(SUM(flat_table[unit_cost_bought]),2),"#,##.00") & " " & MIN(flat_table[currency])
```


### Calculated Columns:


```dax
calc_Demand input = flat_table[demand_bought]
```



```dax
calc_contract_rank = IF(flat_table[contract]=="Spot", 1, IF(flat_table[contract]=="M1", 2, IF(flat_table[contract]=="M2", 3, IF(flat_table[contract]=="M3",4, IF(flat_table[contract]=="M4",5,0)))))
```


## Table: Evaluation

### Measures:


```dax
calc_color_code_bg = 
//VAR best_performing = IF(SELECTEDVALUE(Evaluation[strategy]) = MAX([best_performing_strategy]), True, False)
VAR client = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Client", True, False)
VAR reopt = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Reoptimization", True, False)
VAR perfectforesight = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Perfect Foresight", True, False)
VAR worstcase = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Worst Case", True, False)
VAR forecastbased = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Forecast based", True, False)
VAR oneovern = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "1/N", True, False)
VAR DDA_ML = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "DDA-ML", True, False)

RETURN
SWITCH(
TRUE(),
//best_performing, "#A0D1FF",
client, "#FFFFF", // 005489
//reopt; "#1FA8FF";
//perfectforesight; "#B4E2FF";
//worstcase; "#BFD4E1";
//forecastbased; "#42718E";
//oneovern; "#78A4C0";
DDA_ML, "FFFFF" // 1FA8FF
)
```



```dax
calc_hedging_potential = ABS(CALCULATE(AVERAGE(Evaluation[rel_delta_to_Worst Case_bought]), FILTER(Evaluation, Evaluation[strategy] == "Perfect Foresight")))
```



```dax
calc_avg_saving_to_spot = AVERAGE(Evaluation[rel_delta_to_Spot_bought])
```



```dax
calc_avg_saving_to_client = AVERAGE(Evaluation[rel_delta_to_Client_bought])
```



```dax
calc_color_code_font = 
//VAR best_performing = IF(SELECTEDVALUE(Evaluation[strategy]) = MAX([best_performing_strategy]), True, False)
VAR client = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Client", True, False)
VAR reopt = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Reoptimization", True, False)
VAR perfectforesight = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Perfect Foresight", True, False)
VAR worstcase = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Worst Case", True, False)
VAR forecastbased = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "Forecast based", True, False)
VAR oneovern = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "1/N", True, False)
VAR DDA_ML = IF(SELECTEDVALUE('Evaluation'[Strategy]) = "DDA-ML", True, False)

RETURN
SWITCH(
TRUE(),
//best_performing, "#A0D1FF",
client, "#005489", // #FFFFFF
//reopt; "#1FA8FF";
//perfectforesight; "#B4E2FF";
//worstcase; "#BFD4E1";
//forecastbased; "#42718E";
//oneovern; "#78A4C0";
DDA_ML, "#1FA8FF") // FFFFFF
```



```dax
calc_timeslot = IF(MIN(Evaluation[year]) == MAX(Evaluation[year]), "-> " & MAX(Evaluation[year]), MIN(Evaluation[year]) & " - " & MAX(Evaluation[year]))
```



```dax
calc_Potential Savings to Perfect Foresight = (CALCULATE(AVERAGE(Evaluation[rel_delta_to_Client_bought]), Evaluation[strategy] == "Perfect Foresight"))
```



```dax
calc_Potential Savings to ML = (CALCULATE(AVERAGE(Evaluation[rel_delta_to_Client_bought]), Evaluation[strategy] == "DDA-ML"))
```



```dax
calc_Potential Loss to Worst Case = (CALCULATE(AVERAGE(Evaluation[rel_delta_to_Client_bought]), Evaluation[strategy] == "Worst Case"))
```



```dax
Measure = Not available
```


### Calculated Columns:


```dax
calc_average_unit_price_with_unit = FORMAT(ROUND(Evaluation[average_of_unit_price_bought],2),"#,##0.00") & " " & Evaluation[currency_unit]
```



```dax
calc_Total Purchase costs = Evaluation[sum_of_unit_cost_bought] & " " & Evaluation[currency]
```


## Table: Overview_Baseline_Switch


```dax

 // ATTENTION: CLIENT STRATEGY IS CURRENTLY SPOT!
 {
    ("Abs. Savings to Spot", NAMEOF('Evaluation'[abs_delta_to_Spot_bought]), 0, "Spot"),
        ("% Savings to Spot", NAMEOF([calc_avg_saving_to_spot]), 1, "Spot"),
        ("Abs. Savings to Client", NAMEOF('Evaluation'[abs_delta_to_Client_bought]), 2, "Client"),
    ("% Savings to Client", NAMEOF([calc_avg_saving_to_client]), 3, "Client")
}
```


## Table: Visual_Baseline_Switch


```dax
{
    ("% Savings to Spot", NAMEOF([calc_avg_saving_to_spot]), 0, "Spot"),
      ("% Savings to Client", NAMEOF([calc_avg_saving_to_client]), 1, "Client")
}
```


## Table: Forward_Input_Values

### Measures:


```dax
calc_current_month_year = FORMAT ( TODAY(), "yyyy-mm" )
```



```dax
calc_total_volume_oneovern = AVERAGE('Forward_Input_Values'[calc_volume_oneovern])
```



```dax
calc_total_volume_reoptmization = AVERAGE('Forward_Input_Values'[calc_volume_reoptimization])
```



```dax
calc_total_volume_dda-ml = AVERAGE('Forward_Input_Values'[calc_volume_dda-ml])
```



```dax
calc_total_volume_forecasting = AVERAGE('Forward_Input_Values'[calc_volume_forecasting])
```


### Calculated Columns:


```dax
calc_demand = 'Forward_Input_Values'[Total demand]-'Forward_Input_Values'[Volume purchased]
```



```dax
calc_months_forward_view = 
var contract = 'Forward_Input_Values'[Contract]
var spot_month = TODAY()
var m1_month = EOMONTH(TODAY(),+1)
var m2_month = EOMONTH(TODAY(),+2)
var m3_month = EOMONTH(TODAY(),+3)
var m4_month = EOMONTH(TODAY(),+4)
return 
IF(
    contract="Spot", spot_month, 
        IF(contract="M1", m1_month,
            IF(contract="M2", m2_month, IF(contract="M3", m3_month,
                IF(contract="M4", m4_month)
            )
            )
        )
    )
```



```dax
calc_purchasing_decision_oneovern = IF('Forward_Input_Values'[calc_demand] = 0, "Wait", "Buy")
```



```dax
calc_purchasing_decision_reoptimization = IF(AND('Forward_Input_Values'[calc_demand]> 0, Forward_Input_Values[Price]<= Forward_Input_Values[calc_threshold_reoptimization]),"Buy", "Wait")
```



```dax
calc_threshold_reoptimization = 
var contract = 'Forward_Input_Values'[Contract]
var spot_price = LOOKUPVALUE('Forward_Input_Values'[Price], 'Forward_Input_Values'[Contract], "Spot")
var m1_price = LOOKUPVALUE('Forward_Input_Values'[Price], 'Forward_Input_Values'[Contract], "M1")
var m2_price = LOOKUPVALUE('Forward_Input_Values'[Price], 'Forward_Input_Values'[Contract], "M2")
var m3_price = LOOKUPVALUE('Forward_Input_Values'[Price], 'Forward_Input_Values'[Contract], "M3")
var m4_price = LOOKUPVALUE('Forward_Input_Values'[Price], 'Forward_Input_Values'[Contract], "M4")

var threshold_spot = spot_price
var threshold_m1 = spot_price
var threshold_m2 = IF(spot_price< m1_price, spot_price, m1_price)
var threshold_m3 = IF(threshold_m2< m2_price, threshold_m2, m2_price) 
var threshold_m4 = IF(threshold_m3< m3_price, threshold_m3, m3_price) 

return 
    IF(contract="Spot", threshold_spot, 
        IF(contract="M1", threshold_m1, 
            IF(contract="M2", threshold_m2,
                IF(contract="M3", threshold_m3, 
                    IF(contract="M4", threshold_m4))
                )
            )
        )
```



```dax
calc_volume_reoptimization = IF('Forward_Input_Values'[calc_purchasing_decision_reoptimization] = "Buy", 'Forward_Input_Values'[calc_demand], 0)
```



```dax
calc_months_forward_view_text = 
var contract = 'Forward_Input_Values'[Contract]
var spot_month = [calc_current_month_year]
var m1_month = EOMONTH(TODAY(),+1)
var m2_month = EOMONTH(TODAY(),+2)
var m3_month = EOMONTH(TODAY(),+3)
var m4_month = EOMONTH(TODAY(),+4)
return 
    IF(contract="Spot", spot_month, 
        IF(contract="M1", FORMAT(m1_month, "yyyy-mm"),
            IF(contract="M2", FORMAT(m2_month, "yyyy-mm"), 
                IF(contract="M3", FORMAT(m3_month, "yyyy-mm"),
                    IF(contract="M4", FORMAT(m4_month, "yyyy-mm"))))))
```



```dax
calc_volume_oneovern = 0.2 * 'Forward_Input_Values'[calc_demand]
```



```dax
calc_threshold_dda-ml = 
var contract = Forward_Input_Values[Contract]
return  
    IF(contract="Spot", 0, 
        IF(contract="M1", [calc_threshold_m1], 
            IF(contract="M2", [calc_threshold_m2],
                IF(contract="M3", [calc_threshold_m3], 
                    IF(contract="M4", [calc_threshold_m4]))
                )
            )
        )
    
```



```dax
calc_purchasing_decision_dda-ml = 
IF(
    AND(
        Forward_Input_Values[Contract]= "Spot", 
        Forward_Input_Values[calc_demand]>0), 
        "Buy",
        IF(Forward_Input_Values[Price]<= Forward_Input_Values[calc_threshold_dda-ml], "Buy", "Wait"))
```



```dax
calc_volume_dda-ml = IF(Forward_Input_Values[calc_purchasing_decision_dda-ml] = "Buy", Forward_Input_Values[calc_demand], 0)
```



```dax
calc_purchasing_decision_forecast = 
IF(
    AND(
        Forward_Input_Values[Contract]= "Spot", 
        Forward_Input_Values[calc_demand]>0), 
        "Buy",
        IF(Forward_Input_Values[Price] <= Forward_Input_Values[price_forecast_input],
           "Buy",
            "Wait"))
```



```dax
calc_volume_forecasting = IF('Forward_Input_Values'[calc_purchasing_decision_forecast] = "Buy", 'Forward_Input_Values'[calc_demand], 0)
```


## Table: Forward_Table_Strategy_Switch


```dax
{
    ("Purchasing Signal", NAMEOF('Forward_Input_Values'[calc_purchasing_decision_reoptimization]), 0, "Reoptimization"),
    ("Purchasing Signal", NAMEOF('Forward_Input_Values'[calc_purchasing_decision_oneovern]), 1, "1/N strategy"),
        ("Purchasing Signal", NAMEOF('Forward_Input_Values'[calc_purchasing_decision_dda-ml]), 2, "DDA-ML"),
        ("Purchasing Signal", NAMEOF('Forward_Input_Values'[calc_purchasing_decision_forecast]), 2, "Forecasting"),
    
    ("Volume", NAMEOF('Forward_Input_Values'[calc_total_volume_reoptmization]), 3, "Reoptimization"),
    ("Volume", NAMEOF('Forward_Input_Values'[calc_total_volume_oneovern]), 4, "1/N Strategy"),
    ("Volume", NAMEOF('Forward_Input_Values'[calc_total_volume_dda-ml]), 5, "DDA-ML"),
    ("Volume", NAMEOF('Forward_Input_Values'[calc_total_volume_forecasting]), 5, "Forecasting")
}
```


## Table: feature_beta_input

### Measures:


```dax
calc_threshold_m1 = CALCULATE(SUM(feature_beta_input[calc_beta_x_feature]), Filter(feature_beta_input, feature_beta_input[contract] = "M1"))
```



```dax
calc_threshold_m2 = CALCULATE(SUM(feature_beta_input[calc_beta_x_feature]), Filter(feature_beta_input, feature_beta_input[contract] = "M2"))
```



```dax
calc_threshold_m3 = CALCULATE(SUM(feature_beta_input[calc_beta_x_feature]), Filter(feature_beta_input, feature_beta_input[contract] = "M3"))
```



```dax
calc_threshold_m4 = CALCULATE(SUM(feature_beta_input[calc_beta_x_feature]), Filter(feature_beta_input, feature_beta_input[contract] = "M4"))
```


### Calculated Columns:


```dax
feature_value = IF(feature_beta_input[beta] = "Intercept", 1, RELATED(Feature_Input_Values[feature_value]))
```



```dax
calc_beta_x_feature = feature_beta_input[beta_value] * feature_beta_input[feature_value]
```


## Table: Forecast_Input_Values

### Measures:


```dax
calc_price_forecast_m1 = CALCULATE(AVERAGE(Forecast_Input_Values[price_forecast]), Filter(Forecast_Input_Values, Forecast_Input_Values[contract] = "M1"))
```



```dax
calc_price_forecast_m2 = CALCULATE(AVERAGE(Forecast_Input_Values[price_forecast]), Filter(Forecast_Input_Values, Forecast_Input_Values[contract] = "M2"))
```



```dax
calc_price_forecast_m3 = CALCULATE(AVERAGE(Forecast_Input_Values[price_forecast]), Filter(Forecast_Input_Values, Forecast_Input_Values[contract] = "M3"))
```



```dax
calc_price_forecast_m4 = CALCULATE(AVERAGE(Forecast_Input_Values[price_forecast]), Filter(Forecast_Input_Values, Forecast_Input_Values[contract] = "M4"))
```


## Table: Strategy_performance_evaluation

### Measures:


```dax
calc_best_performing_strategy = 
CALCULATE (
    FIRSTNONBLANK (Strategy_performance_evaluation[strategy], TRUE () ),
    FILTER (
        Strategy_performance_evaluation,
        Strategy_performance_evaluation[rank] = 1
           // &&
           //  Strategy_performance_evaluation[commodity]=EARLIER(Strategy_performance_evaluation[commodity])
    )
)

//LOOKUPVALUE(Strategy_performance_evaluation[strategy]; Strategy_performance_evaluation[rank]; 1)
```


### Calculated Columns:


```dax
rank = RANKX(
    FILTER(Strategy_performance_evaluation,
    Strategy_performance_evaluation[commodity]=EARLIER(Strategy_performance_evaluation[commodity])), 
    Strategy_performance_evaluation[average_delta_to_perfect_foresight],,DESC,Skip)
```

