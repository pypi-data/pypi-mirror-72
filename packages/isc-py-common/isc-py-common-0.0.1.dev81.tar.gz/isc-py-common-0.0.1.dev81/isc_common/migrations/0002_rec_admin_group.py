from django.db import migrations

from isc_common.auth.models.user import User
from isc_common.auth.models.usergroup import UserGroup


def rec_admin_group(apps, schema_editor):
    UserGroup.objects.get_or_create(code='administrators', name="Администраторы", description="Пользователи с полным набором возможностей, не взирая на доступы.", editing=False)
    developers = UserGroup.objects.get_or_create(code='developers', name="Разработчики", editing=False)
    User.objects.create_superuser(username='admin', password='admin', email='info@ivc-inform.ru')
    User.objects.create_user(usergroup=[developers[0]], username='uandrew', password='Uandrew1965', email='uag@ivc-inform.ru')
    User.objects.create_user(usergroup=[developers[0]], username='nasonov', password='nasonov', email='nma@ivc-inform.ru')
    User.objects.create_user(usergroup=[developers[0]], username='developer', password='developer', email='info@ivc-inform.ru', deliting=False, editing=False)


class Migration(migrations.Migration):
    dependencies = [
        ('isc_common', '0001_initial'),
    ]
    atomic = True

    operations = [
        migrations.RunPython(rec_admin_group),
    ]
