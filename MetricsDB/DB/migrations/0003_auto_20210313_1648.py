# Generated by Django 3.1.6 on 2021-03-13 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0002_auto_20210313_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextseq_metrics',
            name='Notes',
            field=models.CharField(max_length=300),
        ),
    ]