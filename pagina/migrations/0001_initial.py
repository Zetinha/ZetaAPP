# Generated by Django 5.2.4 on 2025-07-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.PositiveIntegerField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('total_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('categoria', models.CharField(choices=[('mens_classic', 'Masculino Clássico'), ('womens_classic', 'Feminino Clássico')], max_length=30)),
                ('ipf_gl_points', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
