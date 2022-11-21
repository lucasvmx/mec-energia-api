import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tariffs.models import Distributor

from tests.test_utils.tariff_test_utils.create_tariff_test_util import CreateTariffTestUtil
from tests.test_utils.create_objects_util import CreateObjectsUtil

ENDPOINT = '/api/distributors/'

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university, self.user = CreateObjectsUtil.create_university_and_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])


    def test_cannot_delete_distributor_with_dependent_tariff(self):
        dis = Distributor.objects.create(name='Dis', cnpj='00038174000143', university_id=self.university.id)

        CreateTariffTestUtil.create_blue_tariff(dis.id)

        response = self.client.delete(ENDPOINT + f'{dis.id}/')
        assert status.HTTP_400_BAD_REQUEST == response.status_code
    
    def test_deletes_distributor_with_no_tariffs(self):
        dis = Distributor.objects.create(name='Dis', cnpj='00038174000143', university_id=self.university.id)

        response = self.client.delete(ENDPOINT + f'{dis.id}/')

        assert status.HTTP_204_NO_CONTENT == response.status_code