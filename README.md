# import-dwd-pollen

Imports pollen levels from DWD.

## Outputs
* today (int): level for today
* today_description (string): human-readable description of today
* tomorrow (int): level for tomorrow
* tomorrow_description (string): human-readable description of tomorrow
* day_after_tomorrow (int): level for the day after tomorrow
* day_after_tomorrow_description (string): human-readable description of day_after_tomorrow
* pollen (string)
* region (string)

## Configs
* lat (float): latitude selected. Default: 51.34
* long (float); longitude selected. Default: 12.38
* FilterPollen (List[str]): list of strings describing which pollen should to be imported. Default: []

---

This tool uses publicly available data provided by Deutscher Wetterdienst.
