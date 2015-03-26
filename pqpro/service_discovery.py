#########################################################################
#                                                                       #
# Name:      FINDPACKAGE (Class for service discovery)                  #
#                                                                       #
# Project:   PyQPro - Python Quick Protocol                             #
# Module:    Services                                                   #
# Started:   20101230                                                   #
#                                                                       #
# Important: WHEN EDITING THIS FILE, USE SPACES TO INDENT - NOT TABS!   #
#                                                                       #
#########################################################################
#                                                                       #
# Juan Miguel Taboada Godoy <juanmi@centrologic.com>                    #
#                                                                       #
# This file is part of PQPRO.                                           #
#                                                                       #
# PQPRO is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 2 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# PQPro is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
# You should have received a copy of the GNU General Public License     #
# along with PQPRO.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                       #
#########################################################################
'''
Class to handle discovery of services
'''

__version__ = "2010123000"

import os
import os.path

import pqprows

__all__ = [ "service_discovery" ]

class service_discovery:
    
    def __init__(self):
        
        # Inicialize system
        self.__system={}
        # Inicialize services
        self.__services={}
        # For each directory
        for service in pqprows.__all__:
            # Import it
            module = __import__("pqprows.%s" % (service), fromlist=["pqprows"])
            for action in module.__all__:
                # If the element is not in the services already
                if service not in self.__services:
                    # Inicialize the service
                    self.__services[service]=[]
                    self.__system[service]={}
                # Append the action
                self.__services[service].append(action)
                self.__system[service][action]=None
    
    def services(self):
        # Return the discovered services
        return self.__services
    
    def build(self,service,action):
        # Integrity test
        if service in self.__system and action in self.__system[service]:
            # Look up if we already imported the service
            if not self.__system[service][action]:
                # We didn't import yet, do it know
                path = "pqprows.%s.%s" % (service,action)
                try:
                    module = __import__("%s.sqpro" % (path), fromlist=[path])
                except ImportError, e:
                    # Display error message
                    raise IOError,"Error while importing: %s.sqpro (ERROR: %s)" % (path,e)
                self.__system[service][action]=module
                
            # Return the object related to this service
            return self.__system[service][action]
        else:
            raise IOError,"Action not found for this service"

if __name__ == "__main__":
    service=service_discovery()
    services=service.services()
    print services
    for s in services:
        for a in services[s]+services[s]:
            obj=service.build(s,a)
            print obj
            obj=obj.sqpro("User","Enviroment")
