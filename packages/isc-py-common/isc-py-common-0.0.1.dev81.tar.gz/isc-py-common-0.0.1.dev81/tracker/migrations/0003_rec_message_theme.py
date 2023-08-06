from django.db import migrations

from tracker.models.messages_theme import Messages_theme


def rec_message_theme(apps, schema_editor):
    Messages_theme.objects.create(code="auto_from_error", name="Автоматически занесенные из сообщений об ошибках.", editing=False, deliting=False)


class Migration(migrations.Migration):
    dependencies = [
        ('tracker', '0002_rec_message_states'),
    ]
    atomic = True

    operations = [
        migrations.RunPython(rec_message_theme),
    ]
