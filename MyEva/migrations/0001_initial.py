# Generated by Django 2.1.1 on 2019-03-20 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerList',
            fields=[
                ('AnswerId', models.AutoField(primary_key=True, serialize=False)),
                ('QuestionType', models.IntegerField(default=0)),
                ('isMust', models.BooleanField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssessList',
            fields=[
                ('AssessId', models.AutoField(primary_key=True, serialize=False)),
                ('AssessName', models.CharField(max_length=50)),
                ('AssessOneDes', models.CharField(max_length=200, null=True)),
                ('AssessPro', models.IntegerField(default=0)),
                ('AssessType', models.IntegerField(default=1)),
                ('AssessDes', models.CharField(max_length=500, null=True)),
                ('AssessObject', models.CharField(max_length=300, null=True)),
                ('AssessIndexNum', models.IntegerField(default=0)),
                ('AssessBeginTime', models.DateTimeField(auto_now_add=True)),
                ('People', models.CharField(max_length=300, null=True)),
                ('AssessUseNum', models.IntegerField(default=0)),
                ('AssessIndexId', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SCQorMCQ', models.IntegerField(default=0)),
                ('ChoiceA', models.CharField(max_length=50)),
                ('ChoiceB', models.CharField(max_length=50)),
                ('ChoiceC', models.CharField(max_length=50)),
                ('ChoiceD', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FIBAnswerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FIBAnswer', models.CharField(max_length=100)),
                ('AnswerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AnswerList')),
            ],
        ),
        migrations.CreateModel(
            name='HeuEvaResult',
            fields=[
                ('HeuEvaId', models.AutoField(primary_key=True, serialize=False)),
                ('Interface', models.CharField(max_length=50)),
                ('HeuProblem', models.CharField(max_length=300)),
                ('SeriousDegree', models.IntegerField(default=0)),
                ('Advice', models.CharField(max_length=200, null=True)),
                ('ScreenShot', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IndexList',
            fields=[
                ('IndexId', models.AutoField(primary_key=True, serialize=False)),
                ('IndexName', models.CharField(max_length=50)),
                ('FatherName', models.CharField(max_length=50)),
                ('FamilyName', models.CharField(max_length=50)),
                ('Description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='MCAList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChoiceNum', models.IntegerField(default=1)),
                ('ChoiceAnswer', models.CharField(max_length=50)),
                ('AnswerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AnswerList')),
            ],
        ),
        migrations.CreateModel(
            name='MethodList',
            fields=[
                ('MethodId', models.AutoField(primary_key=True, serialize=False)),
                ('MethodName', models.CharField(max_length=50)),
                ('Description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ModelList',
            fields=[
                ('ModelId', models.AutoField(primary_key=True, serialize=False)),
                ('ModelType', models.IntegerField(default=1)),
                ('AssessId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AssessList')),
            ],
        ),
        migrations.CreateModel(
            name='PaperList',
            fields=[
                ('PaperId', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceRecord',
            fields=[
                ('RecordId', models.AutoField(primary_key=True, serialize=False)),
                ('ErrorRate', models.FloatField(default=0)),
                ('FinishTime', models.FloatField(default=0)),
                ('SuccessRate', models.FloatField(default=0)),
                ('LookingTime', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PlanList',
            fields=[
                ('PlanId', models.AutoField(primary_key=True, serialize=False)),
                ('PlanName', models.CharField(max_length=59)),
                ('PlanDescription', models.CharField(max_length=500)),
                ('PlanTypeId', models.CharField(max_length=50)),
                ('AssessId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AssessList')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionList',
            fields=[
                ('QuestionId', models.AutoField(primary_key=True, serialize=False)),
                ('QueDescription', models.CharField(max_length=500, null=True)),
                ('QuestionType', models.IntegerField(default=0)),
                ('isMust', models.BooleanField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScaleAnswerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DegreeAnswer', models.IntegerField(default=1)),
                ('AnswerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AnswerList')),
            ],
        ),
        migrations.CreateModel(
            name='ScaleList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BeginIndex', models.CharField(max_length=50)),
                ('EndIndex', models.CharField(max_length=50)),
                ('DegreeNum', models.IntegerField(default=0)),
                ('QuestionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.QuestionList')),
            ],
        ),
        migrations.CreateModel(
            name='SCAList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChoiceAnswer', models.CharField(max_length=5)),
                ('AnswerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AnswerList')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyList',
            fields=[
                ('SurveyId', models.AutoField(primary_key=True, serialize=False)),
                ('SurveyName', models.CharField(max_length=50)),
                ('SurveyPro', models.IntegerField(default=0)),
                ('SurveyUseNum', models.IntegerField(default=0)),
                ('SurveyQueNum', models.IntegerField(default=0, null=True)),
                ('AssessId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.AssessList')),
            ],
        ),
        migrations.CreateModel(
            name='UserList',
            fields=[
                ('UserId', models.AutoField(primary_key=True, serialize=False)),
                ('UserName', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('Status', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='questionlist',
            name='SurveyId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.SurveyList'),
        ),
        migrations.AddField(
            model_name='performancerecord',
            name='PlanId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.PlanList'),
        ),
        migrations.AddField(
            model_name='performancerecord',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.UserList'),
        ),
        migrations.AddField(
            model_name='paperlist',
            name='SurveyId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.SurveyList'),
        ),
        migrations.AddField(
            model_name='paperlist',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.UserList'),
        ),
        migrations.AddField(
            model_name='heuevaresult',
            name='IndexId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.IndexList'),
        ),
        migrations.AddField(
            model_name='heuevaresult',
            name='PlanId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.PlanList'),
        ),
        migrations.AddField(
            model_name='heuevaresult',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.UserList'),
        ),
        migrations.AddField(
            model_name='choicelist',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.QuestionList'),
        ),
        migrations.AddField(
            model_name='assesslist',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.UserList'),
        ),
        migrations.AddField(
            model_name='answerlist',
            name='PaperId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.PaperList'),
        ),
        migrations.AddField(
            model_name='answerlist',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyEva.QuestionList'),
        ),
    ]
