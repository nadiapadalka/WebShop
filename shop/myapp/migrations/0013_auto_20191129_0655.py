# Generated by Django 2.2.7 on 2019-11-29 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20191124_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myapp.Cart'),
        ),
    ]
