



# M Code

|Dataset|[Voice of the Customer](./../Voice-of-the-Customer.md)|
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
    #"Replaced Value" = Table.ReplaceValue(msfp_questionresponses_table,"Very dissatisfied","1 - Very dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Rather dissatisfied","2 - Rather dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Neutral","3 - Neutral",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Fairly satisfied","4 - Fairly satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Very satisfied","5 - Very satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Added Custom" = Table.AddColumn(#"Replaced Value4", "msfp_response_numeric", each try Number.From(Text.BeforeDelimiter([msfp_response], " ")) otherwise null)
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
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type","Very dissatisfied","1 - Very dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Rather dissatisfied","2 - Rather dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Neutral","3 - Neutral",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Fairly satisfied","4 - Fairly satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Very satisfied","5 - Very satisfied",Replacer.ReplaceText,{"msfp_response"})
in
    #"Replaced Value4"
```


## Table: nxtgn_opportunityclosereasons


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
   nxtgn_opportunityclosereasons_table = Source{[Name="nxtgn_opportunityclosereasons",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityclosereasons_table,{"_nxtgn_opportunityid_value", "nxtgn_opportunityclosereasonid", "_nxtgn_statusreasonid_value", "createdon", "statecode", "statuscode"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue])
in
    #"Added Custom1"
```


## Table: nxtgn_lookupopportunitystatusreasons


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupopportunitystatusreasons_table = Source{[Name="nxtgn_lookupopportunitystatusreasons",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupopportunitystatusreasons_table,{"nxtgn_name", "nxtgn_lookupopportunitystatusreasonid", "nxtgn_order", "statuscode", "nxtgn_category", "nxtgn_outcome", "statecode"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "nxtgn_category_meta", each Value.Metadata([nxtgn_category])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "nxtgn_outcome_meta", each Value.Metadata([nxtgn_outcome])[OData.Community.Display.V1.FormattedValue])
in
    #"Added Custom3"
```


## Table: nxtgn_opportunityregistrations


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_opportunityregistrations_table = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations_table,{"nxtgn_actualclosedate", "nxtgn_topic", "statecode", "nxtgn_opportunityregistrationid", "_ownerid_value", "nxtgn_othercompetitors", "statuscode", "_nxtgn_competitorid_value", "nxtgn_estrevenue_base", "nxtgn_closereasons_concatenate", "_nxtgn_closedbyuserid_value"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue])
in
    #"Added Custom1"
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
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupplatforms_table,{"nxtgn_name", "nxtgn_lookupplatformid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountries


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountries_table = Source{[Name="nxtgn_lookupcountries",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupcountries_table,{"nxtgn_lookupcountryid", "nxtgn_name"})
in
    #"Removed Other Columns"
```


## Table: systemusers (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers_table,{"_nxtgn_platformid_value", "_nxtgn_lookupcountryid_value", "fullname", "systemuserid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupplatforms (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupplatforms_table = Source{[Name="nxtgn_lookupplatforms",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupplatforms_table,{"nxtgn_name", "nxtgn_lookupplatformid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountries (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountries_table = Source{[Name="nxtgn_lookupcountries",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupcountries_table,{"nxtgn_lookupcountryid", "nxtgn_name"})
in
    #"Removed Other Columns"
```


## Table: competitors


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    competitors_table = Source{[Name="competitors",Signature="table"]}[Data]
in
    competitors_table
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


## Table: nxtgn_lookupcountryaliases (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryaliases_table = Source{[Name="nxtgn_lookupcountryaliases",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupcountryaliases_table,{"nxtgn_lookupcountryaliasid", "_nxtgn_countryid_value", "nxtgn_name"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([nxtgn_name] = "Americas (RB)" or [nxtgn_name] = "Asia (RB)" or [nxtgn_name] = "DACH" or [nxtgn_name] = "EMEA (RB)" or [nxtgn_name] = "Middle East" or [nxtgn_name] = "Southeast Asia")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows"," (RB)","",Replacer.ReplaceText,{"nxtgn_name"})
in
    #"Replaced Value"
```


## Table: systemusers (3)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers_table,{"_nxtgn_platformid_value", "_nxtgn_lookupcountryid_value", "fullname", "systemuserid", "title"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_customersurveytriggers


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_customersurveytriggers_table = Source{[Name="nxtgn_customersurveytriggers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_customersurveytriggers_table,{"nxtgn_surveystatus", "_nxtgn_accountid_value", "nxtgn_sendorreminder", "nxtgn_reasonforcancelation", "nxtgn_name", "nxtgn_datesent", "_nxtgn_surveyprojectid_value", "nxtgn_postponedtill", "_nxtgn_surveyinviteid_value", "statuscode", "nxtgn_donotsendsurvey", "createdon", "nxtgn_customersurveytriggerid", "_nxtgn_reminderemailid_value", "nxtgn_surveyinvitationurl", "_nxtgn_emailid_value", "_nxtgn_projectid_value", "nxtgn_reasonnocustomersurvey", "statecode", "_nxtgn_surveyrecipientid_value"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "nxtgn_surveystatus_meta", each Value.Metadata([nxtgn_surveystatus])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "nxtgn_reasonforcancelation_meta", each if [nxtgn_reasonforcancelation] is null then "" else Value.Metadata([nxtgn_reasonforcancelation])[OData.Community.Display.V1.FormattedValue]),
    #"Replaced Value" = Table.ReplaceValue(#"Added Custom1","Sent","No feedback received",Replacer.ReplaceText,{"nxtgn_surveystatus_meta"})
in
    #"Replaced Value"
```


## Table: nxtgn_opportunityregistrations_other_closereason


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_opportunityregistrations_table = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations_table,{"nxtgn_opportunityregistrationid", "nxtgn_closereasons_concatenate"}),
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(#"Removed Other Columns", {{"nxtgn_closereasons_concatenate", Splitter.SplitTextByDelimiter("|", QuoteStyle.None), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "nxtgn_closereasons_concatenate"),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"nxtgn_closereasons_concatenate", type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type",{{"nxtgn_closereasons_concatenate", Text.Trim, type text}}),
    #"Filtered Rows1" = Table.SelectRows(#"Trimmed Text", each Text.StartsWith([nxtgn_closereasons_concatenate], "Other Reason")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows1","Other Reason - ","",Replacer.ReplaceText,{"nxtgn_closereasons_concatenate"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Other Reasons - ","",Replacer.ReplaceText,{"nxtgn_closereasons_concatenate"})
in
    #"Replaced Value1"
```

