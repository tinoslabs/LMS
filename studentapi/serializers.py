# serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from testapp.models import User, Categories, Course, Categoriestheory, CourseResource, Instructor
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}  # Role will be set automatically to 'student'
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate email uniqueness
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
            
        return attrs
    
    def create(self, validated_data):
        # Force role to be student
        validated_data['role'] = 'student'
        validated_data['is_approved'] = True  # Students are auto-approved
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')
            
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
            
        if user.role != 'student':
            raise serializers.ValidationError('This API is only for student users.')
            
        attrs['user'] = user
        return attrs
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError('Invalid or expired token')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'icon', 'name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'featured_image', 'title', 'author', 'price', 'discount']

class CategoryTheorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoriestheory
        fields = ['id', 'icon', 'name', 'title']

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['id', 'course', 'resource_type', 'title']

class InstructorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Instructor
        fields = ['id', 'user', 'designation', 'about_author']

class HomePageSerializer(serializers.Serializer):
    categories = CategorySerializer(many=True)
    theory_categories = CategoryTheorySerializer(many=True)
    courses = CourseSerializer(many=True)
    course_resources = CourseResourceSerializer(many=True)
    top_teachers = InstructorSerializer(many=True)