import json
import pytest
from datetime import date
from rest_framework import status
from rest_framework.test import APIClient

from users.models import UniversityUser
from universities.models import ConsumerUnit, University

ENDPOINT = '/api/users/'
EMAIL = 'user@user.com'
PASSWORD = 'password'

@pytest.mark.django_db
class TestUsersEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.university = University(name='UnB', cnpj='00038174000143')
        self.university.save()

        self.user = UniversityUser.objects.create_user(
            email=EMAIL, password=PASSWORD, university=self.university)
        self.client.login(email=EMAIL, password=PASSWORD)

        self.consumer_units = []
        for i in range(3):
            self.consumer_units.append(ConsumerUnit(
                name=f'UC {i+1}',
                code=f'{i+1}',
                university=self.university,
                is_active=True,
                created_on=date.today()
            ))
        ConsumerUnit.objects.bulk_create(self.consumer_units)

    def test_university_user_starts_0_favorite_consumer_units(self):
        endpoint = f'{ENDPOINT}{self.user.id}/'

        user = self._get_user_as_response(endpoint)

        assert 0 == len(user['favorite_consumer_units'])

    def test_adds_consumer_unit_to_favorite(self):
        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'

        response = self._add_to_favorite_request(endpoint, self.consumer_units[0].id)

        assert status.HTTP_200_OK == response.status_code

        endpoint = f'{ENDPOINT}{self.user.id}/'
        user = self._get_user_as_response(endpoint)

        assert 1 == len(user['favorite_consumer_units'])
        assert self.consumer_units[0].id == user['favorite_consumer_units'][0]['id']
            

    def test_adds_second_consumer_unit_to_favorite(self):
        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'

        self._add_to_favorite_request(endpoint, self.consumer_units[0].id)
        self._add_to_favorite_request(endpoint, self.consumer_units[1].id)

        endpoint = f'{ENDPOINT}{self.user.id}/'
        user = self._get_user_as_response(endpoint)

        assert 2 == len(user['favorite_consumer_units'])

    def test_removes_second_consumer_unit_from_favorite(self):
        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'

        self._add_to_favorite_request(endpoint, self.consumer_units[0].id)
        self._add_to_favorite_request(endpoint, self.consumer_units[1].id)

        self._remove_from_favorite_request(endpoint, self.consumer_units[1].id)

        endpoint = f'{ENDPOINT}{self.user.id}/'
        assert 1 == UniversityUser.objects.get(pk=self.user.id).favorite_consumer_units.count()

    def test_cannot_add_consumer_unit_from_unrelated_university_to_favorite(self):
        unrelated_university = University(name='UFMG', cnpj='17217985000104')
        unrelated_university.save()

        unit_from_unrelated_university = ConsumerUnit.objects.create(
            name='Unrelated UC',
            code=f'0',
            university=unrelated_university,
            is_active=True,
            created_on=date.today()
        )

        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'
        response = self._add_to_favorite_request(
            endpoint, unit_from_unrelated_university.id)
            
        assert status.HTTP_403_FORBIDDEN == response.status_code

        endpoint = f'{ENDPOINT}{self.user.id}/'
        user = self._get_user_as_response(endpoint)
        assert 0 == len(user['favorite_consumer_units'])
    
    def test_cannot_add_non_existing_consumer_unit_to_favorite(self):
        non_existent_consumer_unit_id = 5
        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'
        
        response = self._add_to_favorite_request(endpoint, non_existent_consumer_unit_id)
        
        assert status.HTTP_404_NOT_FOUND == response.status_code
    
    def test_rejects_request_with_missing_fields(self):
        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'

        response = self.client.post(endpoint, {})
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert 'This field is required' in error['consumer_unit_id'][0]
        assert 'This field is required' in error['action'][0]
            
    def test_rejects_request_with_wrong_action_value(self):
        endpoint = f'{ENDPOINT}{self.user.id}/favorite-consumer-units/'

        response = self.client.post(endpoint, {
            'consumer_unit_id': self.consumer_units[0].id,
            'action': 'wrong action'
        })
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert '"wrong action" is not a valid choice' in error['action'][0]
            
    def _add_to_favorite_request(self, endpoint: str, consumer_unit_id: str):
        return self.client.post(endpoint, 
            {'consumer_unit_id': consumer_unit_id, 'action': 'add'})

    def _remove_from_favorite_request(self, endpoint: str, consumer_unit_id: str):
        return self.client.post(endpoint, 
            {'consumer_unit_id': consumer_unit_id, 'action': 'remove'})

    def _get_user_as_response(self, endpoint: str):
        response = self.client.get(endpoint)
        return json.loads(response.content)
