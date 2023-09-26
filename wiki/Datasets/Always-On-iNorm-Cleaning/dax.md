



# DAX

|Dataset|[Always On iNorm Cleaning](./../Always-On-iNorm-Cleaning.md)|
| :--- | :--- |
|Workspace|[Clorox Data](../../Workspaces/Clorox-Data.md)|

## Table: wipes_dim Wide

### Calculated Columns:


```dax
Brand Type & Mix = CONCATENATE('wipes_dim Wide'[Clorox Brand Value],CONCATENATE("-",'wipes_dim Wide'[Clorox Type Value]))
```



```dax
Brand Type & Size = CONCATENATE([Brand Type & Mix],CONCATENATE("-",'wipes_dim Wide'[Clorox Size Value])) 
```



```dax
New EV Brand column = 
SWITCH (
    TRUE (),
    'wipes_dim Wide'[Clorox Sub Category Value] = "DILUTABLES"
        && 'wipes_dim Wide'[Clorox Brand Value] = "PINE SOL", "CLX",
    'wipes_dim Wide'[Clorox Sub Category Value] = "THROUGH THE WASH STAIN REMOVE"
        && 'wipes_dim Wide'[Clorox Brand Value] = "CLOROX 2", "CLX",
    'wipes_dim Wide'[BU] = "TRASH AND FOOD STORAGE"
        && 'wipes_dim Wide'[Clorox Brand Value] = "GLAD", "CLX",
    'wipes_dim Wide'[BU]
        IN { "GRILLING", "BRITA", "CAT LITTER","FACIAL CLEANSERS","FACIAL MASKS","FACIAL TONERS","ACNE CARE",
                                                    "FACIAL MOISTURIZERS AND TREATMENTS",
                                                    "FACIAL TOWELETTES",
                                                    "LIP CARE",
                                                    "COLD SORE",
                                                    "LIP COMBO",
                                                    "LIP GLOSS",
                                                    "LIP LINER",
                                                    "LIPSTICK",
                                                    "TINTED LIP BALM",
                                                    "LIQUID LIPSTICK/STAIN",
                                                    "COSMETIC LIP TREATMENT",
                                                    "TINTED LIP OIL"
 }
        && 'wipes_dim Wide'[Clorox Manufacturer Value] = "CLOROX COMPANY", "CLX",
    'wipes_dim Wide'[Clorox Sub Category Value]
        IN {
        "BARBECUE SAUCE",
        "AO Food",
        "SS DIPS",
        "AO DIPS",
        "DRY DIPS",
        "DRY SALAD DRESSING",
        "AO Dressing"
    }
        && 'wipes_dim Wide'[Clorox Brand Value]
        IN { "HIDDEN VALLEY", "K C MASTERPIECE", "KC MASTERPIECE", "SOY VAY" }, "CLX",
    'wipes_dim Wide'[Clorox Sub Category Value] = "SS BOTTLED/POURABLE"
        && 'wipes_dim Wide'[Clorox Brand Value] = "HIDDEN VALLEY", "CLX",
    ( 'wipes_dim Wide'[Clorox Brand Value] = "CLOROX"
        && 'wipes_dim Wide'[Clorox Sub Category Value] = "DILUTABLES"
        || 'wipes_dim Wide'[Clorox Brand Value] = "CLOROX"
        && 'wipes_dim Wide'[Clorox Sub Category Value] = "THROUGH THE WASH STAIN REMOVE" ), 'wipes_dim Wide'[Clorox Brand Value],
    'wipes_dim Wide'[Clorox Brand Value] = "CLOROX", "CLX",
    'wipes_dim Wide'[Clorox Brand Value]
)

```


## Table: wipes_val Wide

### Measures:


```dax
Avg of NP $ / unit = CALCULATE(AVERAGE('wipes_val Wide'[NP $ / unit]),FILTER('wipes_val Wide','wipes_val Wide'[Year]= [selected_year]))
```



```dax
count of size calc = CALCULATE(DISTINCTCOUNTNOBLANK('wipes_dim Wide'[SizeCalcOld]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```


### Calculated Columns:


```dax
SP_Retailer rank = RELATED('Retailer Rank'[Rank])
```



```dax
Adhoc RP = 
CONCATENATE("L",
             CONCATENATE(
                 MID('wipes_val Wide'[Refreshed Period],8,2),
                     CONCATENATE("W-",
                        RIGHT('wipes_val Wide'[Refreshed Period],8)
                        )
                        )
                        )
```


## Table: continue_BItable

### Measures:


```dax
Cat_Swot_Selected Driver test = 
IF(HASONEVALUE('Revenue Drivers'[Drivers]),
    SWITCH(
        VALUES('Revenue Drivers'[Drivers]),
        "New Items", [Innovation_%],
        "Assortment Changes", [Mix_%],
        "Price Movements", [Price_%],
        "Organic Sales Lift", [Volume_%]
    ),
    0
)
```



```dax
Cat_Swot_Selected Driver test set2 = 
IF(HASONEVALUE('Revenue Drivers'[Drivers]),
    SWITCH(
        VALUES('Revenue Drivers'[Drivers]),
        "New Items", [Innovation_%_py-1],
        "Assortment Changes", [Mix_% set2],
        "Price Movements", [Price_% set2],
        "Organic Sales Lift", [Volume_% set2]
    ),
    0
)
```



```dax
Cat_Swot_Selected_Comp_Driver_test = 

IF(HASONEVALUE(swot_data_nr[Clorox Brand Value]),
CALCULATE([Cat_Swot_Selected Driver test], FILTER(ALL('wipes_dim Wide'[New Clorox Brand Value]), 'wipes_dim Wide'[New Clorox Brand Value]=SELECTEDVALUE(swot_data_nr[Clorox Brand Value]))))

```



```dax
Cat_Swot_Selected_Comp_Driver_test_set2 = 

IF(HASONEVALUE(swot_data_nr[Clorox Brand Value]),
CALCULATE([Cat_Swot_Selected Driver test set2], FILTER(ALL('wipes_dim Wide'[New Clorox Brand Value]), 'wipes_dim Wide'[New Clorox Brand Value]=SELECTEDVALUE(swot_data_nr[Clorox Brand Value]))))
        
```


## Table: measures_table

### Measures:


```dax
selected_year = max(date_table_2[Year])
```



```dax
Revenue Growth = 
 var en = IF (
    [py_year]
        = MIN ( 'wipes_val Wide'[Year] ) - 1,
    BLANK (),
    CALCULATE (
        SUM ( 'wipes_val Wide'[$] ),
        FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
    )
        - CALCULATE (
            SUM ( 'wipes_val Wide'[$] ),
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
        )
)

return 
IF(ISBLANK(en),0,en)

```



```dax
py_year = 

Var period = SWITCH(
                    TRUE(),
                    SELECTEDVALUE(py_table[Period])="Same Period Year Ago",1,2)


return
[selected_year]-period

```



```dax
$/oz continued SKUs = 
VAR PRICE_PER_LB =
    CALCULATE (
        SUMX ( 'wipes_val Wide', 'wipes_val Wide'[$ / oz_All SKUs] ),
        FILTER ( continue_BItable, continue_BItable[Year] = [selected_year] ),
        FILTER ( continue_BItable, continue_BItable[PY] = "CONTINUE" )
    )
VAR PRICE_PER_LB2 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', 'wipes_val Wide'[$ / oz_All SKUs] ),
        FILTER ( continue_BItable, continue_BItable[Year] = [selected_year] ),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "CONTINUE" )
    )
RETURN
    IF ( [py_year] = [selected_year] - 2, PRICE_PER_LB2, PRICE_PER_LB )

```



```dax
change in $ / oz_continued SKUs = 
VAR Value1 =
    CALCULATE (
        [$/oz continued SKUs],
        FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
    )
        - CALCULATE (
 [$/oz continued SKUs] ,
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
        )
RETURN
   (IF([py_year]=MIN('wipes_val Wide'[Year])-1,BLANK(),Value1))
```



```dax
Volume continued SKUsPY = 


//var ret = SELECTEDVALUE('wipes_val Wide'[Retailer])

//return
        IF([py_year]=[selected_year]-2,CALCULATE( 
            SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),
            KEEPFILTERS(FILTER(ALL(continue_BItable[PY-1]), SEARCH( "CONTINUE", continue_BItable[PY-1], 1, 0 ) >= 1 )),
  //          KEEPFILTERS(FILTER(ALL(continue_BItable[Retailer]), SEARCH(ret, continue_BItable[Retailer], 1, 0 ) >= 1 )),
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]
            )
            ),CALCULATE( SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),
            KEEPFILTERS(FILTER(ALL(continue_BItable[PY]), SEARCH( "CONTINUE", continue_BItable[PY], 1, 0 ) >= 1 )),
    //        KEEPFILTERS(FILTER(ALL(continue_BItable[Retailer]), SEARCH(ret, continue_BItable[Retailer], 1, 0 ) >= 1 )),
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])))
```



```dax
Volume continued SKUs_CY = 

var ret = SELECTEDVALUE('wipes_val Wide'[Retailer])

return
(IF([py_year]=[selected_year]-2,
            CALCULATE( 
            SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
            KEEPFILTERS(FILTER(ALL(continue_BItable[PY-1]), SEARCH( "CONTINUE", continue_BItable[PY-1], 1, 0 ) >= 1 )),
            //KEEPFILTERS(FILTER(ALL(continue_BItable[Retailer]), SEARCH(ret, continue_BItable[Retailer], 1, 0 ) >= 1 )),
            //KEEPFILTERS(FILTER(ALL(continue_BItable), SEARCH(ret, continue_BItable[Retailer], 1, 0 ) >= 1 )),
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]
            )
            ),CALCULATE( SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
            KEEPFILTERS(FILTER(ALL(continue_BItable[PY]), SEARCH( "CONTINUE", continue_BItable[PY], 1, 0 ) >= 1 )),
            //KEEPFILTERS(FILTER(ALL(continue_BItable[Retailer]), SEARCH(ret, continue_BItable[Retailer], 1, 0 ) >= 1 )),
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))))
```



```dax
Price Impact = 

VAR Table1 =
    SUMMARIZE ('wipes_val Wide',
       'wipes_val Wide'[Product Key],
        "$/oz continued SKUs_Year1",
            CALCULATE (
                [$/oz continued SKUs],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year])
            ),
        "$/oz continued SKUs_Year2",
            CALCULATE (
                 [$/oz continued SKUs],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            ),
        "Volume Continued SKUs_Year1",
            CALCULATE (
               [Volume_Sales] ,
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            )
    )
VAR en = IF([py_year]<MIN('wipes_val Wide'[Year]),BLANK(),
    
    CALCULATE(SUMX(table1,([$/oz continued SKUs_Year1]-[$/oz continued SKUs_Year2])*[Volume Continued SKUs_Year1]))
)
    RETURN
   IF((en)<>0,(en),0)
```



```dax
NP Price = 
Var Table1 =
SUMMARIZE (
    'wipes_val Wide',
    'wipes_dim Wide'[Product Key],
    'wipes_val Wide'[Retailer],
    "W.AVG.P", [W.Avg.P],
    "year2  $/lb_All SKUs py",
        CALCULATE (
            [$/oz continued SKUs],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
        ),
    "Total Volume py",
        CALCULATE(
            [Volume_Sales],
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year])
            ))

     

        var en = SUMX(Table1,([W.AVG.P]-[year2  $/lb_All SKUs py] )*[Total Volume py])

return
IF(ISBLANK(en),0,en)

        
```



```dax
Year Promo,Holding promo constant from PY = 
VAR Table1 =
    SUMMARIZE (
        'wipes_val Wide',
        'wipes_dim Wide'[Product Key],
        'wipes_val Wide'[Retailer],
        "NP $/lb_year1",
            CALCULATE (
                [NP $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            ),
        "NP $/lb_year2",
            CALCULATE (
                [NP $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            ),
        "promo $/lb year2",
            CALCULATE (
                [Promo $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            )
    )
RETURN
    IF (
        [py_year] < MIN ( 'wipes_val Wide'[Year] ),
        BLANK (),
        
            CALCULATE (
                SUMX ( Table1, [NP $/lb_year1] - ( [NP $/lb_year2] - [promo $/lb year2] ) )
            )
        )
```



```dax
NP $ / oz = IF([py_year]=[selected_year]-2,CALCULATE (
    SUMX ( 'wipes_val Wide', [NP $ / oz] ),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
    FILTER ( continue_BItable, continue_BItable[PY-1] = "CONTINUE" )
),

CALCULATE (
    SUMX ( 'wipes_val Wide', [NP $ / oz] ),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
    FILTER ( continue_BItable, continue_BItable[PY] = "CONTINUE" )
)
)
```



```dax
Promo $ / oz = 
IF([py_year]=[selected_year]-2,
CALCULATE(SUMX('wipes_val Wide',[Promo $ / oz]),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),FILTER(continue_BItable,continue_BItable[PY-1]="CONTINUE")),
CALCULATE(SUMX('wipes_val Wide',[Promo $ / oz]),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),FILTER(continue_BItable,continue_BItable[PY]="CONTINUE")))
```



```dax
Promo Price = 
 Var Table1 =
SUMMARIZE (
    'wipes_val Wide',
    'wipes_dim Wide'[Product Key],
    'wipes_val Wide'[Retailer],
    "W.AVG.P", [W.Avg.P],
    "year1 $/lb_All SKUs py",
        CALCULATE (
            [$/oz continued SKUs],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
        ),
    "year2 $/lb_All SKUs py",
        CALCULATE (
           [$/oz continued SKUs],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
        ),
    "Total Volume py",
        CALCULATE(
            [Volume_Sales],
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year])
            ))

    
          var en =  CALCULATE(
                SUMX(Table1,
                    ([year1 $/lb_All SKUs py]-[year2 $/lb_All SKUs py]-([W.Avg.P]-[year2 $/lb_All SKUs py]))
                *[Total Volume py] ),FILTER(continue_BItable,continue_BItable[PY]="CONTINUE")
        )

return
IF(ISBLANK(en),0,en)



```



```dax
W.Avg.P = 
          
Var Table1 =
SUMMARIZE (
    'wipes_val Wide',
    'wipes_dim Wide'[Product Key],
    'wipes_val Wide'[Retailer],
    "Year Promo,Holding promo constant from PY", IFERROR([Year Promo,Holding promo constant from PY],0),
    "PY Promo Volume",
        CALCULATE (
           [Promo Volume],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
        ),  
    "year1 NP $/lb",
        CALCULATE (
            [NP $ / oz],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
        ),  
    "year2 NP Volume",
        CALCULATE (
            [NP Volume],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
        ),
    "year2 Total Volume",
        CALCULATE (
            [Volume_Sales],
            FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] ))
)
var value1=
IFERROR(
    CALCULATE(
        SUMX(Table1,DIVIDE((([Year Promo,Holding promo constant from PY]*[PY Promo Volume])+([year1 NP $/lb]*[year2 NP Volume])),[year2 Total Volume]))),0)

Return
value1
```



```dax
NP Volume = 
IF([py_year]=[selected_year]-2,CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[NP Volume]),FILTER(continue_BItable,continue_BItable[PY-1]= "CONTINUE")),CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[NP Volume]),FILTER(continue_BItable,continue_BItable[PY]="CONTINUE")))
```



```dax
Volume_Sales = IF([py_year]=[selected_year]-2,CALCULATE (
            SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Volume Sales] ),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
            FILTER ( continue_BItable, continue_BItable[PY-1] = "CONTINUE" )
     ),CALCULATE (
            SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Volume Sales] ),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
            FILTER ( continue_BItable, continue_BItable[PY] = "CONTINUE" )
     ))
```



```dax
Depth Difference = 
VAR Table1 =
    SUMMARIZE (
        'wipes_val Wide',
        'wipes_dim Wide'[Product Key],
        'wipes_val Wide'[Retailer],
        "Year1 NP $/lb",
            CALCULATE (
                [NP $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            ),
        "Year1 promo $/lb",
            CALCULATE (
                [Promo $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            ),
        "Year2 NP $/lb",
            CALCULATE (
                [NP $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            ),
        "Year2 promo $/lb",
            CALCULATE (
                [Promo $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            ))
RETURN
    IF (
        [py_year]
            = MIN ( 'wipes_val Wide'[Year] ) - 1,
        BLANK (),
        
            SUMX (
                Table1,
                ( [Year1 NP $/lb] - [Year1 promo $/lb] ) - ( [Year2 NP $/lb] - [Year2 promo $/lb] )
            )
        )

```



```dax
Depth Calculation = 

Var Table1=SUMMARIZE(
    'wipes_val Wide',
    'wipes_dim Wide'[Product Key],
    'wipes_val Wide'[Retailer],
    "Depth Difference",[Depth Difference],
    "Year1 Total volume",CALCULATE([Volume_Sales],FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year])),
    "Year2 Total volume",CALCULATE([Volume_Sales],FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])),
    "Year2 promo volume",CALCULATE([Promo Volume],FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])))

    var en =
    
    SUMX(Table1,(-1*[Depth Difference])*DIVIDE([Year2 promo volume],[Year2 Total volume])*[Year1 Total volume])


    return
IF(ISBLANK(en),0,en)

```



```dax
Promo Volume = 

IF([py_year]=[selected_year]-2,CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[Promo Volume]),FILTER(continue_BItable,continue_BItable[PY-1]= "CONTINUE")),CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[Promo Volume]),FILTER(continue_BItable,continue_BItable[PY]= "CONTINUE")))
```



```dax
Pressure Calculation = 

VAR Table1 =
    SUMMARIZE (
        'wipes_val Wide',
        'wipes_dim Wide'[Product Key],
        'wipes_val Wide'[Retailer],
        "Year1  Promo volume",
            CALCULATE (
                [Promo Volume],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            ),
        "Year2 Promo volume ",
            CALCULATE (
                [Promo Volume],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            ),
        "Year1 Total Volume",
            CALCULATE (
                [Volume_Sales],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            ),
        "Year2 Total Volume",
            CALCULATE (
                [Volume_Sales],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
            ),
        "year1 NP $/lb",
            CALCULATE (
                [NP $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            ),
        "year1 Promo $/lb",
            CALCULATE (
                [Promo $ / oz],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            )
    )
var en =
   IF([py_year]=MIN('wipes_val Wide'[Year])-1,BLANK(),
        SUMX (
            Table1,
            -1 * ( [year1 NP $/lb] - [year1 Promo $/lb] ) * [Year1 Total Volume]
                * (
                    DIVIDE ( [Year1  Promo volume], [Year1 Total Volume] )
                        - DIVIDE ( [Year2 Promo volume ], [Year2 Total Volume] )
                )
        )
)


return
IF(ISBLANK(en),0,en)

```



```dax
year2 Mix = 
var val=  CALCULATE(
          [Volume continued SKUsPY],
          ALLSELECTED()
          )    

 var table1 = SUMMARIZE('wipes_val Wide',
     'wipes_val Wide'[Product Key],
     'wipes_val Wide'[Retailer],
     "mix",[Volume continued SKUsPY]
)
    Return
 IFERROR(
     SUMX(table1,
          [mix]/val),
     0
     )

```



```dax
Year Like for Like Volume = 
      var val1=  CALCULATE(
          [Volume continued SKUs_CY],
          ALLSELECTED()
          ) 
      var val=  CALCULATE(
          [Volume continued SKUsPY],
          ALLSELECTED()
          )     

 var table1 = CALCULATETABLE(SUMMARIZE('wipes_val Wide','wipes_val Wide'[Product Key],
     
     "Volume cont_py",[Volume continued SKUsPY]
))
    Return
  SUMX(table1,
    DIVIDE([Volume cont_py],val,0)*val1)
    
```



```dax
Volume continued SKUs(all_selected) = 

CALCULATE([Volume continued SKUsPY],ALLSELECTED()

)
```



```dax
Like for Like Volume Impact = 

VAR Table1 =
  SUMMARIZE (
        'wipes_val Wide',
        'wipes_val Wide'[Product Key],
        "mix", [Volume continued SKUsPY],
        "price/lb",
                CALCULATE (
                    [$/oz continued SKUs],
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ) ,
        "total volume", CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])),
        "val2",
    CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () ),
    "val1",
    CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () )
    )
var en =CALCULATE( SUMX ( Table1, ( ( ( [mix] / [val2] ) * [val1] ) - [total volume] ) * [price/lb] ))

RETURN
    IF ((en
       )<>0,
       (
       en),0)



```



```dax
Velocity = 

VAR val1 =
    CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () )
VAR val =
    CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () )
VAR Table1 =
    CALCULATETABLE (
        SUMMARIZE (
            'wipes_val Wide',
            'wipes_dim Wide'[Product Key],
            "mix", [Volume continued SKUsPY],
            "Year2 $/lb",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', [$ / oz_All SKUs] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year2 Volume",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Volume Sales] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year2 TDP",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[TDP] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year1 TDP",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[TDP] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
                ),
            "val1", CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () ),
            "val", CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () )
        )
    )
var en = 
    IFERROR (
        SUMX (
            table1,
            (
                IFERROR ( ( ( [mix] / [val] ) * [val1] ) / [Year1 TDP], 0 )
                    - IFERROR ( ( [Year2 Volume] / [Year2 TDP] ), 0 )
            ) * [Year1 TDP] * [Year2 $/lb]
        ),
        0
    )
return 
IF([Like for Like Volume Impact]=0 && [Distribution 1]=0 || ISBLANK(en),0,en)
```



```dax
Distribution = 

var Table1= SUMMARIZE(VALUES('wipes_val Wide'),
                        "Year2 $/lb",CALCULATE([$/oz continued SKUs],FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])),
                        "Year2 Volume",[Volume continued SKUsPY],
                       "Year2 TDP",CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[TDP]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])),
                       "Year1 TDP",CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[TDP]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year])))
                        
    Return
 IFERROR(
     SUMX(table1,([Year1 TDP]/[Year2 TDP]-1)*[Year2 Volume]*[Year2 $/lb]
     ),
     0
     )
```



```dax
Baseline Velocity = 
VAR val1 =
    CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () )
VAR val =
    CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () )
VAR table1 =
    CALCULATETABLE (
        SUMMARIZE (
            'wipes_val Wide',
            'wipes_val Wide'[Product Key],
            'wipes_val Wide'[Retailer],
            "Volume cont_py", [Volume continued SKUsPY],
            "Year1 Total Volume", [Volume continued SKUs_CY],
            "Year1 Baseline Volume",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Baseline Volume] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
                ),
            "Year2 Baseline Volume",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Baseline Volume] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year2 $/lb",
                    CALCULATE (
                        [$/oz continued SKUs],
                        FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year1 TDP",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[TDP] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
                ),
            "Year2 TDP",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[TDP] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "val1", CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () ),
            "val", CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () )
        )
    )
var en = 
    IFERROR (
        SUMX (
            table1,
            ( ( ( ( [Year1 Baseline Volume] / [Year1 Total Volume] ) * ( ( [Volume cont_py] / [val] ) * [val1] ) ) / [Year1 TDP] ) - ( [Year2 Baseline Volume] / [Year2 TDP] ) ) * [Year1 TDP] * [Year2 $/lb]
        ),
        0
    )
return
IF(ISBLANK(en),0,en)

```



```dax
Incremental Velocity = 
VAR val1 =
    CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () )
VAR val =
    CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () )
VAR table1 =
    CALCULATETABLE (
        SUMMARIZE (
            'wipes_val Wide',
            'wipes_val Wide'[Product Key],
            "Volume cont_py", [Volume continued SKUsPY],
            "Year1 Total Volume", [Volume continued SKUs_CY],
            "Year1 Baseline Volume",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Baseline Volume] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
                ),
            "Year2 Baseline Volume",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Baseline Volume] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year2 $/lb",
                CALCULATE (
                    [$/oz continued SKUs],
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "Year1 TDP",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[TDP] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
                ),
            "Year2 TDP",
                CALCULATE (
                    SUMX ( 'wipes_val Wide', 'wipes_val Wide'[TDP] ),
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year] )
                ),
            "val1", CALCULATE ( [Volume continued SKUs_CY], ALLSELECTED () ),
            "val", CALCULATE ( [Volume continued SKUsPY], ALLSELECTED () )
        )
    )
var en =
    (
        IFERROR (
            SUMX (
                table1,
                ( ( ( ( ( ( [Year1 Total Volume] - [Year1 Baseline Volume] ) / [Year1 Total Volume] ) * ( ( [Volume cont_py] / [val] ) * [val1] ) ) / [Year1 TDP] ) - ( [Volume cont_py] - [Year2 Baseline Volume] ) / [Year2 TDP] ) ) * [Year1 TDP] * [Year2 $/lb]
            ),
            0
        )
    )
return
IF(ISBLANK(en),0,en)

```



```dax
LY SKU Mix within Brand1 = 
VAR val2 =
    CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Clorox Type Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        )
    )
VAR table1 =
    SUMMARIZE (
        'wipes_val Wide',
        "mix", [Volume continued SKUsPY]
    )
RETURN
    IFERROR ( SUMX ( table1, [mix] / val2 ), 0 )

```



```dax
LY Brand subtotal = CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Clorox Type Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
```



```dax
LY SKU Mix within Brand2 = IF(HASONEVALUE('wipes_dim Wide'[Clorox Brand Value]),[LY SKU Mix within Brand1],SUMX(VALUES('wipes_dim Wide'[Clorox Brand Value]),[LY SKU Mix within Brand1]))
```



```dax
LY Manufacturer subtotal = CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (continue_BItable))
```



```dax
LY Brand Mix% of Manufacturer = IFERROR( DIVIDE([LY Brand subtotal],[LY Manufacturer subtotal]),0)
```



```dax
LY Brand Average Price 1 = 
var   nom= CALCULATE([Brand total price], ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Clorox Type Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
Var den= [LY Brand subtotal]
        Return
       IFERROR( DIVIDE(nom,den),0)
```



```dax
Brand total price = CALCULATE(SUMX('wipes_val Wide',[$]  ),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))                                                                                                                             
```



```dax
CY Brand subtotal = CALCULATE (
        [Volume continued SKUs_CY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Clorox Type Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
```



```dax
Brand L4L CY volume = 

var value1=CALCULATE([Volume continued SKUs_CY],ALLSELECTED())
var value2= [LY Brand Mix% of Manufacturer]
Return
value1*value2
```



```dax
Brand Mix Allocated 1 = 
 ([CY Brand subtotal]- [Brand L4L CY volume])*[LY Brand Average Price 1]*[LY SKU Mix within Brand2]



```



```dax
Brand Mix Allocated 2 = 


var en = IF(HASONEVALUE('wipes_dim Wide'[Clorox Brand Value]),[Brand Mix Allocated 1],SUMX(SUMMARIZE('wipes_dim Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_dim Wide'[Product]),[Brand Mix Allocated 1]))

return
IF(ISBLANK(en),0,en)




```



```dax
LY type within brand subtotal = 
    CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        )
    )

```



```dax
LY SKU mix within type within brand 1 = 
VAR val2 =
    CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        )
    )
VAR table1 =
    SUMMARIZE (
        'wipes_val Wide',
        "mix", [Volume continued SKUsPY]
    )
RETURN
    IFERROR ( SUMX ( table1, [mix] / val2 ), 0 )

```



```dax
LY SKU mix within type within brand 2 = 
IF(HASONEVALUE('wipes_dim Wide'[Product Key]),[LY SKU mix within type within brand 1],SUMX(VALUES('wipes_val Wide'[Product Key]),[LY SKU mix within type within brand 1]))
```



```dax
LY Type Mix% of Brand = IFERROR( DIVIDE([LY type within brand subtotal],[LY Brand subtotal]),0)
```



```dax
LY Brand Average Price 2 = IF(HASONEVALUE('wipes_dim Wide'[Clorox Brand Value]),[LY Brand Average Price 1],SUMX(VALUES('wipes_dim Wide'[Clorox Brand Value]),[LY Brand Average Price 1]))
```



```dax
Ly Type Average price = 
var   nom= CALCULATE([Brand total price], ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
Var den= [LY_type_subtotal]
        Return
       IFERROR( DIVIDE(nom,den),0)
```



```dax
LY_type_subtotal = CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
```



```dax
CY type subtotal = CALCULATE (
        [Volume continued SKUs_CY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product]
        ))
```



```dax
Type L4L CY Volume = 

var value1=CALCULATE (
       [Volume continued SKUs_CY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Clorox Type Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
        
var value2= [LY Type Mix% of Brand]
Return
IFERROR([CY Brand subtotal]*[LY Type Mix% of Brand],0)
```



```dax
Type Mix allocated 1 = IFERROR(([CY type subtotal]-[Type L4L CY Volume])*[Ly Type Average price]*[LY SKU mix within type within brand 1],0)
```



```dax
Type Mix Allocated 2 = 


var en = IF(HASONEVALUE('wipes_dim Wide'[Clorox Type Value]),[Type Mix allocated 1],SUMX(SUMMARIZE('wipes_dim Wide','wipes_dim Wide'[Clorox Type Value],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_dim Wide'[Product]),[Type Mix allocated 1]))

return
IF(ISBLANK(en),0,en)




```



```dax
LY_size_subtotal = CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
```



```dax
LY size within type and brand subtotal = 
    CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED('wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product]
        )
    )
```



```dax
LY size mix % of brand & type = IFERROR(DIVIDE([LY size within type and brand subtotal],[LY_type_subtotal]),0)
```



```dax
Ly Size Average price = 
var   nom= CALCULATE([Brand total price], ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
Var den= [LY_size_subtotal]
        Return
       IFERROR( DIVIDE(nom,den),0)
```



```dax
CY Size subtotal = IFERROR(CALCULATE (
        [Volume continued SKUs_CY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        )),0)
```



```dax
Size L4L CY Volume = 

var value1=CALCULATE (
       [Volume continued SKUs_CY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        ))
        
var value2= [LY size mix % of brand & type]
Return
value1*value2
```



```dax
Size Mix allocated 1 = ( [CY Size subtotal]-[Size L4L CY Volume])*[Ly Size Average price]*[LY SKU Size mix within type and brand 2]
```



```dax
LY SKU size mix within type and brand 1 = 
VAR val2 =
    CALCULATE (
        [Volume continued SKUsPY],
        ALLSELECTED (
            'wipes_dim Wide'[Clorox Category Value],
            'wipes_dim Wide'[Clorox Deal Pack Value],
            'wipes_dim Wide'[Clorox Manufacturer Value],
            'wipes_dim Wide'[Clorox Pack Type Value],
            'wipes_dim Wide'[Clorox Segment Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Size Range Value],
            'wipes_dim Wide'[Clorox Sub Category Value],
            'wipes_dim Wide'[Clorox Sub Type Value],
            'wipes_dim Wide'[Clorox SubBrand Value],
            'wipes_dim Wide'[Product],
            'wipes_dim Wide'[Product Key]
        )
    )
VAR table1 =
    SUMMARIZE (
        'wipes_val Wide',
        "mix", [Volume continued SKUsPY]
    )
RETURN
    IFERROR ( SUMX ( table1, [mix] / val2 ), 0 )
```



```dax
LY SKU Size mix within type and brand 2 = 
IF(HASONEVALUE('wipes_dim Wide'[Clorox Brand Value]),[LY SKU size mix within type and brand 1],SUMX(VALUES('wipes_dim Wide'),[LY SKU size mix within type and brand 1]))
```



```dax
Size Mix Allocated 2 = 

VAR en = IF(HASONEVALUE('wipes_dim Wide'[Clorox Size Value]),[Size Mix allocated 1],SUMX(SUMMARIZE('wipes_dim Wide','wipes_dim Wide'[Clorox Size Value],'wipes_dim Wide'[Clorox Type Value],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_dim Wide'[Product]),[Size Mix allocated 1]))

return
IF(ISBLANK(en),0,en)
```



```dax
Mix Calculation = 
IFERROR(([Volume continued SKUs_CY]-[Year Like for Like Volume])*[Price/lb_py],0)

```



```dax
Price/lb_py = CALCULATE([$/oz continued SKUs],FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
```



```dax
Mix calculation 1 = 

var en = 
// SWITCH(TRUE, DISTINCTCOUNT('wipes_val Wide'[Product Key]) =1,

// IF( ISINSCOPE('wipes_val Wide'[Product Key]),[Mix Calculation],SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value]),[Mix Calculation]))

IF( ISINSCOPE('wipes_val Wide'[Product Key]),[Mix Calculation],
SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value]),[Mix Calculation])
)


return

IF(ISBLANK(en),0,en)
```



```dax
Other Mix = [Mix calculation 1]-[Brand Mix Allocated 2]-[Type Mix Allocated 2]-[Size Mix Allocated 2]
```



```dax
Distribution 1 = 

var en = IF(HASONEVALUE('wipes_val Wide'[Product Key]),[Distribution],SUMX(VALUES('wipes_val Wide'[Product Key]),[Distribution]))

return
IF(ISBLANK(en),0,en)

```



```dax
Incremental Velocity1 = IF(HASONEVALUE('wipes_val Wide'[Product Key]),[Incremental Velocity],SUMX(VALUES('wipes_val Wide'[Product Key]),[Incremental Velocity]))
```



```dax
PP_Promo Units = CALCULATE(SUM('wipes_val Wide'[Any Promo Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
mNP Units = CALCULATE(SUM('wipes_val Wide'[Any Promo Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
PP_NP Units = CALCULATE(SUM('wipes_val Wide'[NP Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
PP_%NP Units = DIVIDE([PP_NP Units],[PP_Total Units])
```



```dax
PP_%Promo Units = DIVIDE([PP_Promo Units],[PP_Total Units])
```



```dax
PP_Total Units = [PP_Promo Units]+[PP_NP Units]
```



```dax
PP_% Units change = 
var a = [PP_Total Units]
var b = CALCULATE(SUM('wipes_val Wide'[Any Promo Units]), FILTER('wipes_val Wide','wipes_val Wide'[Year]= [py_year]))
var c = CALCULATE(SUM('wipes_val Wide'[NP Units]), FILTER('wipes_val Wide','wipes_val Wide'[Year]= [py_year]))

return DIVIDE((a-(b+c)), (b+C),0)

```



```dax
PP_Total units%_Pack = 
var dollar = [PP_Total Units]
var deno = CALCULATE([PP_Total Units],ALL('wipes_val Wide'[Price per pack rng],'wipes_val Wide'[Index P range])
)
return
DIVIDE(dollar,deno,0)

```



```dax
PP_Total_Units_Pack = 
CONCATENATE (
    ( FORMAT ([PP_Total units%_Pack] , "0.0%" ) ),
    CONCATENATE (
        "(",
        CONCATENATE ( FORMAT ( [PP_Total Units], "#,##,,.0M" ), ")" )
    )
)





```



```dax
DT Mix calculation 1 = 

SWITCH(TRUE, DISTINCTCOUNT('wipes_val Wide'[Product Key]) =1,
IF((IF( ISINSCOPE('wipes_val Wide'[Product Key]),[Mix Calculation],SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_val Wide'[Retailer]),[Mix Calculation])))<>0,

(IF( ISINSCOPE('wipes_val Wide'[Product Key]),[Mix Calculation],SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_val Wide'[Retailer]),[Mix Calculation]))),0)
,
IF((IF( HASONEVALUE('wipes_val Wide'[Product Key]),[Mix Calculation],SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_val Wide'[Retailer]),[Mix Calculation])))<>0,

(IF( HASONEVALUE('wipes_val Wide'[Product Key]),[Mix Calculation],SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value],'wipes_val Wide'[Retailer]),[Mix Calculation]))),0)

)



```



```dax
DT Mix_% = DIVIDE([DT Mix calculation 1],[PY Price($)],0)
```



```dax
PP_total units%_Volume = 
var dollar = [PP_Total Units]
var deno = CALCULATE([PP_Total Units],ALL('wipes_val Wide'[Price per vol rng],'wipes_val Wide'[Price per vol rng idx])
)
return
DIVIDE(dollar,deno,0)
```



```dax
PPTotal_Units_Vol = 
CONCATENATE (
    ( FORMAT ([PP_total units%_Volume] , "0.0%" ) ),
    CONCATENATE (
        "(",
        CONCATENATE ( FORMAT ( [PP_Total Units], "#,##,,.0M" ), ")" )
    )
)
```



```dax
APP_Avg of $/unit = CALCULATE(AVERAGE('wipes_val Wide'[$/unit]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
APP_TotalUnits cy = CALCULATE(SUM('wipes_val Wide'[Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
APP_Avg of $/volume = CALCULATE(AVERAGE('wipes_val Wide'[$ / oz_All SKUs]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
APP_TotalUnits py = CALCULATE(SUM('wipes_val Wide'[Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
```



```dax
PP NP YOY % change = 
var a = CALCULATE(SUM('wipes_val Wide'[NP Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var b = CALCULATE(SUM('wipes_val Wide'[NP Units]), FILTER('wipes_val Wide','wipes_val Wide'[Year]= [py_year]))

return DIVIDE((a-b),b,0)

```



```dax
PP NP yoy tt = 
CONCATENATE (
    ( FORMAT ([PP_%NP Units] , "0.0%" ) ),
    CONCATENATE (
        " (",
        CONCATENATE ( FORMAT ([PP NP YOY % change] , "0.0%" ), ")" )
    )
)

```



```dax
PP Promo YOY % change = 
var a = CALCULATE(SUM('wipes_val Wide'[Any Promo Units]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var b = CALCULATE(SUM('wipes_val Wide'[Any Promo Units]), FILTER('wipes_val Wide','wipes_val Wide'[Year]= [py_year]))

return DIVIDE((a-b),b,0)

```



```dax
PP promo yoy tt = 
CONCATENATE (
    ( FORMAT ([PP_%Promo Units] , "0.0%" ) ),
    CONCATENATE (
        " (",
        CONCATENATE ( FORMAT ([PP Promo YOY % change] , "0.0%" ), ")" )
    )
)

```



```dax
$ Share bu levl = 
var all_brand= CALCULATE([$ cy],ALL('wipes_dim Wide'[Clorox Sub Category Value]))

return
DIVIDE([$ cy],all_brand,0)

```



```dax
$ share bu level pt chg = 
                
                    ([$ Share bu levl]-[$ share bu levl py])*100
                    

```



```dax
$ share bu levl py = 
var all_brand= CALCULATE([$_PY],ALL('wipes_dim Wide'[Clorox Sub Category Value]))
return
 DIVIDE([$_PY],all_brand,0)

```



```dax
$_PY = CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
```



```dax
$ Share = 
var all_brand= CALCULATE([$ cy],ALL('wipes_dim Wide'[Clorox Brand Value]))

return
DIVIDE([$ cy],all_brand,0)

```



```dax
$ share pt chg = 
                
                    ([$ Share]-[$ share py])
                    

```



```dax
$ share py = 
var all_brand= CALCULATE([$_PY],ALL('wipes_dim Wide'[Clorox Brand Value]))
return
 DIVIDE([$_PY],all_brand,0)

```



```dax
Volume continued SKUs_CY set 2 = 
(IF(SELECTEDVALUE(py_table[Period])="Same Period Year Ago",
            CALCULATE( 
            SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
            KEEPFILTERS(FILTER(ALL(continue_BItable[PY-1]), SEARCH( "CONTINUE", continue_BItable[PY-1], 1, 0 ) >= 1 )),
            
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]
            )
            ),0))
```



```dax
Volume continued SKUsPY set2 = 



        IF(SELECTEDVALUE(py_table[Period])="Same Period Year Ago",CALCULATE( 
            SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),
            KEEPFILTERS(FILTER(ALL(continue_BItable[PY-1]), SEARCH( "CONTINUE", continue_BItable[PY-1], 1, 0 ) >= 1 )),
  
            FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]-1
            )
            ),0)
```



```dax
$/oz continued SKUs set2 = 

VAR PRICE_PER_LB2 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', 'wipes_val Wide'[$ / oz_All SKUs] ),
        FILTER ( continue_BItable, continue_BItable[Year] = [selected_year] ),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "CONTINUE" )
    )
RETURN
    IF ( SELECTEDVALUE(py_table[Period])="Same Period Year Ago", PRICE_PER_LB2,0 )

```



```dax
Volume_Sales set2 = IF(SELECTEDVALUE(py_table[Period])="Same Period Year Ago",CALCULATE (
            SUMX ( 'wipes_val Wide', 'wipes_val Wide'[Volume Sales] ),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),
            FILTER ( continue_BItable, continue_BItable[PY-1] = "CONTINUE" )
     ),0)
```



```dax
Price/lb_py set2 = CALCULATE([$/oz continued SKUs set2],FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]-1))
```



```dax
Like for Like Volume Impact set2 = 

VAR Table1 =
  SUMMARIZE (
        'wipes_val Wide',
        'wipes_val Wide'[Product Key],
        "mix", [Volume continued SKUsPY set2],
        "price/lb",
                CALCULATE (
                    [$/oz continued SKUs set2],
                    FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year]-1 )
                ) ,
        "total volume", CALCULATE(SUMX('wipes_val Wide','wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]-1)),
        "val2",
    CALCULATE ( [Volume continued SKUsPY set2], ALLSELECTED () ),
    "val1",
    CALCULATE ( [Volume continued SKUs_CY set 2], ALLSELECTED () )
    )
var en =CALCULATE( SUMX ( Table1, ( ( ( [mix] / [val2] ) * [val1] ) - [total volume] ) * [price/lb] ))

RETURN
    IF ((en
       )<>0,
       (
       en),0)



```



```dax
Mix Calculation set2 = 
IFERROR(([Volume continued SKUs_CY set 2]-[Year Like for Like Volume set2])*[Price/lb_py set2],0)

```



```dax
Year Like for Like Volume set2 = 
      var val1=  CALCULATE(
          [Volume continued SKUs_CY set 2],
          ALLSELECTED()
          ) 
      var val=  CALCULATE(
          [Volume continued SKUsPY set2],
          ALLSELECTED()
          )     

 var table1 = CALCULATETABLE(SUMMARIZE('wipes_val Wide','wipes_val Wide'[Product Key],
     
     "Volume cont_py",[Volume continued SKUsPY set2]
))
    Return
  SUMX(table1,
    DIVIDE([Volume cont_py],val,0)*val1)
    
```



```dax
Mix calculation 1 set2 = 

var en = 
IF( ISINSCOPE('wipes_val Wide'[Product Key]),[Mix Calculation set2],
SUMX(SUMMARIZE('wipes_val Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product],'wipes_dim Wide'[Clorox Sub Category Value]),[Mix Calculation set2])
)


return

IF(ISBLANK(en),0,en)
```



```dax
Price Impact set2 = 

VAR Table1 =
    SUMMARIZE ('wipes_val Wide',
       'wipes_val Wide'[Product Key],
        "$/oz continued SKUs_Year1",
            CALCULATE (
                [$/oz continued SKUs set2],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year])
            ),
        "$/oz continued SKUs_Year2",
            CALCULATE (
                 [$/oz continued SKUs set2],
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [py_year]-1 )
            ),
        "Volume Continued SKUs_Year1",
            CALCULATE (
               [Volume_Sales set2] ,
                FILTER ( 'wipes_val Wide', 'wipes_val Wide'[Year] = [selected_year] )
            )
    )
VAR en = IF(SELECTEDVALUE(py_table[Period])="Same Period Year Ago",
    
    CALCULATE(SUMX(table1,([$/oz continued SKUs_Year1]-[$/oz continued SKUs_Year2])*[Volume Continued SKUs_Year1])),0
)
    RETURN
   IF((en)<>0,(en),0)
```


## Table: Measure_Table2

### Measures:


```dax
Innovation_% = 
    DIVIDE([Innovation],[PY Price($)],0)
```



```dax
$ cy = CALCULATE(SUM('wipes_val Wide'[$]),FILTER(continue_BItable,continue_BItable[Year]=[selected_year]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
Innovation = 
VAR val1 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),
        FILTER ( continue_BItable, continue_BItable[PY] = "CUT" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )
VAR val2 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),
        FILTER ( continue_BItable, continue_BItable[PY] = "NEW" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )
VAR val_test1 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]),
        FILTER ( continue_BItable, continue_BItable[PY] = "NEW" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )     
VAR Val3 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "CUT" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )
VAR val4 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "NEW" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )
VAR val_test2 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "NEW" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )     
VAR en = IF ( [py_year] = [selected_year] - 2, ( - val3 + val4-val_test2*2 ), ( - val1 + val2-val_test1*2) )

RETURN
   IF( (en)<>0,

   (en),0)

```



```dax
PY Price($) = CALCULATE(SUMX('wipes_val Wide',[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
```



```dax
Revenue_% = DIVIDE([Revenue Growth],[PY Price($)],0)
```



```dax
Volume_% = DIVIDE([Like for Like Volume Impact],[PY Price($)],0)
```



```dax
Distribution_% = DIVIDE([Distribution 1],[PY Price($)],0)
```



```dax
Baseline_% = DIVIDE([Baseline Velocity],[PY Price($)],0)
```



```dax
Incremental Velocity_% = DIVIDE([Incremental Velocity],[PY Price($)],0)
```



```dax
Price_% = DIVIDE([Price Impact],[PY Price($)],0)
```



```dax
Non-promo price_% = DIVIDE([NP Price],[PY Price($)],0)
```



```dax
Promo Price_% = DIVIDE([Promo Price],[PY Price($)],0)
```



```dax
Promo Depth_% = DIVIDE([Depth Calculation],[PY Price($)],0)
```



```dax
Promo Presser_% = DIVIDE([Pressure Calculation],[PY Price($)],0)
```



```dax
Mix_% = DIVIDE([Mix calculation 1],[PY Price($)],0)
```



```dax
Brand Mix_% = DIVIDE([Brand Mix Allocated 2],[PY Price($)],0)
```



```dax
Type Mix_% = DIVIDE([Type Mix Allocated 2],[PY Price($)],0)
```



```dax
Size Mix_% = DIVIDE([Size Mix Allocated 2],[PY Price($)],0)
```



```dax
Other Mix_% = DIVIDE([Other Mix],[PY Price($)],0)
```



```dax
Velocity_% = DIVIDE([Velocity],[PY Price($)],0)
```



```dax
Total $ share = CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
dollar share = 
var dollar = CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var deno = CALCULATE([Total $ share],ALL('wipes_dim Wide'[Clorox Brand Value])
)
return
DIVIDE(dollar,deno,0)

```



```dax
PSA_Total volume share_cy = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
Volume Share at Brand level = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var deno = CALCULATE([PSA_Total volume share_cy],ALL('wipes_dim Wide'[Clorox Brand Value]))

return
DIVIDE(dollar,deno,0)
```



```dax
EV_Revenue%for Rank = 
// SWITCH (
//  TRUE (),
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "DILUTABLES",
//  IF (
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "PINE SOL",
//  ABS ( [Revenue_%] * 100000000 ),
//  IF ( [Volume Share for  E.V  NRM matrix] > 0.1, [Revenue_%], -10000 )
//  ),
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "THROUGH THE WASH STAIN REMOVE",
//  IF (
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "CLOROX 2",
//  ABS ( [Revenue_%] * 100000000 ),
//  IF ( [Volume Share for  E.V  NRM matrix] > 0.1, [Revenue_%], -10000 )
//  ),
//  SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) in {"CHARCOAL","BRITA","TRASH AND FOOD STORAGE"},
//  IF (
//  (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Manufacturer Value] ) = "CLOROX COMPANY" &&SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value])<> "FOOD BAGS" ) || (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value])= "FOOD BAGS" &&SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "GLAD"),
//  ABS ( [Revenue_%] * 100000000 ),
//  IF ( [Volume Share for  E.V  NRM matrix] > 0.1, [Revenue_%], -10000 )
//  ), 
//  IF (
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "CLOROX",
//  ABS ( [Revenue_%] * 100000000 ),
//  IF ( [Volume Share for  E.V  NRM matrix] > 0.1, [Revenue_%], -10000 )
//  )
// )

SWITCH(TRUE(),
SELECTEDVALUE('wipes_dim Wide'[New EV Brand column])= "CLX",ABS ( [Revenue_%] * 100000000 ),
IF ( [Volume Share for  E.V  NRM matrix] > 0.1, [Revenue_%], -10000 ))

```



```dax
EV_Revenue%_Ranking = RANKX(ALL('wipes_dim Wide'[Clorox Brand Value]),[EV_Revenue%for Rank],,DESC,Dense)
```



```dax
NRM _PSD_Growth from py = 
var 
Total_volume_share_py =
 CALCULATE(
          SUM('wipes_val Wide'[Volume Sales]),
             FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year])
             )
Return
IF((DIVIDE(([PSA_Total volume share_cy]-Total_volume_share_py),Total_volume_share_py,0))<>0,
(DIVIDE(([PSA_Total volume share_cy]-Total_volume_share_py),Total_volume_share_py,0)),0)



```



```dax
% of Market = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var deno = CALCULATE([PSA_Total volume share_cy],ALL('wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range]))

return
DIVIDE(dollar,deno,0)
```



```dax
PSA_Volume Share CY = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var deno = CALCULATE([PSA_Total volume share_cy],ALL('wipes_dim Wide'[Clorox Brand Value]),ALL('wipes_dim Wide'[Clorox Size Range Value]),ALL('wipes_dim Wide'[Clorox Size Value], 'wipes_dim Wide'[Size Calc],'wipes_dim Wide'[Index size range]))

return
DIVIDE(dollar,deno,0)
```



```dax
Volume share for filter = 
var Numerator = [PSA_Total volume share_cy](ALLSELECTED('wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range],'wipes_dim Wide'[Clorox Size Value], 'wipes_dim Wide'[Size Calc]))
var Deno = CALCULATE([PSA_Total volume share_cy],ALL('wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Clorox Size Value], 'wipes_dim Wide'[Size Calc],'wipes_dim Wide'[Index size range])
)

return IF(SELECTEDVALUE('wipes_dim Wide'[New EV Brand column])="CLX", DIVIDE(Numerator,Deno,0)*10000, DIVIDE(Numerator,Deno,0))


```



```dax
lc Total Revenue = CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
lc Promo $/oz WAvg = 
VAR MonthlyTable = 
    ADDCOLUMNS(
        SUMMARIZE(
            'wipes_val Wide',
            'wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product Key],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Size Calc]
        ),
        "Promo$/oz", [lcPromo$/oz],
        "Promo$/unit",[lcPromo$/unit],
        "revenue", [lc Total Revenue]
    )
RETURN
    SWITCH(TRUE(),SELECTEDVALUE('OZ/unit selection'[OZ/Unit sle])="$/volume",DIVIDE((SUMX(
        MonthlyTable,
        [Promo$/oz] * [revenue])),[lc Total Revenue],0
    ),DIVIDE((SUMX(
        MonthlyTable,
        [Promo$/unit] * [revenue])),[lc Total Revenue],0))

```



```dax
lc NP $/oz WAvg = 
VAR MonthlyTable = 
    ADDCOLUMNS(
        SUMMARIZE(
            'wipes_val Wide',
            'wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product Key],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Size Calc]
        ),
        "NP$/oz", [lcNP$/oz],
        "NP$/unit",[lcNP$/unit],
        "revenue", [lc Total Revenue]
    )
RETURN
    SWITCH(TRUE(),SELECTEDVALUE('OZ/unit selection'[OZ/Unit sle])="$/volume",DIVIDE((SUMX(
        MonthlyTable,
        [NP$/oz] * [revenue])),[lc Total Revenue],0
    ),DIVIDE((SUMX(
        MonthlyTable,
        [NP$/unit] * [revenue])),[lc Total Revenue],0))

```



```dax
lc $/oz WAvg = 
VAR MonthlyTable = 
    ADDCOLUMNS(
        SUMMARIZE(
            'wipes_val Wide',
            'wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Product Key],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Size Calc]
        ),
        "$/oz", [lc$/oz],
        "$/unit",[lc$/unit],
        "revenue", [lc Total Revenue]
    )
RETURN
    SWITCH(TRUE(),SELECTEDVALUE('OZ/unit selection'[OZ/Unit sle])="$/volume",DIVIDE((SUMX(
        MonthlyTable,
        [$/oz] * [revenue])),[lc Total Revenue],0
    ),DIVIDE((SUMX(
        MonthlyTable,
        [$/unit] * [revenue])),[lc Total Revenue],0))

```



```dax
lc Price and Promo Vol Share Ranking = RANKX(ALL('wipes_dim Wide'[Clorox Brand Value]),[Volume share for filter],,DESC,Dense)
```



```dax
EV_Revenueshare_Rank = RANKX(ALL('wipes_dim Wide'[Clorox Brand Value]),[EV_Revenue%for Rank],,DESC,Dense)


   






```



```dax
EV_TopN _Ranking by Revenue% = 

// VAR SelectedTop = SELECTEDVALUE('TopN'[TopN])
// var Rank_B = [EV_Revenueshare_Rank]

// RETURN

//                 IF (
//                     Rank_B <= SelectedTop, Rank_B, BLANK()
                    
//                 )

VAR SelectedTop = SELECTEDVALUE('TopN'[TopN])
var Rank_B = [EV_$ sales_Ranking]

RETURN

                IF (
                    Rank_B <= SelectedTop, Rank_B, BLANK()
                    
                )

```



```dax
Volume share brand new 2 = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var deno = CALCULATE([PSA_Total volume share_cy],ALL('wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range]))

return
DIVIDE(dollar,deno,0)
```



```dax
Volume Share for  E.V  NRM matrix = 
// IF (
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "DILUTABLES"
//  && SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "PINE SOL",
//  [Volume Share at Brand level] * 10000,
//  IF (
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "THROUGH THE WASH STAIN REMOVE"
//  && SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "CLOROX 2",
//  [Volume Share at Brand level] * 10000,
 
//  IF (
//  (SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) in {"CHARCOAL","BRITA"}
 
//  && SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Manufacturer Value] ) = "CLOROX COMPANY" )
//  || (SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) in {"TRASH AND FOOD STORAGE"}
//  && SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "GLAD" ),
//  [Volume Share at Brand level] * 10000,
 
//  IF (
//  SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Brand Value] ) = "CLOROX",
//  [Volume Share at Brand level] * 10000,
//  [Volume Share at Brand level]
//  )
//  )
// ))
IF (
 SELECTEDVALUE ( 'wipes_dim Wide'[New EV Brand column] ) = "CLX",
 [Volume Share at Brand level] * 10000,
 [Volume Share at Brand level]
 )
```



```dax
PSA_Volume share PY = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
var deno = CALCULATE([PSA_Total volume share_py],ALL('wipes_dim Wide'[Clorox Brand Value]),ALL('wipes_dim Wide'[Clorox Size Range Value]),ALL('wipes_dim Wide'[Clorox Size Value], 'wipes_dim Wide'[Size Calc],'wipes_dim Wide'[Index size range]))

return
DIVIDE(dollar,deno,0)
```



```dax
PSA_Total volume share_py = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
```



```dax
PSA_Volume Share pt %chg = 
CONCATENATE( FORMAT ([PSA_Volume Share CY], "0.0%" )
     ,
    CONCATENATE (IF(([PSA_Volume Share CY]-[PSA_Volume share PY])<0," (-"," (+"),
        FORMAT ( ABS([PSA_Volume Share CY]-[PSA_Volume share PY]), "0.0%" ))&")"
    
)
```



```dax
lc$/oz = CALCULATE(SUM('wipes_val Wide'[$ / oz_All SKUs]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
lc$/unit = CALCULATE(SUM('wipes_val Wide'[$/unit]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
lcNP$/oz = CALCULATE(SUM('wipes_val Wide'[NP $ / oz]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
lcNP$/unit = CALCULATE(SUM('wipes_val Wide'[NP $ / unit]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
lcPromo$/oz = CALCULATE(SUM('wipes_val Wide'[Promo $ / oz]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
lcPromo$/unit = CALCULATE(SUM('wipes_val Wide'[Promo $ / unit]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
Volume share for filter clx = 
IF (
 SELECTEDVALUE ( 'wipes_dim Wide'[New EV Brand column] ) = "CLX",
 [Volume share for filter] * 10000,
 [Volume share for filter]*100
 )
```



```dax
lc Price and Promo Vol Share Ranking clx = 

RANKX(ALL('wipes_dim Wide'[Clorox Brand Value]),[Volume share for filter clx],,DESC)

```



```dax
Executive header = "NRM - Category Performance ( " & SELECTEDVALUE('wipes_val Wide'[Retailer])&" )"
```



```dax
EV $ sales for rank = 
SWITCH(TRUE(),
SELECTEDVALUE('wipes_dim Wide'[New EV Brand column])= "CLX",ABS ( [$ cy] * 100000000 ), [$ cy])
```



```dax
EV_$ sales_Ranking = RANKX(ALL('wipes_dim Wide'[Clorox Brand Value]),[EV $ sales for rank],,DESC,Dense)
```



```dax
Innovation set2 py-2 = 
 VAR Val3 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "CUT" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )
VAR val4 =
    CALCULATE (
        SUMX ( 'wipes_val Wide', [$] ),
        FILTER ( continue_BItable, continue_BItable[PY-1] = "NEW" ),
        FILTER ( continue_BItable, 'continue_BItable'[Year] = [selected_year] )
    )
VAR en = IF (SELECTEDVALUE(py_table[Period])="Same Period Year Ago", ( - val3 + val4 ),0 )

RETURN
   IF( (en)<>0,

   (en),0)
```



```dax
PY-1 Price($) = CALCULATE(SUMX('wipes_val Wide',[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]-1))
```



```dax
Innovation_%_py-1 = 
    DIVIDE([Innovation set2 py-2],[PY-1 Price($)],0)
```



```dax
Mix_% set2 = DIVIDE([Mix calculation 1 set2],[PY-1 Price($)],0)
```



```dax
Price_% set2 = DIVIDE([Price Impact set2],[PY-1 Price($)],0)
```



```dax
Volume_% set2 = DIVIDE([Like for Like Volume Impact set2],[PY-1 Price($)],0)
```


## Table: OZ/unit selection


```dax
{"$/volume", "$/unit"}
```


## Table: Measure Table 3

### Measures:


```dax
t3 Mix_% = 

CONCATENATE(CONCATENATE (IF([Mix calculation 1]<0,"-$","+$"), FORMAT ( ABS(ROUND([Mix calculation 1],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [Mix_%], "0.0%" ))
    ) 

```



```dax
t3 Price_% = 

CONCATENATE(CONCATENATE (IF([Price Impact]<0,"-$","+$"), FORMAT ( ABS(ROUND([Price Impact],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [Price_%], "0.0%" ))
    ) 


```



```dax
t3 Promo Presser_% = 

CONCATENATE(CONCATENATE (IF([Pressure Calculation]<0,"-$","+$"), FORMAT ( ABS(ROUND([Pressure Calculation],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [Promo Presser_%], "0.0%" ))
    )



```



```dax
t3 Volume_% = 

CONCATENATE(CONCATENATE (IF([Like for Like Volume Impact]<0,"-$","+$"), FORMAT ( ABS(ROUND(IFERROR([Like for Like Volume Impact],1),0)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [Volume_%], "0.0%" ))
    ) 


```



```dax
t3Baseline_% = 

CONCATENATE(CONCATENATE (IF([Baseline Velocity]<0,"-$","+$"), FORMAT ( ABS(ROUND([Baseline Velocity],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [Baseline_%], "0.0%" ))
    )



```



```dax
t3Brand Mix_% = 

CONCATENATE(CONCATENATE (IF([Brand Mix Allocated 2]<0,"-$","+$"), FORMAT ( ABS(ROUND([Brand Mix Allocated 2],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Brand Mix_%], "0.0%" ))
    )


```



```dax
t3Distribution_% = 


CONCATENATE(CONCATENATE (IF([Distribution 1]<0,"-$","+$"), FORMAT ( ABS(ROUND([Distribution 1],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Distribution_%], "0.0%" ))
    )




```



```dax
t3Incremental Velocity_% = 


CONCATENATE(CONCATENATE (IF([Incremental Velocity]<0,"-$","+$"), FORMAT ( ABS(ROUND([Incremental Velocity],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Incremental Velocity_%], "0.0%" ))
    )


```



```dax
t3Innovation_% = 


CONCATENATE(CONCATENATE (IF([Innovation]<0,"-$","+$"), FORMAT ( ABS(ROUND([Innovation],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Innovation_%], "0.0%" ))
    ) 


```



```dax
t3Non-promo price_% = 


CONCATENATE(CONCATENATE (IF([NP Price]<0,"-$","+$"), FORMAT ( ABS(ROUND([NP Price],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Non-promo price_%], "0.0%" ))
    )

```



```dax
t3Other Mix_% = 


CONCATENATE(CONCATENATE (IF([Other Mix]<0,"-$","+$"), FORMAT ( ABS(ROUND([Other Mix],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Other Mix_%], "0.0%" ))
    )


```



```dax
t3Promo Depth_% = 

CONCATENATE(CONCATENATE (IF([Depth Calculation]<0,"-$","+$"), FORMAT ( ABS(ROUND([Depth Calculation],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Promo Depth_%], "0.0%" ))
    )

```



```dax
t3Promo Price_% = 


CONCATENATE(CONCATENATE (IF([Promo Price]<0,"-$","+$"), FORMAT ( ABS(ROUND([Promo Price],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Promo Price_%], "0.0%" ))
    )
```



```dax
t3Revenue_% = 



CONCATENATE(CONCATENATE (IF([Revenue Growth]<0,"-$","+$"), FORMAT ( ABS(ROUND([Revenue Growth],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [Revenue_%], "0.0%" ))
    ) 

```



```dax
t3Size Mix_% = 


CONCATENATE(CONCATENATE (IF([Size Mix Allocated 2]<0,"-$","+$"), FORMAT ( ABS(ROUND([Size Mix Allocated 2],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Size Mix_%], "0.0%" ))
    )

```



```dax
t3Type Mix_% = 

CONCATENATE(CONCATENATE (IF([Type Mix Allocated 2]<0,"-$","+$"), FORMAT ( ABS(ROUND([Type Mix Allocated 2],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Type Mix_%], "0.0%" ))
    )


```



```dax
t3Velocity_% = 

CONCATENATE(CONCATENATE (IF([Velocity]<0,"-$","+$"), FORMAT ( ABS(ROUND([Velocity],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ([Velocity_%], "0.0%" ))
    )
```



```dax
EV NRM Sortmatrix = CONCATENATE(SELECTEDVALUE('wipes_dim Wide'[Clorox Sub Category Value]),[EV_TopN _Ranking by Revenue%])
```



```dax
Swot_X Axis Lable = "Impact of driver("&SELECTEDVALUE('Revenue Drivers'[Drivers])&") for " & IF(SELECTEDVALUE('wipes_dim Wide'[BU])="BRITA","BRITA",IF(SELECTEDVALUE('wipes_dim Wide'[BU])="TRASH AND FOOD STORAGE","GLAD",IF(SELECTEDVALUE('wipes_dim Wide'[BU])="CHARCOAL","KINGSFORD",
IF (
                        SELECTEDVALUE ( 'wipes_dim Wide'[BU] )
                            IN {
                            "FACIAL CLEANSERS",
                            "FACIAL MASKS",
                            "FACIAL TONERS",
                            "ACNE CARE",
                            "FACIAL MOISTURIZERS AND TREATMENTS",
                            "FACIAL TOWELETTES",
                            "LIP CARE",
                            "COLD SORE",
                            "LIP COMBO",
                            "LIP GLOSS",
                            "LIP LINER",
                            "LIPSTICK",
                            "TINTED LIP BALM",
                            "LIQUID LIPSTICK/STAIN",
                            "COSMETIC LIP TREATMENT",
                            "TINTED LIP OIL"
                        },
                        "BURTS BEES",
                    




IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",IF (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "BARBECUE SAUCE","K C MASTERPIECE",IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "FOOD",
                    "HIDDEN VALLEY",SELECTEDVALUE('wipes_dim Wide'[New Clorox Brand Value]))))))








))
```



```dax
Swot_Y Axis Lable = "Impact of driver("&SELECTEDVALUE('Revenue Drivers'[Drivers])&") for "&SELECTEDVALUE(swot_data_nr[Clorox Brand Value])
```



```dax
Driver_Swot$ with units = FORMAT ( ROUND(CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year])),0), "#,##0,,M" )
```



```dax
Axis Lable for Driver Tree = "Driver Tree For " &SELECTEDVALUE('wipes_dim Wide'[Clorox Brand Value])
```



```dax
Swot_Threat = 
SELECTEDVALUE ( swot_data_nr[Clorox Brand Value] ) & " Leads "
    & IF (
        SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "BRITA",
        "BRITA",
        IF (
                        SELECTEDVALUE ( 'wipes_dim Wide'[BU] )
                            IN {
                            "FACIAL CLEANSERS",
                            "FACIAL MASKS",
                            "FACIAL TONERS",
                            "ACNE CARE",
                            "FACIAL MOISTURIZERS AND TREATMENTS",
                            "FACIAL TOWELETTES",
                            "LIP CARE",
                            "COLD SORE",
                            "LIP COMBO",
                            "LIP GLOSS",
                            "LIP LINER",
                            "LIPSTICK",
                            "TINTED LIP BALM",
                            "LIQUID LIPSTICK/STAIN",
                            "COSMETIC LIP TREATMENT",
                            "TINTED LIP OIL"
                        },
                        "BURTS BEES",
                    
        IF (
            SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "TRASH AND FOOD STORAGE",
            "GLAD",
            IF (
                SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CHARCOAL",
                "KINGSFORD",IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",
                    IF (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "BARBECUE SAUCE","K C MASTERPIECE",IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "FOOD","HIDDEN VALLEY",
                IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",
                    SELECTEDVALUE ( 'wipes_dim Wide'[New Clorox Brand Value] )
                )
            )
        )
    )) 
)))& " Lags"
```



```dax
Swot_Strength = 
"Both " & SELECTEDVALUE ( swot_data_nr[Clorox Brand Value] ) & " and "
    & IF (
        SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "BRITA",
        "BRITA",
        IF (
                        SELECTEDVALUE ( 'wipes_dim Wide'[BU] )
                            IN {
                            "FACIAL CLEANSERS",
                            "FACIAL MASKS",
                            "FACIAL TONERS",
                            "ACNE CARE",
                            "FACIAL MOISTURIZERS AND TREATMENTS",
                            "FACIAL TOWELETTES",
                            "LIP CARE",
                            "COLD SORE",
                            "LIP COMBO",
                            "LIP GLOSS",
                            "LIP LINER",
                            "LIPSTICK",
                            "TINTED LIP BALM",
                            "LIQUID LIPSTICK/STAIN",
                            "COSMETIC LIP TREATMENT",
                            "TINTED LIP OIL"
                        },
                        "BURTS BEES",
                    
        IF (
            SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "TRASH AND FOOD STORAGE",
            "GLAD",
            IF (
                SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CHARCOAL",
                "KINGSFORD",
                IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",IF (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "BARBECUE SAUCE","K C MASTERPIECE",IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "FOOD","HIDDEN VALLEY",
                IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",
                    SELECTEDVALUE ( 'wipes_dim Wide'[New Clorox Brand Value] )
                )
            )
        ))
    )
))) & " Lead"
```



```dax
Swot_Weakness = 
"Both " & SELECTEDVALUE ( swot_data_nr[Clorox Brand Value] ) & " and "
    & IF (
        SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "BRITA",
        "BRITA",
        IF (
                        SELECTEDVALUE ( 'wipes_dim Wide'[BU] )
                            IN {
                            "FACIAL CLEANSERS",
                            "FACIAL MASKS",
                            "FACIAL TONERS",
                            "ACNE CARE",
                            "FACIAL MOISTURIZERS AND TREATMENTS",
                            "FACIAL TOWELETTES",
                            "LIP CARE",
                            "COLD SORE",
                            "LIP COMBO",
                            "LIP GLOSS",
                            "LIP LINER",
                            "LIPSTICK",
                            "TINTED LIP BALM",
                            "LIQUID LIPSTICK/STAIN",
                            "COSMETIC LIP TREATMENT",
                            "TINTED LIP OIL"
                        },
                        "BURTS BEES",
                    
        IF (
            SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "TRASH AND FOOD STORAGE",
            "GLAD",
            IF (
                SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CHARCOAL",
                "KINGSFORD",
                IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",IF (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "BARBECUE SAUCE","K C MASTERPIECE",IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "FOOD","HIDDEN VALLEY",
                IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",
                    SELECTEDVALUE ( 'wipes_dim Wide'[New Clorox Brand Value] )
                )
            )
        )
    )) 
)))& " Lag"
```



```dax
Swot_Opportunity = 
IF (
    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "BRITA",
    "BRITA",
IF (
                        SELECTEDVALUE ( 'wipes_dim Wide'[BU] )
                            IN {
                            "FACIAL CLEANSERS",
                            "FACIAL MASKS",
                            "FACIAL TONERS",
                            "ACNE CARE",
                            "FACIAL MOISTURIZERS AND TREATMENTS",
                            "FACIAL TOWELETTES",
                            "LIP CARE",
                            "COLD SORE",
                            "LIP COMBO",
                            "LIP GLOSS",
                            "LIP LINER",
                            "LIPSTICK",
                            "TINTED LIP BALM",
                            "LIQUID LIPSTICK/STAIN",
                            "COSMETIC LIP TREATMENT",
                            "TINTED LIP OIL"
                        },
                        "BURTS BEES",
                    

    IF (
        SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "TRASH AND FOOD STORAGE",
        "GLAD",
        IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER","FRESH STEP",
                    IF (SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "BARBECUE SAUCE","K C MASTERPIECE",
                    
                    
                    IF (SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "FOOD","HIDDEN VALLEY",
        IF (
            SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CHARCOAL",
            "KINGSFORD",
            IF(
                SELECTEDVALUE('wipes_dim Wide'[BU])="CAT LITTER",
                "FRESH STEP",

                SELECTEDVALUE ( 'wipes_dim Wide'[New Clorox Brand Value] )
        )
    )
))) )
))& " Leads "
    & SELECTEDVALUE ( swot_data_nr[Clorox Brand Value] ) & " Lags"

```



```dax
DT Price for Rank = 
IF(SELECTEDVALUE('wipes_val Wide'[Retailer])="Total US - Multi Outlet"||SELECTEDVALUE('wipes_val Wide'[Retailer])="Total US - Food"||SELECTEDVALUE('wipes_val Wide'[Retailer])="Total US - Drug"||SELECTEDVALUE('wipes_val Wide'[Retailer])="Total Mass Aggregate",ABS([Price Impact])*(-10000000),[Price Impact])

```



```dax
Page Header Lable2 = "For FY " &INT(MID(SELECTEDVALUE('wipes_val Wide'[Refresh Period 2]),3,2)) &" & Comparison Period : FY "& (INT(MID(SELECTEDVALUE('wipes_val Wide'[Refresh Period 2]),3,2))- SELECTEDVALUE(py_table[Value]))
```



```dax
Page Header Lable1 = "POS data: "& SELECTEDVALUE('wipes_val Wide'[Refreshed Period])   
```



```dax
dd Price impact = [Price Impact]
```



```dax
dd Innovation = [Innovation]
```



```dax
dd Volume = [Like for Like Volume Impact]
```



```dax
dd Mix = [DT Mix calculation 1]
```



```dax
Cat_Swot$ size = (CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year])))
```



```dax
t3 Mix_% studio lead view = 

CONCATENATE(CONCATENATE (IF([DT Mix calculation 1]<0,"-$","+$"), FORMAT ( ABS(ROUND([DT Mix calculation 1],1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT ( [DT Mix_%], "0.0%" ))
    )
```



```dax
t3 Type&Others_% = 

CONCATENATE(CONCATENATE (IF(([Mix calculation 1] - [Brand Mix Allocated 2]- [Size Mix Allocated 2]) <0,"-$","+$"), FORMAT ( ABS(ROUND(([Mix calculation 1]- [Brand Mix Allocated 2]- [Size Mix Allocated 2]),1)), "#,##0,,.0M" )
     ),
    CONCATENATE (UNICHAR(10),
        FORMAT (( [Mix_%]-[Brand Mix_%]-[Size Mix_%])
, "0.0%" ))
    ) 

```



```dax
Axis Lable for PP = "Price Piano For " &SELECTEDVALUE('wipes_dim Wide'[Clorox Brand Value])
```



```dax
Axis Lable for Add PP = "Price Piano For " &SELECTEDVALUE('wipes_val Wide'[Retailer])
```



```dax
Cat_Swot_Selected Comp Driver = 

IF(HASONEVALUE(swot_data_nr[Clorox Brand Value]),
CALCULATE([Cat_Swot_Selected Driver], FILTER(ALL('wipes_dim Wide'[New Clorox Brand Value]), 'wipes_dim Wide'[New Clorox Brand Value]=SELECTEDVALUE(swot_data_nr[Clorox Brand Value]))))
        







```



```dax
Cat_Swot_Selected Driver = 
IF(HASONEVALUE('Revenue Drivers'[Drivers]),
    SWITCH(
        VALUES('Revenue Drivers'[Drivers]),
        "New Items", [Innovation_%],
        "Assortment Changes", [Mix_%],
        "Price Movements", [Price_%],
        "Organic Sales Lift", [Volume_%]
    ),
    0
)
```



```dax
Driver_Swot_Selected Comp Driver = 

IF(HASONEVALUE(swot_data_nr[Clorox Brand Value]),
CALCULATE([Driver_Swot_Selected Driver], FILTER(ALL('wipes_dim Wide'[New Clorox Brand Value]), 'wipes_dim Wide'[New Clorox Brand Value]=SELECTEDVALUE(swot_data_nr[Clorox Brand Value]))))
```



```dax
Driver_Swot_Selected Driver = 
IF(HASONEVALUE('Revenue Drivers'[Drivers]),
    SWITCH(
        VALUES('Revenue Drivers'[Drivers]),
        "New Items", [Innovation_%],
        "Assortment Changes", [DT Mix_%],
        "Price Movements", [Price_%],
        "Organic Sales Lift", [Volume_%]
    ),
    0
)
```



```dax
Driver_Swot_Selected Driver_Drill = 
IF(HASONEVALUE('DriversL3'[Value]),
    SWITCH(
        VALUES('DriversL3'[Value]),
        "Type Mix",[Type Mix_%],
"Size Mix",[Size Mix_%],
"Promo Depth",[Promo Depth_%],
"Promo Pressure",[Promo Presser_%],
"NP Price",[Non-promo price_%],
"Brand Mix",[Brand Mix_%],
"Other Mix",[Other Mix_%],
"Distribution",[Distribution_%],
"Baseline Velocity",[Baseline_%],
"Incremental Velocity",[Incremental Velocity_%],
"New Items",[Innovation_%]

    ),
    0
)
```



```dax
Driver_Swot_Selected Comp Driver Drill = 

IF(HASONEVALUE(swot_data_nr[Clorox Brand Value]),
CALCULATE([Driver_Swot_Selected Driver_Drill], FILTER(ALL('wipes_dim Wide'[New Clorox Brand Value]), 'wipes_dim Wide'[New Clorox Brand Value]=SELECTEDVALUE(swot_data_nr[Clorox Brand Value]))))
```



```dax
DR_Swot_X Axis Lable = 
"Revenue Opportunity for "
    & SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) & " ("
    & IF (
        SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "BRITA",
        "BRITA",
        IF (
            SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "TRASH AND FOOD STORAGE",
            "GLAD",
            IF (
                SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CHARCOAL",
                "KINGSFORD",
                IF (
                    SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "CAT LITTER",
                    "FRESH STEP",
                    IF (
                        SELECTEDVALUE ( 'wipes_dim Wide'[BU] )
                            IN {
                            "FACIAL CLEANSERS",
                            "FACIAL MASKS",
                            "FACIAL TONERS",
                            "ACNE CARE",
                            "FACIAL MOISTURIZERS AND TREATMENTS",
                            "FACIAL TOWELETTES",
                            "LIP CARE",
                            "COLD SORE",
                            "LIP COMBO",
                            "LIP GLOSS",
                            "LIP LINER",
                            "LIPSTICK",
                            "TINTED LIP BALM",
                            "LIQUID LIPSTICK/STAIN",
                            "COSMETIC LIP TREATMENT",
                            "TINTED LIP OIL"
                        },
                        "BURTS BEES",
                        IF (
                            SELECTEDVALUE ( 'wipes_dim Wide'[Clorox Sub Category Value] ) = "BARBECUE SAUCE",
                            "K C MASTERPIECE",
                            IF (
                                SELECTEDVALUE ( 'wipes_dim Wide'[BU] ) = "FOOD",
                                "HIDDEN VALLEY",
                                SELECTEDVALUE ( 'wipes_dim Wide'[New Clorox Brand Value] )
                            )
                        )
                    )
                )
            )
        )
    ) & ")"

```



```dax
DR_Swot_Y Axis Lable = "Revenue Opportunity for "&SELECTEDVALUE(swot_data_nr[Clorox Sub Category Value])&" (" &SELECTEDVALUE('swot_data_nr'[Clorox Brand Value])&")"
```



```dax
Par_ Axis Lable = "Report for " &SELECTEDVALUE('wipes_val Wide'[Retailer])
```



```dax
Par_$_all_prod = 

CALCULATE([Par_$_selected_year],ALL('wipes_dim Wide'[Product]))

```



```dax
Par_$_selected_year = CALCULATE(SUM('wipes_val Wide'[$]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
```



```dax
Par_$_share_prod = IF(DIVIDE([Par_$_selected_year],[Par_$_all_prod],0)<> 0,DIVIDE([Par_$_selected_year],[Par_$_all_prod],0),0)
```



```dax
Par_cumul_% = DIVIDE([Par_cumulative_$_selected_year],[Par_$_all_prod],0)
```



```dax
Par_cumulative_$_selected_year = 
VAR rev = [Par_$_selected_year]
RETURN 
SUMX(FILTER(SUMMARIZE(ALLSELECTED('wipes_val Wide'),'wipes_dim Wide'[Product],"Revenue",[Par_$_selected_year]),[Revenue]>=rev),[Revenue])

```



```dax
Axis Lable for Price & promo = "Price and Promo Analysis For " &SELECTEDVALUE('wipes_val Wide'[Retailer])
```



```dax
Axis Lable for PP1 = "Price Piano For " &SELECTEDVALUE('wipes_val Wide'[Retailer])
```



```dax
Par_$_Rank = RANKX(ALL('wipes_dim Wide'[Product]),[Par_$_selected_year],,DESC)
```



```dax
$sh_t3$_% = 


CONCATENATE( FORMAT ( [$ share], "0.0%" ),
     
    CONCATENATE (UNICHAR(10),
        FORMAT ( [$ share pt chg]*100, "0.0 pts" ))
    ) 

```


## Table: TopN


```dax
GENERATESERIES(1, 5, 1)
```


### Measures:


```dax
TopN Value = SELECTEDVALUE('TopN'[TopN])
```


## Table: Top Brands


```dax
GENERATESERIES(0, 20, 1)
```


### Measures:


```dax
Top Brands Value = SELECTEDVALUE('Top Brands'[Top Brands])
```


## Table: Brand Ranking


```dax

UNION (
     ALLNOBLANKROW ( 'wipes_dim Wide'[Clorox Brand Value] ),
         { "Others" }
)
```


### Measures:


```dax
Vol Share for NRM PSD = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[selected_year]))
var deno = CALCULATE([PSA_Total volume share_cy],ALL('Brand Ranking'[Clorox Brand Value]),ALL('wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range]))

return
DIVIDE(dollar,deno,0)
```



```dax
Rank 1 = RANKX(ALL('Brand Ranking'[Clorox Brand Value]),[Vol Share for NRM PSD],,DESC)
```



```dax
Measure 1 = IF(SELECTEDVALUE('Brand Ranking'[Clorox Brand Value])="Others",5,IF([Rank 1]>4,6 ,[Rank 1]))
```



```dax
Measure 2 = IF([Measure 1]=6,[Vol Share for NRM PSD])
```



```dax
Measure 3 = SUMX(VALUES('Brand Ranking'[Clorox Brand Value]),[Measure 2])
```



```dax
Sales Amt  test = 
VAR SalesOfAll =
    CALCULATE (
                [Vol Share for NRM PSD],
        REMOVEFILTERS ( 'Brand Ranking')
    )
RETURN
    IF (
        NOT ISINSCOPE ( 'Brand Ranking'[Clorox Brand Value]),
 
        -- Calculation for a group of products 
        SalesOfAll,
 
        -- Calculation for one product name
        VAR ProductsToRank = [TopN Value]
        VAR SalesOfCurrentProduct = [Vol Share for NRM PSD]
        VAR IsOtherSelected =
            SELECTEDVALUE ( 'Brand Ranking'[Clorox Brand Value] ) = "Others"
        RETURN
            IF (
                NOT IsOtherSelected,
 
                -- Calculation for a regular product
                SalesOfCurrentProduct,
 
                -- Calculation for Others
                VAR VisibleProducts =
                    CALCULATETABLE (
                        SUMMARIZE('wipes_dim Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range],"volumeshare",[Vol Share for NRM PSD])
                        
                    )
                VAR ProductsWithSales =
                    ADDCOLUMNS (
                        VisibleProducts,
                        "@volumeshare", [Vol Share for NRM PSD]
                    )
                VAR SalesOfTopProducts =
                    SUMX (
                        TOPN (
                            ProductsToRank ,
                            VisibleProducts,
                            [volumeshare]
                        ),
                        [volumeshare]
                    )
                VAR SalesOthers =
                    CALCULATE([Measure 3],REMOVEFILTERS('Brand Ranking'))
                RETURN
                    SalesOthers
            )
    )
```



```dax
Vol Share for NRM PSD test = 
var dollar = CALCULATE(SUM('wipes_val Wide'[Volume Sales]),FILTER('wipes_val Wide','wipes_val Wide'[Year]=[py_year]))
var deno = CALCULATE([PSA_Total volume share_py],ALL('Brand Ranking'[Clorox Brand Value]),ALL('wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range]))
 
return
DIVIDE(dollar,deno,0)
```



```dax
Measure 2 test = IF([Measure 1]=6,[Vol Share for NRM PSD test])
```



```dax
Measure 3 test = SUMX(VALUES('Brand Ranking'[Clorox Brand Value]),[Measure 2 test])
```



```dax
Sales Amt test 1 = 
VAR SalesOfAll =
 CALCULATE (
 [Vol Share for NRM PSD test],
 REMOVEFILTERS ( 'Brand Ranking')
 )
RETURN
 IF (
 NOT ISINSCOPE ( 'Brand Ranking'[Clorox Brand Value]),
 
 -- Calculation for a group of products 
 SalesOfAll,
 
 -- Calculation for one product name
 VAR ProductsToRank = [TopN Value]
 VAR SalesOfCurrentProduct = [Vol Share for NRM PSD test]
 VAR IsOtherSelected =
 SELECTEDVALUE ( 'Brand Ranking'[Clorox Brand Value] ) = "Others"
 RETURN
 IF (
 NOT IsOtherSelected,
 
 -- Calculation for a regular product
 SalesOfCurrentProduct,
 
 -- Calculation for Others
 VAR VisibleProducts =
 CALCULATETABLE (
 SUMMARIZE('wipes_dim Wide','wipes_dim Wide'[Clorox Brand Value],'wipes_dim Wide'[Clorox Size Range Value],'wipes_dim Wide'[Index size range],"volumeshare",[Vol Share for NRM PSD test])
 
 )
 VAR ProductsWithSales =
 ADDCOLUMNS (
 VisibleProducts,
 "@volumeshare", [Vol Share for NRM PSD test]
 )
 VAR SalesOfTopProducts =
 SUMX (
 TOPN (
 ProductsToRank ,
 VisibleProducts,
 [volumeshare]
 ),
 [volumeshare]
 )
 VAR SalesOthers =
 CALCULATE([Measure 3 test],REMOVEFILTERS('Brand Ranking'))
 RETURN
 SalesOthers
 )
 )
```



```dax
NRM % Growth = [Sales Amt  test]-[Sales Amt test 1]
```



```dax
% mkt share with growth NRM PSD = CONCATENATE( FORMAT ([Sales Amt  test], "0.0%" )
     ,
    CONCATENATE (IF(([NRM % Growth])<0," (-"," (+"),
        FORMAT ( ABS([NRM % Growth]), "0.0%" ))&")"
    
)
```


## Table: DriversL3


```dax
{"Type Mix",
"Size Mix",
"Promo Depth",
"Promo Pressure",
"NP Price",
"Brand Mix",
"Other Mix",
"Distribution",
"Baseline Velocity",
"Incremental Velocity",
"New Items"}
```


## Table: date_table_2


```dax
SUMMARIZE('wipes_val Wide','wipes_val Wide'[Year],'wipes_val Wide'[Adhoc RP])
```

