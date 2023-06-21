# Generated by Django 4.2.1 on 2023-06-15 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post_service", "0006_alter_userprofile_options_userprofile_post"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="post",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="my_followers",
            field=models.ManyToManyField(
                related_name="follow_at", to="post_service.userprofile"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="your_followers",
            field=models.ManyToManyField(
                related_name="follow_for", to="post_service.userprofile"
            ),
        ),
    ]
