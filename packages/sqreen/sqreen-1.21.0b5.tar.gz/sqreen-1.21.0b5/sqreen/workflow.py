# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Sqreen Agent Workflow
"""

import logging

from ._vendors.sqreen_security_signal_sdk import Signal, SignalType
from .runtime_infos import get_agent_type
from .utils import HAS_TYPING, now

if HAS_TYPING:
    from datetime import datetime
    from typing import Optional

LOGGER = logging.getLogger(__name__)


class Context(dict):
    pass


class Transport(dict):
    pass


class Workflow:

    def __init__(self, runner):
        LOGGER.debug("Init workflow")
        self.runner = runner

    def context(self):  # type: () -> Context
        # TODO use the runtime storage
        return Context({})

    def maybe_record_transport(self, scope, transport, at=None):
        # type: (str, Transport, Optional[datetime]) -> bool
        sampler = self.runner.tracing_sampler
        signal_client = self.runner.signal_client
        if sampler is None or signal_client is None:
            return False
        if at is None:
            at = now()
        decision = sampler.should_sample(scope=scope, at=at)
        if not decision:
            return False
        payload = self.runner.interface_manager.call("format_payload", scope, transport)
        if payload is None:
            LOGGER.debug("No tracing payload formatted, skipping")
            return False
        signal = Signal(
            type=SignalType.POINT,
            signal_name="tracing.{}".format(scope),
            payload_schema="tracing/{}-2020-04-21".format(scope),
            payload=payload,
            source="sqreen:agent:{}".format(get_agent_type()),
            trigger=decision.attrs["trigger"],
            time=at,
        )
        LOGGER.debug("Sending signal %r", signal)
        signal_client.signal(**signal)
        return bool(decision)

    def new_data_in_pre(self, context, transport):  # type: (Context, Transport) -> bool
        return self.maybe_record_transport("server", transport)

    def new_data_in_post(self, context, transport):  # type: (Context, Transport) -> bool
        return False

    def new_data_out_pre(self, context, transport):  # type: (Context, Transport) -> bool
        return self.maybe_record_transport("client", transport)

    def new_data_out_post(self, context, transport):  # type: (Context, Transport) -> bool
        return False
