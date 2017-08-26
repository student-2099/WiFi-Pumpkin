#!/usr/bin/env python2.7
from logging import getLogger,ERROR
getLogger('scapy.runtime').setLevel(ERROR)

"""
Author : Marcos Nesster - mh4root@gmail.com  PocL4bs Team
Licence : GPL v3

Description:
    WiFi-Pumpkin - Framework for Rogue Wi-Fi Access Point Attack.

Copyright:
    Copyright (C) 2015-2017 Marcos Nesster P0cl4bs Team
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

from sys import argv,exit,version_info
import core.utility.constants as C
if version_info.major != 2:
    exit('[!] WiFi-Pumpkin need Python 2 :(')

def checkAppQTDesigner(style):
    global main
    if 'gtk+' in str(style).lower():
        main.setStyle(QStyleFactory.create(C.GTKTHEME))

if __name__ == '__main__':
    from core.loaders.checker.depedences import check_dep_pumpkin
    from core.loaders.checker.networkmanager import CLI_NetworkManager,UI_NetworkManager
    from core.utility.collection import SettingsINI
    from core.main import Initialize

    check_dep_pumpkin()
    from os import getuid
    if not getuid() == 0:
        exit('[{}!{}] WiFi-Pumpkin must be run as root.'.format(C.RED,C.ENDC))

    from PyQt4.QtGui import QApplication,QIcon,QStyleFactory
    main = QApplication(argv)
    checkAppQTDesigner(main.style().objectName())

    print('Loading GUI...')
    app = Initialize()
    app.setWindowIcon(QIcon('icons/icon.ico'))
    app.center()
    # check if Wireless connection
    conf = SettingsINI(C.CONFIG_INI)
    if  conf.get_setting('accesspoint','checkConnectionWifi',format=bool):
        networkcontrol = CLI_NetworkManager() # add all interface avaliable for exclude
        app.networkcontrol = networkcontrol
        if networkcontrol.run():
            if  networkcontrol.isWiFiConnected() and len(networkcontrol.ifaceAvaliable) > 0:
                settings = UI_NetworkManager(app)
                settings.setWindowIcon(QIcon('icons/icon.ico'))
                settings.show()
                exit(main.exec_())
    app.show()

    print('WiFi-Pumpkin Running!')
    exit(main.exec_())
