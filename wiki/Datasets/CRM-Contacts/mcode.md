



# M Code

|Dataset|[CRM Contacts](./../CRM-Contacts.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: contact


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_contact = rolandberger{[Schema="dbo",Item="contact"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_contact, each ([statuscodename] <> "Inactive – Deceased" and [statuscodename] <> "Inactive – Retired" and [statuscodename] <> "Outdated in Dyn365 – can be deleted in OL")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"contactid", "fullname", "statuscodename", "nxtgn_accountnamesearch", "accountid", "nxtgn_isalumnus", "emailaddress1", "address1_country", "nxtgn_vipidname", "gendercodename", "nxtgn_lastcampaignname", "lastusedincampaign", "nxtgn_dqapproved", "nxtgn_prebounced", "nxtgn_postbounced", "msdyn_orgchangestatusname", "nxtgn_dqapprovedname", "nxtgn_prebouncedname", "nxtgn_postbouncedname", "donotsendmarketingmaterialname"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_contactresponsibility


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_contactresponsibility = rolandberger{[Schema="dbo",Item="nxtgn_contactresponsibility"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_contactresponsibility, each ([statecodename] = "Active")),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [nxtgn_userid] <> null),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"nxtgn_contactid", "nxtgn_ratingstars", "nxtgn_userid", "nxtgn_donotsynctooutlookname"})
in
    #"Removed Other Columns"
```


## Table: systemuser


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_systemuser = rolandberger{[Schema="dbo",Item="systemuser"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_systemuser, each ([islicensed] = true)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"systemuserid", "internalemailaddress", "fullname", "nxtgn_platformidname", "nxtgn_outlookcontactsyncprofilename", "nxtgn_lookupcountryidname"})
in
    #"Removed Other Columns"
```


## Table: account


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_account = rolandberger{[Schema="dbo",Item="account"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_account, each ([statecodename] = "Active")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"name", "accountid", "nxtgn_industrycrmidname", "nxtgn_subindustrycrmidname", "nxtgn_suggestedindustrycrmidname", "nxtgn_suggestedsubindustrycrmidname", "nxtgn_suggestedindustrylinkedinname", "nxtgn_suggestedsubindustrylinkedinname"})
in
    #"Removed Other Columns"
```


## Table: listmember


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_listmember = rolandberger{[Schema="dbo",Item="listmember"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_listmember, each ([listid] = "1F5CAC95-C271-EB11-A812-000D3A2A665C")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"entityid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_hubspotactivity


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_hubspotactivity = rolandberger{[Schema="dbo",Item="nxtgn_hubspotactivity"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_hubspotactivity, each ([nxtgn_typename] = "Sent")),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each ([nxtgn_hubspotcampaignid] <> null)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"scheduledend", "nxtgn_hubspotcampaignid", "nxtgn_hubspotcampaignidname", "contact"}),
    #"Expanded contact" = Table.ExpandRecordColumn(#"Removed Other Columns", "contact", {"contactid"}, {"contact.contactid"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded contact",{{"scheduledend", type date}})
in
    #"Changed Type"
```


## Table: lead


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_lead = rolandberger{[Schema="dbo",Item="lead"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_lead,{"leadid", "fullname", "companyname", "address1_country", "statecodename", "statecode", "statuscode", "statuscodename", "nxtgn_dealid", "nxtgn_businessfunctions", "nxtgn_existingcompany", "nxtgn_existingcompanyname", "nxtgn_existingcontact", "nxtgn_existingcontactname", "nxtgn_functionfrombc", "nxtgn_hubspotcontactid", "nxtgn_industries", "nxtgn_languageid", "nxtgn_campaignshortname", "nxtgn_vipid", "nxtgn_vipidname", "nxtgn_linkhubspotcontact", "nxtgn_engagementscore", "createdon"}),
    #"Replaced Value13" = Table.ReplaceValue(#"Removed Other Columns",",",", ",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value" = Table.ReplaceValue(#"Replaced Value13","204030000","Aerospace & Defense",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","204030001","Automotive",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","204030002","Chemicals",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","204030003","Civil Economics",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","204030004","Construction",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","204030005","Consumer Goods",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","204030006","Energy & Utilities",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","204030007","Financial Services",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value7","204030008","Industrial Products & Services",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value9" = Table.ReplaceValue(#"Replaced Value8","204030009","Infrastructure",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value10" = Table.ReplaceValue(#"Replaced Value9","204030010","Pharma & Healthcare",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value11" = Table.ReplaceValue(#"Replaced Value10","204030011","Technology",Replacer.ReplaceText,{"nxtgn_industries"}),
    #"Replaced Value12" = Table.ReplaceValue(#"Replaced Value11","204030012","Transportation",Replacer.ReplaceText,{"nxtgn_industries"})
in
    #"Replaced Value12"
```


## Table: team


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_team = rolandberger{[Schema="dbo",Item="team"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_team, each [teamtypename] = "Access"),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"teamid", "regardingobjectid"})
in
    #"Removed Other Columns"
```


## Table: teammembership


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_teammembership = rolandberger{[Schema="dbo",Item="teammembership"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_teammembership,{"teamid", "systemuserid"})
in
    #"Removed Other Columns"
```


## Roles

### P/PRI


Model Permission: Read

systemuser

```m
systemuser[internalemailaddress] = USERPRINCIPALNAME()
```

