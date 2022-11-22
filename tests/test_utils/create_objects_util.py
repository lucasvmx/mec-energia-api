from tests.test_utils.university_test_utils.create_university_test_util import CreateUniversityTestUtil
from tests.test_utils.users_test_utils.create_university_user_test_util import CreateUniversityUserTestUtil
from tests.test_utils.consumer_unit_test_utils.create_consumer_unit_test_util import CreateConsumerUnitTestUtil
from tests.test_utils.contract_test_utils.create_contract_unit_test_util import CreateContractTestUtil
from tests.test_utils.energy_bill_test_utils.create_energy_bill_unit_test_util import CreateEnergyBillTestUtil

class CreateObjectsUtil:
    login_university_user = CreateUniversityUserTestUtil.login_university_user_dict

    def create_university_object():
        return CreateUniversityTestUtil.create_university()

    def create_university_user_object(university):
        return CreateUniversityUserTestUtil.create_university_user(university)

    def create_university_and_user():
        university = CreateObjectsUtil.create_university_object()
        user = CreateObjectsUtil.create_university_user_object(university)

        return (university, user)

    def create_consumer_unit_object(university, consumer_unit_dict_index = None):
        if not consumer_unit_dict_index:
            consumer_unit_dict_index = 0

        consumer_unit_dict, consumer_unit = CreateConsumerUnitTestUtil.create_consumer_unit(consumer_unit_dict_index, university)

        return (consumer_unit_dict, consumer_unit)

    def create_contract_object(consumer_unit, contract_dict_index = None):
        if not contract_dict_index:
            contract_dict_index = 0

        contract = CreateContractTestUtil.create_contract(contract_dict_index, consumer_unit)

        return contract

    def create_energy_bill_object(energy_bill_dict_index, contract, consumer_unit):
        energy_bill = CreateEnergyBillTestUtil.create_energy_bill(energy_bill_dict_index, contract, consumer_unit)
        
        return energy_bill
