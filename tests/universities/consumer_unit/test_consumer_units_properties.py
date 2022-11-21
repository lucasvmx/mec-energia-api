import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils.create_objects_util import CreateObjectsUtil

ENDPOINT = '/api/consumer-units/'
EMAIL = 'admin@admin.com'
PASSWORD = 'admin@admin.com'

@pytest.mark.django_db
class TestConsumerUnitsProperties:
    def setup_method(self):
        self.university, self.user = CreateObjectsUtil.create_university_and_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])

        (self.consumer_unit_test_1_dict,
        self.consumer_unit_test_1) = CreateObjectsUtil.create_consumer_unit_object(
                                        consumer_unit_dict_index = 0,
                                        university = self.university)

        (self.consumer_unit_test_2_dict,
        self.consumer_unit_test_2) = CreateObjectsUtil.create_consumer_unit_object(
                                        consumer_unit_dict_index = 1,
                                        university = self.university)

        self.contract_test_1 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 0,
                                consumer_unit = self.consumer_unit_test_1)

        self.contract_test_2 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 1,
                                consumer_unit = self.consumer_unit_test_2)

        self.energy_bill_test_2 = CreateObjectsUtil.create_energy_bill_object(
                                energy_bill_dict_index = 0,
                                contract = self.contract_test_2,
                                consumer_unit = self.consumer_unit_test_2)


    def test_reads_consumer_unit_properties_no_one_energy_bill_filled(self):
        response = self.client.get(f'{ENDPOINT}{self.consumer_unit_test_1.id}/')
        consumer_unit = json.loads(response.content)

        assert self.contract_test_1.start_date == consumer_unit['date']
        assert False == consumer_unit['is_current_energy_bill_filled']
        assert 12 == consumer_unit['pending_energy_bills_number']
        assert status.HTTP_200_OK == response.status_code
    
    def test_reads_consumer_unit_properties_current_energy_bill_filled_and_all_energy_bills_pending(self):
        response = self.client.get(f'{ENDPOINT}{self.consumer_unit_test_2.id}/')
        consumer_unit = json.loads(response.content)

        assert self.contract_test_2.start_date == consumer_unit['date']
        assert True == consumer_unit['is_current_energy_bill_filled']
        assert 12 == consumer_unit['pending_energy_bills_number']
        assert status.HTTP_200_OK == response.status_code