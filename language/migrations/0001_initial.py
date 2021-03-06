# Generated by Django 3.1.2 on 2020-12-05 19:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LangToLearn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('user', 'user'), ('admin', 'admin')], default='user', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Language To Learn',
                'verbose_name_plural': 'Languages To Learn',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=50, unique=True, verbose_name='Language')),
                ('flag', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Flag')),
                ('desc', models.TextField(blank=True, default='', null=True)),
                ('words_number', models.IntegerField(blank=True, default=0, null=True)),
                ('sentance_number', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Activate')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date Time')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='LanguageLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100, verbose_name='Name')),
                ('level_num', models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4'), (5, 'Level 5'), (6, 'Level 6'), (7, 'Level 7'), (8, 'Level 8'), (9, 'Level 9'), (10, 'Level 10')], verbose_name='Level Number')),
                ('image', models.CharField(blank=True, max_length=1000, null=True)),
                ('xp', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='XP Points')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activate')),
                ('is_free', models.BooleanField(default=True, verbose_name='Is Free')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date Time')),
            ],
            options={
                'verbose_name': 'Language Level',
                'verbose_name_plural': 'Languages Levels',
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.CharField(max_length=1000, verbose_name='Sentence')),
                ('sentence_translate', models.CharField(max_length=1000, verbose_name='Sentence Translated')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sentence Translate',
                'verbose_name_plural': 'Translation',
            },
        ),
        migrations.CreateModel(
            name='WhyToLearn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(max_length=2000)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date Time')),
                ('language_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='language.language', verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Why To Learn',
                'verbose_name_plural': 'Why To Learn',
            },
        ),
    ]
