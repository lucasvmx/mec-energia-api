from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import datetime

from utils.subgroup_util import Subgroup
from utils.date_util import DateUtils

from django.core.validators import FileExtensionValidator


class ContractManager(models.Manager):
    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)

        obj.set_last_contract_end_date()

        return obj


class Contract(models.Model):
    objects = ContractManager()

    def save(self, *args, **kwargs):
        self.check_start_date_is_valid()
        self.subgroup = Subgroup.get_subgroup(self.supply_voltage)

        super().save(*args, **kwargs)

    tariff_flag_choices = (
        ('G', 'Verde'),
        ('B', 'Azul'),
    )

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    distributor = models.ForeignKey(
        'tariffs.Distributor',
        related_name='contracts',
        on_delete=models.PROTECT,
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
        choices=tariff_flag_choices,
        max_length=1,
        null=True,
        blank=True
    )

    subgroup = models.CharField(
        max_length=3,
        null=True,
        blank=True
    )

    supply_voltage = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=False,
        blank=False
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

    def check_start_date_is_valid(self):
        if self.end_date:
            return

        consumer_unit = self.consumer_unit

        if consumer_unit.current_contract:
            if self.start_date >= consumer_unit.oldest_contract.start_date and self.start_date < consumer_unit.current_contract.start_date:
                raise Exception('Already have the contract in this date')

    def set_last_contract_end_date(self):
        day_before_start_date = DateUtils.get_yesterday_date(self.start_date)

        contract = Contract.objects.filter(
            consumer_unit=self.consumer_unit).exclude(start_date__gt=day_before_start_date).last()

        if contract:
            if not contract.end_date:
                contract.end_date = day_before_start_date
                contract.save()

    def get_distributor_name(self):
        return self.distributor.name


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

    energy_bill_file = models.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=[
                                   'pdf', 'doc', 'ppt', 'xlsx', 'png', 'jpg', 'jpeg'])
        ],
        max_length=None,
        null=True,
        blank=True,
    )

    anotacoes = models.TextField( # Novo campo de anotações
        null=True,
        blank=True,
    )

    address = models.TextField(
        null = True,
        blank = True
    )

    @classmethod
    def get_energy_bill(cls, consumer_unit_id, month, year):
        try:
            energy_bill = cls.objects.get(
                consumer_unit=consumer_unit_id,
                date__month=month,
                date__year=year)

            return energy_bill
        except ObjectDoesNotExist:
            return None
        except Exception as error:
            raise Exception('Get Energy Bill: ' + str(error))
        
    def check_energy_bill_month_year(consumer_unit_id, date):
        has_already_energy_bill = EnergyBill.objects.filter(
            consumer_unit=consumer_unit_id,
            date__year=date.year, 
            date__month=date.month).exists()
        
        if has_already_energy_bill:
            return True
        else:
            return False
