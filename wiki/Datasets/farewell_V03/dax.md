



# DAX

|Dataset|[farewell_V03](./../farewell_V03.md)|
| :--- | :--- |
|Workspace|[Farewell](../../Workspaces/Farewell.md)|

## Table: _measures

### Measures:


```dax
number of responses = 
 COUNTROWS(Source)
```



```dax
MinNumberThreshold = 3
```



```dax
IsVisibleDueToThreshold = 
if(calculate(COUNTROWS(Source), ALLSELECTED(Source)) >= [MinNumberThreshold],  COUNTROWS(Source), BLANK())
```



```dax
max 100 = 100 
```



```dax
min -100 = -100
```



```dax
mid 0 = 0
```



```dax
IsVisibleNextCareerMove = 
if(calculate(COUNTROWS(Source), REMOVEFILTERS('Next career moves'[What does your next career move look like?]), ALLSELECTED(Source)) >= [MinNumberThreshold],  COUNTROWS(Source), BLANK())
```



```dax
avg My projects allowed me to further grow my skills / knowledge = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[My projects allowed me to further grow my skills / knowledge]), blank())
```



```dax
avg My projects met my field of interest or expertise = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[My projects met my field of interest or expertise]), blank())
```



```dax
avg The set-up of my projects, e.g. internationality, frequency or variety, met my expectations = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[The set-up of my projects, e.g. internationality, frequency or variety, met my expectations]), blank())
```



```dax
avg I received guidance and feedback from my project responsible superior = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I received guidance and feedback from my project responsible superior]), blank())
```



```dax
avg I received appreciation by my project responsible superior = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I received appreciation by my project responsible superior]), blank())
```



```dax
avg I received guidance and feedback by my mentor to drive my career development = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I received guidance and feedback by my mentor to drive my career development]), blank())
```



```dax
avg I received guidance and feedback by my mentor to drive my personal development = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I received guidance and feedback by my mentor to drive my personal development]), blank())
```



```dax
avg My working hours allowed me to balance work and personal life = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[My working hours allowed me to balance work and personal life]), blank())
```



```dax
avg Flexible work arrangements were supported = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[Flexible work arrangements were supported]), blank())
```



```dax
avg The amount of travelling was in line with my expectations = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[The amount of travelling was in line with my expectations]), blank())
```



```dax
avg The overall workload was manageable = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[The overall workload was manageable]), blank())
```



```dax
avg I was satisfied with the pace of my career development = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I was satisfied with the pace of my career development]), blank())
```



```dax
avg I got the opportunity to broaden my leadership experience = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I got the opportunity to broaden my leadership experience]), blank())
```



```dax
avg Pursuing the career path to Principal/Partner would have been attractive to me = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[Pursuing the career path to Principal/Partner would have been attractive to me]), blank())
```



```dax
avg I would have had the flexibility to change platform/office = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I would have had the flexibility to change platform/office]), blank())
```



```dax
avg I was satisfied with my overall compensation package (base & bonus) = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I was satisfied with my overall compensation package (base & bonus)]), blank())
```



```dax
avg The ratio of compensation and working hours was adequate = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[The ratio of compensation and working hours was adequate]), blank())
```



```dax
avg I was satisfied with the benefits offered = 
if([IsVisibleDueToThreshold] > 0, AVERAGE(Source[I was satisfied with the benefits offered]), blank())
```


## Table: Recommend as employer

### Measures:


```dax
Promoters (employer) = Calculate(COUNTROWS('Recommend as employer'), 'Recommend as employer'[Type] = "Promoters")
```



```dax
Detractors (employer) = Calculate(COUNTROWS('Recommend as employer'), 'Recommend as employer'[Type] = "Detractors")
```



```dax
Passives (employer) = Calculate(COUNTROWS('Recommend as employer'), 'Recommend as employer'[Type] = "Passives")
```



```dax
NPS (employer) = 

if([IsVisibleDueToThreshold] >0
,
var _total = [Promoters (employer)] + [Passives (employer)] + [Detractors (employer)]
var _pro = [Promoters (employer)]
var _det = [Detractors (employer)]

return  (divide(_pro, _total , blank()) - divide(_det, _total , blank()) ) * 100
)
```


## Table: Recommend as client

### Measures:


```dax
Passives (client) = Calculate(COUNTROWS('Recommend as client'), 'Recommend as client'[Type] = "Passives")
```



```dax
Detractors (client) = Calculate(COUNTROWS('Recommend as client'), 'Recommend as client'[Type] = "Detractors")
```



```dax
Promoters (client) = Calculate(COUNTROWS('Recommend as client'), 'Recommend as client'[Type] = "Promoters")
```



```dax
NPS (client) = 

if([IsVisibleDueToThreshold] >0
,
var _total = [Promoters (client)] + [Passives (client)] + [Detractors (client)]
var _pro = [Promoters (client)]
var _det = [Detractors (client)]

return (divide(_pro, _total , blank()) - divide(_det, _total , blank())) * 100 
)
```

