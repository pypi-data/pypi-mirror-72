from django.db.models import BinaryField, Model
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField


class DbStorage(Model):
    blob = BinaryField()
    filename = NameField(max_length=500, unique=True)
    mimetype = CodeField()

    class Meta:
        abstract = True
