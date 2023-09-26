



# M Code

|Dataset|[RB_Dashboard](./../RB_Dashboard.md)|
| :--- | :--- |
|Workspace|[CRM Project](../../Workspaces/CRM-Project.md)|

## Table: User


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com,5558", "org9c81da0a", [Query="Select lower(systemuserid) as systemuserid, fullname, nxtgn_rbuserid, nxtgn_ccdepartment, internalemailaddress  from systemuser where nxtgn_islicensed is null and isdisabled = 0#(lf)"])
in
    Quelle
```


## Table: Contacts


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com,5558", "org9c81da0a", [Query="Select lower(contactid) as contactid, fullname, emailaddress1, statuscodename, [address1_line1],[address1_postalcode], [address1_city],[address1_country], [nxtgn_lastcampaignname], #(lf)[nxtgn_contactresponsibles_concatenate], statecode from contact #(lf)where statecode = 0#(lf)#(lf)"])
in
    Quelle
```


## Table: Responsibles


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com,5558", "org9c81da0a", [Query="Select lower(cr.nxtgn_contactid) as contactid, lower(cr.nxtgn_userid) as userid from nxtgn_contactresponsibility cr#(lf)inner join contact c on c.contactid = cr.nxtgn_contactid #(lf)where c.statecode = 0"])
in
    Quelle
```


## Table: Emailblast


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com,5558", "org9c81da0a", [Query="Select lower(nxtgn_emailcampaignmailblastid) as emailcampaignblastid, lower(nxtgn_emailcampaignid) as hubspotcampaignid, *  from nxtgn_emailcampaignmailblast#(lf)"])
in
    Quelle
```


## Table: HubSpot Campaign


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com,5558", "org9c81da0a", [Query="Select lower(nxtgn_hubspotcampaignid) as hubspotcampaingid,*  from nxtgn_hubspotcampaign"])
in
    Quelle
```


## Table: Opportunity


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com,5558", "org9c81da0a", [Query="Select * from nxtgn_opportunityregistration"])
in
    Quelle
```


## Table: CampaignMember


```m
let
    Quelle = Sql.Database("rolandbergerdev.crm4.dynamics.com", "org9c81da0a", [Query="SELECT TOP 5000 lower(nxtgn_contactid) as nxtgn_contactid, lower(nxtgn_userid) as nxtgn_userid, con.address1_city, con.address1_line1, con.nxtgn_contactresponsibles_concatenate, con.nxtgn_functionbc, con.emailaddress1, con.address1_county, con.fullname, con.lastname, con.address1_postalcode, con.nxtgn_isalumnus, con.accountid, list.listname, list.listid, nxtgn_emailcampaignmailblast.nxtgn_blastname, nxtgn_emailcampaignmailblast.nxtgn_hubspotid, nxtgn_emailcampaignmailblast.nxtgn_subject, nxtgn_emailcampaignmailblast.nxtgn_languageid, nxtgn_emailcampaignmailblast.nxtgn_hubspotsenderid, nxtgn_emailcampaignmailblast.nxtgn_hubspotcampaignid, nxtgn_emailcampaignmailblast.nxtgn_emailcampaignid, nxtgn_emailcampaignmailblast.nxtgn_languageidname, nxtgn_emailcampaignmailblast.nxtgn_emailcampaignmailblastid#(lf)FROM nxtgn_contactresponsibility#(lf)JOIN contact con ON con.contactid = nxtgn_contactresponsibility.nxtgn_contactid#(lf)JOIN listmember listrel ON listrel.entityid = con.contactid#(lf)JOIN list list ON list.listid = listrel.listid#(lf)JOIN nxtgn_mailblasttargetlist nxtgn_mailblasttargetlist ON nxtgn_mailblasttargetlist.nxtgn_marketinglistid = list.listid#(lf)JOIN nxtgn_emailcampaignmailblast nxtgn_emailcampaignmailblast ON nxtgn_emailcampaignmailblast.nxtgn_emailcampaignmailblastid = nxtgn_mailblasttargetlist.nxtgn_emailcampaignmailblastid"])
in
    Quelle
```

