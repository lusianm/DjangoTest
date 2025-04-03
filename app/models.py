import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Custom user manager: 유저 생성 로직 정의
class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, user_name, password=None, **extra_fields):
        if not user_id:
            raise ValueError("user_id 필드는 반드시 필요합니다.")
        user = self.model(user_id=user_id, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, user_name, password, **extra_fields)


# 사용자 모델: 로그인, 회원가입, 프로필 관련 모든 정보를 포함
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 사용자 구분 및 고유 식별자
    user_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # 로그인 및 인증 관련 필드
    login_type = models.CharField(max_length=20, help_text="예: 'kakao' 또는 'google'")
    user_id = models.CharField(max_length=100, unique=True, help_text="사용자 식별 ID (예: SNS ID)")
    access_token = models.CharField(max_length=255, blank=True, null=True)
    # password는 django의 password 기능을 사용하여 저장

    # 회원가입 및 프로필 정보
    # 사용자 이름
    user_name = models.CharField(max_length=100)
    # 사용자 생년월일
    birth_date = models.DateField(blank=True, null=True)
    # 사용자 최종 학력
    # 0 : 고졸
    # 1 : 대졸 예정
    # 2 : 대졸,
    # 3 : 대학원졸업예정
    # 4 : 대학원졸업
    education_level = models.IntegerField(blank=True, null=True)
    # 희망 기업 유형
    # 0 : 대기업
    # 1 : 중견기업
    # 2 : 스타트업
    # 3 : 중소기업
    # 4 : 공기업
    # 5 : 외국계 기업
    desired_company = models.IntegerField(blank=True, null=True)
    # 희망 직무
    # ex) "dev//2//3//5"
    # (대분류_소분류)
    # dev : 개발
    # data : 데이터 & AI
    # plan : 기획 & PM
    # design : 디자인 & 퍼블리싱
    # network : 네트워크 & 보안
    # operate : IT운영 & 기술지원
    desired_job = models.CharField(max_length=100, blank=True, null=True)
    # 취준 기간(년)
    job_prep_period_year = models.IntegerField(blank=True, null=True)
    # 취준 기간(월)
    job_prep_period_month = models.IntegerField(blank=True, null=True)
    # 현재 취업 준비 상태 여부
    # ex) "0//1//5"
    # 0 : 자격증 준비 중
    # 1 : 이력서/포트폴리오 작성 중
    # 2 : 코딩 테스트 준비 중
    # 3 : 인적성 검사 준비 등 (NCS 등 포함)
    # 4 : 채용 지원 후 대기 중
    # 5 : 면접 준비 중 (기술, 임원)
    # 6 : 사이드 프로젝트 진행 중
    # 7 : 이직 준비 중
    # 8 : 부트캠프 참여 중
    job_prep_status = models.CharField(max_length=50, blank=True, null=True)
    # 취업 중 어려운 점
    # ex) "3//6//8//9//10"
    job_difficulties = models.CharField(max_length=100, blank=True, null=True)
    # 취업 루틴 관심 여부
    interested_routine = models.BooleanField(default=False)

    # 프로필 추가 정보
    # 프로필 이미지 링크
    profile_image = models.URLField(max_length=255, blank=True, null=True)
    # 자기 소개글
    bio = models.TextField(blank=True, null=True)
    #구독 여부
    subscription_status = models.BooleanField(default=False)

    # 기본 Django 필드
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_key'
    REQUIRED_FIELDS = ['user_id', 'user_name']

    def __str__(self):
        return f"{self.user_name} ({self.user_id})"


# RoutineTask 모델: 사용자의 루틴(태스크) 관련 정보를 저장
class RoutineTask(models.Model):
    # Routine 식별자
    task_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Task의 소유 유저
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    # Task의 명칭
    task_name = models.CharField(max_length=100)
    # 할 일 유형
    # personal = 개인 생활
    # job = 취업 관련
    task_category = models.CharField(max_length=50)
    # 루틴 반복 유형
    # once = 1회 실행
    # weekly = 요일별 반복
    repeat_type = models.CharField(max_length=50)
    # 루틴 수행 요일
    # ex) 월//수//금
    execute_days = models.CharField(max_length=50)
    # 루틴 수행 시기
    execute_description = models.TextField(blank=True)
    # 루틴 수행 시간
    execute_time = models.TimeField()
    # 타이머 사용 여부
    use_timer = models.BooleanField(default=False)
    # 시간 필터
    # 0 : 오전
    # 1 : 오후
    # 2 : 저녁
    time_filter = models.IntegerField(default=0)
    # 루틴 시작 날짜
    start_date = models.DateField(blank=True, null=True)
    # 루틴 종료 날짜
    end_date = models.DateField(blank=True, null=True)
    # 루틴 생성 일
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_name} ({self.user.user_name})"

class RoutineTaskAchievement(models.Model):
    # 어느 Task가 달성되었는지를 연결
    task = models.ForeignKey(RoutineTask, on_delete=models.CASCADE, related_name='achievements')
    # 달성한 날짜
    achieved_date = models.DateField()

    def __str__(self):
        return f"{self.task.task_name} - {self.achieved_date}"

# SuccessRoutine 모델: 성공한 루틴 데이터를 저장 (예: 좋아요, 복사 등 추가 기능 고려)
class SuccessRoutine(models.Model):
    # 성공자 식별 id
    success_user_id = models.CharField(max_length=100, blank=True, null=True)
    # 성공자의 현재 회사
    current_company = models.CharField(max_length=100, blank=True, null=True)
    # 성공자의 현재 직무
    current_position = models.CharField(max_length=100, blank=True, null=True)
    # 성공자의 프로필 이미지 링크
    profile_image = models.URLField(max_length=255, blank=True, null=True)
    # 성공자의 출신 대학
    university = models.CharField(max_length=100, blank=True, null=True)
    # 성공자의 전공
    major = models.CharField(max_length=100, blank=True, null=True)
    # 졸업 연도
    graduation_year = models.CharField(max_length=4, blank=True, null=True)
    # 이전 직장
    previous_job = models.CharField(max_length=100, blank=True, null=True)
    # 링크드인 주소
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    # 좋아요 수
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"SuccessRoutine by {self.success_user_id}"


# SuccessRoutineTask 모델: 성공자의 루틴 정보를 저장
class SuccessRoutineTask(models.Model):
    # Routine 식별자
    task_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Task의 소유 유저
    success_user = models.ForeignKey(SuccessRoutine, on_delete=models.CASCADE, related_name='tasks')
    # Task의 명칭
    task_name = models.CharField(max_length=100)
    # 할 일 유형
    # personal = 개인 생활
    # job = 취업 관련
    task_category = models.CharField(max_length=50)
    # 루틴 반복 유형
    # once = 1회 실행
    # weekly = 요일별 반복
    repeat_type = models.CharField(max_length=50)
    # 루틴 수행 요일
    # ex) 월//수//금
    execute_days = models.CharField(max_length=50)
    # 루틴 수행 시기
    execute_description = models.TextField(blank=True)
    # 루틴 수행 시간
    execute_time = models.TimeField()
    # 시간 필터
    # 0 : 오전
    # 1 : 오후
    # 2 : 저녁
    time_filter = models.IntegerField(default=0)
    # 루틴 시작 날짜
    start_date = models.DateField(blank=True, null=True)
    # 루틴 종료 날짜
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.task_name} ({self.user.user_name})"
