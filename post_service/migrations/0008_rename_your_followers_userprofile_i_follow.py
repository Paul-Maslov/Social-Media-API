# Generated by Django 4.2.1 on 2023-06-15 16:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "post_service",
            "0007_remove_userprofile_post_userprofile_my_followers_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofile",
            old_name="your_followers",
            new_name="i_follow",
        ),
    ]
