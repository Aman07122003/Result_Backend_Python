from django.db import models

class College(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='programs')

    class Meta:
        unique_together = ('name', 'college')

    def __str__(self):
        return f"{self.name} ({self.college.name})"

class Branch(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='branches')

    class Meta:
        unique_together = ('name', 'program')

    def __str__(self):
        return f"{self.name} - {self.program}"

class Semester(models.Model):
    semester_number = models.PositiveIntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='semesters')

    class Meta:
        unique_together = ('semester_number', 'branch')
        ordering = ['semester_number']

    def __str__(self):
        return f"Semester {self.semester_number} - {self.branch}"

class Subject(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    max_marks = models.PositiveIntegerField(default=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')

    class Meta:
        unique_together = ('code', 'semester')

    def __str__(self):
        return f"{self.name} ({self.code})"

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class SemesterResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='results')
    cgpa = models.FloatField()
    total_grade = models.CharField(max_length=5)

    class Meta:
        unique_together = ('student', 'semester')

    def __str__(self):
        return f"Result for {self.student.roll_number} - Sem {self.semester.semester_number}"

class SubjectMark(models.Model):
    semester_result = models.ForeignKey(SemesterResult, on_delete=models.CASCADE, related_name='subject_marks')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='marks')
    sessional_marks = models.FloatField(null=True, blank=True)
    semester_marks = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=5)
    pointer = models.FloatField()

    class Meta:
        unique_together = ('semester_result', 'subject')

    def __str__(self):
        return f"{self.subject.code} for {self.semester_result.student.roll_number}"