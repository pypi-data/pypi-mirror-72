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

"""Package to provide simple check for being frozen (compiled) and other items"""


__author__ = "Brandon M. Pace"
__copyright__ = "Copyright 2020 Brandon M. Pace"
__license__ = "GNU LGPL 3+"
__maintainer__ = "Brandon M. Pace"
__status__ = "Production"
__version__ = "1.1.0"


from .helpers import get_executable_dir, get_executable_path
from .helpers import is_linux, is_mac, is_windows, is_not_linux, is_not_mac, is_not_windows
from .helpers import from_source, frozen, get_is_child_process

executable_dir = get_executable_dir()
executable_path = get_executable_path()

is_child_process = get_is_child_process()
is_main_process = not is_child_process
