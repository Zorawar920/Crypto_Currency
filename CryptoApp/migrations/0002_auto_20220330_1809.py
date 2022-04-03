# Generated by Django 3.1.6 on 2022-03-30 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='product_files/'),
        ),
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(default='https://google.com'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]