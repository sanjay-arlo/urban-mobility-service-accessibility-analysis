# Excel Analysis Guide

Use `data/cmrl_passenger_flow.csv` as the Excel source table.

## Workbook sheets

1. **Raw_Data** — imported CMRL passenger-flow data
2. **KPI_Checks** — ridership, MoM growth and ticket shares
3. **Pivot_Analysis** — financial-year and monthly pivot tables
4. **Business_Questions** — question → metric → finding → action

## Useful Excel formulas

### MoM growth
`=(Current_Month_Ridership-Prior_Month_Ridership)/Prior_Month_Ridership`

### NCMC share
`=NCMC/Total_Ridership`

### QR share
`=QR_Tickets/Total_Ridership`

### Closed-loop share
`=Closed_Loop/Total_Ridership`

## Pivot questions

- Ridership by financial year
- Highest-demand months
- Average monthly ridership
- Ticketing mix by month
- Interchange station count

## Validation rule

Totals should reconcile back to the CMRL published passenger-flow figures used in the project. Do not change source values in the Raw_Data sheet; perform transformations in separate analysis sheets.
