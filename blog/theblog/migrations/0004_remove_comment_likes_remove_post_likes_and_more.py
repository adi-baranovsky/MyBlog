# Generated by Django 5.1.7 on 2025-03-30 11:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('theblog', '0003_alter_comment_likes_alter_post_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='comment',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]
