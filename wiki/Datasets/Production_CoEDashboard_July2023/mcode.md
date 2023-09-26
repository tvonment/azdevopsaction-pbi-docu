



# M Code

|Dataset|[Production_CoEDashboard_July2023](./../Production_CoEDashboard_July2023.md)|
| :--- | :--- |
|Workspace|[CenterOfExcellenceReport](../../Workspaces/CenterOfExcellenceReport.md)|

## Table: Environment


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_environments = entities{[EntitySetName="admin_environments"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(admin_environments,{{"admin_environmentcreatedon", "Created"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"admin_adminmicrosoftteamsenvironmentstatus", "admin_adminmicrosoftteamsenvironmentstatus_display", "admin_adminreason", "admin_adminreviewon", "admin_businessarea", "admin_businessjustificationdate", "admin_makerrequirementbusinessimpact", "admin_makerrequirementbusinessimpact_display", "admin_makerrequirementbusinessjustification", "admin_microsoftteamsid", "admin_microsoftteamsurl", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
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
    #"Added Custom" = Table.AddColumn(#"Invoked Custom Function", "admin_notmodifiedsincecreated", each if [admin_appmodifiedon] = null 
or 
Duration.TotalMinutes([admin_appmodifiedon]-[admin_appcreatedon])<2 
then 1 
else 0),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"admin_apparchiverequestignoredsince", "admin_appcomplexitydescription", "admin_appcomplexityscore", "admin_appconnections", "admin_appcontainsbrokenconnections", "admin_category", "admin_category_display", "admin_dlplastevaluationdate", "admin_dlpviolationdetails", "admin_inappcatalog", "admin_inappcatalogfeatured", "admin_makersubmittedrequirements", "admin_mau", "admin_mau_date", "admin_mau_state", "admin_recordmodified", "admin_requirement_1", "admin_requirement_2", "admin_requirement_3", "admin_requirement_4", "admin_requirement_4_display", "admin_requirement_5", "admin_requirement_6", "admin_requirement_6_display", "admin_reviewedapp", "admin_riskassessment", "admin_riskassessment_display", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Flow


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_flows = entities{[EntitySetName="admin_flows"]}[Data],
    #"Merged Queries" = Table.NestedJoin(admin_flows, {"admin_derivedowner"}, Maker, {"admin_makerid"}, "Owner", JoinKind.LeftOuter),
    #"Expanded Maker" = Table.ExpandTableColumn(#"Merged Queries", "Owner", {"admin_city"}, {"admin_city.1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Maker",{{"admin_city.1", "Flow_Owner_City"}}),
    #"Merged Queries1" = Table.NestedJoin(#"Renamed Columns", {"admin_flowenvironment"}, Environment, {"admin_environmentid"}, "Environment", JoinKind.LeftOuter),
    #"Expanded Environment" = Table.ExpandTableColumn(#"Merged Queries1", "Environment", {"admin_displayname"}, {"Environment.admin_displayname"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Expanded Environment",{{"Environment.admin_displayname", "Flow_Environment_DisplayName"}}),
    #"Invoked Custom Function" = Table.AddColumn(#"Renamed Columns1", "admin_nonprodflowcheck", each NonProdNameCheck([admin_displayname])),
    #"Added Custom" = Table.AddColumn(#"Invoked Custom Function", "admin_notmodifiedsincecreated", each if [admin_flowmodifiedon] = null 
or 
Duration.TotalMinutes([admin_flowmodifiedon]-[admin_flowcreatedon])<2 
then 1 
else 0),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"admin_adminrequirementreviewedflow", "admin_adminrequirementriskassessment", "admin_adminrequirementriskassessment_display", "admin_flowarchiverequestignoredsince", "admin_flowcontainsbrokenconnections", "admin_makerrequirementdependencies", "admin_makersubmittedrequirements", "admin_mitigationplanprovided", "admin_recordmodified", "admin_requirement_1", "admin_requirement_2", "admin_requirement_2_display", "admin_workflowentityid", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Maker


```m
let
   Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
   admin_makers = entities{[EntitySetName="admin_makers"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_makers,{"createdby", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_numberofapps", "admin_numberofapps_date", "admin_numberofapps_state", "admin_numberofcanvasapps", "admin_numberofcanvasapps_date", "admin_numberofcanvasapps_state", "admin_numberofcustomconnectors", "admin_numberofcustomconnectors_date", "admin_numberofcustomconnectors_state", "admin_numberofenvironments", "admin_numberofenvironments_date", "admin_numberofenvironments_state", "admin_numberofflows", "admin_numberofflows_date", "admin_numberofflows_state", "admin_numberofmodeldrivenapps", "admin_numberofmodeldrivenapps_date", "admin_numberofmodeldrivenapps_state", "admin_numberofpvas", "admin_numberofpvas_date", "admin_numberofpvas_state", "admin_numberofsharepointapps", "admin_numberofsharepointapps_date", "admin_numberofsharepointapps_state", "admin_numberofuiflows", "admin_numberofuiflows_date", "admin_numberofuiflows_state", "admin_photo", "admin_recordguidasstring"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "isSystem", each [admin_displayname] = "SYSTEM")
in
    #"Added Custom"
```


## Table: App Connection Reference


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_connectionreferences = entities{[EntitySetName="admin_connectionreferences"]}[Data],
    #"Filtered Rows" = Table.SelectRows(admin_connectionreferences, each ([admin_app] <> null)),
    #"Outer Join" = Table.Join(#"Filtered Rows", "admin_connector", Connector, "admin_connectorid")
in
    #"Outer Join"
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
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"})
in
    #"Removed Columns"
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


## Table: Flow Action Details


```m
let
 Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_flowactiondetails = entities{[EntitySetName="admin_flowactiondetails"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_flowactiondetails,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"})
in
    #"Removed Columns"
```


## Table: Flow Connection Reference


```m
let
     Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_connectionreferences = entities{[EntitySetName="admin_connectionreferences"]}[Data],
    #"Filtered Rows" = Table.SelectRows(admin_connectionreferences, each ([admin_flow] <> null)),
    #"Outer Join" = Table.Join(#"Filtered Rows", "admin_connector", Connector, "admin_connectorid")
in
    #"Outer Join"
```


## Table: Virtual Agent


```m
let
 Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_pvas = entities{[EntitySetName="admin_pvas"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_pvas,{"admin_adminrequirementreviewedbot", "admin_adminrequirementriskassessment", "admin_adminrequirementriskassessment_display", "admin_makerrequirementaccessmanagement", "admin_makerrequirementbusinessimpact", "admin_makerrequirementbusinessimpact_display", "admin_makerrequirementbusinessjustification", "admin_makerrequirementdependencies", "admin_makersubmittedrequirements", "admin_mitigationplanprovided", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "processid", "stageid", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "traversedpath", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Virtual Agent Component


```m
let
 Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_pvacomponents = entities{[EntitySetName="admin_pvacomponents"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_pvacomponents,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
  
in
    #"Removed Columns"
```


## Table: Virtual Agent Flows


```m
let
 Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_pvacomponentflowlookups = entities{[EntitySetName="admin_pvacomponentflowlookups"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_pvacomponentflowlookups,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"})
   
in
    #"Removed Columns"
```


## Table: RPA


```m
let
 Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_rpas = entities{[EntitySetName="admin_rpas"]}[Data],
    #"Added Custom" = Table.AddColumn(admin_rpas, "admin_notmodifiedsincecreated", each if [[admin_rpamodifiedon]] = null 
or 
Duration.TotalMinutes([admin_rpamodifiedon]-[admin_rpacreatedon])<2 
then 1 
else 0),
    #"Invoked Custom Function" = Table.AddColumn(#"Added Custom", "admin_nonprodappnamecheck", each NonProdNameCheck([admin_displayname])),
    #"Removed Columns" = Table.RemoveColumns(#"Invoked Custom Function",{"admin_adminrequirementreviewedrpa", "admin_adminrequirementriskassessment", "admin_adminrequirementriskassessment_display", "admin_clientdatajson", "admin_makerrequirementbusinessimpact", "admin_makerrequirementbusinessimpact_display", "admin_makerrequirementbusinessjustification", "admin_makerrequirementdependencies", "admin_makersubmittedrequirements", "admin_mitigationplanprovided", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: RPA Sessions


```m
let
 Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_rpasessionses = entities{[EntitySetName="admin_rpasessionses"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_rpasessionses,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber"})
    
in
    #"Removed Columns"
```


## Table: OrgUrl


```m
"https://orga9543460.crm4.dynamics.com/" meta [IsParameterQuery=true, Type="Any", IsParameterQueryRequired=true]
```


## Table: Power Platform User


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_powerplatformusers = entities{[EntitySetName="admin_powerplatformusers"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_powerplatformusers,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Portals


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_portals = entities{[EntitySetName="admin_portals"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_portals,{"timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "admin_recordguidasstring"})
in
    #"Removed Columns"
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


## Table: Business Process Flows


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_businessprocessflowses = entities{[EntitySetName="admin_businessprocessflowses"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_businessprocessflowses,{"createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Solutions


```m
let
    Source = Cds.Entities(#"OrgUrl", [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_solutions = entities{[EntitySetName="admin_solutions"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_solutions,{"timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Soltion_Apps


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_ppsolution_apps_tableset = entities{[EntitySetName="admin_ppsolution_apps_tableset"]}[Data]
in
    admin_ppsolution_apps_tableset
```


## Table: Soltion_BPFs


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_ppsolution_bpf_tableset = entities{[EntitySetName="admin_ppsolution_bpf_tableset"]}[Data]
in
    admin_ppsolution_bpf_tableset
```


## Table: Soltion_Flows


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_ppsolution_flow_tableset = entities{[EntitySetName="admin_ppsolution_flow_tableset"]}[Data]
in
    admin_ppsolution_flow_tableset
```


## Table: AI Builder Models


```m
let
    Source = Cds.Entities(#"OrgUrl", [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_aibuildermodel = entities{[EntitySetName="admin_aibuildermodels"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_aibuildermodel,{"timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display", "admin_recordguidasstring"})
in
    #"Removed Columns"
```


## Table: Connection Reference Identity


```m
let
    Source = Cds.Entities(OrgUrl, [ReorderColumns=null, UseFormattedValue=null]),
    entities = Source{[Group="entities"]}[Data],
    admin_connectionreferenceidentities = entities{[EntitySetName="admin_connectionreferenceidentities"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(admin_connectionreferenceidentities,{"timezoneruleversionnumber", "utcconversiontimezonecode", "versionnumber", "createdby", "createdon", "createdonbehalfby", "importsequencenumber", "modifiedby", "modifiedon", "modifiedonbehalfby", "overriddencreatedon", "ownerid", "owningbusinessunit", "owningteam", "owninguser", "statecode", "statecode_display", "statuscode", "statuscode_display"})
in
    #"Removed Columns"
```

