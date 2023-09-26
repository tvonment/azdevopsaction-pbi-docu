



# DAX

|Dataset|[20221205_Dashboard](./../20221205_Dashboard.md)|
| :--- | :--- |
|Workspace|[Purchase Optimization](../../Workspaces/Purchase-Optimization.md)|

## Table: flat_table

### Measures:


```dax
best_performing_strategy = CALCULATE(LOOKUPVALUE(Evaluation[strategy], Evaluation[rel_delta_to_Perfect Foresight_bought], MIN(Evaluation[rel_delta_to_Perfect Foresight_bought])),
FILTER(Evaluation, Evaluation[strategy] <> "Perfect Foresight")) 
//var best_perorming_unit_price_bought = CALCULATE(Min(Evaluation[Average of unit_price_bought]), Evaluation[strategy]= best_performing_strategy_)
```



```dax
delta_to_reopt_bought = MAX(Evaluation[rel_delta_to_Reoptimization_bought])
```



```dax
Measure = Not available
```



```dax
average_of_unit_price_with_unit = FORMAT(ROUND([average_of_unit_price],2), "#,##0") & " " &  MIN(flat_table[currency_unit])
```



```dax
Total Volume = sum(flat_table[demand_bought]) & " " & MIN(flat_table[unit])
```



```dax
average_of_unit_price_perfect_foresight = CALCULATE([average_of_unit_price_with_unit], flat_table[strategy] == "Perfect Foresight")
```



```dax
average_of_unit_price = AVERAGE(flat_table[unit_price_planned])
```



```dax
Total Purchase costs = FORMAT(ROUND(SUM(flat_table[unit_cost_bought]),2),"#,##0") & " " & MIN(flat_table[currency])
```


## Table: Evaluation

### Measures:


```dax
color_code_bg = 
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
hedging_potential = ABS(CALCULATE(AVERAGE(Evaluation[rel_delta_to_Worst Case_bought]), FILTER(Evaluation, Evaluation[strategy] == "Perfect Foresight")))
```



```dax
avg_saving_to_spot = AVERAGE(Evaluation[rel_delta_to_Spot_bought])
```



```dax
avg_saving_to_client = AVERAGE(Evaluation[rel_delta_to_Client_bought])
```



```dax
color_code_font = 
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
timeslot = IF(MIN(Evaluation[year]) == MAX(Evaluation[year]), MIN(Evaluation[year]), MIN(Evaluation[year]) & " - " & MAX(Evaluation[year]))
```


### Calculated Columns:


```dax
average_unit_price_with_unit = ROUND(Evaluation[average_of_unit_price_bought],2) & " " & Evaluation[currency_unit]
```



```dax
Total Purchase costs = Evaluation[sum_of_unit_cost_bought] & " " & Evaluation[currency]
```


## Table: Overview_Baseline_Switch


```dax
{
    ("Abs. Savings to Spot", NAMEOF('Evaluation'[abs_delta_to_Spot_bought]), 0, "Spot"),
        ("% Savings to Spot", NAMEOF([avg_saving_to_spot]), 1, "Spot"),
        ("Abs. Savings to Client", NAMEOF('Evaluation'[abs_delta_to_Client_bought]), 2, "Client"),
    ("% Savings to Client", NAMEOF([avg_saving_to_client]), 3, "Client")
}
```


## Table: Visual_Baseline_Switch


```dax
{
    ("% Savings to Spot", NAMEOF([avg_saving_to_spot]), 0, "Spot"),
      ("% Savings to Client", NAMEOF([avg_saving_to_client]), 1, "Client")
}
```

