



# DAX

|Dataset|[idea management](./../idea-management.md)|
| :--- | :--- |
|Workspace|[Test FZr - APP](../../Workspaces/Test-FZr---APP.md)|

## Table: New Requests

### Measures:


```dax
Selected Description = if(count('New Requests'[Id])= 1, min('New Requests'[Description]), blank())
```



```dax
Selected Solution = if(count('New Requests'[Id])= 1, min('New Requests'[Solution]), "")
```



```dax
Selected Requestor = if(count('New Requests'[Id])= 1, min('New Requests'[Requestor.EMail]), "")
```



```dax
Selected Date = if(count('New Requests'[Id])= 1, min('New Requests'[Date]), "")
```



```dax
Selected Licensing = if(count('New Requests'[Id])= 1, min('New Requests'[Licensing Cost]), blank())
```



```dax
Selected Link = if(count('New Requests'[Id])= 1, min('New Requests'[Link]), "")
```



```dax
Selected Budget Owner = if(count('New Requests'[Id])= 1, min('New Requests'[Budget Owner]), "")
```



```dax
StatusColor = 
if(count('New Requests'[Id])= 1,
switch(min('New Requests'[Status])
    , "Completed", "#AFE8AA" 
    , "Not started", "#CCCCCC" 
    , "In progress", "#FFE99D" 
    , "Stopped", "#FCA080" 
    , "Declined", "#FBCFD3" 
    )
)
```



```dax
ClassificationColor = 
if(count('New Requests'[Id])= 1,
switch(min('New Requests'[Classification])
    , "Digital Workplace", "#AFE8AA" 
    , "Launched supported", "#BFEDBB" 
    , "Launched unsupported", "#DFF6DD" 
    , "Denied", "#FBCFD3" 
    , "Unclassified", "#CCCCCC" 
    )
)
```



```dax
Selected Type = if(count('New Requests'[Id])= 1, min('New Requests'[Type]), "")
```



```dax
Selected Scope = if(count('New Requests'[Id])= 1, min('New Requests'[Scope]), "")
```



```dax
Selected Status = if(count('New Requests'[Id])= 1, min('New Requests'[Status]), "")
```



```dax
Selected Classification = if(count('New Requests'[Id])= 1, min('New Requests'[Classification]), "")
```



```dax
Drill Deatil = if( COUNTROWS('New Requests') = 1, "Detail", blank()) 
```



```dax
StatusColor (all) = 
switch(min('New Requests'[Status])
    , "Completed", "#AFE8AA" 
    , "Not started", "#CCCCCC" 
    , "In progress", "#FFE99D" 
    , "Stopped", "#FCA080" 
    , "Declined", "#FBCFD3" 
    )

```



```dax
ClassificationColor (all) = 
if(min('New Requests'[Classification]) = blank(), "#999999",
switch(min('New Requests'[Classification])
    , "Digital Workplace", "#AFE8AA" 
    , "Launched supported", "#BFEDBB" 
    , "Launched unsupported", "#DFF6DD" 
    , "Denied", "#FBCFD3" 
    , "Unclassified", "#CCCCCC"
    )
)
```


## Table: Suggestions

### Measures:


```dax
Selected Suggestion Description = if(count('Suggestions'[Id])= 1, min('Suggestions'[short_description]), blank())
```



```dax
SuggestionColor = 
switch(min('Suggestions'[Status])
    , "Will be evaluated", "#AFE8AA" 
    , "Suggested", "#FFE99D" 
    , "Will not be evaluated", "#FCA080" 
    )
```

