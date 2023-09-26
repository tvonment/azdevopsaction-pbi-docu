



# M Code

|Dataset|[SR_Scorecard_Dashboard_V2](./../SR_Scorecard_Dashboard_V2.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: SR report


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M800426\OneDrive - Roland Berger Holding GmbH\Carolin\Dashboard\SR Scorecards Reporting\Scorecards-P_dir_pri-Interview-Processes-2023-07-27.xlsx"), null, true),
    report1 = Quelle{[Name="report"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(report1, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Job Title", type text}, {"Candidate Last Name", type text}, {"Candidate First Name", type text}, {"Current Employer", type text}, {"Department Org Field Value", type text}, {"Reviewer First and Last Name", type text}, {"Review Rating", Int64.Type}, {"Review Text", type text}, {"Criteria Name", type text}, {"Criteria Description", type text}, {"Criteria Feedback", type text}, {"Criteria Rating", Int64.Type}, {"Number of Reviewers", Int64.Type}, {"Application field: Interview 10 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 1 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 2 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 3 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 4 (YYYY.MM.DD interviewer name)", type text}, {"Application field: Interview 5 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 6 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 7 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 8 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 9 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Offer level", type text}}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Geänderter Typ",{{"Application field: Interview 1 (YYYY.MM.DD, interviewer name)", "Interview 1"}, {"Application field: Interview 2 (YYYY.MM.DD, interviewer name)", "Interview 2"}, {"Application field: Interview 3 (YYYY.MM.DD, interviewer name)", "Interview 3"}, {"Application field: Interview 4 (YYYY.MM.DD interviewer name)", "Interview 4"}, {"Application field: Interview 5 (YYYY.MM.DD, interviewer name)", "Interview 5"}, {"Application field: Interview 6 (YYYY.MM.DD, interviewer name)", "Interview 6"}, {"Application field: Interview 7 (YYYY.MM.DD, interviewer name)", "Interview 7"}, {"Application field: Interview 8 (YYYY.MM.DD, interviewer name)", "Interview 8"}, {"Application field: Interview 9 (YYYY.MM.DD, interviewer name)", "Interview 9"}, {"Application field: Interview 10 (YYYY.MM.DD, interviewer name)", "Interview 10"}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Umbenannte Spalten", "Benutzerdefiniert", each [Candidate Last Name]&", "&[Candidate First Name]),
    #"Umbenannte Spalten1" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"Benutzerdefiniert", "Candidate full name"}}),
    #"Added Conditional Column" = Table.AddColumn(#"Umbenannte Spalten1", "Criteria Name2", each if [Criteria Name] = "P04E_Client Management / Product portfolio" then "P04E_o#(tab)Client Mgmt./Product Portfolio" else if [Criteria Name] = "P05E_Acquisition relevant network / Sales contribution" then "P05E_o#(tab)Acquisition: Network/Sales Contr." else [Criteria Name]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Conditional Column",{{"Criteria Name", "Criteria Name long"}, {"Criteria Name2", "Criteria Name"}}),
    #"Added Conditional Column1" = Table.AddColumn(#"Renamed Columns", "Vote yes/no", each if Text.Contains([Criteria Feedback], "yes") then "yes" else if Text.Contains([Criteria Feedback], "no") then "no" else if [Criteria Feedback] = null then null else [Criteria Feedback])
in
    #"Added Conditional Column1"
```


## Table: reportV2


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M800426\OneDrive - Roland Berger Holding GmbH\Carolin\Dashboard\SR Scorecards Reporting\Scorecards-P_dir_pri-Interview-Processes-2023-08-28.xlsx"), null, true),
    report_Sheet = Source{[Item="report",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(report_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Job Title", type text}, {"Candidate Last Name", type text}, {"Candidate First Name", type text}, {"Current Employer", type text}, {"Department Org Field Value", type text}, {"Reviewer First and Last Name", type text}, {"Review Rating", Int64.Type}, {"Review Text", type text}, {"Criteria Name", type text}, {"Criteria Description", type text}, {"Criteria Feedback", type text}, {"Criteria Rating", Int64.Type}, {"Number of Reviewers", Int64.Type}, {"Application field: Interview 1 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 2 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 3 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 4 (YYYY.MM.DD interviewer name)", type text}, {"Application field: Interview 5 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 6 (YYYY.MM.DD, interviewer name)", type text}, {"Application field: Interview 7 (YYYY.MM.DD, interviewer name)", type any}, {"Application field: Interview 8 (YYYY.MM.DD, interviewer name)", type any}, {"Application field: Interview 9 (YYYY.MM.DD, interviewer name)", type any}, {"Application field: Offer level", type text}, {"Application field: First contact interview (YYYY.MM.DD, interviewer name)", type any}, {"Application field: Focus area", type text}, {"Application field: Gender", type text}, {"Application field: Platform offered", type text}, {"Current Title", type text}, {"Application Status", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Application field: Focus area", "Focus area"}, {"Application field: Interview 1 (YYYY.MM.DD, interviewer name)", "Interview 1"}, {"Application field: Interview 2 (YYYY.MM.DD, interviewer name)", "Interview 2"}, {"Application field: Interview 3 (YYYY.MM.DD, interviewer name)", "Interview 3"}, {"Application field: Interview 4 (YYYY.MM.DD interviewer name)", "Interview 4"}, {"Application field: Interview 5 (YYYY.MM.DD, interviewer name)", "Interview 5"}, {"Application field: Interview 6 (YYYY.MM.DD, interviewer name)", "Interview 6"}, {"Application field: Interview 7 (YYYY.MM.DD, interviewer name)", "Interview 7"}, {"Application field: Interview 8 (YYYY.MM.DD, interviewer name)", "Interview 8"}, {"Application field: Interview 9 (YYYY.MM.DD, interviewer name)", "Interview 9"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Candidate full name", each [Candidate Last Name]&", "&[Candidate First Name]),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Application field: First contact interview (YYYY.MM.DD, interviewer name)", "First contact interview"}, {"Application field: Platform offered", "Platform offered"}}),
    #"Added Conditional Column" = Table.AddColumn(#"Renamed Columns1", "Criteria Name short", each if [Criteria Name] = "Client Management / Product portfolio" then "Client Mgmt./Product Portfolio" else if [Criteria Name] = "Acquisition relevant network / Sales contribution" then "Acquisition: Network/Sales Contr." else [Criteria Name]),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Criteria name sortID", each if [Criteria Name short] = "Motivation" then 1 else if [Criteria Name short] = "Ability to create impact" then 2 else if [Criteria Name short] = "Market exposure / Innovation" then 3 else if [Criteria Name short] = "Client Mgmt./Product Portfolio" then 4 else if [Criteria Name short] = "Acquisition: Network/Sales Contr." then 5 else if [Criteria Name short] = "Leadership" then 6 else if [Criteria Name short] = "Vote for hiring: Yes or no; if yes please specify level" then 7 else if [Criteria Name short] = "Recommendations for subsequent interviews" then 8 else 0),
    #"Added Conditional Column2" = Table.AddColumn(#"Added Conditional Column1", "Vote yes/no", each if Text.Contains([Criteria Feedback], "yes") then "yes" else if Text.Contains([Criteria Feedback], "no") then "no" else if Text.Contains([Criteria Feedback], "Yes") then "yes" else if Text.Contains([Criteria Feedback], "No") then "no" else [Criteria Feedback]),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Added Conditional Column2", {{"Vote yes/no", "no feedback"}}),
    #"Added Conditional Column3" = Table.AddColumn(#"Replaced Errors", "Vote level", each if Text.Contains([Criteria Feedback], "Pri") then "Pri" else if Text.Contains([Criteria Feedback], "pri") then "Pri" else if Text.Contains([Criteria Feedback], "Dir") then "Dir" else if Text.Contains([Criteria Feedback], "dir") then "Dir" else if Text.Contains([Criteria Feedback], "P1") then "P1" else if Text.Contains([Criteria Feedback], "P2") then "P2" else if Text.Contains([Criteria Feedback], "P3") then "P3" else [Criteria Feedback])
in
    #"Added Conditional Column3"
```

