# Generated by Django 3.0.4 on 2020-07-03 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timing', '0002_auto_20200704_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='kind',
            field=models.CharField(choices=[('exercise', 'Exercise'), ('break', 'Break time')], default='exercise', max_length=8),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=42),
        ),
    ]
