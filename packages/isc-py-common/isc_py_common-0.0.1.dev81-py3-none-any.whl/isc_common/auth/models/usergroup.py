import logging

from django.utils.translation import gettext_lazy as _

from isc_common import delAttr
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_manager import CommonManager
from isc_common.models.base_ref import BaseRef

logger = logging.getLogger(__name__)


class GroupManager(CommonManager):
    @staticmethod
    def getRecord(record):
        res = {
            "id": record.id,
            "code": record.code,
            "name": record.name,
            "description": record.description,
            "parent_id": record.parent_id,
            "lastmodified": record.lastmodified,
            "editing": record.editing,
            "deliting": record.deliting,
        }
        return res

    def updateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        delAttr(_data, 'isFolder')
        delAttr(_data, 'children')
        super().filter(id=request.get_id()).update(**_data)
        return data


class UserGroup(BaseRef):
    code = CodeField(unique=True)
    parent = ForeignKeyProtect('self', null=True, blank=True)

    @property
    def is_admin(self):
        return self.code.lower() == 'administrators' or self.code.lower() == 'admin'

    @property
    def is_develop(self):
        return self.code == 'developers'

    def __str__(self):
        return f"{self.code}"

    objects = GroupManager()

    def save(self, *args, **kwargs):
        assert (self.code != '')
        assert (self.code != None)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
