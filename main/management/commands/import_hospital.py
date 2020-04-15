from django.core.management.base import BaseCommand

from main.models import ImportedHospital
from main.utils.dataimport.healthsites import HealthSites

import logging
import sys


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Imports a hospital from HealthSites"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--facility-id', type=str, help="The facility ID from HealthSites to import")
        parser.add_argument('--search-term', type=str, help="The search term to query for in the HealthSites "
                                                            "facilities API")

        parser.add_argument('--insert-search-results', action='store_true', help="Indicates that search results should "
                                                                                 "be inserted as the models")

    def handle(self, *args, **options):

        facility_id = options['facility_id']
        search_term = options['search_term']

        healthsites = HealthSites()
        response_json = healthsites.get_facility_data(facility_id)

        if (facility_id):
            logger.info('Starting import of facility ID %s from HealthSites', facility_id)
            self.insert_facility_id(healthsites, facility_id)
        elif (search_term):
            logger.info('Searching HealthSites for facilities matching: %s', search_term)
            results = self.get_facilies_ids_from_search_response(healthsites.run_facility_search(search_term))
            logger.debug('Search results: %s', results)
            if options['insert_search_results']:
                logger.info('Search results from HealthSites will be inserted as models')
                for facility_id, label in results.items():
                    logger.debug("Attempting to query HealthSites for details on %s (%s)", label, facility_id)
                    self.insert_facility_id(healthsites, facility_id)


    def get_facilies_ids_from_search_response(self, search_response):
        """
            Unwraps a facility search response from the requests library
            :returns a dict from facility ID to label
        """
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
        logger.debug('Detail results: %s', details)
        if details['attributes']['amenity'] == "hospital":
            try:
                model = self.build_model_from_facility_response(details)
            except KeyError:
                logger.warning("Not enough data to build model")
            else:
                model.save()
        else:
            logger.debug("skipping because not an hospital")
