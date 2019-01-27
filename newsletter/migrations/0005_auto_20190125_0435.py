# Generated by Django 2.1.4 on 2019-01-25 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_auto_20180407_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, db_index=True, help_text='If you select none, the system will automatically find the subscribers for you.', limit_choices_to={'subscribed': True}, to='newsletter.Subscription', verbose_name='recipients'),
        ),
    ]
