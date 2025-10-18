from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

# Create admin
admin = User.objects.create_user(
    username='admin',
    email='admin@test.com',
    password='admin123',
    role='admin',
    first_name='Admin',
    last_name='User'
)

# Create teacher
teacher = User.objects.create_user(
    username='teacher1',
    email='teacher@test.com',
    password='teacher123',
    role='teacher',
    first_name='Teacher',
    last_name='One'
)

# Create students
for i in range(1, 6):
    User.objects.create_user(
        username=f'student{i}',
        email=f'student{i}@test.com',
        password='student123',
        role='student',
        first_name=f'Student',
        last_name=f'{i}'
    )

exit()