# Generated by Django 5.1.1 on 2024-10-09 10:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('pdetails', models.CharField(max_length=100)),
                ('cat', models.IntegerField(choices=[(1, 'Pure Veg'), (2, 'Non Veg'), (3, 'Others')])),
                ('is_active', models.BooleanField(default=True)),
                ('pimage', models.ImageField(upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.CharField(max_length=50)),
                ('qty', models.IntegerField(default=1)),
                ('uid', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pid', models.ForeignKey(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, to='vfoodapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('uid', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pid', models.ForeignKey(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, to='vfoodapp.product')),
            ],
        ),
    ]
