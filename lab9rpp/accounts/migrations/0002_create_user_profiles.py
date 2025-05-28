from django.db import migrations


def create_profiles_and_roles(apps, schema_editor):
    # Получаем исторические модели
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')
    Role = apps.get_model('accounts', 'Role')

    # Создаем стандартные роли
    Role.objects.get_or_create(name='Оператор')
    Role.objects.get_or_create(name='Начальник')

    # Создаем профили для всех пользователей
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


def reverse_create_profiles(apps, schema_editor):
    # При откате миграции удаляем все профили и роли
    UserProfile = apps.get_model('accounts', 'UserProfile')
    Role = apps.get_model('accounts', 'Role')
    UserProfile.objects.all().delete()
    Role.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_profiles_and_roles,
            reverse_code=reverse_create_profiles
        ),
    ]