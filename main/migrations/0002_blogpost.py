# Generated migration for BlogPost model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Blog post title', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, help_text='Auto-generated URL slug', unique=True)),
                ('excerpt', models.TextField(help_text='Short summary of the blog post (appears in listings)')),
                ('content', models.TextField(help_text='Full content of the blog post')),
                ('image', models.ImageField(help_text='Featured image for the blog post', upload_to='blog/')),
                ('author', models.CharField(default='Diamond Hill Resort', help_text='Author name', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True, help_text='Whether this post is published')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
                'ordering': ['-created_at'],
            },
        ),
    ]
