# -*- coding: UTF-8 -*-
# Copyright (C) 2019, 2020 Brandon M. Pace
#
# This file is part of logcontrol
#
# logcontrol is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# logcontrol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with logcontrol.
# If not, see <https://www.gnu.org/licenses/>.

"""Package to simplify and centralize handling of loggers created throughout a program"""


__author__ = "Brandon M. Pace"
__copyright__ = "Copyright 2019, 2020 Brandon M. Pace"
__license__ = "GNU LGPL 3+"
__maintainer__ = "Brandon M. Pace"
__status__ = "Production"
__version__ = "0.2.1"


import logging

from .constants import DEBUG, INFO, WARNING, ERROR, CRITICAL, log_level_integers, log_level_strings

# Items to add loggers and handlers
from .loggers import add_handler, has_handler, log_to_console, register_logger, remove_handler

# Items to toggle logger settings
from .loggers import disable_propagation, enable_propagation, remove_log_file, set_level, set_log_file

# Items to get current configuration of specific group or root logger
from .loggers import current_level, current_level_name, log_files, logging_to_console, propagation_enabled

# Information about groups
from .loggers import group_level_names, group_levels, group_names

logger = logging.getLogger(__name__)
