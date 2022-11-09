from django.db import models
import datetime

class Contract(models.Model):

    cod_tariff_flag = (
        ('V', 'Verde'),
        ('A', 'Azul'),
    )

    cod_sub_group = (
        ('A1', '≥ 230 kV'),
        ('A2', 'de 88 kV a 138 kV'),
        ('A3', 'de 69 kV'),
        ('A3a', 'de 30 kV a 44 kV'),
        ('A4', 'de 2,3 kV a 25 kV'),
        ('AS', '< a 2,3 kV, a partir de sistema subterrâneo de distribuição'),
    )

    # TODO: - OneToOneField:
    # - Operadora

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    start_date = models.DateField(
        default=datetime.date.today,
        null=False,
        blank=False
    )
    
    end_date = models.DateField(
        null=True,
        blank=True
    )
    
    tariff_flag = models.CharField( 
        choices=cod_tariff_flag,
        max_length=1,
        null=True,
        blank=True
    )

    sub_group = models.CharField(
        choices=cod_sub_group,
        max_length=3,
        null=True,
        blank=True
    )

    supply_voltage = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    peak_contracted_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_contracted_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )


class EnergyBill(models.Model):

    contract = models.ForeignKey(
        'Contract',
        on_delete=models.PROTECT
    )

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    date = models.DateField(
        null=True,
        blank=True
    )

    invoice_in_reais = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    is_atypical = models.BooleanField(
        default=False
    )

    peak_consumption_in_kwh = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_consumption_in_kwh = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    peak_measured_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_measured_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    @classmethod
    def get_energy_bill(cls, consumer_unit_id, month, year):
        energy_bill = cls.objects.all().filter(
            consumer_unit=consumer_unit_id,
            date__month=month,
            date__year=year)

        return energy_bill