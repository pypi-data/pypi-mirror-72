# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#

from .http_client import HttpClientTransportAdapter


def init(interface_manager):
    """ Sqreen ecosystem transport adapters initialization
    """
    interface_manager.register(HttpClientTransportAdapter())
