from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('training', '0005_planfeedback'),
    ]
    operations = [
        migrations.AddField(
            model_name='trainingsession',
            name='effectiveness_index',
            field=models.FloatField(default=0.0),
        ),
    ]
