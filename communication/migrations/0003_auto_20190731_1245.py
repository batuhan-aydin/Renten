# Generated by Django 2.2.3 on 2019-07-31 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0002_auto_20190729_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='user_message_files/', verbose_name='File'),
        ),
    ]
