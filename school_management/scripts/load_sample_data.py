"""
Sample Data Script for School Management System
Run with: python manage.py shell < scripts/load_sample_data.py
"""

from django.utils import timezone
from datetime import date, timedelta
import random

print("Creating sample data...")

# Create Admin User
from users.models import User
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@school.com',
        'first_name': 'System',
        'last_name': 'Admin',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print("Admin user created: admin / admin123")
else:
    print("Admin user already exists")

# Create Teachers
teachers_data = [
    {'username': 'teacher1', 'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@school.com'},
    {'username': 'teacher2', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah.johnson@school.com'},
    {'username': 'teacher3', 'first_name': 'Michael', 'last_name': 'Williams', 'email': 'michael.williams@school.com'},
]

teachers = []
for data in teachers_data:
    teacher, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': 'teacher',
        }
    )
    if created:
        teacher.set_password('password123')
        teacher.save()
    teachers.append(teacher)

print(f"Teachers created: {len(teachers)}")

# Create Students
students_data = [
    {'username': 'student1', 'first_name': 'Emma', 'last_name': 'Brown', 'email': 'emma.brown@school.com'},
    {'username': 'student2', 'first_name': 'James', 'last_name': 'Davis', 'email': 'james.davis@school.com'},
    {'username': 'student3', 'first_name': 'Olivia', 'last_name': 'Miller', 'email': 'olivia.miller@school.com'},
    {'username': 'student4', 'first_name': 'William', 'last_name': 'Wilson', 'email': 'william.wilson@school.com'},
    {'username': 'student5', 'first_name': 'Sophia', 'last_name': 'Moore', 'email': 'sophia.moore@school.com'},
    {'username': 'student6', 'first_name': 'Benjamin', 'last_name': 'Taylor', 'email': 'benjamin.taylor@school.com'},
    {'username': 'student7', 'first_name': 'Isabella', 'last_name': 'Anderson', 'email': 'isabella.anderson@school.com'},
    {'username': 'student8', 'first_name': 'Lucas', 'last_name': 'Thomas', 'email': 'lucas.thomas@school.com'},
    {'username': 'student9', 'first_name': 'Mia', 'last_name': 'Jackson', 'email': 'mia.jackson@school.com'},
    {'username': 'student10', 'first_name': 'Henry', 'last_name': 'White', 'email': 'henry.white@school.com'},
]

students = []
for data in students_data:
    student, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': 'student',
        }
    )
    if created:
        student.set_password('password123')
        student.save()
    students.append(student)

print(f"Students created: {len(students)}")

# Create Subjects
from academics.models import Subject
subjects_data = [
    {'name': 'Mathematics', 'code': 'MATH101'},
    {'name': 'English', 'code': 'ENG101'},
    {'name': 'Science', 'code': 'SCI101'},
    {'name': 'History', 'code': 'HIS101'},
    {'name': 'Computer Science', 'code': 'CS101'},
]

subjects = []
for data in subjects_data:
    subject, created = Subject.objects.get_or_create(
        code=data['code'],
        defaults={'name': data['name'], 'description': f'{data["name"]} course material'}
    )
    subjects.append(subject)

print(f"Subjects created: {len(subjects)}")

# Create Classes
from academics.models import Class
classes_data = [
    {'name': 'Class 1', 'section': 'A', 'academic_year': '2025-2026'},
    {'name': 'Class 2', 'section': 'A', 'academic_year': '2025-2026'},
    {'name': 'Class 3', 'section': 'A', 'academic_year': '2025-2026'},
]

classes = []
for i, data in enumerate(classes_data):
    class_obj, created = Class.objects.get_or_create(
        name=data['name'],
        section=data['section'],
        academic_year=data['academic_year'],
        defaults={
            'class_teacher': teachers[i] if i < len(teachers) else None,
        }
    )
    class_obj.subjects.set(subjects)
    classes.append(class_obj)

print(f"Classes created: {len(classes)}")

# Create Enrollments
from academics.models import Enrollment
enrollments = []
for i, student in enumerate(students):
    enrollment, created = Enrollment.objects.get_or_create(
        student=student,
        class_enrolled=classes[i % len(classes)],
        defaults={'roll_number': f'2026{(i+1):03d}'}
    )
    enrollments.append(enrollment)

print(f"Enrollments created: {len(enrollments)}")

# Create Teacher Subject Assignments
from academics.models import TeacherSubjectAssignment
for i, teacher in enumerate(teachers):
    for j in range(min(2, len(subjects))):
        assignment, created = TeacherSubjectAssignment.objects.get_or_create(
            teacher=teacher,
            subject=subjects[(i+j) % len(subjects)],
            class_assigned=classes[j % len(classes)]
        )

print("Teacher assignments created")

# Create Attendance Records
from attendance.models import Attendance
today = timezone.now().date()
for enrollment in enrollments[:5]:
    for i in range(10):
        att_date = today - timedelta(days=i)
        status = random.choice(['present', 'present', 'present', 'absent', 'late'])
        attendance, created = Attendance.objects.get_or_create(
            student=enrollment.student,
            class_enrolled=enrollment.class_enrolled,
            date=att_date,
            defaults={
                'status': status,
                'marked_by': admin
            }
        )

print("Attendance records created")

# Create Exams
from results.models import Exam
for class_obj in classes[:2]:
    for subject in subjects[:2]:
        exam, created = Exam.objects.get_or_create(
            name=f'{subject.name} Midterm',
            class_enrolled=class_obj,
            subject=subject,
            defaults={
                'exam_type': 'term',
                'date': today - timedelta(days=30),
                'total_marks': 100,
                'passing_marks': 33,
                'created_by': admin
            }
        )

print("Exams created")

# Create Results
from results.models import Result
exams = Exam.objects.all()
for exam in exams:
    for enrollment in enrollments[:3]:
        if enrollment.class_enrolled == exam.class_enrolled:
            marks = random.randint(40, 100)
            result, created = Result.objects.get_or_create(
                student=enrollment.student,
                exam=exam,
                defaults={'marks_obtained': marks}
            )

print("Results created")

# Create Fee Categories
from fees.models import FeeCategory
categories_data = [
    {'name': 'Tuition Fee', 'description': 'Monthly tuition fee'},
    {'name': 'Admission Fee', 'description': 'One-time admission fee'},
    {'name': 'Lab Fee', 'description': 'Laboratory fee'},
    {'name': 'Library Fee', 'description': 'Library services fee'},
]

categories = []
for data in categories_data:
    category, created = FeeCategory.objects.get_or_create(
        name=data['name'],
        defaults={'description': data['description']}
    )
    categories.append(category)

print(f"Fee categories created: {len(categories)}")

# Create Fee Structures
from fees.models import FeeStructure
for class_obj in classes:
    for category in categories[:2]:
        structure, created = FeeStructure.objects.get_or_create(
            fee_category=category,
            class_enrolled=class_obj,
            defaults={
                'amount': random.randint(50, 200),
                'duration': 'monthly',
                'academic_year': '2025-2026',
                'due_date': today + timedelta(days=30)
            }
        )

print("Fee structures created")

# Create Fee Payments
from fees.models import FeePayment
structures = FeeStructure.objects.all()[:5]
for i, student in enumerate(students[:5]):
    for structure in structures[:2]:
        payment, created = FeePayment.objects.get_or_create(
            student=student,
            fee_structure=structure,
            defaults={
                'amount': structure.amount,
                'status': random.choice(['paid', 'paid', 'pending']),
                'payment_date': today if random.random() > 0.3 else None,
                'collected_by': admin
            }
        )

print("Fee payments created")

print("\n=== Sample Data Loaded Successfully ===")
print("\nLogin Credentials:")
print("  Admin: admin / admin123")
print("  Teacher: teacher1 / password123")
print("  Student: student1 / password123")
