# Generated by Django 5.0.6 on 2025-01-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0033_quizresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizresult',
            name='correct_answers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='score_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='total_questions',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
