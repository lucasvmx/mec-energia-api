from mec_energia import settings
from datetime import date

class EnergyBillUtils:

    @classmethod
    def generate_dates_for_recommendation(cls, date):
        energy_bills_list = []

        month = date.month
        year = date.year

        for i in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bills_list, month, year = cls.update_date_and_insert_energy_bill_on_list(energy_bills_list, month, year)

        return energy_bills_list

    @classmethod
    def energy_bill_dictionary(cls, energy_bill):
        if energy_bill == None:
            return None

        dictionary = {}
        dictionary["date"] = energy_bill.date
        dictionary["invoice_in_reais"] = energy_bill.invoice_in_reais
        dictionary["is_atypical"] = energy_bill.is_atypical
        dictionary["peak_consumption_in_kwh"] = energy_bill.peak_consumption_in_kwh
        dictionary["off_peak_consumption_in_kwh"] = energy_bill.off_peak_consumption_in_kwh
        dictionary["peak_measured_demand_in_kw"] = energy_bill.peak_measured_demand_in_kw
        dictionary["off_peak_measured_demand_in_kw"] = energy_bill.off_peak_measured_demand_in_kw

        return dictionary

    @classmethod
    def update_date_and_insert_energy_bill_on_list(cls, energy_bills_list, month, year):
        energy_bill, month, year = cls.create_energy_bill_date(month, year)
        energy_bills_list.append(energy_bill)

        return (energy_bills_list, month, year)

    @classmethod
    def create_energy_bill_date(cls, month, year):
        month, year = (month - 1, year) if month != 1 else (12, year - 1)

        energy_bill = {
            'month': month,
            'year': year,
            'energy_bill': None
        }

        return (energy_bill, month, year)

    @classmethod
    def generate_latest_dates_for_recommendation(cls):
        energy_bills_list = []

        month = date.today().month
        year = date.today().year

        for i in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bill, month, year = cls._create_energy_bill_date(month, year)
            energy_bills_list.append(energy_bill)

        return energy_bills_list

    @classmethod
    def generate_dates_by_year(cls, year):
        energy_bills_list = []

        month = 12
        year = year

        for i in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bill, month, year = cls._create_energy_bill_date(month, year)
            energy_bills_list.append(energy_bill)

        return energy_bills_list

    @staticmethod
    def _create_energy_bill_date(month, year):
        energy_bill = {
            'month': month,
            'year': year,
        }

        month, year = (month - 1, year) if month != 1 else (12, year - 1)

        return (energy_bill, month, year)
