# Generated by Django 4.0 on 2021-12-19 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pick_up_site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.pickupsite'),
        ),
    ]
