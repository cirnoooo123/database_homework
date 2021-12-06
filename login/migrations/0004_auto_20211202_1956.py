# Generated by Django 3.2.8 on 2021-12-02 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20211118_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='movieCost',
        ),
        migrations.AlterField(
            model_name='actor',
            name='actorAge',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='actor',
            name='majorActedMovies',
            field=models.ManyToManyField(to='login.Movie'),
        ),
        migrations.AlterField(
            model_name='company',
            name='companyAddr',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='company',
            name='companyName',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='director',
            name='directorAge',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='director',
            name='representativeMovies',
            field=models.ManyToManyField(to='login.Movie'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movieIntroduction',
            field=models.CharField(default='无', max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movieStyle',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewDate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='loveActors',
            field=models.ManyToManyField(to='login.Actor'),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='loveDirectors',
            field=models.ManyToManyField(to='login.Director'),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='loveMovies',
            field=models.ManyToManyField(to='login.Movie'),
        ),
    ]