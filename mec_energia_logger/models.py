from django.db import models
from django.forms.models import model_to_dict

from datetime import date
from users.models import CustomUser

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
        verbose_name=('Operação'),
        help_text=(
            'Tipo de operação realizada: Create(C), Read(R), Update(U), Delete(D)')
    )

    time_stamp = models.DateTimeField(
        auto_now_add=False,
        null=False,
        max_length=50,
        verbose_name=('Horário'),
        help_text=('Horário em que a alteração foi feita'),
    )

    user = models.ForeignKey(
        CustomUser,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Usuário',
        help_text=('Usuário responsável pela alteração da aplicação')
    )

    item_type = models.CharField(
        max_length=80,
        help_text=('Classe responsável pela alteração'),
    )

    id_item_type = models.CharField(
        max_length=80,
        null=False,
        help_text=('Id relacionado a classe usada na alteração'),
    )
