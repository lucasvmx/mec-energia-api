from django.db import models
from django.forms.models import model_to_dict

from datetime import date
from contracts.models import Contract, EnergyBill

class Logger(models.Model):
    CREATE = "C"
    READ = "R"
    UPDATE = "U"
    DELETE = "D"
    OPERATION_TYPES = [
        (CREATE, "Create"),
        (READ, "Read"),
        (UPDATE, "Update"),
        (DELETE, "Delete"),
    ]

    operation = models.CharField(
        null=False,
        max_length=1,
        choices=OPERATION_TYPES,
        verbose_name=_('Operação'),
        help_text=_(
            'Tipo de operação realizada: Create(C), Read(R), Update(U), Delete(D)')
    )

    time_stamp = models.CharField(
        null=False,
        max_length=50,
        verbose_name=_('Horário'),
        help_text=_('Horário em que a alteração foi feita'),
    )

    user = models.ForeignKey(
        CustomUser,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Usuário',
        help_text=_(
            'Usuário responsável pela alteração da aplicação')    
    )

    item_type = models.BooleanField(
        default=True
    )
