# Generated by Django 5.0.3 on 2024-05-16 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminSide', '0004_alter_passapplications_options_enquiries_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiries',
            name='status',
            field=models.CharField(default=0, max_length=50),
        ),
    ]