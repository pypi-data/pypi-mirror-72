# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#

from .client import ClientTracer
from .server import ServerTracer


def init(interface_manager):
    """ Sqreen ecosystem tracers initialization
    """
    interface_manager.register(ClientTracer())
    interface_manager.register(ServerTracer())
