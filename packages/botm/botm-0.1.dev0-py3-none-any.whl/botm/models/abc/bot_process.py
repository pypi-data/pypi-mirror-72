# botm - Automatize your bots.
# Copyright (C) 2020  Hearot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <https: //www.gnu.org/licenses/>.

from abc import ABC, abstractmethod

from botm.models.dataclasses.bot_information import BotInformation


class BotProcess(ABC):
    @abstractmethod
    def information(self) -> BotInformation:
        raise NotImplementedError

    @abstractmethod
    def is_running(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> bool:
        raise NotImplementedError
