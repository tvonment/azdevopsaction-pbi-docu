



# M Code

|Dataset|[demoSynapseSQL](./../demoSynapseSQL.md)|
| :--- | :--- |
|Workspace|[Corporate_Reporting_Synapse_PoC](../../Workspaces/Corporate_Reporting_Synapse_PoC.md)|

## Table: nxtgn_opportunityregistraion_T


```m
let
    Source = nxtgn_opportunityregistration_E,
    #"Removed Columns" = Table.RemoveColumns(Source,{"nxtgn_functioncc", "nxtgn_statusreasonwon", "nxtgn_statusreasonlost", "nxtgn_industrycc", "nxtgn_priority_leads", "nxtgn_dandbaccountadhocqueryid", "nxtgn_dandbaccountadhocqueryid_entitytype", "nxtgn_otherresponsiblerbppri", "nxtgn_otherresponsiblerbppri_entitytype", "nxtgn_additionalsalesunitid", "nxtgn_additionalsalesunitid_entitytype", "nxtgn_additionalcontacts", "nxtgn_additionalcontacts_entitytype", "nxtgn_salesunit_lookup", "nxtgn_salesunit_lookup_entitytype", "owningteam", "owningteam_entitytype", "createdonbehalfby", "createdonbehalfby_entitytype", "nxtgn_salesunit2_lookup", "nxtgn_salesunit2_lookup_entitytype", "nxtgn_masteropportunityid", "nxtgn_masteropportunityid_entitytype", "nxtgn_coownerrb", "nxtgn_coownerrb_entitytype", "nxtgn_sapbydopportunityid", "nxtgn_sapbydopportunityid_entitytype", "nxtgn_additionalppriinacquisition", "nxtgn_additionalppriinacquisition_entitytype", "modifiedonbehalfby", "modifiedonbehalfby_entitytype", "nxtgn_masteropportunity", "nxtgn_masteropportunity_entitytype", "nxtgn_additionalcontact", "nxtgn_additionalcontact_entitytype", "nxtgn_myopportunitycalcplatformvalue", "nxtgn_myopportunitycalcvalue_base", "nxtgn_salesaccessteam_concat", "nxtgn_myopportunitycalcvalue", "nxtgn_myopportunitycalccountryvalue", "nxtgn_myopportunitycalccountryvalue_base", "nxtgn_weightedvalueleadcc_base", "nxtgn_weightedvalueleadcc", "nxtgn_myopportunitycalcplatformvalue_base", "nxtgn_salesaccessteam_concat_base", "nxtgn_additionalcontactyominame", "new_owneremployeeid", "nxtgn_additionalcontactname", "nxtgn_otherccyominame", "nxtgn_dandbaccountadhocqueryidname", "nxtgn_competitoridyominame", "nxtgn_additionalppriinacquisitionyominame", "nxtgn_salesunit_lookupname", "nxtgn_salesteam_concat", "nxtgn_eststartdate", "nxtgn_nextactivityowner", "nxtgn_additionalsalesunitidname", "nxtgn_coownerrbname", "nxtgn_myopportunityweightedvalue_usercurrency", "nxtgn_otherresponsiblerbppriyominame", "nxtgn_additionalcontactsyominame", "nxtgn_sharesalesunit2", "traversedpath", "nxtgn_customerneed", "createdonbehalfbyname", "nxtgn_otherresponsiblerbppriname", "owneridtype", "modifiedonbehalfbyname", "overriddencreatedon", "nxtgn_shareownercc", "nxtgn_accountidyominame", "nxtgn_masteropportunityidname", "nxtgn_coownerrbyominame", "nxtgn_additionalcontactsname", "nxtgn_actualaccountidyominame", "nxtgn_sapbydopportunityidname", "stageid", "nxtgn_additionalppriinacquisitionname", "nxtgn_share_leadcc", "nxtgn_masteropportunityname", "createdonbehalfbyyominame", "modifiedonbehalfbyyominame", "nxtgn_plannedteamsize", "nxtgn_sapopportunityid", "nxtgn_myopportunityvaluecurrency", "new_effortforproposalinfte", "utcconversiontimezonecode", "nxtgn_nextactivitydate", "nxtgn_estprojectduration", "importsequencenumber", "nxtgn_myopportunityvalue_usercurrency", "nxtgn_salesunit2_lookupname", "new_plannedoverdraft", "nxtgn_keyaccountyominame"})
in
    #"Removed Columns"
```

