# Generated by Django 4.1.4 on 2023-02-03 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(default=1, help_text='Select a language for this book', on_delete=django.db.models.deletion.CASCADE, to='books.language'),
            preserve_default=False,
        ),
    ]