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

"""Default HTML file renderer"""

from evariste.plugins.renderer.jinja2.file import Jinja2FileRenderer


class HtmlFileRenderer(Jinja2FileRenderer):
    """Default HTML file renderer"""

    # pylint: disable=too-few-public-methods

    plugin_type = "renderer.html.file"
    keyword = "renderer.html.file.default"
    extension = "html"
