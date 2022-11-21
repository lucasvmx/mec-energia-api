from datetime import date

from utils.energy_bill_util import EnergyBillUtils
from contracts.models import EnergyBill

class Recommendation:

    @classmethod
    def get_energy_bills_for_recommendation(cls, consumer_unit_id):
        energy_bills = []

        try:
            energy_bills_dates = EnergyBillUtils.generate_dates_for_recommendation(date.today())

            for energy_bill_object in energy_bills_dates:
                energy_bill = EnergyBill.get_energy_bill(
                    consumer_unit_id,
                    energy_bill_object['month'], 
                    energy_bill_object['year'])

                if energy_bill:
                    energy_bill_object['energy_bill'] = EnergyBillUtils.energy_bill_dictionary(energy_bill)
                
                energy_bills.append(energy_bill_object)

            return energy_bills
        except Exception as e:
            raise Exception('Error get Energy Bills for recommendation: ' + str(e))

