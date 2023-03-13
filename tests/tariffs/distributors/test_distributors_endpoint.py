import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

from tests.test_utils.create_objects_util import CreateObjectsUtil

ENDPOINT = '/api/distributors/'

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(
            email = self.user_dict['email'], 
            password = self.user_dict['password'])

        self.unit1_dict = dicts_test_utils.consumer_unit_dict_1
        self.unit1 = create_objects_test_utils.create_test_consumer_unit(self.unit1_dict, self.university)

        self.unit2_dict = dicts_test_utils.consumer_unit_dict_2
        self.unit2 = create_objects_test_utils.create_test_consumer_unit(self.unit2_dict, self.university)

        self.unit3_dict = dicts_test_utils.consumer_unit_dict_3
        self.unit3 = create_objects_test_utils.create_test_consumer_unit(self.unit3_dict, self.university)

        self.neoenergia_dict = dicts_test_utils.distributor_dict_1
        self.neoenergia = create_objects_test_utils.create_test_distributor(self.neoenergia_dict, self.university)


    def test_cannot_delete_distributor_when_its_linked_to_a_consumer_units_current_contract(self):
        self.contract_test_1_dict = dicts_test_utils.contract_dict_1
        self.contract_test_2_dict = dicts_test_utils.contract_dict_2

        create_objects_test_utils.create_test_contract(self.contract_test_1_dict, self.neoenergia, self.unit1)
        create_objects_test_utils.create_test_contract(self.contract_test_2_dict, self.neoenergia, self.unit2)

        response = self.client.delete(ENDPOINT + f'{self.neoenergia.id}/')
        
        assert status.HTTP_400_BAD_REQUEST == response.status_code
        
        error = json.loads(response.content)
        
        assert 'There are active contracts associated to this distributor' in error['errors']
        assert self.unit1.id in error['consumer_units_ids']
        assert self.unit2.id in error['consumer_units_ids']
        assert self.unit3.id not in error['consumer_units_ids']
    
    def test_deletes_distributor_when_its_not_linked_to_any_contract(self):
        distributor_dict = dicts_test_utils.distributor_dict_2
        distributor = create_objects_test_utils.create_test_distributor(distributor_dict, self.university)

        response = self.client.delete(ENDPOINT + f'{distributor.id}/')

        assert status.HTTP_204_NO_CONTENT == response.status_code
    
    @pytest.mark.skip
    def test_consumer_units_count_by_distributor(self):
        _, unit1 = CreateObjectsUtil.create_consumer_unit_object(self.university, 0)
        _, unit2 = CreateObjectsUtil.create_consumer_unit_object(self.university, 1)
        _, unit3 = CreateObjectsUtil.create_consumer_unit_object(self.university, 2)
        _, neoenergia = CreateObjectsUtil.create_distributor_object(self.university, 0)
        _, ceb = CreateObjectsUtil.create_distributor_object(self.university, 1)
        CreateObjectsUtil.create_contract_object(unit1, neoenergia, 0)
        CreateObjectsUtil.create_contract_object(unit2, ceb, 1)
        CreateObjectsUtil.create_contract_object(unit3, ceb, 2)

        response = self.client.get(ENDPOINT + f"?university_id={neoenergia.id}")
        assert status.HTTP_200_OK == response.status_code
        distributors = json.loads(response.content)

        neoenergia = list(filter(lambda dist: dist['id'] == neoenergia.id, distributors))[0]
        ceb = list(filter(lambda dist: dist['id'] == ceb.id, distributors))[0]

        # TODO Reavaliar condição de teste
        # assert 1 == neoenergia['consumer_units']
        # assert 2 == ceb['consumer_units']
    
    @pytest.mark.skip
    def test_zero_consumer_units_count_by_distributor(self):
        ...