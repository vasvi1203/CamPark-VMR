# Generated by Django 3.2.12 on 2022-05-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_ui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='videoupload',
            name='query',
        ),
    ]
