class Subgroup:
    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    A3A = 'A3a'
    A4 = 'A4'
    AS = 'AS'


    def get_subgroup(supply_voltage_in_kv: float):
        if supply_voltage_in_kv < 2.3:
            return Subgroup.AS
        elif supply_voltage_in_kv >= 2.3 and supply_voltage_in_kv < 25:
            return Subgroup.A4
        elif supply_voltage_in_kv >= 30 and supply_voltage_in_kv < 44:
            return Subgroup.A3A
        elif supply_voltage_in_kv == 69:
            return Subgroup.A3
        elif supply_voltage_in_kv >= 88 and supply_voltage_in_kv < 138:
            return Subgroup.A2
        elif supply_voltage_in_kv >= 230:
            return Subgroup.A1
        else:
            raise Exception('Subgroup not found for this supply voltage')
