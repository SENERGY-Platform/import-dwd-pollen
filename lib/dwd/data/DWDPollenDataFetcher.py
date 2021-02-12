#  Copyright 2021 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import datetime
from typing import Tuple, List, Optional, Dict

import requests
from import_lib.import_lib import get_logger
from pytz import timezone

from lib.dwd.data.Value import Value
from lib.dwd.meta.DWDPollenArea import DWDPollenArea

DWD_BASE_URL = "https://opendata.dwd.de"
DWD_POLLEN_DATA_URL = DWD_BASE_URL + "/climate_environment/health/alerts/s31fg.json"
logger = get_logger(__name__)


class DWDPollenDataFetcher:
    def __init__(self):
        self.__zone = timezone('Europe/Berlin')

    def get_data(self, area: DWDPollenArea, filter_pollen: Optional[List[str]]) -> Tuple[datetime, List[Tuple[datetime, Value]]]:
        r = requests.get(DWD_POLLEN_DATA_URL)
        if not r.ok:
            raise RuntimeError("Error contacting DWD Api")
        j = r.json()
        last_update = self.__zone.localize(datetime.fromisoformat(j["last_update"][:16]))
        next_update = self.__zone.localize(datetime.fromisoformat(j["next_update"][:16]))

        legend_str_id: Dict[str, int] = {"-1": -1}
        legend_id_desc: Dict[int, str] = {-1: "no forecast"}
        for key, value in j["legend"].items():
            if not key.endswith('_desc'):
                key = key.removeprefix('id')
                legend_str_id[value] = int(key)
        for key, value in j["legend"].items():
            if key.endswith('_desc'):
                key = key.removesuffix('_desc')
                key = key.removeprefix('id')
                legend_id_desc[int(key)] = value

        for region in j["content"]:
            if region["partregion_name"] == area.region:
                values: List[Tuple[datetime, Value]] = []
                for polle, data in region["Pollen"].items():
                    if filter_pollen is None or polle in filter_pollen:
                        values.append((last_update, Value(legend_str_id[data["today"]], legend_id_desc[legend_str_id[data["today"]]],
                                                          legend_str_id[data["tomorrow"]], legend_id_desc[legend_str_id[data["tomorrow"]]],
                                                          legend_str_id[data["dayafter_to"]], legend_id_desc[legend_str_id[data["dayafter_to"]]],
                                                          polle, area.region)))
                return next_update, values


if __name__ == "__main__":
    from lib.dwd.meta.DWDPollenAreaMetadataManager import DWDPollenAreaMetadataManager
    manager = DWDPollenAreaMetadataManager()
    area = manager.get_area(51.34, 12.38)
    fetcher = DWDPollenDataFetcher()
    values = fetcher.get_data(area, None)

    import json
    for time, value in values[1]:
        print(str(time), json.dumps(value.dict(), ensure_ascii=False))
    print('next update: ', str(values[0]))
