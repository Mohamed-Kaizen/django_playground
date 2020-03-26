# Generated by Django 3.0.4 on 2020-03-25 08:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='unique id'),
        ),
    ]
