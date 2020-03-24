# Generated by Django 2.2.9 on 2020-03-18 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0004_auto_20200318_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'ordering': ['email'],
            },
        ),
    ]