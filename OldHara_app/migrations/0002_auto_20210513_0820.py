# Generated by Django 3.1.7 on 2021-05-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OldHara_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biblio',
            name='title',
            field=models.TextField(),
        ),
    ]
