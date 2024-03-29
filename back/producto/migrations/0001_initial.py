# Generated by Django 4.2.1 on 2023-05-19 04:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('imagen', models.ImageField(upload_to='photos/%Y/%m/')),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cantidad', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categoria.categoria')),
            ],
        ),
    ]
