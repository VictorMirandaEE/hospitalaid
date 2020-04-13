from django.core.management.base import BaseCommand

from main.models import ImportedHospital
from main.utils.dataimport.healthsites import HealthSites

import logging
import sys

class Command(BaseCommand):
    logger = None
    help = "Imports a hospital from HealthSites"

    def __init__(self):
        super().__init__()
        # TODO: figure out if this configuration can come from the wider application
        # somehow, the stuff in LOGGING under PROJECT/settings.py isn't taking effect
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--facility_id', type=str, help="The facility ID from HealthSites to import")
        parser.add_argument('--search_term', type=str, help="The search term to query for in the HealthSites "
                                                            "facilities API")

        parser.add_argument('--insert_search_results', action='store_true', help="Indicates that search results should "
                                                                                 "be inserted as the models")

    def handle(self, *args, **options):

        facility_id = options['facility_id']
        search_term = options['search_term']

        healthsites = HealthSites()
        response_json = healthsites.get_facility_data(facility_id)

        if (facility_id):
            self.logger.info('Starting import of facility ID %s from HealthSites', facility_id)
            self.insert_facility_id(healthsites, facility_id)
        elif (search_term):
            self.logger.info('Searching HealthSites for facilities matching: %s', search_term)
            results = self.get_facilies_ids_from_search_response(healthsites.run_facility_search(search_term))
            self.logger.debug('Search results: %s', results)
            if options['insert_search_results']:
                self.logger.info('Search results from HealthSites will be inserted as models')
                for facility_id, label in results.items():
                    self.logger.debug("Attempting to query HealthSites for details on %s (%s)", label, facility_id)
                    self.insert_facility_id(healthsites, facility_id)


    """
        Unwraps a facility search response from the requests library
        :returns a dict from facility ID to label
    """
    def get_facilies_ids_from_search_response(self, search_response):
        return {item['id']: item['label'] for item in search_response}

    def build_model_from_facility_response(self, facility_response):
        imported_hospital = ImportedHospital()
        imported_hospital.name = facility_response['attributes']['name']
        imported_hospital.addr_city = facility_response['attributes']['addr_city']
        imported_hospital.addr_street = facility_response['attributes']['addr_street']
        imported_hospital.addr_postcode = facility_response['attributes']['addr_postcode']
        imported_hospital.addr_housenumber = facility_response['attributes']['addr_housenumber']
        imported_hospital.location_latitude = facility_response['centroid']['coordinates'][1]
        imported_hospital.location_longitude = facility_response['centroid']['coordinates'][0]
        return imported_hospital

    def insert_facility_id(self, healthsites, facility_id):
        details = healthsites.get_facility_data(facility_id)
        self.logger.debug('Detail results: %s', details)
        model = self.build_model_from_facility_response(details)
        model.save()