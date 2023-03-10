# Generated by Django 4.1.4 on 2023-02-03 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_book_inventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='inventory',
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='inventory',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Инвентарный номер'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=200, unique=True),
        ),
    ]
