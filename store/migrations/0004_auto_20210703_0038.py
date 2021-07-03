# Generated by Django 3.2.4 on 2021-07-03 00:38

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productmodel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='digital',
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=0, size=[200, 200], upload_to=''),
        ),
    ]
