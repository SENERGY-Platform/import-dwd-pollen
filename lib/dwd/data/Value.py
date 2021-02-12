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


class Value(object):

    def __init__(self, today: float, today_description: str,
                 tomorrow: float, tomorrow_description: str,
                 day_after_tomorrow: float, day_after_tomorrow_description: str,
                 pollen: str, region: str):
        self.today = today
        self.today_description = today_description
        self.tomorrow = tomorrow
        self.tomorrow_description = tomorrow_description
        self.day_after_tomorrow = day_after_tomorrow
        self.day_after_tomorrow_description = day_after_tomorrow_description
        self.pollen = pollen
        self.region = region


    def dict(self) -> dict:
        d = {
            "today": self.today,
            "today_description": self.today_description,
            "tomorrow": self.tomorrow,
            "tomorrow_description": self.tomorrow_description,
            "day_after_tomorrow": self.day_after_tomorrow,
            "day_after_tomorrow_description": self.day_after_tomorrow_description,
            "pollen": self.pollen,
            "region": self.region,
        }
        return d
