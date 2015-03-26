#########################################################################
#                                                                       #
# Name:      SQPRO (Service definition for Quick Protocolo              #
#                                                                       #
# Project:   PQPRO                                                      #
# Module:    Services                                                   #
# Started:   20130319                                                   #
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
# PQPRO is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
# You should have received a copy of the GNU General Public License     #
# along with PQPRO.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                       #
#########################################################################
'''
<EDIT HERE: Service default definition>
'''

__version__ = "yyyymmdd00"

# Get the Interface Service definition for Quick Protocolo
from pqpro.isqpro import isqpro

__all__ = [ "sqpro" ]


class sqpro(isqpro):
    def validator(self):
        return True
    
    def preprocessor(self,request):
        return request
    
    def query(self,query):
        return query
    
    def postprocessor(self,answer):
        return answer

