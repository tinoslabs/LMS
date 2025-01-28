# views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from testapp.models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


@api_view(['POST'])
@permission_classes([AllowAny])
def student_register(request):
    """Registration endpoint for students only"""
    serializer = StudentRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Registration successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def student_login(request):
    """Login endpoint for students only"""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint - invalidates the refresh token
    Requires the refresh token in the request body
    """
    serializer = LogoutSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(
                {"message": "Successfully logged out"}, 
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_page(request):
    """Home page data endpoint"""
    # Ensure user is a student
    if request.user.role != 'student':
        return Response(
            {'detail': 'Access denied. Students only.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get top instructors (instructors with most courses)
    top_instructors = Instructor.objects.annotate(
        course_count=Count('course')
    ).order_by('-course_count')[:5]
    
    data = {
        'categories': Categories.objects.all().order_by('id')[:6],
        'theory_categories': Categoriestheory.objects.all().order_by('id')[:6],
        'courses': Course.objects.filter(status='PUBLISH').order_by('-id'),
        'course_resources': CourseResource.get_all_category(CourseResource),
        'top_teachers': top_instructors
    }
    
    serializer = HomePageSerializer(data)
    return Response(serializer.data)