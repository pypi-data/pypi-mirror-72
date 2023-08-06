from . import resources
from jsonschema import validate
from jsonschema.exceptions import ValidationError

import aiohttp_client
import importlib.resources as pkg_resources
import json
import logging

log = logging.getLogger("amplitude-client")

API_URL = "https://api.amplitude.com/2/httpapi"


class AmplitudeLogger:
    def __init__(self, api_key: str):
        self.api_key = api_key

        self.api_schema = json.loads(pkg_resources.read_text(resources, "schema.json"))

    async def log_event(self, event):
        # Amplitude API requires (user_id OR device_id) AND event_type

        event = {"api_key": self.api_key, "events": [event]}

        try:
            validate(instance=event, schema=self.api_schema)
        except ValidationError:
            log.error("Invalid payload", exc_info=True)
            return None

        async with aiohttp_client.post(API_URL, data=json.dumps(event)) as resp:
            if resp.status != 200:
                log.warn("Failed to log event", exc_info=True)

        return resp
