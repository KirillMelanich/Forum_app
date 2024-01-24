# Generated by Django 5.0.1 on 2024-01-24 11:13

import commentator.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "commentator",
            "0003_dislike_comment_like_comment_alter_dislike_post_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="image",
            field=models.ImageField(
                null=True, upload_to=commentator.models.image_file_path
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                null=True, upload_to=commentator.models.image_file_path
            ),
        ),
    ]
