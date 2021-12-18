# Generated by Django 4.0 on 2021-12-18 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_pickupsite_adress'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copy_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bookcopy'),
        ),
    ]
