# import-dwd-pollen

Imports pollen levels from DWD.

## Outputs
* today (float): level for today
* today_description (string): human-readable description of today
* tomorrow (float): level for tomorrow
* tomorrow_description (string): human-readable description of tomorrow
* day_after_tomorrow (float): level for the day after tomorrow
* day_after_tomorrow_description (string): human-readable description of day_after_tomorrow
* pollen (string)
* region (string)

## Configs
* lat (float): latitude selected
* long (float); longitude selected
* pollen (List[str]): list of strings describing which pollen should to be imported

---

This tool uses publicly available data provided by Deutscher Wetterdienst.