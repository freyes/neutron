#!/usr/bin/env python

# Copyright 2011 VMware, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# If ../neutron/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...

from oslo_config import cfg
from oslo_log import log
from oslo_service import service as common_service

from neutron._i18n import _LI
from neutron import service

LOG = log.getLogger(__name__)


def eventlet_rpc_server():
    LOG.info(_LI("Eventlet based AMQP RPC server starting..."))
    rpc_workers_launcher = common_service.ProcessLauncher(
        cfg.CONF, wait_interval=1.0
    )
    try:
        service.start_rpc_workers(rpc_workers_launcher)
    except NotImplementedError:
        LOG.info(_LI("RPC was already started in parent process by "
                     "plugin."))
    else:
        rpc_workers_launcher.wait()
