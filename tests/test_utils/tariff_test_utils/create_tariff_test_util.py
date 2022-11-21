from datetime import date

from tariffs.models import Tariff

class CreateTariffTestUtil:
    def create_blue_tariff(distributor_id, subgroup='A3'):
        blue_tarif = Tariff.objects.create(
            distributor_id=distributor_id,
            subgroup=subgroup,
            start_date=date.today(),
            end_date=date.today(),
            flag=Tariff.BLUE,
            peak_tusd_in_reais_per_kw=1,
            peak_tusd_in_reais_per_mwh=2,
            peak_te_in_reais_per_mwh=3,
            off_peak_tusd_in_reais_per_kw=4,
            off_peak_tusd_in_reais_per_mwh=5,
            off_peak_te_in_reais_per_mwh=6,
        )

        return blue_tarif

    def create_green_tariff(distributor_id, subgroup='A3'):
        green_tariff = Tariff.objects.create(
            distributor_id=distributor_id,
            subgroup=subgroup,
            flag=Tariff.GREEN,
            start_date=date.today(),
            end_date=date.today(),
            peak_tusd_in_reais_per_mwh=1,
            peak_te_in_reais_per_mwh=2,
            off_peak_tusd_in_reais_per_mwh=3,
            off_peak_te_in_reais_per_mwh=4,
            na_tusd_in_reais_per_kw=5,
        )
        
        return green_tariff
