from django.contrib import admin
from .models import Subject, Result, Student

class SubjectInline(admin.TabularInline):
    model = Result.subjects.through
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'pointer', 'grade', 'total_marks')
    search_fields = ('code', 'name')
    list_filter = ('grade',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'semester', 'cgpa', 'total_pointer')
    search_fields = ('roll_number', 'name')
    list_filter = ('semester',)
    ordering = ('-cgpa', '-total_pointer')
    readonly_fields = ('total_pointer', 'cgpa')
    inlines = [SubjectInline]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_results_count')
    search_fields = ('results__roll_number',)
    filter_horizontal = ('results',)

    def get_results_count(self, obj):
        return obj.results.count()
    get_results_count.short_description = "Results Count"
