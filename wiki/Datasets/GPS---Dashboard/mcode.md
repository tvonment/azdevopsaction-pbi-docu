



# M Code

|Dataset|[GPS - Dashboard](./../GPS---Dashboard.md)|
| :--- | :--- |
|Workspace|[SAP Business ByDesign](../../Workspaces/SAP-Business-ByDesign.md)|

## Table: Work progress tracker


```m
let
    Quelle = SharePoint.Tables("https://rberger.sharepoint.com/sites/GPS-GlobalMigrationPeopleSofttoSAPByD", [Implementation=null, ApiVersion=15]),
    #"27c83550-ea12-467e-aba6-03e32e2040b7" = Quelle{[Id="27c83550-ea12-467e-aba6-03e32e2040b7"]}[Items],
    #"Entfernte Spalten" = Table.RemoveColumns(#"27c83550-ea12-467e-aba6-03e32e2040b7",{"ContentTypeId", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "ComplianceAssetId"}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Entfernte Spalten",{{"Created", type date}}),
    #"Entfernte Spalten1" = Table.RemoveColumns(#"Geänderter Typ",{"Created", "Modified", "ServerRedirectedEmbedUrl", "ServerRedirectedEmbedUri"}),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Entfernte Spalten1",{{"StartDate", type date}, {"DueDate", type date}}),
    #"Entfernte Spalten2" = Table.RemoveColumns(#"Geänderter Typ1",{"AssignedToId", "AssignedToStringId", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Author", "Editor", "AssignedTo", "Id", "FileSystemObjectType"})
in
    #"Entfernte Spalten2"
```

