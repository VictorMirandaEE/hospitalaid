import requests

class HealthSites:
    FACILITIES_SEARCH_BASE_URL = "https://healthsites.io/api/v2/facilities/autocomplete/?q="
    FACILITIES_GET_BY_ID_BASE_URL = "https://healthsites.io/api/v2/facilities"

    def get_facility_data(self, facility_id):
        # TODO: convert to using coreapi once this issue is resolved:
        # https://github.com/healthsites/healthsites/issues/1411

        # TODO: add HealthSites API token somehow?

        res = requests.get(f'{self.FACILITIES_GET_BY_ID_BASE_URL}/{facility_id}')
        return res.json()

    def run_facility_search(self, search_term):
        res = requests.get(f'{self.FACILITIES_SEARCH_BASE_URL}{search_term}')
        return res.json()