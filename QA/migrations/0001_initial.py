# Generated by Django 2.1.2 on 2018-10-29 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('nickname', models.CharField(blank=True, max_length=50)),
                ('profession', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
