============
django-pqpro
============

Python Quick Protocol development for Django
============================================

* Let's say you need to implement a robust JSON based webservice focusing strong on security, granular control over clients and several other features.
* Let's say you are the PQPRO-SERVER and the system that connect to you is the PQPRO-CLIENT.
* Let's say that you need full centralized control over your PQPRO-CLIENT's clients (FINAL-USER or USERS).
* Let's say you may want to decide what to render to who (using the same logic).
* Let's say you may want to show informatino from different sources depending on who is connecting (different products, different prices, different aspect, different language,...).
* Let's say you want to make your PQPRO-CLIENTS easy to connect to you...they just need to know how to build a Dictionary on their usual programming language.
* Wouldn't be easier to implement a webservice then?
* This is what PQPro does.

Features
--------

* HTTP security standars like SSL support or HTTP AUTH.
* Test panel so you can check what the server is answering on each time with capabilites to work as another user.
* Digital signature on each package implementing a JSON-Signature on top of HTTP HEADER (no to mess up the body)
* Easy integration with Django (and with Django models)
* IP control for PQPRO-CLIENT and also support for FINAL-USER control.
* Ŝession over Session support: allow you to open a local session on PQPRO-SERVER to manage remote sessions locally (PQPRO-CLIENT sessions), so you can identify each client connected to yours PQPRO-CLIENT.
* Capable to send/receive encrypted information (withouth loosing JSON visibility and traceback).
* Capable to send/receive feedback information (which the PQPRO-CLIENT can not change)
* Capable to manage internal structures insid ethe answer that will never leave the PQPRO-SERVER.
* Granular control on remote calls: 4 system calls to validate query, preprocess query, prepare response and postprocess the answer. In this way you keep things where they belong.
* Integrated validators to make easy and quick validation of the incoming query.
* And all Django feature to your disposal.

Examples of uses:
-----------------

* 2009: Insurance company to get and send product's prices on real time
* 2010: Private tranport company to sell their products online (like big companies do)
* 2012: Medical company to sell their products on several websites they own with different prices, different aspect, allowing the PQPRO-CLIENT to work without a Database there. PQPRO-SERVER was managing users authentication, users sessions, shopping carts, etc... Google even realized they are the same website (either the same owner).
* 2013: Data acquisition system for industrial enviroment where a very robust security system was mandatory.


Installation:
=============

settings.py
-----------

``At the beginning``
DEBUG_PQPRO = True


``Somewhere``

PQPRO_ENVIROMENT = 'dev'     # dev / test / real

PQPRO_SECRET_KEY = '12341234123412341234123412341234' # Make this unique, and don't share it with anybody. (PQPro Secret's key)

PQPRO_DEBUGGER = DEBUG and DEBUG_PQPRO

PQPRO_EXAMPLES = []

PQPRO_EXAMPLES.append(('Example 1','{"config": {"action": "getprice","auth": "127.0.0.1","enviroment": "dev","service": "package","user":"br0th3r"},"request": {"cp":"29003","kg":3.0}}'))

PQPRO_EXAMPLES.append(('Example 2','{"123":"456"}'))

``Add the project to your INSTALLED_APPS``

urls.py
-------

url(r'^pqpro/',     include('pqpro.urls')),

(r'^pqpro$',        include('pqpro.urls')),

(r'^pqpro/',        include('pqpro.urls')),

Why this project?
=================

This is a project I build during christmas from 2010 to 2011.

The idea of PQPro came up when I was workig for a company that needed to write several connectors to different providers to get prices for a huge number of products on real time and be able to deliver this information on real time also to clients. Everything using an API and like a WS.

After working with several technologies for 3 years (2008-2009-2010) I realized that SOAP-RPC was slow to integrate (too much provider's logic in the client side), XML was a mess (too much meta data for such a few information to send/receive), I also saw many ugly implemtations for SOAP+XML (combined in several non-standard ways).

So I decided to write my own library for Django, focusing on several points that were important to me.

TODO
====

Add full documentation explaning how to use it.

License
=======

Copyright &copy; 2015 Juan Miguel Taboada Godoy.

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007.
