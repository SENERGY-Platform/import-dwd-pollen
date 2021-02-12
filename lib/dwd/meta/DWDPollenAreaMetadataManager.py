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

from typing import List, Optional

import requests

from lib.dwd.meta.DWDPollenArea import DWDPollenArea

DWD_BASE_URL = "https://maps.dwd.de"
DWD_POLLEN_METADATA_URL = DWD_BASE_URL + "/geoserver/dwd/ows?service=WFS&version=2.0.0&request=GetFeature&typeName" \
                                         "=dwd:Pollenfluggebiete&outputFormat=application/json"


class DWDPollenAreaMetadataManager:
    def __init__(self):
        self.__areas: List[DWDPollenArea] = []
        self.refresh_metadata()

    def refresh_metadata(self):
        r = requests.get(DWD_POLLEN_METADATA_URL)
        if not r.ok:
            raise RuntimeError("Error collecting metadata from DWD")
        j = r.json()
        if "features" not in j:
            raise RuntimeError("Error collecting metadata from DWD. Missing 'features' from response")
        for feature in j["features"]:
            if "geometry" not in feature or "properties" not in feature or "coordinates" not in \
                    feature["geometry"] or "GEN" not in feature["properties"]:
                raise RuntimeError("Error collecting metadata from DWD. Missing data from area")
            self.__areas.append(DWDPollenArea(feature["properties"]["GEN"], feature["geometry"]["coordinates"]))

    def get_area(self, lat: float, long: float) -> Optional[DWDPollenArea]:
        for area in self.__areas:
            if self.__point_in_area(area, lat, long):
                return area

    @staticmethod
    def __point_in_area(area: DWDPollenArea, lat: float, long: float) -> bool:
        for poly in area.polygon:
            inside = False
            x = long
            y = lat
            i = 0
            j = len(poly) - 1
            for _ in poly:
                xi = poly[i][0]
                yi = poly[i][1]
                xj = poly[j][0]
                yj = poly[j][1]
                intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
                if intersect:
                    inside = not inside
                j = i
                i += 1
            if inside:
                return True
        return False


if __name__ == "__main__":
    manager = DWDPollenAreaMetadataManager()
    area = manager.get_area(51.34, 12.38)
    if area.region != "Tiefland Sachsen":
        raise Exception("unexpected area")
    print("init area manager completed")
