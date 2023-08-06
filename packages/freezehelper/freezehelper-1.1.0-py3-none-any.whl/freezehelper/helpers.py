# -*- coding: UTF-8 -*-
# Copyright (C) 2020 Brandon M. Pace
#
# This file is part of freezehelper
#
# freezehelper is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# freezehelper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with freezehelper.
# If not, see <https://www.gnu.org/licenses/>.

"""module for small helper functions"""


import multiprocessing
import os
import sys


frozen = getattr(sys, "frozen", False)
from_source = not frozen


is_linux = sys.platform.startswith("linux")
is_not_linux = not is_linux
is_mac = sys.platform == "darwin"
is_not_mac = not is_mac
is_windows = sys.platform == "win32"
is_not_windows = not is_windows


def get_executable_dir(resolve_links: bool = True) -> str:
    return os.path.dirname(get_executable_path(resolve_links))


def get_executable_path(resolve_links: bool = True) -> str:
    if frozen:
        my_path = sys.executable
    else:
        my_path = sys.argv[0]
    if resolve_links:
        my_path = os.path.realpath(my_path)
    return os.path.abspath(my_path)


def get_is_child_process() -> bool:
    if is_windows and frozen and (len(sys.argv) >= 2) and (sys.argv[1] == "--multiprocessing-fork"):
        return True  # frozen Windows executable child process
    elif multiprocessing.current_process().name != "MainProcess":
        return True
    else:
        return False

