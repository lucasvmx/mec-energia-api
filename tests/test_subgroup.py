import pytest

ENDPOINT = '/api/contracts/'

from utils.subgroup_util import Subgroup

@pytest.mark.django_db
class TestContractEndpoint:
    def setup_method(self):
        self.contract_test_supply_voltage_1 = 250
        self.contract_test_supply_voltage_2 = 100
        self.contract_test_supply_voltage_3 = 40
        self.contract_test_supply_voltage_4 = 70

    def test_get_what_subgroup_contract_is_A1(self):
        assert Subgroup.get_subgroup(self.contract_test_supply_voltage_1) == Subgroup.A1

    def test_get_what_subgroup_contract_is_A2(self):
        assert Subgroup.get_subgroup(self.contract_test_supply_voltage_2) == Subgroup.A2

    def test_get_what_subgroup_contract_is_A3a(self):
        assert Subgroup.get_subgroup(self.contract_test_supply_voltage_3) == Subgroup.A3A

    def test_throws_exception_when_suply_voltage_does_not_match_ranges(self):
        with pytest.raises(Exception) as e:
            Subgroup.get_subgroup(self.contract_test_supply_voltage_4)

        assert 'Subgroup not found' in str(e.value)