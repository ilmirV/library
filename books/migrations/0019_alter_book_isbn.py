# Generated by Django 4.1.4 on 2023-02-06 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0018_alter_book_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=17, unique=True, verbose_name='ISBN'),
        ),
    ]
