'''
Created on 23 Sep 2009

@author: Tom Okas
'''

import urllib.request

#########################################
# Error Handling
#########################################
class PyprError(Exception):
    """ Base class for exceptions in pypr"""
    pass

class BadRequestError(PyprError):
    def __init__(self):
        self.message = "400 Bad request, the parameters you provided did not validate."

class NotAuthorizedError(PyprError):
    def __init__(self):
        self.message = "401 Not authorized, the API key given is not valid, and does not correspond to a user."

class MethodNotAllowedError(PyprError):
    def __init__(self):
        self.message = "405 Method not allowed, you attempted to use a non-SSL connection to Prowl."

class NotAcceptableError(PyprError):
    def __init__(self):
        self.message = "406 Not acceptable, your IP address has exceeded the API limit."
        
class InternalServerError(PyprError):
    def __init__(self):
        self.message = "500 Internal server error, something failed to execute properly on the Prowl side."

#########################################
# pypr
#########################################


class Pypr(object):
    '''
    Pypr (pronounced "piper") is a python library for Prowl ( http://prowlapp.com/ )
    
    Use the add method to send a message, and the verify_api_key to check your key, although this uses one of your requests.
    
    PyPr does not (currently) provide support for provider API keys.
    '''

    base_url = "https://prowlapp.com/publicapi/"
    
    add_suffix = "add"
    verify_suffix = "verify"
    
    errorcodes =  { 
        400:BadRequestError, 
        401:NotAuthorizedError, 
        405:MethodNotAllowedError, 
        406:NotAcceptableError, 
        500:InternalServerError}
    
    def __init__(self, apikey):
        self.apikey = apikey
        self.post = self.add
        
    def add(self , priority=0, application=None , event=None, description=None):
        params = urllib.parse.urlencode({"apikey" : self.apikey ,
                                         "priority":priority ,
                                         "application":application ,
                                         "event":event,
                                         "description":description})
        
        try:
            resp = urllib.request.urlopen(self.base_url + self.add_suffix , params)
        except Exception as e:
            self.handle_status(e.code)
    
    def verify_api_key(self):
        params = urllib.parse.urlencode({ "apikey" : self.apikey })
        
        try:
            resp = urllib.request.urlopen(self.base_url + self.verify_suffix + "?%s" % params)
        except urllib.error.HTTPError as e:
            self.handle_status(e.code)
        
    def handle_status(self, status):
        if status in self.errorcodes:
            raise self.errorcodes[status]
        else:
            raise Exception("Error: error code: " + str(status))
    
            