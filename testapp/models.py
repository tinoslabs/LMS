from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.timezone import now, timedelta



class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default/default_profile.jpg', blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username


class Categories(models.Model):
    icon = models.ImageField(upload_to="Media/icons")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_category(self):
        return Categories.objects.all().order_by('id')
    
    
class Categoriestheory(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default='default_value_here')
    def __str__(self):
        return self.name
    
    def get_all_theory(self):
        return Theory.objects.all().order_by('id') # type: ignore
    
class Author(models.Model):
    author_profile = models.ImageField(upload_to="Media/author")
    designation = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="instructor")  
    designation = models.CharField(max_length=100, null=True, blank=True)
    about_author = models.TextField()

    def __str__(self):
        return f"{self.user.username} - (Role: {self.designation})"

class Level(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Language(models.Model):
    language = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Instructor,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level= models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    deadline = models.CharField(max_length=100,null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    Certificate=models.CharField(null=True,max_length=100)
    is_free = models.BooleanField(default=False)  

    
    def __str__(self):
         return f"{self.title} - {self.language}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_detail", kwargs={'course_id': self.id})

# theory courses 
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name

# models
class CourseResource(models.Model):
    RESOURCE_TYPE = (
        ('Note', 'Note'),
        ('PDF', 'PDF'),
        ('PPT', 'PPT'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    resource_type = models.CharField(choices=RESOURCE_TYPE, max_length=10)
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="course_resources/",default='path/to/default/file.pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #   @classmethod
    def get_all_category(cls):
        return cls.objects.all()
    
    def __str__(self):
        return f"{self.title} - {self.resource_type} for {self.course.title}"


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Course)


class What_u_learn(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    points=models.CharField(max_length=500)

    def __str__(self):
        return self.points
    

class Requirements(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    points=models.CharField(max_length=500) 

    def __str__(self):
        return self.points


class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + " - " + self.course.title

    
class VideoModel(models.Model):  
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    def __str__(self):
        return self.title 
    
class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # True = Completed
    completed_at = models.DateTimeField(null=True, blank=True)

# not needed, since yt video link not doing
class Video(models.Model):  
    serial_number = models.IntegerField(null=True)
    thumbnail=models.ImageField(upload_to="Media/Yt_Thumbnail",null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=300)
    time_duration = models.IntegerField(null=True)
    preview=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Use getattr to provide default values if first_name or title is None
        user_name = getattr(self.user, 'username', 'No Name')
        course_title = getattr(self.course, 'title', 'No Title')
        return f"{user_name} - {course_title}"
    
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    user_course = models.ForeignKey(UserCourse,on_delete=models.CASCADE,null=True)
    date= models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " -- " + self.course.title  
     

# for otp expiry time setting
def default_expiry():
    return now() + timedelta(minutes=5)

class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=6)
    expiry = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return f"OTP for {self.user.email} - Expires at {self.expiry}"


# for exams
# Model to store a quiz against each course

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return f"{self.question_text} - Quiz: {self.quiz.title}"

class QuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who took the quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # The quiz being taken
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # The question answered
    selected_option = models.IntegerField(
    choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')],
    null=True,
    blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the answer was saved

    def __str__(self):
        return f"Answer for {self.question.question_text} by {self.user.username}"
    
    
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(null=True, blank=True)
    total_questions = models.IntegerField(null=True, blank=True)
    score_percentage = models.FloatField(null=True, blank=True)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s result for {self.quiz.title}"

