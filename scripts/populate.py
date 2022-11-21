#!/usr/local/bin/python
from datetime import date, timedelta

from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff

university = University.objects.create(
    name='Universidade de Brasília',
    acronym='UnB',
    cnpj='63025530000104'
)

unit = ConsumerUnit.objects.create(
    name='Darcy Ribeiro',
    code='1111111',
    is_active=True,
    university=university,
)

distributor = Distributor.objects.create(
    name='Neoenergia',
    cnpj='00038174000143',
    university=university,
)

TODAY = date.today()
YEAR_LATER = TODAY + timedelta(days=365)
blue = {
    'peak_tusd_in_reais_per_kw':1,
    'peak_tusd_in_reais_per_mwh':2,
    'peak_te_in_reais_per_mwh':3,
    'off_peak_tusd_in_reais_per_kw':4,
    'off_peak_tusd_in_reais_per_mwh':5,
    'off_peak_te_in_reais_per_mwh':6,
}
green = {
    'peak_tusd_in_reais_per_mwh':10,
    'peak_te_in_reais_per_mwh':20,
    'off_peak_tusd_in_reais_per_mwh':30,
    'off_peak_te_in_reais_per_mwh':40,
    'na_tusd_in_reais_per_kw':50,
}

Tariff.objects.bulk_create([
    Tariff(subgroup='A4', distributor=distributor, flag=Tariff.BLUE, **blue, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A4', distributor=distributor, flag=Tariff.GREEN, **green, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A3', distributor=distributor, flag=Tariff.BLUE, **blue, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A3', distributor=distributor, flag=Tariff.GREEN, **green, start_date=TODAY, end_date=YEAR_LATER),
])
