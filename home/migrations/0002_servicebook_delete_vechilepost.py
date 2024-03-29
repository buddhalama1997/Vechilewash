# Generated by Django 4.1.5 on 2023-02-09 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceType', models.CharField(max_length=100)),
                ('problemInVechile', models.TextField()),
                ('serviceDate', models.DateField()),
                ('serviceTime', models.TimeField()),
                ('bookingStatus', models.CharField(default='requested', max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='vechilePost',
        ),
    ]
