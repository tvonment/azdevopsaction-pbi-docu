



# M Code

|Dataset|[Client Satisfaction Report](./../Client-Satisfaction-Report.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: msfp_surveyresponses


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_surveyresponses_table = Source{[Name="msfp_surveyresponses",Signature="table"]}[Data]
in
    msfp_surveyresponses_table
```


## Table: msfp_questionresponses


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questionresponses",Signature="table"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(msfp_questionresponses_table, "Not at all satisfied (1/5)","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Dissatisfied (2/5)","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Neutral (3/5)","3 - Neutral",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Satisfied (4/5)","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Completely satisfied (5/5)","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","Very dissatisfied","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","Rather dissatisfied","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","Neutral","3 - Neutral",Replacer.ReplaceValue,{"msfp_response"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value7","Fairly satisfied","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value9" = Table.ReplaceValue(#"Replaced Value8","Very satisfied","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Added Custom" = Table.AddColumn(#"Replaced Value9", "msfp_response_numeric", each try Number.From(Text.BeforeDelimiter([msfp_response], " ")) otherwise null)
in
    #"Added Custom"
```


## Table: msfp_surveyinvites


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_surveyinvites",Signature="table"]}[Data]
in
    msfp_questionresponses_table
```


## Table: msfp_surveies


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_surveies_table = Source{[Name="msfp_surveies",Signature="table"]}[Data]
in
    msfp_surveies_table
```


## Table: msfp_questions


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questions",Signature="table"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(msfp_questionresponses_table,"Why did you initially decide to conduct this project with Roland Berger?","Approach & Presentation",Replacer.ReplaceValue,{"msfp_name"})
in
    #"Replaced Value"
```


## Table: msfp_questionresponses_individual


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questionresponses",Signature="table"]}[Data],
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(msfp_questionresponses_table, {{"msfp_response", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "msfp_response"),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"msfp_response", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type", "Not at all satisfied (1/5)","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Dissatisfied (2/5)","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Neutral (3/5)","3 - Neutral",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Satisfied (4/5)","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Completely satisfied (5/5)","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","Very dissatisfied","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","Rather dissatisfied","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","Neutral","3 - Neutral",Replacer.ReplaceValue,{"msfp_response"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value7","Fairly satisfied","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value9" = Table.ReplaceValue(#"Replaced Value8","Very satisfied","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"})
in
    #"Replaced Value9"
```


## Table: nxtgn_projects


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_projects_table = Source{[Name="nxtgn_projects",Signature="table"]}[Data],
    #"Added Custom" = Table.AddColumn(nxtgn_projects_table, "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Removed Other Columns" = Table.SelectColumns(#"Added Custom1",{"nxtgn_projectid", "_nxtgn_deliverymanagerid_value", "nxtgn_accountname", "nxtgn_project_planned_enddate", "nxtgn_budget_base"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Other Columns",{{"nxtgn_project_planned_enddate", type date}})
in
    #"Changed Type"
```


## Table: systemusers


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers_table,{"_nxtgn_platformid_value", "_nxtgn_lookupcountryid_value", "fullname", "systemuserid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupplatforms


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupplatforms_table = Source{[Name="nxtgn_lookupplatforms",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupplatforms_table, each ([statuscode] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_lookupplatformid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountries


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountries_table = Source{[Name="nxtgn_lookupcountries",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountries_table, each ([nxtgn_rblegalunit] = true)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupcountryid", "nxtgn_name"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountryaliases


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryaliases_table = Source{[Name="nxtgn_lookupcountryaliases",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupcountryaliases_table,{"_nxtgn_countryid_value", "nxtgn_lookupcountryaliasid", "nxtgn_name"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([nxtgn_name] = "Americas (RB)" or [nxtgn_name] = "Asia (RB)" or [nxtgn_name] = "DACH" or [nxtgn_name] = "EMEA (RB)" or [nxtgn_name] = "Middle East" or [nxtgn_name] = "Southeast Asia")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows"," (RB)","",Replacer.ReplaceText,{"nxtgn_name"})
in
    #"Replaced Value"
```


## Table: nxtgn_customersurveytriggers


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_customersurveytriggers_table = Source{[Name="nxtgn_customersurveytriggers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_customersurveytriggers_table,{"nxtgn_surveystatus", "_nxtgn_accountid_value", "nxtgn_sendorreminder", "nxtgn_reasonforcancelation", "nxtgn_name", "nxtgn_datesent", "_nxtgn_surveyprojectid_value", "nxtgn_postponedtill", "_nxtgn_surveyinviteid_value", "statuscode", "nxtgn_donotsendsurvey", "createdon", "nxtgn_customersurveytriggerid", "_nxtgn_reminderemailid_value", "nxtgn_surveyinvitationurl", "_nxtgn_emailid_value", "_nxtgn_projectid_value", "nxtgn_reasonnocustomersurvey", "statecode", "_nxtgn_surveyrecipientid_value"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "nxtgn_surveystatus_meta", each Value.Metadata([nxtgn_surveystatus])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "nxtgn_reasonforcancelation_meta", each if [nxtgn_reasonforcancelation] is null then "" else Value.Metadata([nxtgn_reasonforcancelation])[OData.Community.Display.V1.FormattedValue]),
    #"Added Conditional Column" = Table.AddColumn(#"Added Custom1", "nxtgn_surveystatus_meta_grouped", each if [nxtgn_surveystatus_meta] = "Open" then "Due" else if [nxtgn_surveystatus_meta] = "Sent" then "Requested" else if [nxtgn_surveystatus_meta] = "Received" then "Received" else "Handled (not sent)", type text),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "nxtgn_surveystatus_meta_grouped_sort", each if [nxtgn_surveystatus_meta_grouped] = "Handled (not sent)" then 2 else if [nxtgn_surveystatus_meta_grouped] = "Due" then 1 else if [nxtgn_surveystatus_meta_grouped] = "Requested" then 3 else if [nxtgn_surveystatus_meta_grouped] = "Received" then 4 else null, type number),
    #"Replaced Value" = Table.ReplaceValue(#"Added Conditional Column1","Sent","No feedback received",Replacer.ReplaceText,{"nxtgn_surveystatus_meta"})
in
    #"Replaced Value"
```

