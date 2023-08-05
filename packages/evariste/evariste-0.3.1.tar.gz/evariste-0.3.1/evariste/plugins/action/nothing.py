# Copyright Louis Paternault 2015-2020
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Actions that does nothing; simply provides a link to download file."""

import logging

from evariste.plugins.action import Action, Report

LOGGER = logging.getLogger(__name__)


class Raw(Action):
    """Do nothing. Source is not compiled."""

    keyword = "action.raw"
    priority = -float("inf")

    def match(self, value):
        # pylint: disable=unused-argument
        return True

    def compile(self, path):
        return Report(path, targets=[], success=True)


class NoPlugin(Action):
    """Special action used when no plugin is found."""

    keyword = "action.noplugin"
    priority = -float("inf")

    def match(self, value):
        # pylint: disable=unused-argument
        return False

    def compile(self, path):
        message = "Error: Plugin not found for '{}'.".format(path.from_source)
        LOGGER.warning(message)
        return Report(path, success=False, log=message,)
