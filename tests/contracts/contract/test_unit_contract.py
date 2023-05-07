import pytest
from rest_framework.test import APIClient

from contracts.models import Contract

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

@pytest.mark.django_db
class TestUnitContract:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(
            email = self.user_dict['email'], 
            password = self.user_dict['password'])
        
        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

        self.consumer_unit_test_dict = dicts_test_utils.consumer_unit_dict_1
        self.consumer_unit_test = create_objects_test_utils.create_test_consumer_unit(self.consumer_unit_test_dict, self.university)

        self.contract_test_1_dict = dicts_test_utils.contract_dict_1
        self.contract_test_1 = create_objects_test_utils.create_test_contract(self.contract_test_1_dict, self.distributor, self.consumer_unit_test)


    def test_check_start_date_is_valid(self):
        self.contract_test_1.check_start_date_is_valid()

        assert self.contract_test_1.start_date == self.contract_test_1_dict['start_date']

    def test_check_start_date_is_not_valid(self):
        contract_test_2_dict = dicts_test_utils.contract_dict_2
        contract_test_2 = create_objects_test_utils.create_test_contract(contract_test_2_dict, self.distributor, self.consumer_unit_test)

        with pytest.raises(Exception) as e:
            contract_test_2.check_start_date_is_valid()

        assert 'Already have the contract in this date' in str(e.value)

    def test_get_distributor_name(self):
        teste = 10
        assert teste == 10