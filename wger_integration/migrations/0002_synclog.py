# Generated by Django 5.2 on 2025-05-25 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wger_integration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=100)),
                ('detail', models.TextField(blank=True)),
            ],
        ),
    ]
