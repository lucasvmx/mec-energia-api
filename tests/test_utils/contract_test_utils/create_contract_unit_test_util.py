from contracts.models import Contract

class CreateContractTestUtil:
    contract_dicts = [
        {
            'start_date': '2022-01-01',
            'end_date': '2022-12-31',
            'tariff_flag': 'V',
            'sub_group': 'A1',
            'supply_voltage': 100.00,
            'peak_contracted_demand_in_kw': 100.00,
            'off_peak_contracted_demand_in_kw': 100.00,
        },
        {
            'start_date': f'2023-01-01',
            'end_date': '2023-12-31',
            'tariff_flag': 'A',
            'sub_group': 'A2',
            'supply_voltage': 200.00,
            'peak_contracted_demand_in_kw': 200.00,
            'off_peak_contracted_demand_in_kw': 200.00,
        }
    ]
    
    def create_contract(index, consumer_unit):
        contract_dict = CreateContractTestUtil.contract_dicts[index]
        
        contract = Contract.objects.create(
            start_date = contract_dict['start_date'],
            end_date = contract_dict['end_date'],
            tariff_flag = contract_dict['tariff_flag'],
            sub_group = contract_dict['sub_group'],
            supply_voltage = contract_dict['supply_voltage'],
            peak_contracted_demand_in_kw = contract_dict['peak_contracted_demand_in_kw'],
            off_peak_contracted_demand_in_kw = contract_dict['off_peak_contracted_demand_in_kw'],
            consumer_unit = consumer_unit
        )

        return contract