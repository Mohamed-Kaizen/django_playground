# Generated by Django 3.0.4 on 2020-04-01 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('author', models.UUIDField(verbose_name='author')),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], default='Draft', max_length=15, verbose_name='status')),
                ('read_time', models.IntegerField(default=0, verbose_name='read time')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='slug')),
                ('published_at', models.DateTimeField(verbose_name='published at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('tags', models.ManyToManyField(related_name='posts', to='blog.Tag', verbose_name='tags')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
    ]
