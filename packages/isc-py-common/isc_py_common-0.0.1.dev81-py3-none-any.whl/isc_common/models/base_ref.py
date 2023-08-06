import logging

from isc_common.fields.code_field import CodeField
from isc_common.fields.description_field import DescriptionField
from isc_common.fields.name_field import NameField
from isc_common.models.audit import AuditModel

logger = logging.getLogger(__name__)


class BaseRef(AuditModel):
    code = CodeField()
    name = NameField()
    description = DescriptionField()

    class Meta:
        abstract = True


class BaseRefShort(AuditModel):
    code = CodeField()
    name = NameField()

    class Meta:
        abstract = True
