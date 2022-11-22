import pytest

from contracts.models import Contract

from tests.test_utils.create_objects_util import CreateObjectsUtil

@pytest.mark.django_db
class TestContractCreation:
    def setup_method(self):
        self.university = CreateObjectsUtil.create_university_object()

        (self.consumer_unit_dict,
        self.consumer_unit) = CreateObjectsUtil.create_consumer_unit_object(
                                university = self.university)

    def test_throws_exception_when_suply_voltage_does_not_match_ranges(self):
        with pytest.raises(Exception) as e:
            CreateObjectsUtil.create_contract_object(
                contract_dict_index = 3,
                consumer_unit = self.consumer_unit)

        assert 'Subgroup not found' in str(e.value)
        assert 0 == Contract.objects.all().count()