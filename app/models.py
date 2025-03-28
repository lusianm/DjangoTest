# models.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


# Custom user manager: 유저 생성 로직 정의
class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_id, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email 필드는 반드시 필요합니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, user_id=user_id, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, user_id, user_name, password, **extra_fields)


# 사용자 모델: 로그인, 회원가입, 프로필 관련 모든 정보를 포함
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 사용자 구분 및 고유 식별자
    user_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # 로그인 및 인증 관련 필드
    login_type = models.CharField(max_length=20, help_text="예: 'kakao' 또는 'google'")
    user_id = models.CharField(max_length=100, unique=True, help_text="사용자 식별 ID (예: SNS ID)")
    email = models.EmailField(unique=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    user_token = models.CharField(max_length=255, blank=True, null=True)

    # 회원가입 및 프로필 정보
    user_name = models.CharField(max_length=100)
    # AbstractBaseUser에서 password 필드 제공
    birth_date = models.DateField(blank=True, null=True)
    education_level = models.IntegerField(blank=True, null=True)
    desired_company = models.IntegerField(blank=True, null=True)
    desired_job = models.CharField(max_length=100, blank=True, null=True)
    job_prep_period_year = models.IntegerField(blank=True, null=True)
    job_prep_period_month = models.IntegerField(blank=True, null=True)
    job_prep_status = models.CharField(max_length=50, blank=True, null=True)
    job_difficulties = models.CharField(max_length=100, blank=True, null=True)
    interested_routine = models.BooleanField(default=False)

    # 프로필 추가 정보
    profile_image = models.URLField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    subscription_status = models.BooleanField(default=False)

    # 기본 Django 필드
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id', 'user_name']

    def __str__(self):
        return f"{self.user_name} ({self.email})"


# Task 모델: 사용자의 루틴(태스크) 관련 정보를 저장
class Task(models.Model):
    task_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=100)
    task_category = models.CharField(max_length=50)
    execute_description = models.TextField(blank=True)
    execute_time = models.TimeField()
    completed = models.BooleanField(default=False)
    use_timer = models.BooleanField(default=False)
    time_filter = models.IntegerField(default=0)
    routine_date = models.DateField(blank=True, null=True)

    # AddRoutineRequestData에 해당하는 추가 필드
    repeat_type = models.CharField(max_length=50, blank=True, null=True)
    # execute_days: 반복 실행 요일을 JSON 형태로 저장 (예: ["Monday", "Wednesday"])
    execute_days = models.JSONField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_name} ({self.user.user_name})"


# SuccessRoutine 모델: 성공한 루틴 데이터를 저장 (예: 좋아요, 복사 등 추가 기능 고려)
class SuccessRoutine(models.Model):
    # 성공 루틴을 등록한 사용자와 대상 사용자를 ForeignKey로 연결하여 user_key를 활용
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='success_routines')
    success_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='success_posts')

    current_company = models.CharField(max_length=100, blank=True, null=True)
    current_position = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.URLField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.CharField(max_length=4, blank=True, null=True)
    previous_job = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    likes = models.IntegerField(default=0)
    routine_date = models.DateField()
    # 루틴의 상세 태스크 정보를 JSON 형태로 저장하거나, 별도의 모델로 분리 가능
    routine_details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"SuccessRoutine by {self.success_user.user_name} on {self.routine_date}"
