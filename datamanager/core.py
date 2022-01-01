import json
import logging
import requests
from sqlalchemy.sql.expression import except_

from db.models import Scholar, Track


logger = logging.getLogger(f"{__name__}")
axie_api_url = "https://game-api.axie.technology/api/v1/{ronin_id}"


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
            return
                
        try:
            data = json.loads(response.content)
            print(data)
        except json.JSONDecodeError:
            err = "Cannot read json response."
            logger.error(err)
            return

        if not data:
            err = f"No data for scholar {Scholar}. Please check ronin_id"
            logger.warning(err)
            return

        t = Track()
        t.slp_total = data.get('spl_total')
        t.slp_raw_total = data.get('raw_total')
        t.slp_ronin = data.get('ronin_spl')
        t.slp_ingame = data.get('in_game_spl')
        t.mmr = data.get('mmr')
        t.rank = data.get('rank')
        t.scholar = self.scholar
        t.save()
