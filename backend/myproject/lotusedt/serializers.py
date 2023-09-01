from rest_framework import serializers
from .models import Instructor,Expertise,StudentModel, Department, Enrollment

class InstructorSerializer(serializers.ModelSerializer):
    expertise = serializers.PrimaryKeyRelatedField(queryset=Expertise.objects.all(), many=True)

    class Meta:
        model = Instructor
        fields = ['id', 'first_name', 'last_name', 'expertise', 'email', 'password', 'created_at']


class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = ['id', 'name']







from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['id', 'title','description','instructors','department','created_at']



class getcourseSerialiser(serializers.ModelSerializer):
    instructors = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructors', 'department', 'created_at']

    def get_instructors(self, obj):
        instructors = obj.instructors.all()
        instructor_data = []
        for instructor in instructors:
            instructor_data.append({
                'id': instructor.id,
                'name': f"{instructor.first_name} {instructor.last_name}",
                'email': instructor.email,
                'expertise': [expertise.name for expertise in instructor.expertise.all()]
            })
        return instructor_data

    def get_department(self, obj):
        department = obj.department
        return {
            'id': department.id,
            'name': department.name
        }
    
class DepartmentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)  # Use your getcourseSerialiser here

    class Meta:
        model = Department
        fields = ['id', 'name', 'created_at', 'courses']



class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


# serializers.py

from rest_framework import serializers

class EnrolledStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = ['id', 'first_name', 'last_name', 'email', 'age']  # Include the fields you need


# serializers.py

class CourseWithEnrolledStudentsSerializer(serializers.ModelSerializer):
    enrolled_students = EnrolledStudentSerializer(many=True, read_only=True, source='enrollments.student')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'enrolled_students']


# serializers.py

class DepartmentWithCoursesSerializer(serializers.ModelSerializer):
    courses = CourseWithEnrolledStudentsSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'courses']

