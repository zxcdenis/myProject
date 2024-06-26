# Generated by Django 4.2.2 on 2024-03-24 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("news_app", "0004_articlecomment"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlecomment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="news_app.articlecomment",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="news_app.comment",
            ),
        ),
    ]
