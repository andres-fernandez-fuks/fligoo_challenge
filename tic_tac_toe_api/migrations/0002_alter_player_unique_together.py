# Generated by Django 4.2.6 on 2023-10-28 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tic_tac_toe_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('symbol', 'game'), ('name', 'game')},
        ),
    ]