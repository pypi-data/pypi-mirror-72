#!/usr/bin/env python
# -*- coding: utf-8 -*-
from djangohotsauce.controllers.wsgi import WSGIController
from djangohotsauce.utils.log import configure_logging
log = configure_logging('OAuthController')

from djangohotsauce.http.oauthclient import (
     OAuthClient,
     OAuthResponseMiddleware,
     google
     )

__all__ = ['OAuthController', 'oauthclient']

class OAuthController(OAuthResponseMiddleware):
    pass

oauthclient = OAuthClient
