# SPDX-License-Identifier: LGPL-2.1-or-later
#
# This file is formatted with Python Black

from tests.templates import Response, init_logger, ImplRequest
import dbus.service
import dbus

BUS_NAME = "org.freedesktop.impl.portal.Test"
MAIN_OBJ = "/org/freedesktop/portal/desktop"
SYSTEM_BUS = False
MAIN_IFACE = "org.freedesktop.impl.portal.Account"

logger = init_logger(__name__)


def load(mock, parameters={}):
    logger.debug(f"Loading parameters: {parameters}")

    mock.delay: int = parameters.get("delay", 200)
    mock.response: int = parameters.get("response", 0)
    mock.results: bool = parameters.get("results", {})
    mock.expect_close: bool = parameters.get("expect-close", False)


@dbus.service.method(
    MAIN_IFACE,
    in_signature="ossa{sv}",
    out_signature="ua{sv}",
    async_callbacks=("cb_success", "cb_error"),
)
def GetUserInformation(self, handle, app_id, window, options, cb_success, cb_error):
    logger.debug(f"GetUserInformation({handle}, {app_id}, {window}, {options})")

    request = ImplRequest(
        self,
        BUS_NAME,
        handle,
        logger,
        cb_success,
        cb_error,
    )

    if self.expect_close:
        request.wait_for_close()
    else:
        request.respond(Response(self.response, self.results), delay=self.delay)
