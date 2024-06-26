# Generated by Django 4.2 on 2024-05-14 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("news_app", "0015_alter_article_content"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="image",
        ),
        migrations.AlterField(
            model_name="article",
            name="content",
            field=models.TextField(default="No content", verbose_name="Описание"),
        ),
        migrations.CreateModel(
            name="ArticleImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="article_images/", verbose_name="Изображение"
                    ),
                ),
                (
                    "caption",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Подпись"
                    ),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="news_app.article",
                    ),
                ),
            ],
        ),
    ]
