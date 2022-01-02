from datetime import datetime
import json
import logging
import requests
from sqlalchemy.sql.expression import except_

from db.models import Scholar, Track


logger = logging.getLogger(f"{__name__}")
axie_api_url = "https://game-api.axie.technology/api/v1/ronin:{ronin_id}"


class DataManager:
    def __init__(self, scholar):
        self.scholar = scholar

    def collect_new_data(self):
        ronin_id = self.scholar.ronin_id
        response = requests.get(axie_api_url.format(ronin_id=ronin_id))

        if response.status_code != 200:
            err = f"Error while gathering new data for scholar {self.scholar}."
            err += f" Details: {response.reason}"
            logger.error(err)
            return False
                
        try:
            data = json.loads(response.content)
        except json.JSONDecodeError:
            err = "Cannot read json response."
            logger.error(err)
            return False

        if not data:
            err = f"No data for scholar {Scholar}. Please check ronin_id"
            logger.warning(err)
            return False

        t = Track()
        t.mmr = data.get('mmr', None)
        t.rank = data.get('rank', None)
        t.total_slp = data.get('total_slp', None)
        t.raw_total = data.get('raw_total', None)
        t.in_game_slp = data.get('in_game_spl', None)
        t.last_claim = datetime.fromtimestamp(data.get('last_claim', 0))
        t.next_claim = datetime.fromtimestamp(data.get('next_claim', 0))
        t.player_name = data.get('name', None)
        t.scholar = self.scholar
        t.save()

        return True
