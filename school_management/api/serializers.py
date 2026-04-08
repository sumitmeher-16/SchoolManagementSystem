from rest_framework import serializers
from django.contrib.auth import get_user_model
from academics.models import Subject, Class, Enrollment
from attendance.models import Attendance
from results.models import Exam, Result
from fees.models import FeePayment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'address']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description']
        read_only_fields = ['id']


class ClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(source='class_teacher.get_full_name', read_only=True)
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'section', 'class_teacher', 'class_teacher_name', 'subjects', 'academic_year', 'student_count']
        read_only_fields = ['id']
    
    def get_student_count(self, obj):
        return obj.student_count


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    class_name = serializers.CharField(source='class_enrolled.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'class_enrolled', 'class_name', 'roll_number', 'status', 'enrollment_date']
        read_only_fields = ['id']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'class_enrolled', 'subject', 'date', 'status', 'remarks']
        read_only_fields = ['id']


class ExamSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_enrolled.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'name', 'exam_type', 'class_enrolled', 'class_name', 'subject', 'subject_name', 'date', 'total_marks', 'passing_marks']
        read_only_fields = ['id']


class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    
    class Meta:
        model = Result
        fields = ['id', 'student', 'student_name', 'exam', 'exam_name', 'marks_obtained']
        read_only_fields = ['id']


class FeePaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    category_name = serializers.CharField(source='fee_structure.fee_category.name', read_only=True)
    
    class Meta:
        model = FeePayment
        fields = ['id', 'student', 'student_name', 'fee_structure', 'category_name', 'amount', 'status', 'payment_date']
        read_only_fields = ['id']
