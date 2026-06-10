from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='calc_method',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='base_yield_qty',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='base_yield_unit',
        ),
    ]
