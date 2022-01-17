# Generated by Django 3.2.6 on 2021-12-07 15:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211207_1733'),
        ('courses', '0010_course_course_selling_times'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EditorialQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, default='', null=True)),
                ('answer', models.TextField(blank=True, default='', null=True)),
                ('answer_as_image', models.FileField(blank=True, null=True, upload_to='static/images')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('meeting_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('topic', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('data', models.DateField(blank=True, null=True)),
                ('from_hour', models.TimeField(blank=True, null=True)),
                ('to_hour', models.TimeField(blank=True, null=True)),
                ('is_weekly', models.BooleanField(default=False)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_instructor', to='users.instructor')),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='courses.video')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, default='', null=True)),
                ('answer1', models.TextField(blank=True, default='', null=True)),
                ('answer2', models.TextField(blank=True, default='', null=True)),
                ('answer3', models.TextField(blank=True, default='', null=True)),
                ('answer4', models.TextField(blank=True, default='', null=True)),
                ('correct_answer', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SingleMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.meeting')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_student', to='users.instructor')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='course_coupons',
            field=models.ManyToManyField(blank=True, related_name='course_coupons', to='courses.Coupon'),
        ),
        migrations.DeleteModel(
            name='Stream',
        ),
        migrations.AddField(
            model_name='coursetest',
            name='editorial_questions',
            field=models.ManyToManyField(blank=True, to='courses.EditorialQuestion'),
        ),
        migrations.AddField(
            model_name='coursetest',
            name='multiple_choice_questions',
            field=models.ManyToManyField(blank=True, to='courses.MultipleChoiceQuestion'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_tests',
            field=models.ManyToManyField(blank=True, related_name='course_tests', to='courses.CourseTest'),
        ),
    ]