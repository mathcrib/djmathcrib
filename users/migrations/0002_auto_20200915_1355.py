# Generated by Django 3.1 on 2020-09-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Телеграм аккаунт'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('author', 'Author'), ('moderator', 'Moderator'), ('editor', 'Editor')], default='author', max_length=50, verbose_name='Роль'),
        ),
    ]
