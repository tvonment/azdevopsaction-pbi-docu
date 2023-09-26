



# M Code

|Dataset|[RB_IT_Product_Catalog](./../RB_IT_Product_Catalog.md)|
| :--- | :--- |
|Workspace|[Idea & Demand](../../Workspaces/Idea-&-Demand.md)|

## Table: New Requests


```m
let
    Quelle = SharePoint.Tables("https://rberger.sharepoint.com/sites/IdeationManagement/", [Implementation=null, ApiVersion=15]),
    #"18e43564-a752-42ad-a5c2-9d03038b6d17" = Quelle{[Id="18e43564-a752-42ad-a5c2-9d03038b6d17"]}[Items],
    #"Filtered Rows" = Table.SelectRows(#"18e43564-a752-42ad-a5c2-9d03038b6d17", each ([Status] = "Completed") and ([Visible] = true)),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Filtered Rows",{{"ID", "ID.1"}}),
    #"Expanded FieldValuesAsText" = Table.ExpandRecordColumn(#"Umbenannte Spalten", "FieldValuesAsText", {"ShortDescription"}, {"FieldValuesAsText.Description"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded FieldValuesAsText",{"FileSystemObjectType", "Id", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "RequestorId", "RequestorStringId", "ITContactId", "ITContactStringId", "teamsConversationMetadata_D86AE2", "ContentTypeId", "ComplianceAssetId", "ID.1", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Requestor", "Budget Owner", "ITContact", "Author", "Editor", "Categ", "Description", "w3tt", "Data Security", "IT Security", "Infrastructure", "Status", "CategoryText", "Logo", "Licensing Cost", "Class", "Link", "u4rg", "Budget OwnerId", "Budget OwnerStringId", "Project", "Scope", "Legal", "ShortDescription", "Visible"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"FieldValuesAsText.Description", "Description"}, {"ReqName", "Responsible"}, {"CategoryNew", "Category"}})
in
    #"Renamed Columns"
```


## Table: Applications List


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/IT/", [Implementation=null, ApiVersion=15]),
    #"b6ffd0ac-d32a-4dd6-856f-2c7da6d8843e" = Source{[Id="b6ffd0ac-d32a-4dd6-856f-2c7da6d8843e"]}[Items],
    #"Renamed Columns" = Table.RenameColumns(#"b6ffd0ac-d32a-4dd6-856f-2c7da6d8843e",{{"ID", "ID.1"}}),
    #"Expanded FieldValuesAsText" = Table.ExpandRecordColumn(#"Renamed Columns", "FieldValuesAsText", {"Description"}, {"FieldValuesAsText.Description"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded FieldValuesAsText", each ([Visibility] = "Public")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"FileSystemObjectType", "Id", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ID.1", "ContentTypeId", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "ComplianceAssetId", "IT PMId", "IT PMStringId", "IT PM BackupId", "IT PM BackupStringId", "Business PMId", "Business PMStringId", "SubdivisionIdId", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Author", "Editor", "IT PM", "IT PM Backup", "SubdivisionId", "Description", "Hosting", "Finish Date", "Visibility", "URLs", "Project ID", "Area Path"}),
    #"Expanded Business PM1" = Table.ExpandRecordColumn(#"Removed Columns", "Business PM", {"FirstName", "LastName"}, {"Business PM.FirstName", "Business PM.LastName"}),
    #"Merged Columns" = Table.CombineColumns(#"Expanded Business PM1",{"Business PM.FirstName", "Business PM.LastName"},Combiner.CombineTextByDelimiter(" ", QuoteStyle.None),"Responsible"),
    #"Renamed Columns1" = Table.RenameColumns(#"Merged Columns",{{"FieldValuesAsText.Description", "Description"}, {"Functional Area", "Category"}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Renamed Columns1",{"Title", "Responsible", "Category", "Description"})
in
    #"Reordered Columns"
```


## Table: Apps&Solutions


```m
let
    Source = Table.Combine({#"New Requests", #"Applications List"})
in
    Source
```


## Table: TechLab Asset manager


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TechLab2.0/", [ApiVersion = 15]),
    #"97372e81-d0db-492b-b23a-3d7e39d9576f" = Source{[Id="97372e81-d0db-492b-b23a-3d7e39d9576f"]}[Items],
    #"Renamed Columns" = Table.RenameColumns(#"97372e81-d0db-492b-b23a-3d7e39d9576f",{{"ID", "ID.1"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each ([VisibleforReports] = "Visible")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"FileSystemObjectType", "Id", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ID.1", "ContentTypeId", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "ComplianceAssetId", "PurchasePrice", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Author", "Editor", "PurchaseDate", "OrderNumber", "ConditionNotes", "VisibleforReports"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"Title", "Technology Name"}, {"Type2", "Asset Type"}, {"Manufacturer", "Ubication"}, {"Model", "Reviewed"}, {"SerialNumber", "Published Date"}, {"AssetType", "Asset Description"}, {"GoodNotes", "Good Notes"}, {"BadNotes", "Bad Notes"}, {"DueDate", "Evaluation"}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Renamed Columns1",{"DevicePhoto", "Technology Name", "Asset Type", "Status", "Ubication", "Reviewed", "Published Date", "Asset Description", "Good Notes", "Bad Notes", "Evaluation"}),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Reordered Columns", {{"Evaluation", type number}}, "de-DE"),
    #"Inserted Text Between Delimiters" = Table.AddColumn(#"Changed Type with Locale", "Asset Image", each Text.BetweenDelimiters([DevicePhoto], "serverRelativeUrl"":""", """,""id"":"""), type text),
    #"Added Prefix" = Table.TransformColumns(#"Inserted Text Between Delimiters", {{"Asset Image", each "https://rberger.sharepoint.com" & _, type text}})
in
    #"Added Prefix"
```

