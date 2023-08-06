import logging

from django.db.models import Model, BooleanField, BigAutoField, BigIntegerField, DateTimeField
from django.utils import timezone

from isc_common.managers.common_manager import CommonManager

logger = logging.getLogger(__name__)


class NotUnique(Exception):
    pass


class IsBlankStr(Exception):
    pass


class AuditModel(Model):
    id = BigAutoField(primary_key=True, verbose_name="Идентификатор")
    id_old = BigIntegerField(verbose_name="Идентификатор старый", null=True, blank=True)
    deleted = BooleanField(verbose_name="Признак удаления", default=False, db_index=True)
    editing = BooleanField(verbose_name="Возможность редактирования", default=True)
    deliting = BooleanField(verbose_name="Возможность удаления", default=True)
    lastmodified = DateTimeField(verbose_name='Последнее обновление', editable=False, db_index=True, default=timezone.now)

    objects = CommonManager()  # The default manager.

    class Meta:
        abstract = True
