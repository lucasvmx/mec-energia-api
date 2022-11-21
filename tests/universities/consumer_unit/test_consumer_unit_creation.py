import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils.create_objects_util import CreateObjectsUtil

TESTSERVER_ADDR = 'http://testserver/api/universities/'
ENDPOINT = '/api/consumer-units/'

@pytest.mark.django_db
class TestConsumerUnitsEndpoint:
    def setup_method(self):
        self.university, self.user = CreateObjectsUtil.create_university_and_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])

        self.university_url = f'{TESTSERVER_ADDR}{self.university.id}/'
        self.consumer_unit_to_be_created = {
            'name': 'Faculdade do Gama',
            'code': '111111111',
            'created_on': '2022-10-02',
            'is_active': True,
            'university': self.university_url
        }


    def test_creates_consumer_unit(self):
        response = self.client.post(ENDPOINT, self.consumer_unit_to_be_created)
        created_consumer_unit = json.loads(response.content)

        assert created_consumer_unit['name'] == self.consumer_unit_to_be_created['name']
        assert created_consumer_unit['university'] == self.consumer_unit_to_be_created['university']
        assert response.status_code == status.HTTP_201_CREATED