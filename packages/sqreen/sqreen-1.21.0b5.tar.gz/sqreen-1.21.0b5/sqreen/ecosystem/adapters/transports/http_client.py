# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
import uuid

from ....constants import ACTIONS
from ....rules import RuleCallback
from ....workflow import Transport


class HttpClientTransportCallback(RuleCallback):

    def pre(self, instance, args, kwargs, **options):
        try:
            host_ip, host_port = instance.sock.getpeername()
        except Exception:
            host_ip, host_port = None, None

        tracing_identifier_prefix = self.runner.settings.tracing_identifier_prefix
        if tracing_identifier_prefix is not None:
            request_identifier = uuid.uuid4()
            tracing_identifier = "{}.{}".format(tracing_identifier_prefix, request_identifier)
        else:
            tracing_identifier = None
            request_identifier = None

        transport = Transport({
            "host": instance.host or host_ip,
            "host_ip": host_ip,
            "host_port": host_port,
            "tracing_identifier_prefix": tracing_identifier_prefix,
            "tracing_identifier": tracing_identifier,
            "request_identifier": request_identifier,
        })

        context = self.runner.interface_manager.call("context")
        if not self.runner.interface_manager.call("new_data_out_pre", context, transport) \
                or tracing_identifier is None:
            return

        method, url, body, headers, encode_chunked = args
        new_headers = dict(headers)
        new_headers["X-Sqreen-Trace-Identifier"] = tracing_identifier
        return {
            "status": ACTIONS["MODIFY_ARGS"],
            "args": ((method, url, body, new_headers, encode_chunked), {}),
        }


class HttpClientTransportAdapter:

    def instrumentation_callbacks(self, runner, storage):
        return [
            HttpClientTransportCallback.from_rule_dict({
                "name": "ecosystem_http_client",
                "rulespack_id": "ecosystem/transport",
                "block": True,
                "test": False,
                "hookpoint": {
                    "klass": "http.client::HTTPConnection",
                    "method": "_send_request"
                },
                "callbacks": {},
            }, runner, storage)
        ]
