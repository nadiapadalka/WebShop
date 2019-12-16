# Generated by Django 2.2.7 on 2019-12-05 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_auto_20191205_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('In process', 'In process'), ('Performing', 'Performing'), ('Paid for', 'Paid for')], default='In process', max_length=120),
        ),
    ]