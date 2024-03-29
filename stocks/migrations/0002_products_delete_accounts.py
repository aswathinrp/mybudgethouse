# Generated by Django 4.0.5 on 2022-06-28 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_delete_accounts'),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, max_length=555)),
                ('max_area', models.IntegerField(blank=True, null=True)),
                ('bedrooms', models.IntegerField(blank=True, null=True)),
                ('bathrooms', models.IntegerField(blank=True, null=True)),
                ('floors', models.IntegerField(blank=True, null=True)),
                ('parking', models.TextField(max_length=100, null=True)),
                ('price', models.IntegerField()),
                ('images', models.ImageField(upload_to='photos/products')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
        migrations.DeleteModel(
            name='Accounts',
        ),
    ]
