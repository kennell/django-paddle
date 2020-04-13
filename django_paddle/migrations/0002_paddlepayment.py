# Generated by Django 3.0.5 on 2020-04-13 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_paddle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaddlePayment',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('amount', models.PositiveIntegerField()),
                ('currency', models.CharField(max_length=255)),
                ('payout_date', models.CharField(max_length=255)),
                ('is_paid', models.BooleanField()),
                ('is_one_off_charge', models.BooleanField()),
                ('receipt_url', models.CharField(max_length=255)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_paddle.PaddleSubscription')),
            ],
        ),
    ]
