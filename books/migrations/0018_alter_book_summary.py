# Generated by Django 4.1.4 on 2023-02-05 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_remove_book_bbk_remove_book_copy_sign_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(default='Описание отсутствует', help_text='Enter a brief description of the book', max_length=1500),
        ),
    ]
