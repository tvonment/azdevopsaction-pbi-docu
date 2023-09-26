



# M Code

|Dataset|[UPS_Dashboard_v01](./../UPS_Dashboard_v01.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Sheet1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710176\Documents\2020-12-16 UPS\Dashboard\df_dash.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Share_Match_Key", type text}, {"Country", type text}, {"Region", type text}, {"Region_UPS", type text}, {"Year", Int64.Type}, {"Q", Int64.Type}, {"Player", type text}, {"Share", type number}, {"Q_ind", Int64.Type}, {"Month", Int64.Type}, {"Quarter", Int64.Type}, {"date", type date}, {"date_q", type text}, {"Q_ind_q_weights", type number}, {"Q_ind_q", Int64.Type}, {"horizon", Int64.Type}, {"Q_ind_q_pred", type number}, {"Q_ind_q_UPS", Int64.Type}, {"Q_ind_q_pred_UPS", type number}, {"Parcel_weight", Int64.Type}, {"Q_type", type text}, {"Q_R_ind_q", Int64.Type}, {"Q_R_ind_q_pred", type number}, {"Q_R_ind_q_UPS", Int64.Type}, {"Q_R_ind_q_pred_UPS", type number}, {"Q_P_ind_q", Int64.Type}, {"Q_P_ind_q_pred", type number}, {"Q_P_ind_q_UPS", Int64.Type}, {"Q_P_ind_q_pred_UPS", type number}, {"Q_ind_q_vis", Int64.Type}, {"Q_ind_q_vis_hist", Int64.Type}, {"Q_ind_q_vis_pred", type number}, {"Q_ind_q_vis_pred_alt", type number}, {"Q_ind_q_vis_UPS", Int64.Type}, {"Q_ind_q_vis_hist_UPS", Int64.Type}, {"Q_ind_q_vis_pred_UPS", type number}, {"ERROR", Percentage.Type}})
in
    #"Changed Type"
```

