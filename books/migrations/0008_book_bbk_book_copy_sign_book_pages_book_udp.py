# Generated by Django 4.1.4 on 2023-02-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_readers'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bbk',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ББК'),
        ),
        migrations.AddField(
            model_name='book',
            name='copy_sign',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Авторский знак'),
        ),
        migrations.AddField(
            model_name='book',
            name='pages',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='udp',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='УДК'),
        ),
    ]
