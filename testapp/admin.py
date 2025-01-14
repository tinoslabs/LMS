from django.contrib import admin
from .models import User
from .models import*

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'is_approved']
    list_filter = ['role', 'is_approved']

    def approve_instructor(self, request, queryset):
        queryset.update(is_approved=True)

    approve_instructor.short_description = "Approve selected instructors"

    actions = [approve_instructor]
    
class What_u_learn_TabularInline(admin.TabularInline):
    model = What_u_learn


class Requirements_TabularInline(admin.TabularInline):
    model=Requirements

class Video_TabularInline(admin.TabularInline):
    model=VideoModel

class course_admin(admin.ModelAdmin):
    inlines=(What_u_learn_TabularInline,Requirements_TabularInline,Video_TabularInline)


admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(What_u_learn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(UserCourse)
# admin.site.register(Payment)
admin.site.register(Instructor)
admin.site.register(Categoriestheory)

admin.site.register(CourseResource)
admin.site.register(VideoModel)
admin.site.register(OTPModel)

# test
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizAnswer)
admin.site.register(QuizResult)
# admin.site.register(StudentQuizResult)
# admin.site.register(StudentAnswer)