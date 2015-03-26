#########################################################################
#                                                                       #
# Name:      PQPRO (Interface Service for Quick Protocolo)              #
#                                                                       #
# Project:   PyQPro - Python Quick Protocol                             #
# Module:    Services                                                   #
# Started:   20110108                                                   #
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
View for PQPro
'''

__version__ = "2010123001"

import time
import simplejson
import hashlib

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _

from django.conf import settings
from pqpro.models import Key
from pqpro.isqpro import isqpro

__all__ = [ "entry" , "panel" ]

def hashfunc(string,algorithm):
    '''
    General hashing function
    '''
    if algorithm == 'M':
        # MD5
        result = hashlib.md5(string).hexdigest()
    elif algorithm == 'S':
        # SHA1
        result = hashlib.sha1(string).hexdigest()
    else:
        # None
        result = None
    
    # Return the result
    return result

@csrf_exempt
def entry(request):
    '''
    Process the given query (CSRF control is avoided)
    '''
    
    # Get the query from the user
    query_json=request.raw_post_data
    try:
        # Read the query
        query = simplejson.loads(query_json)
        # Get username
        username = query['config']['user']
        # Load the signature
        signature_remote = request.META['HTTP_SIGNATURE']
    except Exception:
        # Invalid query
        query = None
        signature_remote = None
    
    # If we have a valid query, locate the user
    if query:
        
        # Get user information from the query
        keys = Key.objects.filter(user__username=username)
        # Check if we got only one user with that username
        if len(keys)==1:
            # User found
            key = keys[0].key
            user = keys[0].user
            algorithm = keys[0].algorithm
        else:
            # User denied (not found)
            key = None
            user = None
            algorithm = None
            
    else:
        # User denied (invalid query)
        key = None
        user = None
        algorithm = None
    
    # Key exists and we already loaded it
    if key:
        
        # Check signature of the request
        query_hash = hashfunc(query_json,algorithm)
        signature_local = hashfunc("%s%s%s%s%s" % (query_hash, username, query_hash, key, query_hash),algorithm)
        if signature_local == signature_remote:
            # Build the protocolo object
            proto=isqpro(user,request,settings.PQPRO_ENVIROMENT)
            # Process the query
            try:
                answer = proto.query(query)
            except:
                user=None
                username=None
                algorithm=None
                key=None
                keys=None
                raise
            if not answer: answer=''
        else:
            
            answer = 'Not allowed!'
        # Build the answer json
        answer_json = simplejson.dumps(answer)
        # Build the signature from the answer
        answer_hash = hashfunc(answer_json,algorithm)
        signature = hashfunc("%s%s%s%s%s" % (answer_hash, username, answer_hash, key, answer_hash),algorithm)
    else:
        
        answer_json = 'Not allowed!'
        signature = None
    
    # Add the headers
    response = HttpResponse(answer_json, mimetype='application/json')
    response['Signature'] = signature
    return response

def example(cid,query):
    '''
    Function to build an example object for the list of examples in the panel
    '''
    e={}
    e['cid']=cid
    e['query']=simplejson.dumps(simplejson.loads(query), sort_keys=True, indent=4)
    return e

@login_required
def panel(request):
    '''
    Show the panel
    '''
    
    # Initialization
    started=time.time()
    template='pqpro/panel.html'
    output={}
    output['user']=request.user
    
    # Add exampls
    output['examples']=[]
    if settings.PQPRO_EXAMPLES:
        for ex in settings.PQPRO_EXAMPLES:
            output['examples'].append(example(*ex))
    else:
        output['examples'].append(example('Basic 1','{"config": {"action": "tarificar","auth": "127.0.0.1","enviroment": "dev","service": "paquetes","user":"br0th3r"},"field1": 3}'));
        output['examples'].append(example('Basic 2','{"123":"456"}'));
    
    # Process the query
    query_json=request.POST.get('query',None)
    
    if query_json:
        try:
            # Read the query
            query = simplejson.loads(query_json)
        except Exception:
            # Invalid query
            query = None
    else:
        # Invalid query
        query = None
    
    # If we have a query to process, send it to pqpro
    if query:
        # Save the query and the answer already formated
        output['query']=simplejson.dumps(query, sort_keys=True, indent=4)
        # Build the protocolo object
        proto=isqpro(request.user,request,settings.PQPRO_ENVIROMENT)
        
        # Find key
        keys=request.user.security.all()
        if len(keys)==1:
            key=keys[0].key
        else:
            raise IOError,"Access key not found for this user!"
        
        # Encrypt private array
        if 'private*' in query:
            # Encrypt
            query['private'] = proto._encrypt(query['private*'], key)
            # Remove private*
            query.pop('private*',None)
        
        # Send the query
        answer = proto.query(query)
        
        # Decrypt private array
        if 'private' in answer:
            # Encrypt
            answer['private*'] = proto._decrypt(answer['private'], key)
            # Remove private*
            answer.pop('private',None)
        
        if answer:
            output['answer']=simplejson.dumps(answer, sort_keys=True, indent=4)
        else:
            output['answer']=''
    else:
        output['query']=query_json
        output['error']=True
        output['answer']=_('Not valid JSON!')
    
    # Compute total execution time
    output['total_time']="%2.4f" % (time.time()-started)
    
    # Show the web
    ctx = RequestContext(request,output)
    return render_to_response(template, context_instance=ctx)

