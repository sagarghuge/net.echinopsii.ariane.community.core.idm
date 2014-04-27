# CC installer IDM cache JGroup configuration unit processor
#
# Copyright (C) 2014 Mathilde Ffrench
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
import json
import os
from tools.AConfParamNotNone import AConfParamNotNone
from tools.AConfUnit import AConfUnit
from tools.NetworkTools import getSystemNetworkInterfacesAndIPaddresses, isPortAvailable, printSystemNetworkInterfaces

__author__ = 'mffrench'


class cpJGroupsTCPBindAddress(AConfParamNotNone):

    name = "##JGroupsTCPBindAddress"
    description = "CC IDM JGroups TCP bind address"
    hide = False

    def __init__(self):
        self.value = None


class cpJGroupsMPINGBindAddress(AConfParamNotNone):

    name = "##JGroupsMPINGBindAddress"
    description = "CC IDM JGroups MPING bind address"
    hide = False

    def __init__(self):
        self.value = None


class cpJGroupsTCPBindPort(AConfParamNotNone):

    name = "##JGroupsTCPBindPort"
    description = "CC IDM JGroups TCP bind port"
    hide = False

    def __init__(self):
        self.value = None


class cuIDMCacheJGroupsProcessor(AConfUnit):

    def __init__(self, targetConfDir):
        self.confUnitName = "CC IDM cache JGroups"
        self.confTemplatePath = os.path.abspath("resources/templates/components/idm-jgroups-tcp.xml.tpl")
        self.confFinalPath = targetConfDir + "jgroups-tcp.xml"
        JGroupsTCPBindAddress = cpJGroupsTCPBindAddress()
        JGroupsTCPBindPort = cpJGroupsTCPBindPort()
        JGroupsMPINGBindAddress = cpJGroupsMPINGBindAddress()
        self.paramsDictionary = {
            JGroupsTCPBindAddress.name: JGroupsTCPBindAddress,
            JGroupsTCPBindPort.name: JGroupsTCPBindPort,
            JGroupsMPINGBindAddress.name: JGroupsMPINGBindAddress
        }


class idmCacheJGroupsSyringe:

    def __init__(self, targetCacheDir, silent):
        self.IDMCacheJGroupsProcessor = cuIDMCacheJGroupsProcessor(targetCacheDir)
        idmCacheJGroupCUJSON = open("resources/configvalues/components/cuIDMCacheJGroups.json")
        self.idmCacheJGroupsCUValues = json.load(idmCacheJGroupCUJSON)
        idmCacheJGroupCUJSON.close()
        self.silent = silent

    def shootBuilder(self):
        #DEFAULT VALUES
        idmCacheTCPBindAddressDefault = self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name]
        idmCacheTCPBindAddressDefaultUI = "[default - "+idmCacheTCPBindAddressDefault+"]"

        idmCacheTCPBindPortDefault = self.idmCacheJGroupsCUValues[cpJGroupsTCPBindPort.name]
        idmCacheTCPBindPortDefaultUI = "[default - "+idmCacheTCPBindPortDefault+"]"

        idmCacheMPINGBindAddressDefault = self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name]
        idmCacheMPINGBindAddressDefaultUI = "[default - "+idmCacheMPINGBindAddressDefault+"]"

        availabeIPAddresses = getSystemNetworkInterfacesAndIPaddresses()

        #BEGIN CONFIGURATION SETTING
        if not self.silent:
            idmCacheJGroupsTCPBindingAddressValid = False
            while not idmCacheJGroupsTCPBindingAddressValid:
                if len(availabeIPAddresses) > 0:
                    printSystemNetworkInterfaces(availabeIPAddresses)
                    self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name] = input("%-- >> Define CC idm cache TCP bind address " + idmCacheTCPBindAddressDefaultUI + ": ")

                if self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name] != "":
                    idmCacheJGroupsTCPBindingAddressValid = True
                    idmCacheTCPBindAddressDefault = self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name]
                    idmCacheTCPBindAddressDefaultUI = "[default - "+idmCacheTCPBindAddressDefault+"]"
                elif idmCacheTCPBindAddressDefault != "":
                    idmCacheJGroupsTCPBindingAddressValid = True
                    self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name] = idmCacheTCPBindAddressDefault

            idmCacheJGroupsTCPBindingPortValid = False
            while not idmCacheJGroupsTCPBindingPortValid:
                tcpBindPort = 0
                tcpBindPortStr = input("%-- >> Define CC idm cache TCP bind port " + idmCacheTCPBindPortDefaultUI + ": ")

                if tcpBindPortStr is not None and tcpBindPortStr != "":
                    tcpBindPort = int(tcpBindPortStr)
                elif idmCacheTCPBindPortDefault != "":
                    tcpBindPort = int(idmCacheTCPBindPortDefault)
                    tcpBindPortStr = idmCacheTCPBindPortDefault

                if (tcpBindPort <= 0) and (tcpBindPort > 65535):
                    print("%-- !! Invalid JGroups TCP bind port " + tcpBindPortStr + ": not in port range")
                elif isPortAvailable(self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name], tcpBindPort):
                    idmCacheJGroupsTCPBindingPortValid = True
                    self.idmCacheJGroupsCUValues[cpJGroupsTCPBindPort.name] = tcpBindPortStr
                    idmCacheTCPBindPortDefault = self.idmCacheJGroupsCUValues[cpJGroupsTCPBindPort.name]
                    idmCacheTCPBindPortDefaultUI = "[default - "+idmCacheTCPBindPortDefault+"]"

            idmCacheJGroupsMPINGBindingAddressValid = False
            while not idmCacheJGroupsMPINGBindingAddressValid:
                if len(availabeIPAddresses) > 0:
                    printSystemNetworkInterfaces(availabeIPAddresses)
                    self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name] = input("%-- >> Define CC idm cache MPING bind address " + idmCacheMPINGBindAddressDefaultUI + ": ")

                if self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name] != "":
                    idmCacheJGroupsMPINGBindingAddressValid = True
                    idmCacheMPINGBindAddressDefault = self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name]
                    idmCacheMPINGBindAddressDefaultUI = "[default - "+idmCacheMPINGBindAddressDefault+"]"
                elif idmCacheMPINGBindAddressDefault != "":
                    idmCacheJGroupsMPINGBindingAddressValid = True
                    self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name] = idmCacheMPINGBindAddressDefault

        else:
            self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name] = idmCacheTCPBindAddressDefault
            self.idmCacheJGroupsCUValues[cpJGroupsTCPBindPort.name] = idmCacheTCPBindPortDefault
            self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name] = idmCacheMPINGBindAddressDefault

        self.IDMCacheJGroupsProcessor.setKeyParamValue(cpJGroupsTCPBindAddress.name, self.idmCacheJGroupsCUValues[cpJGroupsTCPBindAddress.name])
        self.IDMCacheJGroupsProcessor.setKeyParamValue(cpJGroupsTCPBindPort.name, self.idmCacheJGroupsCUValues[cpJGroupsTCPBindPort.name])
        self.IDMCacheJGroupsProcessor.setKeyParamValue(cpJGroupsMPINGBindAddress.name, self.idmCacheJGroupsCUValues[cpJGroupsMPINGBindAddress.name])

    def inject(self):
        idmCacheJGroupCUJSON = open("resources/configvalues/components/cuIDMCacheJGroups.json", "w")
        jsonStr = json.dumps(self.idmCacheJGroupsCUValues, sort_keys=True, indent=4, separators=(',', ': '))
        idmCacheJGroupCUJSON.write(jsonStr)
        idmCacheJGroupCUJSON.close()
        self.IDMCacheJGroupsProcessor.process()