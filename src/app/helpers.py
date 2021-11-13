import json
import logging
import requests

logger = logging.getLogger(__name__)


class AmplitudeLogger:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = 'https://api.amplitude.com/2/httpapi'

    def log(self, user_id: int, event: str, user_properties=None, event_properties=None, timestamp=None):
        amp_event = {
            'user_id': user_id,
            'event_type': event,
            'platform': 'Telegram',
        }

        if user_properties is not None:
            amp_event['user_properties'] = user_properties

        if event_properties is not None:
            amp_event['event_properties'] = event_properties

        if timestamp is not None:
            amp_event['time'] = timestamp

        amp_request = {
            'api_key': self.api_key,
            'events': [
                amp_event,
            ],
        }

        requests.post(self.endpoint, data=json.dumps(amp_request))
