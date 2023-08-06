import requests


class DomainZones:

    def __init__(self, api_token):
        self.api_token = api_token
        self.base = "https://connect.nicapi.eu/api/v1/{endpoint}?authToken={API_TOKEN}"

    def get_zones(self):
        r = requests.get(self.base.format(endpoint="dns/zones", API_TOKEN=self.api_token))

        return r.json()

    def get_zone(self, zone):
        r = requests.get(self.base.format(endpoint="dns/zones/show", API_TOKEN=self.api_token), params={
            "zone": zone
        })

        return r.json()

    def