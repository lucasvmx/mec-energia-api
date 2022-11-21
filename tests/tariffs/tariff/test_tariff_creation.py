import pytest

from tests.test_utils.tariff_test_utils.create_tariff_test_util import CreateTariffTestUtil
from tests.test_utils.university_test_utils.create_university_test_util import CreateUniversityTestUtil
from tests.test_utils.distributors_test_utils.create_distributors_test_util import CreateDistributorTestUtil

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university = CreateUniversityTestUtil.create_university()
        self.distributor = CreateDistributorTestUtil.create_distributor(self.university)


    def test_creates_blue_tariff(self):
        tariff = CreateTariffTestUtil.create_blue_tariff(self.distributor.id)

        assert tariff.is_blue()

        blue_tariff = tariff.as_blue_tariff()

        assert 1 == blue_tariff.peak_tusd_in_reais_per_kw
        assert 4 == blue_tariff.off_peak_tusd_in_reais_per_kw

    def test_creates_green_tariff(self):
        tariff = CreateTariffTestUtil.create_green_tariff(self.distributor.id)

        assert not tariff.is_blue()

        green_tariff = tariff.as_green_tariff()

        assert 1 == green_tariff.peak_tusd_in_reais_per_mwh
        assert 5 == green_tariff.na_tusd_in_reais_per_kw

    def test_mishandles_green_tariff_as_blue_tariff(self):
        tariff = CreateTariffTestUtil.create_green_tariff(self.distributor.id)

        with pytest.raises(Exception) as e:
            tariff.as_blue_tariff()
        assert 'Cannot convert' in str(e.value)

    def test_mishandles_blue_tariff_as_green_tariff(self):
        tariff = CreateTariffTestUtil.create_blue_tariff(self.distributor.id)

        with pytest.raises(Exception) as e:
            tariff.as_green_tariff()
        assert 'Cannot convert' in str(e.value)
