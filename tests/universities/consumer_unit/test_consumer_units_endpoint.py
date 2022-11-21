import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils.create_objects_util import CreateObjectsUtil

TESTSERVER_ADDR = 'http://testserver/api/universities/'
ENDPOINT = '/api/consumer-units/'
EMAIL = 'admin@admin.com'
PASSWORD = 'admin@admin.com'

@pytest.mark.django_db
class TestConsumerUnitsEndpoint:
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
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])

        self.university_url = f'{TESTSERVER_ADDR}{self.university.id}/'


    def test_rejects_deleting_consumer_unit(self):
        response = self.client.delete(ENDPOINT, self.consumer_unit_test_1_dict)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_updates_is_active_of_consumer_unit_to_false(self):
        self.consumer_unit_test_1_dict['is_active'] = False
        self.consumer_unit_test_1_dict['university'] = self.university_url
        
        response = self.client.put(
            f'{ENDPOINT}{self.consumer_unit_test_1.id}/',
            self.consumer_unit_test_1_dict)

        assert response.status_code == status.HTTP_200_OK

