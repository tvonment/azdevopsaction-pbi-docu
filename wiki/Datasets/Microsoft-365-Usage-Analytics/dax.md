



# DAX

|Dataset|[Microsoft 365 Usage Analytics](./../Microsoft-365-Usage-Analytics.md)|
| :--- | :--- |
|Workspace|[Microsoft 365 Usage Analytics](../../Workspaces/Microsoft-365-Usage-Analytics.md)|

## Table: TenantClientUsage

### Measures:


```dax
MostRecent-UserCount = CALCULATE(SUM([UserCount]),LASTDATE('TenantClientUsage'[TimeFrame]))
```



```dax
ClientIDTitle = VAR SelectedClient = VALUES('TenantClientUsage'[ClientId])
VAR	NumofSelectedClients = COUNTROWS(SelectedClient)
VAR	NumofPossibleClients = COUNTROWS(ALL('TenantClientUsage'[ClientId]))
var	allbutlastselectedclient = TOPN(NumofSelectedClients-1,SelectedClient)
var lastselectedclient = EXCEPT(SelectedClient,allbutlastselectedclient)
RETURN
"Access from anywhere, on "
& IF(NumofSelectedClients=NumofPossibleClients,
	" any device"
	," "
	& IF(NumofSelectedClients =1,
		"",
		CONCATENATEX(allbutlastselectedclient,'TenantClientUsage'[ClientId],", ")
		& " and " )
		& lastselectedclient
)
```


### Calculated Columns:


```dax
EOMTimeFrame = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(NOW() >= DATEADD('TenantClientUsage'[EOMTimeFrame].[Date],5,DAY),TRUE(),FALSE())
```


## Table: TenantMailboxUsage

### Measures:


```dax
EXO-StorageUsed = CALCULATE(SUM([DiskUsedbyStorageType]))
```



```dax
TotalIssueWarningQuota(GB) = CALCULATE(DIVIDE(SUM([IssueWarningQuota]),1073741824,0))
```



```dax
TotalMailboxes-withinLimit = CALCULATE(SUM([TotalMailboxes])-SUM([MailboxesIssueWarning]))
```



```dax
TotalProhibitSend/ReceiveQuota(GB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1073741824,0))
```



```dax
TotalProhibitSendQuota(GB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1073741824,0))
```



```dax
ExceededSend/ReceiveQuota = CALCULATE(SUM([MailboxesExceedSendReceiveQuota]))
```



```dax
ExceededSendQuota = CALCULATE(SUM([MailboxesExceedSendQuota]))
```



```dax
IssuedWarning = CALCULATE(SUM([MailboxesIssueWarning]))
```



```dax
MostRecent-IssueWarningQuota(GB) = CALCULATE(DIVIDE(SUM([IssueWarningQuota]),1073741824,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-MailboxesNoWarning = CALCULATE(SUM([MailboxesNoWarning]),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-ExceededSend/ReceiveQuota = CALCULATE(SUM([MailboxesExceedSendReceiveQuota]),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-ExceededSendQuota = CALCULATE(SUM([MailboxesExceedSendQuota]),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-StorageUsed(GB) = CALCULATE(DIVIDE(SUM([TotalItemBytes]),1073741824,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-TotalProhibitSend/ReceiveQuota(GB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1073741824,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-Mailboxes = CALCULATE(SUM([TotalMailboxes]),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-MailboxesWithinLimit = CALCULATE(SUM([TotalMailboxes])-SUM([MailboxesIssueWarning]),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-TotalProhibitSendQuota(GB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1073741824,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-IssuedWarning = CALCULATE(SUM([MailboxesIssueWarning]),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
TotalStorageUsed = CALCULATE(SUM([TotalItemBytes]))
```



```dax
TotalProhibitSend/ReceiveQuota(TB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1099511627776,0))
```



```dax
TotalProhibitSendQuota(TB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1099511627776,0))
```



```dax
IssueWarningQuota_calc = CALCULATE(SUM([IssueWarningQuota]))
```



```dax
MostRecent-TotalProhibitSendQuota(TB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1099511627776,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-TotalProhibitSend/ReceiveQuota(TB) = CALCULATE(DIVIDE(SUM([ProhibitSendQuota]),1099511627776,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-StorageUsed(TB) = CALCULATE(DIVIDE(SUM([TotalItemBytes]),1099511627776,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
MostRecent-IssueWarningQuota(TB) = CALCULATE(DIVIDE(SUM([IssueWarningQuota]),1099511627776,0),LASTDATE('TenantMailboxUsage'[TimeFrame]))
```



```dax
EXO-Storage(%) = CALCULATE(DIVIDE([EXO-StorageUsed],[IssueWarningQuota_calc],0))
```



```dax
MostRecent-EXO-Storage(%) = CALCULATE(DIVIDE([MostRecent-EXO_StorageUsed],[MostRecent-IssueWarningQuota],0))
```



```dax
Mailbox_MostRecentDate = FORMAT(LASTDATE('TenantMailboxUsage'[TimeFrame]),"mmmm")& " " & FORMAT(LASTDATE('TenantMailboxUsage'[TimeFrame]),"YYYY")
```



```dax
TotalIssueWarningQuota = CALCULATE(SUM([TotalIssueWarningQuotaValue]))
```



```dax
MostRecent-StorageUsed = LASTNONBLANK(TenantMailboxUsage[MailboxStorageUsed], 1)
```



```dax
MostRecent-EXO_StorageUsed = CALCULATE(SUM(TenantMailboxUsage[DiskUsedbyStorageType]), LASTDATE(TenantMailboxUsage[TimeFrame]))
```



```dax
MostRecent-IssueWarningQuota = CALCULATE(SUM(TenantMailboxUsage[TotalIssueWarningQuotaValue]), LASTDATE(TenantMailboxUsage[TimeFrame]))
```



```dax
MostRecent-EXO_StorageType = LASTNONBLANK(TenantMailboxUsage[EXO-StorageType], 1)
```



```dax
MostRecent-TotalIssueWarningQuotaType = LASTNONBLANK(TenantMailboxUsage[TotalIssueWarningQuotaType], 1) 
```



```dax
MostRecent-EXO-Storage(GB)(%) = CALCULATE(DIVIDE([MostRecent-StorageUsed(GB)],[MostRecent-IssueWarningQuota(GB)],0))
```



```dax
MostRecent-StorageType(GB) = "GB"
```



```dax
EXO-StorageUsed(GB) = CALCULATE(DIVIDE(SUM([TotalItemBytes]), 1073741824, 0))
```



```dax
Mailbox Label = CONCATENATE( [Mailbox_MostRecentDate], " Mailbox Count")
```



```dax
Storage Label = CONCATENATE( [Mailbox_MostRecentDate], " Storage Used")
```



```dax
EXO storage Label = CONCATENATE( [Mailbox_MostRecentDate], " Storage Used (GB)")
```


### Calculated Columns:


```dax
Product = "Exchange"
```



```dax
StorageUsed(KB/MB/GB/TB) = IF([TotalStorageUsed]/1024 <= 1, FIXED([TotalStorageUsed],2,1)& " " & "Bytes",IF([TotalStorageUsed]/1048576 <= 1 && [TotalStorageUsed]/1024 > 1, FIXED([TotalStorageUsed]/1024,2,1) &" " & "KB",IF([TotalStorageUsed]/1073741824 <= 1 && [TotalStorageUsed]/1048576 > 1,FIXED([TotalStorageUsed]/1048576,2,1)  & " " & "MB",IF([TotalStorageUsed]/1073741824 > 1 && [TotalStorageUsed]/1099511627776 <= 1 ,FIXED([TotalStorageUsed]/1073741824,2,1)  & " " & "GB",IF([TotalStorageUsed]/1099511627776 >= 1,FIXED([TotalStorageUsed]/1099511627776,2,1)  & " " & "TB","0")))))
```



```dax
EXO-StorageType = RIGHT([StorageUsed(KB/MB/GB/TB)],LEN([StorageUsed(KB/MB/GB/TB)])-SEARCH(" ",[StorageUsed(KB/MB/GB/TB)]))
```



```dax
DiskUsedbyStorageType = LEFT([StorageUsed(KB/MB/GB/TB)],SEARCH(" ",[StorageUsed(KB/MB/GB/TB)]))
```



```dax
EOMTimeFrame = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EOMTimeFrame],[ContentDate] > [EOMTimeFrame]),TRUE(),FALSE())
```



```dax
TotalIssueWarningQuota(KB/MB/GB/TB) = IF([IssueWarningQuota_calc]/1024 <= 1, FIXED([IssueWarningQuota_calc],2,1)& " " & "Bytes",IF([IssueWarningQuota_calc]/1048576 <= 1 && [IssueWarningQuota_calc]/1024 > 1, FIXED([IssueWarningQuota_calc]/1024,2,1) &" " & "KB",IF([IssueWarningQuota_calc]/1073741824 <= 1 && [IssueWarningQuota_calc]/1048576 > 1,FIXED([IssueWarningQuota_calc]/1048576,2,1)  & " " & "MB",IF([IssueWarningQuota_calc]/1073741824 > 1 && [IssueWarningQuota_calc]/1099511627776 <= 1 ,FIXED([IssueWarningQuota_calc]/1073741824,2,1)  & " " & "GB",IF([IssueWarningQuota_calc]/1099511627776 >= 1,FIXED([IssueWarningQuota_calc]/1099511627776,2,1)  & " " & "TB","0")))))
```



```dax
TotalIssueWarningQuotaType = RIGHT([TotalIssueWarningQuota(KB/MB/GB/TB)],LEN([StorageUsed(KB/MB/GB/TB)])-SEARCH(" ",[StorageUsed(KB/MB/GB/TB)])) 
```



```dax
TotalIssueWarningQuotaValue = LEFT([TotalIssueWarningQuota(KB/MB/GB/TB)],SEARCH(" ",[TotalIssueWarningQuota(KB/MB/GB/TB)]))
```



```dax
MailboxStorageUsed = IF([TotalStorageUsed]/1024 < 1, FIXED([TotalStorageUsed],0,1)& " " & "Bytes",IF([TotalStorageUsed]/1048576 < 1 && [TotalStorageUsed]/1024 > 1, FIXED([TotalStorageUsed]/1024,0,1) &" " & "KB",IF([TotalStorageUsed]/1073741824 < 1 && [TotalStorageUsed]/1048576 > 1,FIXED([TotalStorageUsed]/1048576,0,1)  & " " & "MB",IF([TotalStorageUsed]/1073741824 > 1 && [TotalStorageUsed]/1099511627776 < 1 ,FIXED([TotalStorageUsed]/1073741824,0,1)  & " " & "GB",IF([TotalStorageUsed]/1099511627776 > 1,FIXED([TotalStorageUsed]/1099511627776,0,1)  & " " & "TB","0"))))) 
```


## Table: TenantOfficeActivation

### Measures:


```dax
MostRecent-TotalActivatedUsers = CALCULATE(SUM([TotalActivatedUsers]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-TotalEnabledUsers = CALCULATE(SUM([TotalEnabled]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-Activation% = DIVIDE('TenantOfficeActivation'[MostRecent-TotalActivatedUsers],'TenantOfficeActivation'[MostRecent-TotalEnabledUsers],0)
```



```dax
MostRecent-TotalAndroidCount = CALCULATE(SUM([AndroidCount]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-TotaliOSCount = CALCULATE(SUM([iOSCount]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-TotalMacCount = CALCULATE(SUM([MacCount]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-TotalPcCount = CALCULATE(SUM([PcCount]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-TotalWinRTCount = CALCULATE(SUM([WinRtCount]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
MostRecent-TotalActivations = CALCULATE(SUM([TotalActivations]),LASTDATE('TenantOfficeActivation'[TimeFrame]))
```



```dax
OfficeActivationTitle = VAR	SelectedServicePlan = VALUES('TenantOfficeActivation'[ServicePlanName])
var	NumofSelectedSvcPlans = COUNTROWS(SelectedServicePlan)
var NumofPossibleSvcPlans = COUNTROWS(ALL('TenantOfficeActivation'[ServicePlanName]))
var AllbutLastSelectedSvcPLan = TOPN(NumofSelectedSvcPlans-1,SelectedServicePlan)
VAR LastSelectedSvcPlan = EXCEPT(SelectedServicePlan,AllbutLastSelectedSvcPLan)
RETURN
"Office activation "
& IF(NumofSelectedSvcPlans=NumofPossibleSvcPlans,
	BLANK(), " : "
	& IF(NumofSelectedSvcPlans=1,
		"",CONCATENATEX(AllbutLastSelectedSvcPLan,'TenantOfficeActivation'[ServicePlanName],", " )
		& ",  and " )
		& LastSelectedSvcPlan
)
```



```dax
OfficeActivation_MostRecentDate = FORMAT(LASTDATE('TenantOfficeActivation'[TimeFrame]),"mmmm")& " " & FORMAT(LASTDATE('TenantOfficeActivation'[TimeFrame]),"YYYY")
```



```dax
Activation % Label = CONCATENATE( [OfficeActivation_MostRecentDate], " Activation %")
```



```dax
Activated Label = CONCATENATE( [OfficeActivation_MostRecentDate], " Activated Users")
```



```dax
Activation Count Label = CONCATENATE( [OfficeActivation_MostRecentDate], " Total Activation Count")
```


### Calculated Columns:


```dax
EOMTimeFrame = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EOMTimeFrame],[ContentDate] > [EOMTimeFrame]),TRUE(),FALSE())
```



```dax
IsLastMonth = IF(MAX([TimeFrame])=[TimeFrame],TRUE(),FALSE())
```


## Table: TenantOneDriveUsage

### Calculated Columns:


```dax
EOMTimeframe = EOMONTH([TimeFrame],0)
```


## Table: TenantProductActivity

### Measures:


```dax
ODB-FilesSharedINT = CALCULATE(SUM([ActivityCount]),'TenantProductActivity'[Product]="OneDrive",'TenantProductActivity'[Activity]="Files Shared Internally")
```



```dax
ODB-FilesSharedEXT = CALCULATE(SUM([ActivityCount]),'TenantProductActivity'[Product]="OneDrive",'TenantProductActivity'[Activity]="Files Shared Externally")
```



```dax
SPO-FilesSharedINT = CALCULATE(SUM([ActivityCount]),'TenantProductActivity'[Product]="SharePoint",'TenantProductActivity'[Activity]="Files Shared Internally")
```



```dax
SPO-FilesSharedEXT = CALCULATE(SUM([ActivityCount]),'TenantProductActivity'[Product]="SharePoint",'TenantProductActivity'[Activity]="Files Shared Externally")
```



```dax
MostRecent-SFB_TimeSpent(Hours) = CALCULATE(DIVIDE(SUM([TotalDurationInMinute]),60,0),'TenantProductActivity'[Product]="Skype",LASTDATE('TenantProductActivity'[TimeFrame]))
```



```dax
MostRecent-TotalDuration = CALCULATE(SUM([TotalDurationInMinute]),LASTDATE('TenantProductActivity'[TimeFrame]))
```



```dax
Avg Duration(Min)/User = DIVIDE(CALCULATE(SUM([TotalDurationInMinute]),TenantProductActivity[Product]="Skype"),CALCULATE(SUM([ActiveUserCount]),'TenantProductActivity'[Product]="Skype"),0)
```



```dax
Avg#ofActivities/User = DIVIDE(CALCULATE(SUM([ActivityCount])),CALCULATE(SUM([ActiveUserCount])),0)
```



```dax
MostRecent-SFB_TimeSpent(Days) = CALCULATE(DIVIDE(CALCULATE(DIVIDE(SUM([TotalDurationInMinute]),60,0),'TenantProductActivity'[Product]="Skype",LASTDATE('TenantProductActivity'[TimeFrame])),24,0))
```



```dax
MostRecent-ActivityCount = CALCULATE(SUM([ActivityCount]),LASTDATE('TenantProductActivity'[TimeFrame]))
```



```dax
MostRecent-ActiveUserCount = CALCULATE(SUM([ActiveUserCount]),LASTDATE('TenantProductActivity'[TimeFrame]))
```



```dax
SFBUsage_CollabTypeTitle = VAR	SelectedCollabType = VALUES('TenantProductActivity'[HierarchyCategory])
var	NumofSelectedCollabType = COUNTROWS(SelectedCollabType)
var NumofPossibleCollabType = COUNTROWS(ALL('TenantProductActivity'[HierarchyCategory]))
var AllbutLastSelectedCollabType = TOPN(NumofSelectedCollabType-1,SelectedCollabType)
VAR LastSelectedCollabType = EXCEPT(SelectedCollabType,AllbutLastSelectedCollabType)
RETURN
"Skype for Business usage "
& IF(NumofSelectedCollabType=NumofPossibleCollabType,
	BLANK(), " : "
	& IF(NumofSelectedCollabType=1,
		"",CONCATENATEX(AllbutLastSelectedCollabType,'TenantProductActivity'[HierarchyCategory],", " )
		& " and " )
		& LastSelectedCollabType
)
```



```dax
ProdActivity_MostRecentDate = FORMAT(LASTDATE('TenantProductActivity'[TimeFrame]),"mmmm")& " " & FORMAT(LASTDATE('TenantProductActivity'[TimeFrame]),"YYYY")
```



```dax
MostRecent-Avg#ofActivities/User = DIVIDE(CALCULATE(SUM([ActivityCount]),LASTDATE('TenantProductActivity'[TimeFrame])),CALCULATE(SUM([ActiveUserCount]),LASTDATE('TenantProductActivity'[TimeFrame])),0)
```



```dax
PrevMonthAvg#ofActivities = CALCULATE([Avg#ofActivities/User],PREVIOUSMONTH('Calendar'[Date]))
```



```dax
(%)ChangeinAvg#ofActivities = CALCULATE(DIVIDE([Avg#ofActivities/User]-[PrevMonthAvg#ofActivities],[PrevMonthAvg#ofActivities],BLANK()),USERELATIONSHIP('TenantProductActivity'[TimeFrame],'Calendar'[Date]))
```



```dax
MostRecent-(%)ChangeinAvg#ofActivities = CALCULATE(DIVIDE([Avg#ofActivities/User]-[PrevMonthAvg#ofActivities],[PrevMonthAvg#ofActivities],BLANK()),LASTDATE('TenantProductActivity'[TimeFrame]))
```



```dax
PrevMonth(%)ChangeinAvg#ofActivities = CALCULATE(DIVIDE([Avg#ofActivities/User]-[PrevMonthAvg#ofActivities],[PrevMonthAvg#ofActivities],BLANK()),PREVIOUSMONTH('Calendar'[Date]),USERELATIONSHIP('TenantProductActivity'[TimeFrame],'Calendar'[Date]),'TenantProductActivity'[IsMonthComplete]=TRUE())
```



```dax
PrevMonthActiveUserCount = CALCULATE(SUM([ActiveUserCount]),PREVIOUSMONTH('Calendar'[Date]))
```



```dax
(%)ChangeinActiveUserCount = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveUserCount]))-[PrevMonthActiveUserCount],[PrevMonthActiveUserCount],BLANK()),USERELATIONSHIP('TenantProductActivity'[TimeFrame],'Calendar'[Date]))
```



```dax
PrevMonthActivityCount = CALCULATE(SUM([ActivityCount]),PREVIOUSMONTH('Calendar'[Date]))
```



```dax
(%)ChangeinActivityCount = CALCULATE(DIVIDE(CALCULATE(SUM([ActivityCount]))-[PrevMonthActivityCount],[PrevMonthActivityCount],BLANK()),USERELATIONSHIP('TenantProductActivity'[TimeFrame],'Calendar'[Date]))
```



```dax
Product Active User Display = IF(ISFILTERED(TenantProductActivity[ProductActivityCombo]), SUM(TenantProductActivity[ActiveUserCount]), IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Exchange", CALCULATE(SUM(TenantProductActivity[ActiveUserCount]),TenantProductActivity[ProductActivityCombo]="EXO - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="OneDrive", CALCULATE(SUM(TenantProductActivity[ActiveUserCount]),TenantProductActivity[ProductActivityCombo]="ODB - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="SharePoint", CALCULATE(SUM(TenantProductActivity[ActiveUserCount]),TenantProductActivity[ProductActivityCombo]="SPO - Any - Any"), IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Skype", CALCULATE(SUM(TenantProductActivity[ActiveUserCount]),TenantProductActivity[ProductActivityCombo]="SFB - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Teams", CALCULATE(SUM(TenantProductActivity[ActiveUserCount]),TenantProductActivity[ProductActivityCombo]="Teams - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Yammer", CALCULATE(SUM(TenantProductActivity[ActiveUserCount]),TenantProductActivity[ProductActivityCombo]="YAM - Any"),SUM(TenantProductActivity[ActiveUserCount]))))))))
```



```dax
Product Activity Display = IF(ISFILTERED(TenantProductActivity[ProductActivityCombo]), SUM(TenantProductActivity[ActivityCount]), IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Exchange", CALCULATE(SUM(TenantProductActivity[ActivityCount]),TenantProductActivity[ProductActivityCombo]="EXO - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="OneDrive", CALCULATE(SUM(TenantProductActivity[ActivityCount]),TenantProductActivity[ProductActivityCombo]="ODB - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="SharePoint", CALCULATE(SUM(TenantProductActivity[ActivityCount]),TenantProductActivity[ProductActivityCombo]="SPO - Any - Any"), IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Skype", CALCULATE(SUM(TenantProductActivity[ActivityCount]),TenantProductActivity[ProductActivityCombo]="SFB - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Teams", CALCULATE(SUM(TenantProductActivity[ActivityCount]),TenantProductActivity[ProductActivityCombo]="Teams - Any"),IF(FIRSTNONBLANK(TenantProductActivity[Product],0)="Yammer", CALCULATE(SUM(TenantProductActivity[ActivityCount]),TenantProductActivity[ProductActivityCombo]="YAM - Any"),SUM(TenantProductActivity[ActivityCount]))))))))
```



```dax
Emails Read Label = CONCATENATE( [ProdActivity_MostRecentDate], " - Emails Read")
```



```dax
Emails Sent Label = CONCATENATE( [ProdActivity_MostRecentDate], " - Emails Sent")
```



```dax
Total Messages Label = CONCATENATE( [ProdActivity_MostRecentDate], " - Teams Messages Posted")
```



```dax
Yammer msg Label = CONCATENATE( [ProdActivity_MostRecentDate], " - Yammer Messages Posted")
```



```dax
Active Users Label Com = CONCATENATE( [ProdActivity_MostRecentDate], " Active Users")
```



```dax
Avg Emails Label = CONCATENATE( [ProdActivity_MostRecentDate], " Avg Emails Sent")
```



```dax
Avg Emails read Label = CONCATENATE( [ProdActivity_MostRecentDate], " Avg Emails Read")
```



```dax
Avg Emails Rec Label = CONCATENATE( [ProdActivity_MostRecentDate], " Avg Emails Received")
```



```dax
Product Active User Display2 = IF(ISFILTERED(TenantProductActivity[SFB-CollaborationType]),SUM(TenantProductActivity[ActiveUserCount]), CALCULATE(SUM(TenantProductActivity[ActiveUserCount]), TenantProductActivity[SFB_CollabActivityCombo] = "Any") )
```


### Calculated Columns:


```dax
SPO-SiteType = TRIM(IF([Product]="SharePoint",PATHITEM(SUBSTITUTE(IF(SEARCH(" /",[Activity],1,0)>0,LEFT([Activity],SEARCH(" /",[Activity],1,0)),LEFT([Activity],SEARCH("/",[Activity],1,0))),"/","|"),1),BLANK()))
```



```dax
SFB-CollaborationType = IF([Product]="Skype",IF(SEARCH("Organizer/",[Activity],1,0)>0,"Conference Organizer",IF(SEARCH("Peer/Peer",[Activity],1,0)>0,"Peer-to-Peer",IF(SEARCH("Participant/",[Activity],1,0)>0,"Conference Participant",IF(SEARCH("Summary/Conference Organizer",[Activity],1,0)>0,"Skype - Conference Organizer",IF(SEARCH("Summary/Peer-to-Peer",[Activity],1,0)>0,"Skype - Peer-to-Peer",IF(SEARCH("Summary/Conference Participant",[Activity],1,0)>0,"Skype - Conference Participant",IF(SEARCH("/Any",[Activity],1,0)>0,"Skype - Any",BLANK()))))))))
```



```dax
TotalDurationinHours = IF([Product]="Skype",DIVIDE([TotalDurationInMinute],60,0))
```



```dax
TotalDurationinDays = IF([Product]="Skype",DIVIDE([TotalDurationinHours],24,0))
```



```dax
ActivitySubType = IF(SEARCH("Summary",TRIM([Activity]),1,0)>0,TRIM(REPLACE(TRIM([SFB-CollaborationType]),1,7,"")),IF(SEARCH("CloudDialOut",IF([Product]="Skype" && SEARCH("Message",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"IM",IF([Product]="Skype" && SEARCH("Web",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Web",TRIM(IF([Product]="Skype" && SEARCH("Participant",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,11,""),TRIM(IF([Product]="Skype" && SEARCH("Organizer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,9,""),TRIM(IF([Product]="Skype" && SEARCH("Organizer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,9,""),TRIM(IF([Product]="Skype" && NOT(SEARCH("Summary",[Activity],1,0)>0) && SEARCH("Peer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,4,""),IF([Product]="Yammer" && SEARCH("liked",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Liked",IF([Product]="Yammer" && SEARCH("message_created",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Posted", IF([Product]="Yammer" && SEARCH("message_viewed",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Read",IF([Product]="SharePoint" && SEARCH("Active Files",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0, "Files Viewed/Modified",IF([Product]="Exchange" && SEARCH("MarkAsRead",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Read",IF([Product]="Exchange" && SEARCH("MessageSent",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Sent",IF([Product]="Exchange" && SEARCH("MessageDelivered",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Received",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity])))))))))))))))))))),1,0)>0,"Dial-Out Cloud",IF(SEARCH("CloudDialIn",IF([Product]="Skype" && SEARCH("Message",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"IM",IF([Product]="Skype" && SEARCH("Web",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Web",TRIM(IF([Product]="Skype" && SEARCH("Participant",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,11,""),TRIM(IF([Product]="Skype" && SEARCH("Organizer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,9,""),TRIM(IF([Product]="Skype" && SEARCH("Organizer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,9,""),TRIM(IF([Product]="Skype" && NOT(SEARCH("Summary",[Activity],1,0)>0) && SEARCH("Peer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,4,""),IF([Product]="Yammer" && SEARCH("liked",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Liked",IF([Product]="Yammer" && SEARCH("message_created",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Posted", IF([Product]="Yammer" && SEARCH("message_viewed",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Read",IF([Product]="SharePoint" && SEARCH("Active Files",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0, "Files Viewed/Modified",IF([Product]="Exchange" && SEARCH("MarkAsRead",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Read",IF([Product]="Exchange" && SEARCH("MessageSent",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Sent",IF([Product]="Exchange" && SEARCH("MessageDelivered",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Delivered",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity])))))))))))))))))))),1,0)>0,"Dial-In Cloud",IF([Product]="Skype" && SEARCH("Message",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"IM",IF([Product]="Skype" && SEARCH("Web",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Web",TRIM(IF([Product]="Skype" && SEARCH("Participant",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,11,""),TRIM(IF([Product]="Skype" && SEARCH("Organizer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,9,""),TRIM(IF([Product]="Skype" && SEARCH("Organizer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,9,""),TRIM(IF([Product]="Skype" && NOT(SEARCH("Summary",[Activity],1,0)>0) && SEARCH("Peer",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,REPLACE(TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,4,""),IF([Product]="Yammer" && SEARCH("liked",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Liked",IF([Product]="Yammer" && SEARCH("message_created",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Posted", IF([Product]="Yammer" && SEARCH("message_viewed",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Message Read",IF([Product]="SharePoint" && SEARCH("Active Files",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0, "Files Viewed/Modified",IF([Product]="Exchange" && SEARCH("MarkAsRead",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Read",IF([Product]="Exchange" && SEARCH("MessageSent",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Sent",IF([Product]="Exchange" && SEARCH("MessageDelivered",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0,"Email Received",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),IF([Product]="OneDrive" && SEARCH("Active Files",TRIM(IF(NOT(SEARCH("/",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity],"/","|"),2),IF(NOT(SEARCH(" /",[Activity],1,0)=0),PATHITEM(SUBSTITUTE([Activity]," /","|"),2),[Activity]))),1,0)>0, "Files Viewed/Modified",[Activity]))))))))))))))))))))))))
```



```dax
SFB_CollabActivityCombo = IF(IF(SEARCH("Skype",IF([Product]="Skype",[SFB-CollaborationType] & " - " &[ActivitySubType],BLANK()),1,0)>0,[ActivitySubType],IF([Product]="Skype",[SFB-CollaborationType] & " - " &[ActivitySubType],IF(ISBLANK([SFB-CollaborationType]),[ActivitySubType],BLANK())))=" - Any","Any", IF(SEARCH("Skype",IF([Product]="Skype",[SFB-CollaborationType] & " - " &[ActivitySubType],BLANK()),1,0)>0,[ActivitySubType],IF([Product]="Skype",[SFB-CollaborationType] & " - " &[ActivitySubType], IF(ISBLANK([SFB-CollaborationType]),[ActivitySubType],BLANK()))))
```



```dax
ProductActivityCombo = IF([Product]="SharePoint","SPO" & " - " &[SPO-SiteType] & " - " & [ActivitySubType],IF([Product]="Skype" && NOT(SEARCH("Skype",[SFB-CollaborationType],1,0)>0),"SFB" & " - " &[SFB-CollaborationType] & " - " & [ActivitySubType],IF([Product]="Skype" && SEARCH("Skype",[SFB-CollaborationType],1,0)>0,"SFB" & " - " &[ActivitySubType],IF([Product]="OneDrive","ODB" & " - " &[ActivitySubType],IF([Product]="Exchange","EXO" & " - " &[ActivitySubType],IF([Product]="Yammer","YAM" & " - " &[ActivitySubType],[Product] & " - " &[ActivitySubType]))))))
```



```dax
HierarchyCategory = IF([Product]="Skype" && [SFB-CollaborationType]="Conference Organizer" , "Conference Organizer",IF([Product]="Skype" && [SFB-CollaborationType]="Conference Participant" , "Conference Participant",IF([Product]="Skype" && [SFB-CollaborationType]="Peer-to-Peer" , "Peer-to-Peer",IF([Product]="SharePoint",[SPO-SiteType],IF([Product]="Exchange","Email",IF([Product]="Yammer","Message",IF([Product]="OneDrive","File",IF([Product]="Teams", "Teams", "Summary"))))))))
```



```dax
HierarchySubCategory = IF([Product]="Skype" && [SFB-CollaborationType]="Conference Organizer" , [ActivitySubType],IF([Product]="Skype" && [SFB-CollaborationType]="Conference Participant" , [ActivitySubType],IF([Product]="Skype" && [SFB-CollaborationType]="Peer-to-Peer" , [ActivitySubType],
    IF([Product]="SharePoint",[ActivitySubType],IF([Product]="Exchange" && NOT([ActivitySubType]="Any"),TRIM(REPLACE([ActivitySubType],1,5,BLANK())),IF([Product]="Yammer" && NOT([ActivitySubType]="Any"),TRIM(REPLACE([ActivitySubType],1,7,BLANK())),IF([Product]="OneDrive" && NOT([ActivitySubType]="Any"),TRIM(REPLACE([ActivitySubType],1,5,BLANK())),IF([HierarchyCategory]="Summary","Any",
        IF([Product]="Exchange" && [ActivitySubType]="Any","Any",IF([Product]="Yammer" && [ActivitySubType]="Any","Any",IF([Product]="OneDrive" && [ActivitySubType]="Any","Any", [ActivitySubType])))))))))))
```



```dax
IsLastMonth = IF([TimeFrame]=MAX([TimeFrame]),TRUE(),FALSE())
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EndofMonth],[ContentDate] > [EndofMonth]),TRUE(),FALSE())
```



```dax
SPO_ActivityCombo = IF([Product]="SharePoint", IF([ActivitySubType]="Any", [ActivitySubType], [SPO-SiteType] & " - " & [ActivitySubType]), "")
```


## Table: TenantProductUsage

### Measures:


```dax
ActiveUsers(%) = CALCULATE(DIVIDE(SUM([Active Users]),SUM([Enabled Users]),0))
```



```dax
ReturningUsers(%) = CALCULATE(DIVIDE(SUM([MoMReturningUsers]),[PrvMonthActiveUsers]))
```



```dax
PrvMonthActiveUsers = CALCULATE([TotalActiveUsers],PREVIOUSMONTH('Calendar'[Date]))
```



```dax
MoMActiveUsers = CALCULATE(SUM([Active Users])-[PrvMonthActiveUsers])
```



```dax
MoMActiveUsersVariance(%) = DIVIDE([MoMActiveUsers],[PrvMonthActiveUsers],0)
```



```dax
TotalActiveUsers = CALCULATE(SUM([Active Users]))
```



```dax
MostRecent-ReturningUsers = CALCULATE(SUM([MoMReturningUsers]),LASTDATE('TenantProductUsage'[TimeFrame]))
```



```dax
ProdUsage_MostRecentDate = FORMAT(LASTDATE('TenantProductUsage'[TimeFrame]),"mmmm")& " " & FORMAT(LASTDATE('TenantProductUsage'[TimeFrame]),"YYYY")
```



```dax
MoMReturningUsers(%) = DIVIDE(SUM([MoMReturningUsers]),[PrvMonthActiveUsers],0)
```



```dax
MostRecent-ActiveUsers = CALCULATE(SUM([Active Users]),LASTDATE('TenantProductUsage'[TimeFrame]))
```



```dax
MostRecent-LicensedUsers = CALCULATE(SUM([Enabled Users]),LASTDATE('TenantProductUsage'[TimeFrame]))
```



```dax
MostRecent-ActiveUsers(%) = CALCULATE(DIVIDE(SUM([Active Users]),SUM([Enabled Users]),0),LASTDATE('TenantProductUsage'[TimeFrame]))
```



```dax
AdoptionProductTitle = VAR SelectedProduct = VALUES('TenantProductUsage'[Product])
var NumofSelectedProducts =COUNTROWS(SelectedProduct)
VAR NumofPossibleProducts = COUNTROWS(ALL('TenantProductUsage'[Product]))
VAR AllbutLastSelectedProduct = TOPN(NumofSelectedProducts-1,SelectedProduct)
VAR	LastSelectedProduct = EXCEPT(SelectedProduct,AllbutLastSelectedProduct)
RETURN
"Adoption overview"
& IF(NumofSelectedProducts=NumofPossibleProducts,
	":All Products",
	": "
	& IF(NumofSelectedProducts=1,
		"",
		CONCATENATEX(AllbutLastSelectedProduct,'TenantProductUsage'[Product],", ")
		& " And "
	)
	&LastSelectedProduct
)
```



```dax
MostRecent-ReturningUsers(%) = DIVIDE(CALCULATE(SUM([MoMReturningUsers]),LASTDATE('TenantProductUsage'[TimeFrame])),[MostRecent-PrvMonthActiveUsers],0)
```



```dax
MostRecent-PrvMonthActiveUsers = CALCULATE(SUM([Active Users]),DATEADD(LASTDATE('TenantProductUsage'[TimeFrame]),-1,MONTH))
```



```dax
TEST = CALCULATE(SUM(TenantProductUsage[Active Users]), ALL('Calendar'))
```



```dax
Most Recent Active User % = IF(ISFILTERED('TenantProductUsage'[Product]),[MostRecent-ActiveUsers(%)], CALCULATE([MostRecent-ActiveUsers(%)], 'TenantProductUsage'[Product]="Office365"))
```



```dax
Active Users of Enabled = CONCATENATE(FORMAT([Most Recent Active User Count Display],"#,#"),CONCATENATE(" of ",FORMAT([Most Recent Enabled User Count Display],"#,#")))
```



```dax
MostRecent-EnabledUser = CALCULATE(SUM([Enabled Users]),LASTDATE('TenantProductUsage'[TimeFrame]))
```



```dax
Active User % Label = CONCATENATE( [ProdUsage_MostRecentDate], " Active User %")
```



```dax
Active Users Label = CONCATENATE( [ProdUsage_MostRecentDate], " Active and Enabled Users")
```



```dax
Returning Users % Label = CONCATENATE( [ProdUsage_MostRecentDate], " Returning User %")
```



```dax
First Time Users = IF(ISFILTERED('TenantProductUsage'[Product]),SUM([FirstTimeUsers] ), CALCULATE(SUM([FirstTimeUsers]), 'TenantProductUsage'[Product]="Office365"))
```



```dax
Most Recent Active User Count Display = IF(ISFILTERED('TenantProductUsage'[Product]),[MostRecent-ActiveUsers], CALCULATE([MostRecent-ActiveUsers], 'TenantProductUsage'[Product]="Office365"))
```



```dax
Most Recent Enabled User Count Display = IF(ISFILTERED('TenantProductUsage'[Product]),[MostRecent-EnabledUser], CALCULATE([MostRecent-EnabledUser], 'TenantProductUsage'[Product]="Office365"))
```



```dax
Most Recent Returning User Display = DIVIDE(
    CALCULATE(SUM([MoMReturningUsers]),LASTDATE('TenantProductUsage'[TimeFrame])),
    CALCULATE(SUM([Active Users]), ALL('Calendar'[Year]), ALL('Calendar'[MonthName]),DATEADD(LASTDATE('TenantProductUsage'[TimeFrame]),-1,MONTH)), 
    0)
```



```dax
Active User %  Display = IF(ISFILTERED('TenantProductUsage'[Product]),[ActiveUsers(%)], CALCULATE([ActiveUsers(%)], 'TenantProductUsage'[Product]="Office365"))
```



```dax
MoM Returning User %  Display = IF(ISFILTERED('TenantProductUsage'[Product]),[MoMReturningUsers(%)], CALCULATE([MoMReturningUsers(%)], 'TenantProductUsage'[Product]="Office365"))
```



```dax
Active Users Label2 = CONCATENATE( [ProdUsage_MostRecentDate], " Active Users")
```


### Calculated Columns:


```dax
LastMonth = MAX('TenantProductUsage'[TimeFrame])
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EndofMonth],[ContentDate] > [EndofMonth]),TRUE(),FALSE())
```



```dax
DateChecker = DATEADD('TenantProductUsage'[EndofMonth].[Date],3,DAY)
```


## Table: UserActivity

### Measures:


```dax
EXO_AvgEmailSent = CALCULATE(AVERAGE([EXO_EmailSent]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_AvgEmailRead = CALCULATE(AVERAGE([EXO_EmailRead]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM_AvgMessageRead = CALCULATE(AVERAGE([YAM_MessageRead]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM_AvgMessagePosted = CALCULATE(AVERAGE([YAM_MessagePost]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalEmailRead = CALCULATE(SUM([EXO_EmailRead]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalEmailSent = CALCULATE(SUM([EXO_EmailSent]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SFB_TotalConferenceOrganizerSummary = CALCULATE(SUM([SFB_ConfOrgSummary]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SFB_TotalPeertoPeerSummary = CALCULATE(SUM([SFB_P2PSummary]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM_TotalMessageRead = CALCULATE(SUM([YAM_MessageRead]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM_TotalMessageLiked = CALCULATE(SUM([YAM_MessageLiked]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM_TotalMessagePost = CALCULATE(SUM([YAM_MessagePost]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
ODB_CollaboratedByOthers = CALCULATE(SUM([ODB_AccessedByOthers]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
ODB_CollaboratedByOwner = CALCULATE(SUM([ODB_AccessedByOwner]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
ODB_TotalFileSharedEXT = CALCULATE(SUM([ODB_FileSharedExternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
ODB_TotalFileSharedINT = CALCULATE(SUM([ODB_FileSharedInternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalTeamAccessedbyOthers = CALCULATE(SUM([SPO_TeamAccessedByOthers]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalTeamAccessedbyOwner = CALCULATE(SUM([SPO_TeamAccessedByOwner]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalGrpAccessedbyOthers = CALCULATE(SUM([SPO_GroupAccessedByOthers]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalGrpAccessedbyOwner = CALCULATE(SUM([SPO_GroupAccessedByOwner]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalGrpFileSharedEXT = CALCULATE(SUM([SPO_GroupFileSharedExternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalGrpFileSharedINT = CALCULATE(SUM([SPO_GroupFileSharedInternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalTeamFileSharedINT = CALCULATE(SUM([SPO_TeamFileSharedInternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalTeamFileSharedEXT = CALCULATE(SUM([SPO_TeamFileSharedExternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
ODB_TotalFileSynched = CALCULATE(SUM([ODB_FileSynched]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
ODB_TotalFileViewed/Modified = CALCULATE(SUM([ODB_FileViewedModified]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalEmailReceived = CALCULATE(SUM([EXO_EmailReceived]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SFB_TotalConferenceParticipantSummary = CALCULATE(SUM([SFB_ConfPartSummary]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalGrpFileSynched = CALCULATE(SUM([SPO_GroupFileSynched]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalGrpFileViewed/Modified = CALCULATE(SUM([SPO_GroupFileViewedModified]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalTeamFileSynched = CALCULATE(SUM([SPO_TeamFileSynched]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalTeamFileViewed/Modified = CALCULATE(SUM([SPO_TeamFileViewedModified]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalofAllActivities = [EXO_TotalEmailRead]+[EXO_TotalEmailSent]+[EXO_TotalEmailReceived]+[EXO_TotalMeetingSent]+[EXO_TotalMeetingCancelled]+[EXO_TotalMeetingAccepted]+[EXO_TotalMeetingDeclined]+[EXO_TotalAppointmentCreated]
```



```dax
EXO_RankofUserActivities = IF(NOT(ISBLANK([EXO_TotalofAllActivities])),RANKX(ALL('UserActivity'[UserId]),[EXO_TotalofAllActivities],,DESC),BLANK())
```



```dax
EXO_RankofDeptActivities = IF(NOT(ISBLANK([EXO_TotalofAllActivities])),RANKX(ALL('UserState'[Department]),[EXO_TotalofAllActivities],,DESC),BLANK())
```



```dax
ODB_TotalofAllActivities = [ODB_TotalFileSharedEXT]+[ODB_TotalFileSharedINT]+[ODB_TotalFileSynched]+[ODB_TotalFileViewed/Modified]
```



```dax
ODB_RankofUserActivities = IF(NOT(ISBLANK([ODB_TotalofAllActivities])),RANKX(ALL('UserActivity'[UserId]),[ODB_TotalofAllActivities],,DESC),BLANK())
```



```dax
ODB_RankofDeptActivities = IF(NOT(ISBLANK([ODB_TotalofAllActivities])),RANKX(ALL('UserState'[Department]),[ODB_TotalofAllActivities],,DESC),BLANK())
```



```dax
SFB_TotalofAllActivities = [SFB_TotalConferenceOrganizerSummary]+[SFB_TotalConferenceParticipantSummary]+[SFB_TotalPeertoPeerSummary]
```



```dax
YAM_TotalofAllActivities = [YAM_TotalMessageLiked]+[YAM_TotalMessagePost]+[YAM_TotalMessageRead]
```



```dax
HasEXOActivity_Count = IF(CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasEXOActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasEXOActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))))
```



```dax
HasODBActivity_Count = IF(CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasODBActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasODBActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))))
```



```dax
HasSFBActivity_Count = IF(CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasSFBActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasSFBActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))))
```



```dax
HasSPOActivity_Count = IF(CALCULATE(COUNTX(FILTER('UserActivity',OR(OR('UserActivity'[HasSPOGrpActivity]=TRUE(),'UserActivity'[HasSPOTeamActivity]=TRUE()),'UserActivity'[HasSPOOtherActivity]=TRUE()) && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserActivity',OR(OR('UserActivity'[HasSPOGrpActivity]=TRUE(),'UserActivity'[HasSPOTeamActivity]=TRUE()),'UserActivity'[HasSPOOtherActivity]=TRUE()) && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))))
```



```dax
HasYAMActivity_Count = IF(CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasYAMActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasYAMActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))))
```



```dax
SPO_TotalofallActivities(Grp) = [SPO_TotalGrpFileSharedEXT]+[SPO_TotalGrpFileSharedINT]+[SPO_TotalGrpFileSynched]+[SPO_TotalGrpFileViewed/Modified]
```



```dax
SPO_TotalofallActivities(Team) = [SPO_TotalTeamFileSharedEXT]+[SPO_TotalTeamFileSharedINT]+[SPO_TotalTeamFileSynched]+[SPO_TotalTeamFileViewed/Modified]
```



```dax
SPO_RankofDeptActivities(Grp) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Grp)])),RANKX(ALL('UserState'[Department]),[SPO_TotalofallActivities(Grp)],,DESC),BLANK())
```



```dax
SPO_RankofDeptActivities(Team) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Team)])),RANKX(ALL('UserState'[Department]),[SPO_TotalofallActivities(Team)],,DESC),BLANK())
```



```dax
SPO_RankofUserActivities(Grp) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Grp)])),RANKX(ALL('UserActivity'[UserId]),[SPO_TotalofallActivities(Grp)],,DESC),BLANK())
```



```dax
SPO_RankofUserActivities(Team) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Team)])),RANKX(ALL('UserActivity'[UserId]),[SPO_TotalofallActivities(Team)],,DESC),BLANK())
```



```dax
SFB_RankofDeptActivities = IF(NOT(ISBLANK([SFB_TotalofAllActivities])),RANKX(ALL('UserState'[Department]),[SFB_TotalofAllActivities],,DESC),BLANK())
```



```dax
SFB_RankofUserActivities = IF(NOT(ISBLANK([SFB_TotalofAllActivities])),RANKX(ALL('UserActivity'[UserId]),[SFB_TotalofAllActivities],,DESC),BLANK())
```



```dax
SFB_AvgP2PSummarySession = CALCULATE(AVERAGE([SFB_P2PSummary]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SFB_AvgConfOrgSumSession = CALCULATE(AVERAGE([SFB_ConfOrgSummary]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_AvgEmailReceived = CALCULATE(AVERAGE([EXO_EmailReceived]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SFB_AvgConfOrgPartSession = CALCULATE(AVERAGE([SFB_ConfPartSummary]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM_AvgMessageLiked = CALCULATE(AVERAGE([YAM_MessageLiked]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SFB_RankofCompActivities = IF(NOT(ISBLANK([SFB_TotalofAllActivities])),RANKX(ALL('UserState'[Company]),[SFB_TotalofAllActivities],,DESC),BLANK())
```



```dax
ODB_RankofCompActivities = IF(NOT(ISBLANK([ODB_TotalofAllActivities])),RANKX(ALL('UserState'[Company]),[ODB_TotalofAllActivities],,DESC),BLANK())
```



```dax
SPO_RankofCompActivities(Team) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Team)])),RANKX(ALL('UserState'[Company]),[SPO_TotalofallActivities(Team)],,DESC),BLANK())
```



```dax
SPO_RankofCompActivities(Grp) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Grp)])),RANKX(ALL('UserState'[Company]),[SPO_TotalofallActivities(Grp)],,DESC),BLANK())
```



```dax
YAM_RankofDeptActivities = IF(NOT(ISBLANK([YAM_TotalofAllActivities])),RANKX(ALL('UserState'[Department]),[YAM_TotalofAllActivities],,DESC),BLANK())
```



```dax
YAM_RankofCompActivities = IF(NOT(ISBLANK([YAM_TotalofAllActivities])),RANKX(ALL('UserState'[Company]),[YAM_TotalofAllActivities],,DESC),BLANK())
```



```dax
YAM_RankofUserActivities = IF(NOT(ISBLANK([YAM_TotalofAllActivities])),RANKX(ALL('UserActivity'[UserId]),[YAM_TotalofAllActivities],,DESC),BLANK())
```



```dax
EXO_RankofCompActivities = IF(NOT(ISBLANK([EXO_TotalofAllActivities])),RANKX(ALL('UserState'[Company]),[EXO_TotalofAllActivities],,DESC),BLANK())
```



```dax
SPO_TotalAccessedbyOwner = [SPO_TotalGrpAccessedbyOwner]+[SPO_TotalTeamAccessedbyOwner]+[SPO_TotalOtherAccessedbyOwner]
```



```dax
SPO_TotalAccessedbyOther = [SPO_TotalGrpAccessedbyOthers]+[SPO_TotalTeamAccessedbyOthers]+[SPO_TotalOtherAccessedbyOthers]
```



```dax
SPO_TotalFilesSharedEXT = [SPO_TotalGrpFileSharedEXT]+[SPO_TotalTeamFileSharedEXT]+[SPO_TotalOtherFileSharedEXT]
```



```dax
SPO_TotalFilesSharedINT = [SPO_TotalGrpFileSharedINT]+[SPO_TotalTeamFileSharedINT]+[SPO_TotalOtherFileSharedINT]
```



```dax
SPO_TotalFilesSynched = [SPO_TotalGrpFileSynched]+[SPO_TotalTeamFileSynched]+[SPO_TotalOtherFileSynched]
```



```dax
SPO_TotalFilesViewed/Modified = [SPO_TotalGrpFileViewed/Modified]+[SPO_TotalTeamFileViewed/Modified]+[SPO_TotalOtherFileViewed/Modified]
```



```dax
SPO_TotalofAllActivities = [SPO_TotalofallActivities(Grp)]+[SPO_TotalofallActivities(Team)]+[SPO_TotalofallActivities(Other)]
```



```dax
ActivatedYammerUsers = CALCULATE(DISTINCTCOUNT([UserId]),'UserActivity'[IsYammerActivated]="Active")
```



```dax
YammerActiveRate(%) = DIVIDE([ActivatedYammerUsers],[EnabledYammerUsers],0)
```



```dax
EnabledYammerUsers = CALCULATE(DISTINCTCOUNT([UserId]),'UserActivity'[HasYammerLicense]=TRUE(),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
YAM-Active(%)ofActivated = CALCULATE(DIVIDE([HasYAMActivity_Count],[ActivatedYammerUsers]))
```



```dax
YAM-Activated(%)ofEnabled = CALCULATE(DIVIDE([ActivatedYammerUsers],[EnabledYammerUsers]))
```



```dax
AllProductActivityCount = [HasEXOActivity_Count]+[HasODBActivity_Count]+[HasSFBActivity_Count]+[HasSPOActivity_Count]+[HasYAMActivity_Count]
```



```dax
ALL_RankofProductActivityperDEPT = IF(NOT(ISBLANK([AllProductActivityCount])),RANKX(ALL('UserState'[Department]),[AllProductActivityCount],,DESC),BLANK())
```



```dax
SelectedTopNValue = IF(HASONEVALUE('TopN'[TopN]),VALUES('TopN'[TopNValues]),BLANK())
```



```dax
TopN-AllProductActivityCnt = IF([ALL_RankofProductActivityperDEPT]<=[SelectedTopNValue],[AllProductActivityCount],BLANK())
```



```dax
EXO_TotalMeetingSent = CALCULATE(SUM([EXO_MeetingSent]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalMeetingCancelled = CALCULATE(SUM([EXO_MeetingCancelled]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalMeetingAccepted = CALCULATE(SUM([EXO_MeetingAccepted]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalMeetingDeclined = CALCULATE(SUM([EXO_MeetingDeclined]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
EXO_TotalAppointmentCreated = CALCULATE(SUM([EXO_AppointmentCreated]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
HasTEAMSActivity_Count = IF(CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasTEAMSActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserActivity','UserActivity'[HasTEAMSActivity]=TRUE() && 'UserActivity'[IsUserDeleted]=FALSE()),COUNTA(UserActivity[UserId]))))
```



```dax
TEAMS_AvgCallParticipate = CALCULATE(AVERAGE([Teams_CallParticipate]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_AvgChannelMessage = CALCULATE(AVERAGE([Teams_ChannelMessage]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_AvgChatMessage = CALCULATE(AVERAGE([Teams_ChatMessage]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_AvgMeetingParticipate = CALCULATE(AVERAGE([Teams_MeetingParticipate]),LASTDATE('UserActivity'[TimeFrame]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_TotalCallParticipate = CALCULATE(SUM([Teams_CallParticipate]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_TotalChannelMessage = CALCULATE(SUM([Teams_ChannelMessage]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_TotalChatMessage = CALCULATE(SUM([Teams_ChatMessage]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_TotalMeetingParticipate = CALCULATE(SUM([Teams_MeetingParticipate]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
TEAMS_TotalofAllActivities = [TEAMS_TotalChannelMessage]+[TEAMS_TotalChatMessage]+[TEAMS_TotalCallParticipate]+[TEAMS_TotalMeetingParticipate]
```



```dax
TEAMS_RankofCompActivities = IF(NOT(ISBLANK([TEAMS_TotalofAllActivities])),RANKX(ALL('UserState'[Company]),[TEAMS_TotalofAllActivities],,DESC),BLANK())
```



```dax
TEAMS_RankofDeptActivities = IF(NOT(ISBLANK([TEAMS_TotalofAllActivities])),RANKX(ALL('UserState'[Department]),[TEAMS_TotalofAllActivities],,DESC),BLANK())
```



```dax
TEAMS_RankofUserActivities = IF(NOT(ISBLANK([TEAMS_TotalofAllActivities])),RANKX(ALL('UserActivity'[UserId]),[TEAMS_TotalofAllActivities],,DESC),BLANK())
```



```dax
SPO_TotalOtherAccessedbyOthers = CALCULATE(SUM([SPO_OtherAccessedByOthers]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalOtherAccessedbyOwner = CALCULATE(SUM([SPO_OtherAccessedByOwner]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalOtherFileSharedEXT = CALCULATE(SUM([SPO_OtherFileSharedExternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalOtherFileSharedINT = CALCULATE(SUM([SPO_OtherFileSharedInternally]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalOtherFileSynched = CALCULATE(SUM([SPO_OtherFileSynched]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalOtherFileViewed/Modified = CALCULATE(SUM([SPO_OtherFileViewedModified]),USERELATIONSHIP('UserActivity'[TimeFrame],'Calendar'[Date]),'UserActivity'[IsUserDeleted]=FALSE())
```



```dax
SPO_TotalofallActivities(Other) = [SPO_TotalOtherFileSharedEXT]+[SPO_TotalOtherFileSharedINT]+[SPO_TotalOtherFileSynched]+[SPO_TotalOtherFileViewed/Modified]
```



```dax
SPO_RankofCompActivities(Other) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Other)])),RANKX(ALL('UserState'[Company]),[SPO_TotalofallActivities(Other)],,DESC),BLANK())
```



```dax
SPO_RankofDeptActivities(Other) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Other)])),RANKX(ALL('UserState'[Department]),[SPO_TotalofallActivities(Other)],,DESC),BLANK())
```



```dax
SPO_RankofUserActivities(Other) = IF(NOT(ISBLANK([SPO_TotalofallActivities(Other)])),RANKX(ALL('UserActivity'[UserId]),[SPO_TotalofallActivities(Other)],,DESC),BLANK())
```



```dax
SPO_RankofCompActivities = IF(NOT(ISBLANK([SPO_TotalofallActivities])),RANKX(ALL('UserState'[Company]),[SPO_TotalofallActivities],,DESC),BLANK())
```



```dax
SPO_RankofDeptActivities = IF(NOT(ISBLANK([SPO_TotalofallActivities])),RANKX(ALL('UserState'[Department]),[SPO_TotalofallActivities],,DESC),BLANK())
```



```dax
SPO_RankofUserActivities = IF(NOT(ISBLANK([SPO_TotalofallActivities])),RANKX(ALL('UserActivity'[UserId]),[SPO_TotalofallActivities],,DESC),BLANK())
```


### Calculated Columns:


```dax
IsUserDeleted = CALCULATE(LASTNONBLANK('UserState'[Deleted],TRUE()))
```



```dax
HasEXOActivity = if (OR([EXO_EmailRead]>0,[EXO_EmailSent]>0),TRUE(),FALSE())
```



```dax
HasODBActivity = if (OR([ODB_FileSharedExternally]>0,OR([ODB_FileSharedExternally]>0,OR([ODB_FileSynched]>0,[ODB_FileViewedModified]>0))),TRUE(),FALSE())
```



```dax
HasSFBActivity = if (OR([SFB_ConfOrgSummary]>0,OR([SFB_ConfPartSummary]>0,[SFB_P2PSummary]>0)),TRUE(),FALSE())
```



```dax
HasSPOGrpActivity = if (OR([SPO_GroupFileSharedExternally]>0,OR([SPO_GroupFileSharedInternally]>0,OR([SPO_GroupFileSynched]>0,[SPO_GroupFileViewedModified]> 0))),TRUE(),FALSE())
```



```dax
HasYAMActivity = if (OR([YAM_MessageLiked]>0,OR([YAM_MessagePost]>0,[YAM_MessageRead]>0)),TRUE(),FALSE())
```



```dax
ProductActivity = IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/SPO/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/SPO/SFB/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/SPO/SFB/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/SPO/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/SPO/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/SPO/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/SPO/SFB"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/SPO/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/SPO/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/SFB/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/SFB/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/SPO/SFB/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/SPO/SFB/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/SPO/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with ODB/SPO/SFB/TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/SPO/SFB/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/SPO/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with SPO/SFB/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/SPO"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/SFB"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/ODB/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/ODB/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/SPO/SFB"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/SPO/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/SPO/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with EXO/SFB/TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/SFB/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with EXO/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"Active users with ODB/SPO/SFB"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with ODB/SPO/TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/SPO/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with ODB/SFB/TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/SFB/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with ODB/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"Active users with SPO/SFB/TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"Active users with SPO/SFB/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with SPO/TEAM/YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"Active users with SFB/TEAM/YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in EXO & ODB"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in EXO & SPO"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in EXO & SFB"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"User Active only in EXO & TEAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"User Active only in EXO & YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in ODB & SPO"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in ODB & SFB"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"User Active only in ODB & TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"User Active only in ODB & YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in SPO & SFB"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"User Active only in SPO & TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"User Active only in SPO & YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"User Active only in SFB & TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"User Active only in SFB & YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=TRUE(),
"User Active only in TEAM & YAM"
,
IF([HasEXOActivity]=TRUE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in EXO"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=TRUE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in ODB"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=TRUE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in SPO"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=TRUE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User Active only in SFB"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=TRUE() && [HasYAMActivity]=FALSE(),
"User Active only in TEAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=TRUE(),
"User Active only in YAM"
,
IF([HasEXOActivity]=FALSE() && [HasODBActivity]=FALSE() && [HasSPOActivity]=FALSE() && [HasSFBActivity]=FALSE() && [HasTEAMSActivity]=FALSE() && [HasYAMActivity]=FALSE(),
"User inactive in all Office 365"
,
 "NA"
))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
```



```dax
UserActivity_MostRecentDate = FORMAT([TimeFrame],"MMMM")& " " & FORMAT([TimeFrame],"YYYY")
```



```dax
YAM_ActivatedDate = RELATED('UserState'[YAM_ActivationDate])
```



```dax
IsYammerActivated = RELATED('UserState'[YAM_State])
```



```dax
HasYammerLicense = RELATED('UserState'[HasLicenseYAM])
```



```dax
HasSPOTeamActivity = if (OR([SPO_TeamFileSharedExternally]>0,OR([SPO_TeamFileSharedInternally]>0,OR([SPO_TeamFileSynched]>0,[SPO_TeamFileViewedModified]> 0))),TRUE(),FALSE())
```



```dax
HasTEAMSActivity = IF(OR([Teams_ChannelMessage]>0,OR([Teams_ChatMessage]>0,OR([Teams_CallParticipate]>0,[Teams_MeetingParticipate]>0))),TRUE(),FALSE())
```



```dax
HasSPOOtherActivity = if (OR([SPO_OtherFileSharedExternally]>0,OR([SPO_OtherFileSharedInternally]>0,OR([SPO_OtherFileSynched]>0,[SPO_OtherFileViewedModified]> 0))),TRUE(),FALSE())
```



```dax
HasSPOActivity = IF(OR(OR(UserActivity[HasSPOGrpActivity], UserActivity[HasSPOTeamActivity]), UserActivity[HasSPOOtherActivity]), TRUE(), FALSE())
```


## Table: UserState

### Measures:


```dax
HasEXOLicense_Count = IF(CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseEXO]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseEXO]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))))
```



```dax
HasODBLicense_Count = IF(CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseODB]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseODB]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))))
```



```dax
HasSPOLicense_Count = IF(CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseSPO]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseSPO]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))))
```



```dax
HasSFBLicense_Count = IF(CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseSFB]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseSFB]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))))
```



```dax
HasYAMLicense_Count = IF(CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseYAM]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseYAM]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))))
```



```dax
TotalUserCount = IF(CALCULATE(DISTINCTCOUNT([UserId]),'UserState'[Deleted]=FALSE()) = BLANK(), 0, CALCULATE(DISTINCTCOUNT([UserId]),'UserState'[Deleted]=FALSE()))
```



```dax
HasTEAMSLicense_Count = IF(CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseTeams]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))) = BLANK(), 0, CALCULATE(COUNTX(FILTER('UserState','UserState'[HasLicenseTeams]=TRUE() && 'UserState'[Deleted]=FALSE()),COUNTA(UserState[UserId]))))
```


### Calculated Columns:


```dax
ProductLicense = IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/SPO/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/SPO/SFB/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/SPO/SFB/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/SPO/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/SPO/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/SPO/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/SPO/SFB"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/SPO/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/SPO/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/SFB/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/SFB/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/SPO/SFB/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/SPO/SFB/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/SPO/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with ODB/SPO/SFB/TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/SPO/SFB/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/SPO/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with SPO/SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/SPO"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/SFB"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/ODB/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/ODB/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/SPO/SFB"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/SPO/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/SPO/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with EXO/SFB/TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/SFB/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with EXO/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"License users with ODB/SPO/SFB"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with ODB/SPO/TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/SPO/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with ODB/SFB/TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/SFB/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with ODB/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"License users with SPO/SFB/TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"License users with SPO/SFB/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with SPO/TEAM/YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"License users with SFB/TEAM/YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in EXO & ODB"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in EXO & SPO"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in EXO & SFB"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"User Active only in EXO & TEAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"User Active only in EXO & YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in ODB & SPO"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in ODB & SFB"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"User Active only in ODB & TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"User Active only in ODB & YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in SPO & SFB"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"User Active only in SPO & TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"User Active only in SPO & YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"User Active only in SFB & TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"User Active only in SFB & YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=TRUE(),
"User Active only in TEAM & YAM"
,
IF([HasLicenseEXO]=TRUE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in EXO"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=TRUE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in ODB"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=TRUE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in SPO"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=TRUE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User Active only in SFB"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=TRUE() && [HasLicenseYAM]=FALSE(),
"User Active only in TEAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=TRUE(),
"User Active only in YAM"
,
IF([HasLicenseEXO]=FALSE() && [HasLicenseODB]=FALSE() && [HasLicenseSPO]=FALSE() && [HasLicenseSFB]=FALSE() && [HasLicenseTeams]=FALSE() && [HasLicenseYAM]=FALSE(),
"User inactive in all 0365"
,
 "NA"
))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
```


## Table: Calendar


```dax
CALENDAR(DATE(2016,1,1),DATE(2025,12,31))
```


### Calculated Columns:


```dax
DayOfWeek = FORMAT([Date],"dddd")
```



```dax
DayOfWeekNo = IF(WEEKDAY([Date])=1,WEEKDAY([Date]) & "st",IF(WEEKDAY([Date])=2, WEEKDAY([Date]) & "nd",IF(WEEKDAY([Date])=3,WEEKDAY([Date])& "rd",IF(WEEKDAY([Date])> 3,WEEKDAY([Date])&"th",""))))
```



```dax
IsInCurrentYear = if(YEAR(NOW())= [Year],TRUE(),FALSE())
```



```dax
IsInPrevOrCurrentYear = IF(OR([IsInCurrentYear],[IsInPrevYear])=TRUE(),TRUE(),FALSE())
```



```dax
IsInPrevYear = 'Calendar'[Year]=(YEAR(NOW())-1)
```



```dax
MonthName = FORMAT([Date],"MMMM")
```



```dax
MonthNo = MONTH([Date])
```



```dax
Quarter = "Q" & FORMAT([Date],"Q")
```



```dax
Semester = IF([MonthNo] <=6," Semester 1","Semester 2")
```



```dax
Year = FORMAT([Date],"yyyy")
```



```dax
YearQuarter = FORMAT([Date],"YYYY")& "-"&"Q" & FORMAT([Date],"Q")
```


## Table: TenantOfficeLicenses

### Measures:


```dax
MostRecent-AssignedLicenses = CALCULATE(MAX(TenantOfficeLicenses[AssignedCount]), LASTDATE(TenantOfficeLicenses[TimeFrame]))
```



```dax
LicenseTitle = 
VAR SelectedLicense = VALUES( 'TenantOfficeLicenses'[LicenseName])
VAR NumberOfSelectedLicenses = COUNTROWS ( SelectedLicense)
VAR NumberOfPossibleLicenses = COUNTROWS ( ALL ( 'TenantOfficeLicenses'[LicenseName] ) ) - 1
VAR AllButLastSelectedLicense = TOPN ( NumberOfSelectedLicenses - 1, SelectedLicense )
VAR LastSelectedLicense = EXCEPT ( SelectedLicense, AllButLastSelectedLicense )
RETURN
    "Assigned subscription"
        & IF (
            NumberOfSelectedLicenses = NumberOfPossibleLicenses,
            ": all",
           ": "
                & IF (
                    NumberOfSelectedLicenses = 1,
                    "",
                    CONCATENATEX ( 
                       AllButLastSelectedLicense, 
                       'TenantOfficeLicenses'[LicenseName], 
                       ", " )
                        & " and "
                )
                & UPPER(LastSelectedLicense)
        )
```



```dax
OfficeLicense_MostRecentDate = FORMAT(LASTDATE('TenantOfficeLicenses'[TimeFrame]),"mmmm")& " " & FORMAT(LASTDATE('TenantOfficeLicenses'[TimeFrame]),"YYYY")
```



```dax
Assigned Label = CONCATENATE( [OfficeLicense_MostRecentDate], " Count of License Types")
```



```dax
Assigned User Label = CONCATENATE( [OfficeLicense_MostRecentDate], " Users with Assigned Licenses")
```


### Calculated Columns:


```dax
IsLastMonth = IF(MAX([TimeFrame])=[TimeFrame],TRUE(),FALSE())
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```


## Table: SPO-UserActivity

### Measures:


```dax
TotalActivityCount = CALCULATE(SUM([Count]))
```



```dax
SPO_RankofActivities(User) = RANKX(ALL('SPO-UserActivity'[UserId]),[TotalActivityCount],,DESC)
```



```dax
SPO_RankofActivities(Dept) = RANKX(ALL('SPO-UserActivity'[UserStateDept]),[TotalActivityCount],,DESC)
```



```dax
SPO_RankofActivities(Activity) = RANKX(ALL('SPO-UserActivity'[Activity]),[TotalActivityCount],,DESC)
```



```dax
SPO_RankofActivities(Comp) = RANKX(ALL('SPO-UserActivity'[UserStateCompany]),[TotalActivityCount],,DESC)
```


### Calculated Columns:


```dax
SPO-SiteType = IF(SEARCH("Group",[Activity],1,0)>0,"Group",IF(SEARCH("Team",[Activity],1,0)>0,"Team",BLANK()))
```



```dax
UserStateDept = RELATED(UserState[Department])
```



```dax
UserStateCompany = RELATED('UserState'[Company])
```



```dax
UserStateDisplayName = RELATED('UserState'[DisplayName])
```



```dax
UserStateUPN = RELATED('UserState'[UPN])
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(NOW() >= DATEADD('SPO-UserActivity'[EndofMonth].[Date],5,DAY),TRUE(),FALSE())
```


## Table: TenantOneDrive-Activity

### Measures:


```dax
MostRecent-ActiveSites(ODB) = CALCULATE(SUM('TenantOneDrive-Activity'[ActivityTotalAccounts]),LASTDATE('TenantOneDrive-Activity'[TimeFrame]))
```


### Calculated Columns:


```dax
ODB-ActivityType = IF([Product]="OneDrive" && SEARCH("Active Files",TRIM(IF(NOT(SEARCH("/",[ActivityType],1,0)=0),PATHITEM(SUBSTITUTE([ActivityType],"/","|"),2),IF(NOT(SEARCH(" /",[ActivityType],1,0)=0),PATHITEM(SUBSTITUTE([ActivityType]," /","|"),2),[ActivityType]))),1,0)>0, "Files Viewed/Modified",[ActivityType])
```



```dax
EOMTimeFrame = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EOMTimeFrame],[ContentDate] > [EOMTimeFrame]),TRUE(),FALSE())
```


## Table: TenantOneDrive-Usage

### Measures:


```dax
ODB-TotalDiskQuota = SUM([DiskQuotabyQuotaType])
```



```dax
ODB-TotalDiskUsed = SUM([DiskUsedbyStorageType])
```



```dax
ODB-TotalAccounts = CALCULATE(SUM([TotalAccounts]))
```



```dax
ODB-MostRecent-TotalAccounts = CALCULATE(SUM([TotalAccounts]),LASTDATE('TenantOneDrive-Usage'[TimeFrame]))
```



```dax
ODB-MostRecent-DocumentCount = CALCULATE(SUM([DocumentCount]),LASTDATE('TenantOneDrive-Usage'[TimeFrame]))
```



```dax
ODB-MostRecent-DiskUsed = CALCULATE(SUM([DiskUsedbyStorageType]),LASTDATE('TenantOneDrive-Usage'[TimeFrame]))
```



```dax
ODB-MostRecent-DiskQuota = CALCULATE(SUM([DiskQuotabyQuotaType]),LASTDATE('TenantOneDrive-Usage'[TimeFrame]))
```



```dax
ODB-MostRecent-%StorageUsed = CALCULATE(DIVIDE([ODB-MostRecent-DiskUsed],[ODB-MostRecent-DiskQuota],0))
```



```dax
ODB_MostRecentDate = FORMAT(LASTDATE('TenantOneDrive-Usage'[TimeFrame]),"mmmm") & " " & FORMAT(LASTDATE('TenantOneDriveUsage'[TimeFrame]),"YYYY")
```



```dax
ODB-MostRecent-StorageType = LASTNONBLANK('TenantOneDrive-Usage'[ODB-StorageType], 1)
```



```dax
ODB-MostRecent-QuotaType = LASTNONBLANK('TenantOneDrive-Usage'[ODB-QuotaType], 1)
```



```dax
ODB-MostRecent-DiskQuota(GB) = CALCULATE(DIVIDE(SUM([DiskQuota]), 1073741824, 0),LASTDATE('TenantOneDrive-Usage'[TimeFrame]))
```



```dax
ODB-MostRecent-DiskUsed(GB) = CALCULATE(DIVIDE(SUM([DiskUsed]), 1073741824, 0),LASTDATE('TenantOneDrive-Usage'[TimeFrame]))
```



```dax
ODB-MostRecent-%StorageUsed(GB) = CALCULATE(DIVIDE([ODB-MostRecent-DiskUsed(GB)],[ODB-MostRecent-DiskQuota(GB)],0)) 
```



```dax
ODB-MostRecent-StorageType(GB) = "GB"
```



```dax
ODB-TotalDiskQuota(GB) = CALCULATE(DIVIDE(SUM([DiskQuota]), 1073741824, 0))
```



```dax
ODB-TotalDiskUsed(GB) = CALCULATE(DIVIDE(SUM([DiskUsed]), 1073741824, 0))
```



```dax
OD Storage Label = CONCATENATE( [ODB_MostRecentDate], " Storage Used (GB)")
```



```dax
ODB-MostRecent-DocumentCount Label = CONCATENATE( [ODB_MostRecentDate], " Total Files")
```



```dax
ODB-MostRecent-DocumentCount Label 2 = CONCATENATE( [ODB_MostRecentDate], " Total Files in OneDrive")
```


### Calculated Columns:


```dax
DiskUsed(KB/MB/GB/TB) = IF([DiskUsed]/1024 <= 1, FIXED([DiskUsed],2,1)& " " & "Bytes",IF([DiskUsed]/1048576 <= 1 && [DiskUsed]/1024 > 1, FIXED([DiskUsed]/1024,2,1) &" " & "KB",IF([DiskUsed]/1073741824 <= 1 && [DiskUsed]/1048576 > 1,FIXED([DiskUsed]/1048576,2,1)  & " " & "MB",IF([DiskUsed]/1073741824 > 1 && [DiskUsed]/1099511627776 <= 1 ,FIXED([DiskUsed]/1073741824,2,1)  & " " & "GB",IF([DiskUsed]/1099511627776 >= 1,FIXED([DiskUsed]/1099511627776,2,1)  & " " & "TB","0")))))
```



```dax
ODB-StorageType = RIGHT([DiskUsed(KB/MB/GB/TB)],LEN([DiskUsed(KB/MB/GB/TB)])-SEARCH(" ",[DiskUsed(KB/MB/GB/TB)]))
```



```dax
DiskUsedbyStorageType = LEFT([DiskUsed(KB/MB/GB/TB)],SEARCH(" ",[DiskUsed(KB/MB/GB/TB)]))
```



```dax
DiskQuota(KB/MB/GB/TB) = IF([DiskQuota]/1024 <= 1, FIXED([DiskQuota],2,1)& " " & "Bytes",IF([DiskQuota]/1048576 <= 1 && [DiskQuota]/1024 > 1, FIXED([DiskQuota]/1024,2,1) &" " & "KB",IF([DiskQuota]/1073741824 <= 1 && [DiskQuota]/1048576 > 1,FIXED([DiskQuota]/1048576,2,1)  & " " & "MB",IF([DiskQuota]/1073741824 > 1 && [DiskQuota]/1099511627776 <= 1 ,FIXED([DiskQuota]/1073741824,2,1)  & " " & "GB",IF([DiskQuota]/1099511627776 >= 1,FIXED([DiskQuota]/1099511627776,2,1)  & " " & "TB","0")))))
```



```dax
ODB-QuotaType = RIGHT([DiskQuota(KB/MB/GB/TB)],LEN([DiskQuota(KB/MB/GB/TB)])-SEARCH(" ",[DiskQuota(KB/MB/GB/TB)]))
```



```dax
DiskQuotabyQuotaType = LEFT([DiskQuota(KB/MB/GB/TB)],SEARCH(" ",[DiskQuota(KB/MB/GB/TB)]))
```



```dax
EOMTimeFrame = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EOMTimeFrame],[ContentDate] > [EOMTimeFrame]),TRUE(),FALSE())
```


## Table: TenantSharePoint-Activity

### Measures:


```dax
SPO-MostRecent-ActivityTotalSites = CALCULATE(SUM([ActivityTotalSites]),LASTDATE('TenantSharePoint-Activity'[TimeFrame]))
```



```dax
SPO-MostRecent-SitesW/OwnerActivities = CALCULATE(SUM([SPO-CollaboratedbyOwner]),LASTDATE('TenantSharePoint-Activity'[TimeFrame]))
```



```dax
SPO-MostRecent-SitesW/NonOwnerActivities = CALCULATE(SUM([SPO-CollaboratedbyOthers]),LASTDATE('TenantSharePoint-Activity'[TimeFrame]))
```


### Calculated Columns:


```dax
SiteActivityCombo = IF([ActivityType]="Active Files", [SiteType] & " - " & "Files Viewed/Modified", [SiteType] & " - " & [ActivityType])
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EndofMonth],[ContentDate] > [EndofMonth]),TRUE(),FALSE())
```


## Table: TenantSharePoint-Usage

### Measures:


```dax
SPO-TotalDiskQuota = SUM([DiskQuotabyQuotaType])
```



```dax
SPO-TotalDiskUsed = SUM([DiskUsedbyStorageType])
```



```dax
SPO-MostRecent-TotalSites = CALCULATE(SUM([TotalSites]),LASTDATE('TenantSharePoint-Usage'[TimeFrame]))
```



```dax
SPO-MostRecent-DocumentCount = CALCULATE(SUM([DocumentCount]),LASTDATE('TenantSharePoint-Usage'[TimeFrame]))
```



```dax
SPO-MostRecent-DiskUsed = CALCULATE(SUM([DiskUsedbyStorageType]),LASTDATE('TenantSharePoint-Usage'[TimeFrame]))
```



```dax
SPO-MostRecent-DiskQuota = CALCULATE(SUM([DiskQuotabyQuotaType]),LASTDATE('TenantSharePoint-Usage'[TimeFrame]))
```



```dax
SPO-MostRecent-%StorageUsed = CALCULATE(DIVIDE([SPO-MostRecent-DiskUsed],[SPO-MostRecent-DiskQuota],0))
```



```dax
SPO-%StorageUsed = CALCULATE(DIVIDE([SPO-TotalDiskUsed],[SPO-TotalDiskQuota],0))
```



```dax
SPO DiskUsed(TB) = DIVIDE(CALCULATE(SUM([DiskUsed])),1099511627776,0)
```



```dax
SPO DiskQuota(TB) = DIVIDE(CALCULATE(SUM([DiskQuota])),1099511627776,0)
```



```dax
SPO DiskQuota(GB) = DIVIDE(CALCULATE(SUM([DiskQuota])),1073741824,0)
```



```dax
SPO DiskUsed(GB) = DIVIDE(CALCULATE(SUM([DiskUsed])),1073741824,0)
```



```dax
SPO_MostRecentDate = FORMAT(LASTDATE('TenantSharePoint-Usage'[TimeFrame]),"mmmm") & " " & FORMAT(LASTDATE('TenantSharePoint-Usage'[TimeFrame]),"YYYY")
```



```dax
SPO-MostRecent-StorageType = LASTNONBLANK('TenantSharePoint-Usage'[SPO-StorageType], 1)
```



```dax
SPO-MostRecent-QuotaType = LASTNONBLANK('TenantSharePoint-Usage'[SPO-QuotaType], 1)
```



```dax
SPO-MostRecent-DiskQuota(GB) = CALCULATE(DIVIDE(SUM('TenantSharePoint-Usage'[DiskQuota]), 1073741824, 0), LASTDATE('TenantSharePoint-Usage'[TimeFrame]))
```



```dax
SPO-MostRecent-DiskUsed(GB) = CALCULATE(DIVIDE(SUM([DiskUsed]), 1073741824, 0),LASTDATE('TenantSharePoint-Usage'[TimeFrame]))
```



```dax
SPO-MostRecent-%StorageUsed(GB) = CALCULATE(DIVIDE([SPO-MostRecent-DiskUsed(GB)],[SPO-MostRecent-DiskQuota(GB)],0))
```



```dax
SPO-MostRecent-StorageType(GB) = "GB"
```



```dax
SPO-TotalDiskQuota(GB) = CALCULATE(DIVIDE(SUM([DiskQuota]), 1073741824, 0))
```



```dax
SPO-TotalDiskUsed(GB) = CALCULATE(DIVIDE(SUM([DiskUsed]), 1073741824, 0))
```



```dax
SPO Storage Label = CONCATENATE( [SPO_MostRecentDate], " Storage Used (GB)")
```



```dax
SPO-MostRecent-DocumentCount Label = CONCATENATE( [SPO_MostRecentDate], " Total Files")
```



```dax
SPO-MostRecent-DocumentCount Label 2 = CONCATENATE( [SPO_MostRecentDate], " Total Files in SharePoint")
```


### Calculated Columns:


```dax
DiskUsed(KB/MB/GB/TB) = IF([DiskUsed]/1024 <= 1, FIXED([DiskUsed],2,1)& " " & "Bytes",IF([DiskUsed]/1048576 <= 1 && [DiskUsed]/1024 > 1, FIXED([DiskUsed]/1024,2,1) &" " & "KB",IF([DiskUsed]/1073741824 <= 1 && [DiskUsed]/1048576 > 1,FIXED([DiskUsed]/1048576,2,1)  & " " & "MB",IF([DiskUsed]/1073741824 > 1 && [DiskUsed]/1099511627776 <= 1 ,FIXED([DiskUsed]/1073741824,2,1)  & " " & "GB",IF([DiskUsed]/1099511627776 >= 1,FIXED([DiskUsed]/1099511627776,2,1)  & " " & "TB","0")))))
```



```dax
DiskQuota(KB/MB/GB/TB) = IF([DiskQuota]/1024 <= 1, FIXED([DiskQuota],2,1)& " " & "Bytes",IF([DiskQuota]/1048576 <= 1 && [DiskQuota]/1024 > 1, FIXED([DiskQuota]/1024,2,1) &" " & "KB",IF([DiskQuota]/1073741824 <= 1 && [DiskQuota]/1048576 > 1,FIXED([DiskQuota]/1048576,2,1)  & " " & "MB",IF([DiskQuota]/1073741824 > 1 && [DiskQuota]/1099511627776 <= 1 ,FIXED([DiskQuota]/1073741824,2,1)  & " " & "GB",IF([DiskQuota]/1099511627776 >= 1,FIXED([DiskQuota]/1099511627776,2,1)  & " " & "TB","0")))))
```



```dax
DiskUsedbyStorageType = VALUE(LEFT([DiskUsed(KB/MB/GB/TB)],SEARCH(".",[DiskUsed(KB/MB/GB/TB)])))
```



```dax
DiskQuotabyQuotaType = LEFT([DiskQuota(KB/MB/GB/TB)],SEARCH(" ",[DiskQuota(KB/MB/GB/TB)]))
```



```dax
SPO-QuotaType = RIGHT([DiskQuota(KB/MB/GB/TB)],LEN([DiskQuota(KB/MB/GB/TB)])-SEARCH(" ",[DiskQuota(KB/MB/GB/TB)]))
```



```dax
SPO-StorageType = RIGHT([DiskUsed(KB/MB/GB/TB)],LEN([DiskUsed(KB/MB/GB/TB)])-SEARCH(" ",[DiskUsed(KB/MB/GB/TB)]))
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF([EndofMonth]=[ContentDate],TRUE(),FALSE())
```


## Table: ODBActive-Sites/Users/Docs

### Measures:


```dax
ODB-ActiveUsers(%) = DIVIDE(CALCULATE(SUM([ActiveUsers])),CALCULATE(SUM([EnabledUsers])),0)
```



```dax
ODB-ActiveAccounts(%) = DIVIDE(CALCULATE(SUM([ActiveSites])),CALCULATE(SUM([TotalSites])),0)
```



```dax
MostRecent-TotalAccounts(ODB) = CALCULATE(SUM([TotalSites]),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-ActiveAccounts(ODB) = CALCULATE(SUM([ActiveSites]),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-ActiveUsers(ODB) = CALCULATE(SUM([ActiveUsers]),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-EnabledUsers(ODB) = CALCULATE(SUM([EnabledUsers]),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-DocumentCount(ODB) = CALCULATE(SUM([TotalFiles]),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-ActiveDocument(ODB) = CALCULATE(SUM([ActiveFiles]),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
ODB-MostRecent-ActiveAccounts(%) = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveSites])),CALCULATE(SUM([TotalSites])),0),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
ODB-MostRecent-ActiveUsers(%) = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveUsers])),CALCULATE(SUM([EnabledUsers])),0),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
ODB-MostRecent-ActiveDocument(%) = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveFiles])),CALCULATE(SUM([TotalFiles])),0),LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
ODB-ActiveDocs(%) = DIVIDE(CALCULATE(SUM([ActiveFiles])),CALCULATE(SUM([TotalFiles])),0)
```



```dax
ODBActive_MostRecentDate = FORMAT(LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]),"mmmm") & " " & FORMAT(LASTDATE('ODBActive-Sites/Users/Docs'[TimeFrame]),"YYYY")
```



```dax
Active Sites Label = CONCATENATE( [ODBActive_MostRecentDate], " Active Sites")
```



```dax
Active Sites % Label = CONCATENATE( [ODBActive_MostRecentDate], " Active Sites %")
```



```dax
ODB Active Users Label = CONCATENATE( [ODBActive_MostRecentDate], " Active Users")
```



```dax
ODB Active User % Label = CONCATENATE( [ODBActive_MostRecentDate], " Active User %")
```



```dax
Active Files Label = CONCATENATE( [ODBActive_MostRecentDate], " Active Files")
```



```dax
Active Files % Label = CONCATENATE( [ODBActive_MostRecentDate], " Active File %")
```



```dax
ODB - Active Files of Total Label = CONCATENATE( [ODBActive_MostRecentDate], " Active and Total Files in OneDrive")
```



```dax
ODB - Active Files of Total = CONCATENATE(FORMAT([MostRecent-ActiveDocument(ODB)],"#,#"),CONCATENATE(" of ",FORMAT([ODB-MostRecent-DocumentCount],"#,#")))
```


### Calculated Columns:


```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EndofMonth],[ContentDate] > [EndofMonth]),TRUE(),FALSE())
```


## Table: SPO-SiteType

### Measures:


```dax
SPOUsage_SiteTypeTitle = VAR SelectedSiteType = VALUES('SPO-SiteType'[SiteType])
var	NumofSelectedSiteType = COUNTROWS(SelectedSiteType)
var NumofPossibleSiteType = COUNTROWS(ALL('SPO-SiteType'[SiteType]))
var AllbutLastSelectedSiteType = TOPN(NumofSelectedSiteType-1,SelectedSiteType)
VAR LastSelectedSiteType = EXCEPT(SelectedSiteType,AllbutLastSelectedSiteType)
RETURN
"SharePoint "
& IF(NumofSelectedSiteType=NumofPossibleSiteType,
	BLANK(), " : "
	& IF(NumofSelectedSiteType=1,
		"",CONCATENATEX(AllbutLastSelectedSiteType,'SPO-SiteType'[SiteType],", " )
		& " and " )
		& LastSelectedSiteType
)
```



```dax
SPOUsage_SiteTypeTitle(ActivevsInactive) = 
VAR	SelectedSiteType = VALUES('SPO-SiteType'[SiteType])
var	NumofSelectedSiteType = COUNTROWS(SelectedSiteType)
var NumofPossibleSiteType = COUNTROWS(ALL('SPO-SiteType'[SiteType])) - 1
var AllbutLastSelectedSiteType = TOPN(NumofSelectedSiteType-1,SelectedSiteType)
VAR LastSelectedSiteType = EXCEPT(SelectedSiteType,AllbutLastSelectedSiteType)
RETURN
"SharePoint usage "
& IF(NumofSelectedSiteType=NumofPossibleSiteType,
	BLANK(), " : "
	& IF(NumofSelectedSiteType=1,
		"",CONCATENATEX(AllbutLastSelectedSiteType,'SPO-SiteType'[SiteType],", " )
		& " and " )
		& LastSelectedSiteType
)
```


## Table: SPOActive-Sites/Users/Docs

### Measures:


```dax
MostRecent-ActiveDocuments(SPO) = CALCULATE(SUM([ActiveFiles]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-ActiveUsers(SPO) = CALCULATE(SUM([ActiveUsers]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-DocumentCount(SPO) = CALCULATE(SUM([TotalFiles]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-EnabledUsers(SPO) = CALCULATE(SUM([EnabledUsers]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-ActiveSites(SPO) = CALCULATE(SUM([ActiveSites]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-TotalSites(SPO) = CALCULATE(SUM([TotalSites]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
SPO-ActiveSites(%) = DIVIDE(CALCULATE(SUM([ActiveSites])),CALCULATE(SUM([TotalSites])),0)
```



```dax
SPO-ActiveUsers(%) = DIVIDE(CALCULATE(SUM([ActiveUsers])),CALCULATE(SUM([EnabledUsers])),0)
```



```dax
SPO-ActiveDocs(%) = DIVIDE(CALCULATE(SUM([ActiveFiles])),CALCULATE(SUM([TotalFiles])),0)
```



```dax
SPO-MostRecent-ActiveDocs(%) = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveFiles])),CALCULATE(SUM([TotalFiles])),0),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
SPO-MostRecent-ActiveUsers(%) = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveUsers])),CALCULATE(SUM([EnabledUsers])),0),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
SPO-MostRecent-ActiveSites(%) = CALCULATE(DIVIDE(CALCULATE(SUM([ActiveSites])),CALCULATE(SUM([TotalSites])),0),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
SPOActive_MostRecentDate = FORMAT(LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]),"mmmm") & " " & FORMAT(LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]),"YYYY")
```



```dax
MostRecent-TotalFiles(SPO) = CALCULATE(SUM([TotalFiles]),LASTDATE('SPOActive-Sites/Users/Docs'[TimeFrame]))
```



```dax
MostRecent-TotalFiles(SPO) Label = CONCATENATE( [SPOActive_MostRecentDate], " Total Files")
```



```dax
SPO - Active Files of Total Label = CONCATENATE( [SPOActive_MostRecentDate], " Active and Total Files in SharePoint")
```



```dax
SPO - Active Files of Total = CONCATENATE(FORMAT([MostRecent-ActiveDocuments(SPO)],"#,#"),CONCATENATE(" of ",FORMAT([MostRecent-TotalFiles(SPO)],"#,#")))
```



```dax
SPO Active Sites Label = CONCATENATE( [SPOActive_MostRecentDate], " Active Sites")
```



```dax
SPO Active Users Label = CONCATENATE( [SPOActive_MostRecentDate], " Active Users")
```


### Calculated Columns:


```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EndofMonth],[ContentDate] > [EndofMonth]),TRUE(),FALSE())
```


## Table: RegionActivity

### Measures:


```dax
TotalUsersEOM = CALCULATE(DISTINCTCOUNT([UserId]),ALLSELECTED('RegionActivity'))
```



```dax
ActiveUsersEOM = CALCULATE(DISTINCTCOUNT([UserId]))
```



```dax
%ofTotalUsers = DIVIDE([ActiveUsersEOM],[TotalUsersEOM],0)
```



```dax
RegionProductTitle = VAR SelectedProduct = VALUES('RegionActivity'[Product])
var NumofSelectedProducts =COUNTROWS(SelectedProduct)
VAR NumofPossibleProducts = COUNTROWS(ALL('RegionActivity'[Product]))
VAR AllbutLastSelectedProduct = TOPN(NumofSelectedProducts-1,SelectedProduct)
VAR	LastSelectedProduct = EXCEPT(SelectedProduct,AllbutLastSelectedProduct)
RETURN
"Adoption by region "
& IF(NumofSelectedProducts=NumofPossibleProducts,
	" : All products",
	": "
	& IF(NumofSelectedProducts=1,
		"",
		CONCATENATEX(AllbutLastSelectedProduct,'RegionActivity'[Product],", ")
		& " and "
	)
	&LastSelectedProduct
)
```


### Calculated Columns:


```dax
City = RELATED('UserState'[LocationCity])
```



```dax
Country = RELATED('UserState'[LocationCountry])
```



```dax
State = RELATED('UserState'[LocationState])
```


## Table: TenantO365GroupsUsage

### Measures:


```dax
MostRecent-ActiveO365Groups(%) = CALCULATE(DIVIDE(SUM([ActiveGroups]),SUM([TotalGroups]),0),LASTDATE('TenantO365GroupsUsage'[TimeFrame]))
```



```dax
MostRecent-ActiveO365GrpCount = CALCULATE(SUM([ActiveGroups]),LASTDATE('TenantO365GroupsUsage'[TimeFrame]))
```



```dax
MostRecent-GrpSiteFileCount = CALCULATE(SUM([SPO_TotalFiles]),LASTDATE('TenantO365GroupsUsage'[TimeFrame]))
```



```dax
MostRecent-O365GrpCount = CALCULATE(SUM([TotalGroups]),LASTDATE('TenantO365GroupsUsage'[TimeFrame]))
```



```dax
MostRecent-O365GrpSiteActiveFile(%) = CALCULATE(DIVIDE(SUM([SPO_ActiveFiles]),SUM([SPO_TotalFiles]),0),LASTDATE('TenantO365GroupsUsage'[TimeFrame]))
```



```dax
MostRecent-O365GrpSiteActiveFileCount = CALCULATE(SUM([SPO_ActiveFiles]),LASTDATE('TenantO365GroupsUsage'[TimeFrame]))
```



```dax
O365GroupUsage_MostRecentDate = FORMAT(LASTDATE(TenantO365GroupsUsage[TimeFrame]),"mmmm")& " " & FORMAT(LASTDATE(TenantO365GroupsUsage[TimeFrame]),"YYYY")
```



```dax
MostRecent_MBX_StorageUsed = CALCULATE(SUM(TenantO365GroupsUsage[DiskUsedbyEXOStorageType]), LASTDATE(TenantO365GroupsUsage[TimeFrame]))
```



```dax
MostRecent_SPO_StorageUsed = CALCULATE(SUM(TenantO365GroupsUsage[DiskUsedbySPOStorageType]), LASTDATE(TenantO365GroupsUsage[TimeFrame]))
```



```dax
MostRecent-MBX_StorageType = LASTNONBLANK(TenantO365GroupsUsage[MBX_StorageType], 1)
```



```dax
MostRecent-SPO_StorageType = LASTNONBLANK(TenantO365GroupsUsage[SPO_StorageType], 1)
```



```dax
MostRecent-MBX_TotalActivities = CALCULATE(SUM(TenantO365GroupsUsage[MBX_TotalActivities]), LASTDATE(TenantO365GroupsUsage[TimeFrame]))
```



```dax
O365 Groups Label = CONCATENATE( [O365GroupUsage_MostRecentDate], " Active Groups %")
```



```dax
O365 Group mailbox act Label = CONCATENATE( [O365GroupUsage_MostRecentDate], " Mailbox Activities")
```



```dax
O365 Files Label = CONCATENATE( [O365GroupUsage_MostRecentDate], " Active File %")
```



```dax
O365 File count Label = CONCATENATE( [O365GroupUsage_MostRecentDate], " Active Files")
```


### Calculated Columns:


```dax
TotalActivityCount = (TenantO365GroupsUsage[MBX_TotalActivities] + TenantO365GroupsUsage[SPO_TotalActivities] + TenantO365GroupsUsage[YAM_PostedActivties])
```



```dax
EndofMonth = EOMONTH([TimeFrame],0)
```



```dax
IsMonthComplete = IF(OR([ContentDate]=[EndofMonth],[ContentDate] > [EndofMonth]),TRUE(),FALSE())
```



```dax
MBX_StorageUsed(KB/MB/GB/TB) = IF([MBX_StorageUsed]/1024 < 1, FIXED([MBX_StorageUsed],2,1)& " " & "Bytes",IF([MBX_StorageUsed]/1048576 < 1 && [MBX_StorageUsed]/1024 > 1, FIXED([MBX_StorageUsed]/1024,2,1) &" " & "KB",IF([MBX_StorageUsed]/1073741824 < 1 && [MBX_StorageUsed]/1048576 > 1,FIXED([MBX_StorageUsed]/1048576,2,1)  & " " & "MB",IF([MBX_StorageUsed]/1073741824 > 1 && [MBX_StorageUsed]/1099511627776 < 1 ,FIXED([MBX_StorageUsed]/1073741824,2,1)  & " " & "GB",IF([MBX_StorageUsed]/1099511627776 > 1,FIXED([MBX_StorageUsed]/1099511627776,2,1)  & " " & "TB","0"))))) 
```



```dax
MBX_StorageType = RIGHT([MBX_StorageUsed(KB/MB/GB/TB)],LEN([MBX_StorageUsed(KB/MB/GB/TB)])-SEARCH(" ",[MBX_StorageUsed(KB/MB/GB/TB)]))
```



```dax
DiskUsedbyEXOStorageType = LEFT([MBX_StorageUsed(KB/MB/GB/TB)],SEARCH(" ",[MBX_StorageUsed(KB/MB/GB/TB)]))
```



```dax
SPO_StorageUsed(KB/MB/GB/TB) = IF([SPO_StorageUsed]/1024 < 1, FIXED([SPO_StorageUsed],2,1)& " " & "Bytes",IF([SPO_StorageUsed]/1048576 < 1 && [SPO_StorageUsed]/1024 > 1, FIXED([SPO_StorageUsed]/1024,2,1) &" " & "KB",IF([SPO_StorageUsed]/1073741824 < 1 && [SPO_StorageUsed]/1048576 > 1,FIXED([SPO_StorageUsed]/1048576,2,1)  & " " & "MB",IF([SPO_StorageUsed]/1073741824 > 1 && [SPO_StorageUsed]/1099511627776 < 1 ,FIXED([SPO_StorageUsed]/1073741824,2,1)  & " " & "GB",IF([SPO_StorageUsed]/1099511627776 > 1,FIXED([SPO_StorageUsed]/1099511627776,2,1)  & " " & "TB","0"))))) 
```



```dax
SPO_StorageType = RIGHT([SPO_StorageUsed(KB/MB/GB/TB)],LEN([SPO_StorageUsed(KB/MB/GB/TB)])-SEARCH(" ",[SPO_StorageUsed(KB/MB/GB/TB)]))
```



```dax
DiskUsedbySPOStorageType = LEFT([SPO_StorageUsed(KB/MB/GB/TB)],SEARCH(" ",[SPO_StorageUsed(KB/MB/GB/TB)]))
```

