# Generated by Django 4.1.7 on 2023-03-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_feedback_email_alter_feedback_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageblock',
            options={'ordering': ['order'], 'verbose_name': 'Блок страницы', 'verbose_name_plural': 'Блоки страницы'},
        ),
        migrations.AddField(
            model_name='pageblock',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]