



# M Code

|Dataset|[PowerPlatformGovernance_CoEDashboard_July2023](./../PowerPlatformGovernance_CoEDashboard_July2023.md)|
| :--- | :--- |
|Workspace|[CenterOfExcellenceReport](../../Workspaces/CenterOfExcellenceReport.md)|

## Table: Environment


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_environments = entities{[EntitySetName="admin_environments"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(admin_environments,{{"admin_environmentcreatedon", "Created"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"admin_adminreason", "admin_adminreviewon", "admin_businessarea", "admin_makerrequirementbusinessimpact", "admin_makerrequirementbusinessimpact_display", "admin_makerrequirementbusinessjustification", "admin_microsoftteamsid", "admin_microsoftteamsurl", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: App


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_apps = entities{[EntitySetName="admin_apps"]}[Data],
     #"Invoked Custom Function" = Table.AddColumn(admin_apps, "admin_nonprodappnamecheck", each NonProdNameCheck([admin_displayname])),
    #"Added admin_notmodifiedsincecreated" = Table.AddColumn(#"Invoked Custom Function", "admin_notmodifiedsincecreated", each if [admin_appmodifiedon] = null 
or 
Duration.TotalMinutes([admin_appmodifiedon]-[admin_appcreatedon])<2 
then 1 
else 0),
    #"Removed Columns" = Table.RemoveColumns(#"Added admin_notmodifiedsincecreated",{"admin_apparchiverequestignoredsince", "admin_appcomplexitydescription", "admin_appcomplexityscore", "admin_appconnections", "admin_appcontainsbrokenconnections", "admin_category", "admin_category_display", "admin_dlplastevaluationdate", "admin_dlpviolationdetails", "admin_inappcatalog", "admin_inappcatalogfeatured", "admin_makersubmittedrequirements", "admin_mau", "admin_mau_date", "admin_mau_state", "admin_recordmodified", "admin_requirement_1", "admin_requirement_2", "admin_requirement_3", "admin_requirement_4", "admin_requirement_4_display", "admin_requirement_5", "admin_requirement_6", "admin_requirement_6_display", "admin_reviewedapp", "admin_riskassessment", "admin_riskassessment_display", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"}),
    #"Added IsNotCurrentMonth" = Table.AddColumn(#"Removed Columns", "IsNotCurrentMonth", each if [admin_applastlaunchedon] = null then true else if Date.IsInCurrentMonth([admin_applastlaunchedon]) then false else true),
    #"Added IsInCurrentQuarter" = Table.AddColumn(#"Added IsNotCurrentMonth", "IsInCurrentQuarter", each if [admin_applastlaunchedon] = null then false else if Date.IsInCurrentQuarter([admin_applastlaunchedon]) then true else false)
in
    #"Added IsInCurrentQuarter"
```


## Table: Flow


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_flows = entities{[EntitySetName="admin_flows"]}[Data],
    #"Merged Queries" = Table.NestedJoin(admin_flows, {"admin_flowcreator"}, Maker, {"admin_makerid"}, "Maker", JoinKind.LeftOuter),
    #"Removed Columns" = Table.RemoveColumns(#"Merged Queries",{"admin_recordguidasstring"}),
    #"Expanded Maker" = Table.ExpandTableColumn(#"Removed Columns", "Maker", {"admin_city"}, {"admin_city.1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Maker",{{"admin_city.1", "Flow_Creator_City"}}),
    #"Merged Queries1" = Table.NestedJoin(#"Renamed Columns", {"admin_flowenvironment"}, Environment, {"admin_environmentid"}, "Environment", JoinKind.LeftOuter),
    #"Expanded Environment" = Table.ExpandTableColumn(#"Merged Queries1", "Environment", {"admin_displayname"}, {"Environment.admin_displayname"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Expanded Environment",{{"Environment.admin_displayname", "Flow_Environment_DisplayName"}}),
    #"Invoked Custom Function" = Table.AddColumn(#"Renamed Columns1", "admin_nonprodflowcheck", each NonProdNameCheck([admin_displayname])),
    #"Added Custom" = Table.AddColumn(#"Invoked Custom Function", "admin_notmodifiedsincecreated", each if [admin_flowmodifiedon] = null 
or 
Duration.TotalMinutes([admin_flowmodifiedon]-[admin_flowcreatedon])<2 
then 1 
else 0),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Custom", each if [admin_flowpendingsuspensionpowerappplanexcluded] = false then [admin_flowsuspensionreason] else if [admin_flowpendingsuspensionpowerappplanexcluded] = true and [admin_flowpendingsuspensionreason] = "MissingPremiumLicense" then [admin_flowpendingsuspensionreason] & " - out of context of Power Apps" else [admin_flowpendingsuspensionreason]),
    #"Renamed Columns2" = Table.RenameColumns(#"Added Custom1",{{"Custom", "Suspension Reason"}})
in
    #"Renamed Columns2"
```


## Table: Maker


```m
let
   Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
   admin_makers = entities{[EntitySetName="admin_makers"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_makers,{"createdby", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_numberofapps", "admin_numberofapps_date", "admin_numberofapps_state", "admin_numberofcanvasapps", "admin_numberofcanvasapps_date", "admin_numberofcanvasapps_state", "admin_numberofcustomconnectors", "admin_numberofcustomconnectors_date", "admin_numberofcustomconnectors_state", "admin_numberofenvironments", "admin_numberofenvironments_date", "admin_numberofenvironments_state", "admin_numberofflows", "admin_numberofflows_date", "admin_numberofflows_state", "admin_numberofmodeldrivenapps", "admin_numberofmodeldrivenapps_date", "admin_numberofmodeldrivenapps_state", "admin_numberofpvas", "admin_numberofpvas_date", "admin_numberofpvas_state", "admin_numberofsharepointapps", "admin_numberofsharepointapps_date", "admin_numberofsharepointapps_state", "admin_numberofuiflows", "admin_numberofuiflows_date", "admin_numberofuiflows_state", "admin_photo", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: App Connection Reference


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_connectionreferences = entities{[EntitySetName="admin_connectionreferences"]}[Data],
    #"Filtered Rows" = Table.SelectRows(admin_connectionreferences, each ([admin_app] <> null))
in
    #"Filtered Rows"
```


## Table: Audit Log


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_auditlogs = entities{[EntitySetName="admin_auditlogs"]}[Data],
    #"Duplicated Column" = Table.DuplicateColumn(admin_auditlogs, "admin_creationtime", "admin_creationtime - Copy"),
    #"Calculated Start of Hour" = Table.TransformColumns(#"Duplicated Column",{{"admin_creationtime - Copy", Time.StartOfHour, type datetimezone}}),
    #"Renamed Columns" = Table.RenameColumns(#"Calculated Start of Hour",{{"admin_creationtime - Copy", "admin_creationhour"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each true),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"admin_creationtime", type datetime}, {"admin_creationhour", type datetime}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns",#datetime(2021, 10, 4, 14, 44, 0),#datetime(2022, 5, 15, 14, 44, 0),Replacer.ReplaceValue,{"admin_creationtime"}),
    #"Added Custom" = Table.AddColumn(#"Replaced Value", "IsNotCurrentMonth", each if Date.IsInCurrentMonth([admin_creationtime])
then false
else true),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "IsInCurrentQuarter", each if Date.IsInCurrentQuarter([admin_creationtime])
    then true
    else false)
in
    #"Added Custom1"
```


## Table: Connector


```m
let
Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_connectors = entities{[EntitySetName="admin_connectors"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_connectors,{"admin_adminrequirementreviewedconnector", "admin_adminrequirementriskassessment", "admin_adminrequirementriskassessment_display", "admin_makerrequirementaccessmanagement", "admin_makerrequirementbusinessjustification", "admin_makerrequirementconditionsofuse", "admin_makerrequirementdependencies", "admin_recordmodified", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"admin_displayname", "admin_connectordisplayname"}})
in
    #"Renamed Columns"
```


## Table: NonProdWords


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCnENDlGK1QExfAPADN9KMOWSmpsPZjjnF1Qq5KeB2boxpQYGxqlgdnBibkEOkBkLAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Label = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Label", type text}})
in
    #"Changed Type"
```


## Table: Flow Connection Reference


```m
let
     Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_connectionreferences = entities{[EntitySetName="admin_connectionreferences"]}[Data],
    #"Filtered Rows" = Table.SelectRows(admin_connectionreferences, each ([admin_flow] <> null))
in
    #"Filtered Rows"
```


## Table: OrgUrl


```m
" https://orga9543460.crm4.dynamics.com/" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Table: Environment Capacity


```m
let
    Source = Cds.Entities(#"OrgUrl", [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_environmentcapacity = entities{[EntitySetName="admin_environmentcapacities"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_environmentcapacity,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"})
 in
    #"Removed Columns"
```


## Table: Connection Identity


```m
let
    Source = Cds.Entities(#"OrgUrl", [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_environmentcapacity = entities{[EntitySetName="admin_connectionreferenceidentities"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_environmentcapacity,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"})
 in
    #"Removed Columns"
```


## Table: Environment Request


```m
let
    Source = Cds.Entities(#"OrgUrl", [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_environmentrequests = entities{[EntitySetName="coe_environmentcreationrequests"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_environmentrequests,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each [coe_requeststatus_display] = "Pending")
 in
    #"Filtered Rows"
```

