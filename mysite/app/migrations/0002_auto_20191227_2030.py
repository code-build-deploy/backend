# Generated by Django 3.0.1 on 2019-12-27 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='certificate_hash',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='certificate',
            name='certificate_hash_indexes',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='certificate',
            name='display',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
    ]
