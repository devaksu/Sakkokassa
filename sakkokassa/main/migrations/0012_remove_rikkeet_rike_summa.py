# Generated by Django 3.2.5 on 2021-11-07 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20211107_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rikkeet',
            name='rike_summa',
        ),
    ]