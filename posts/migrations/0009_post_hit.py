# Generated by Django 4.0.1 on 2022-03-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_slider_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hit',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
