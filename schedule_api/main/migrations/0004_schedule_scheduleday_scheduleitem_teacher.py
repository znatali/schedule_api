# Generated by Django 3.0.3 on 2020-04-24 09:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200424_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('faculty', models.CharField(max_length=500)),
                ('year', models.IntegerField()),
                ('term', models.IntegerField()),
                ('education_format', models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Part-time-express', 'Part-time-express')], default='Full-time', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduleDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Schedule')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('teaching_subject', django.contrib.postgres.fields.jsonb.JSONField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('type', models.CharField(choices=[('End-of-term-test', 'End-of-term-test'), ('Test', 'Test'), ('Exam', 'Exam'), ('Lecture', 'Lecture'), ('Practice', 'Practice')], default='Lecture', max_length=20)),
                ('schedule_day', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.ScheduleDay')),
                ('sub_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item_sub_teacher', to='main.Teacher')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_teacher', to='main.Teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
