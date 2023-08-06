from django.db import migrations

from tracker.models.messages_state import Messages_state


def rec_message_states(apps, schema_editor):
    Messages_state.objects.create(code="new", name="Новая", editing=False, deliting=False)
    Messages_state.objects.create(code="closed", name="Закрыто")
    Messages_state.objects.create(code="postponed", name="Отложено")
    Messages_state.objects.create(code="onworking", name="В работе")
    Messages_state.objects.create(code="wait", name="Ожидание")


class Migration(migrations.Migration):
    dependencies = [
        ('tracker', '0001_initial'),
    ]
    atomic = True

    operations = [
        migrations.RunPython(rec_message_states),
    ]
