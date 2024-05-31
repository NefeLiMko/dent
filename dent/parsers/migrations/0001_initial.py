# Generated by Django 5.0.6 on 2024-05-19 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('articul', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=10)),
                ('date', models.DateField(auto_now=True)),
                ('site', models.CharField(choices=[('ED', 'El-Dent'), ('WS', 'W-Storm'), ('RM', 'Rocamed'), ('AD', 'Aveldent')], max_length=2)),
            ],
        ),
    ]
