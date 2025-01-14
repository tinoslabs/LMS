# Generated by Django 5.0.6 on 2025-01-03 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0028_remove_question_correct_option_alter_question_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentanswer',
            name='selected_option',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='studentanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='studentanswer',
            name='student',
        ),
        migrations.RemoveField(
            model_name='studentquizresult',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='studentquizresult',
            name='student',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='title',
        ),
        migrations.AddField(
            model_name='quiz',
            name='correct_option',
            field=models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='op1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='op2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='op3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='op4',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='question',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='testapp.course'),
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='StudentAnswer',
        ),
        migrations.DeleteModel(
            name='StudentQuizResult',
        ),
    ]
