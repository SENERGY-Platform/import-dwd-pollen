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

import sched
from datetime import date, timezone, datetime, timedelta
from typing import Optional
import time

from import_lib.import_lib import get_logger, ImportLib

from lib.dwd.data.DWDPollenDataFetcher import DWDPollenDataFetcher
from lib.dwd.meta.DWDPollenAreaMetadataManager import DWDPollenAreaMetadataManager

logger = get_logger(__name__)
slice_size = timedelta(days=30)


class DWDPollenImport:
    def __init__(self, lib: ImportLib, scheduler: sched.scheduler):
        self.__lib = lib
        self.__scheduler = scheduler
        lat = self.__lib.get_config("lat", 51.34)
        long = self.__lib.get_config("long", 12.38)

        logger.info("Loading metadata...")
        meta = DWDPollenAreaMetadataManager()
        self.__area = meta.get_area(lat, long)
        if self.__area is None:
            logger.error("Configured coordinates don't match any DWD pollen area!")
            raise ValueError
        logger.info('Selected region ' + self.__area.region)
        self.__fetcher = DWDPollenDataFetcher()

        self.__filter_pollen = self.__lib.get_config("FilterPollen", [])
        if len(self.__filter_pollen) == 0:
            self.__filter_pollen = None

        dt, _ = self.__lib.get_last_published_datetime()
        if dt is not None:
            if dt.date() < date.today():
                self.import_current()
                logger.debug("Found older data, but not from today. Importing current data")
            else:
                logger.debug("Found older data. and today is included. Will run at next update")
                self.__schedule_next_run(None)
        else:
            logger.debug("Import starting fresh")
            self.import_current()

    def import_current(self):
        dt, values = self.__fetcher.get_data(self.__area, self.__filter_pollen)
        if dt < datetime.fromtimestamp(time.time(), tz=timezone.utc):
            logger.info("Next update scheduled, but not yet available. Retrying in 5 minutes.")
            self.__scheduler.enter(300, 0, self.import_current)
            return
        for value_dt, value in values:
            self.__lib.put(value_dt.astimezone(timezone.utc), value.dict())
        logger.info("Imported " + str(len(values)) + " values")
        self.__schedule_next_run(dt)

    def __schedule_next_run(self, dt: Optional[datetime]):
        if dt is None:
            dt, _ = self.__fetcher.get_data(self.__area, self.__filter_pollen)
        logger.info("Scheduling next run for " + str(dt))
        self.__scheduler.enterabs(dt.timestamp(), 1, self.import_current)
