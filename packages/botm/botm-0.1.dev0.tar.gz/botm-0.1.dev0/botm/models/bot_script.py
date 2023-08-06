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

import signal
from subprocess import Popen, TimeoutExpired
from typing import List

from telegram_me import Link

from botm.models.abc.bot_process import BotInformation, BotProcess
from botm.errors import AlreadyRunningError, NotRunningError


class BotScript(BotProcess):
    args: List[str]
    timeout: int = 10
    username: str
    _process: Popen

    def __init__(self, username: str, args: List[str], timeout: int = 10):
        self.args = args
        self.timeout = timeout
        self.username = username

    def information(self) -> BotInformation:
        information = Link.from_username(self.username)

        return BotInformation(
            name=information.name,
            running=self.is_running(),
            username=self.username,
            description=information.bio,
            image=information.image,
        )

    def is_running(self) -> bool:
        if not isinstance(self._process, Popen):
            return False

        return self._process.poll() is None

    def start(self) -> bool:
        if self.is_running():
            raise AlreadyRunningError

        self._process = Popen(self.args)
        return self.is_running()

    def stop(self) -> bool:
        if not self.is_running():
            raise NotRunningError

        self._process.terminate()

        try:
            self._process.wait(timeout=self.timeout)
        except TimeoutExpired:
            self._process.kill()

        del self._process
        self._process = None

        return True
