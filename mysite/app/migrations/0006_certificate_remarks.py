# Generated by Django 3.0.1 on 2019-12-30 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_certificate_organisation_associated'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='remarks',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
