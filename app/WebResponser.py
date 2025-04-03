# your_app/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .JsonClassis import *
from .models import CustomUser, RoutineTask, RoutineTaskAchievement
from django.db.models import Q
from asgiref.sync import sync_to_async
from datetime import date, timedelta
import calendar

class LoginResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            loginrequestdata = LoginRequestData(**content)
        except (json.JSONDecodeError, ValidationError) as e:
            print("데이터 처리 오류:", e)
            login_response = LoginResponseData(
                user_key="",
                access_token="",
                is_login_success=False,
                is_new_user=False,
                login_message="login_success",
                user_info="Missing data: " + e
            )
            await self.send_json(login_response.get_json())
            return

        #dummy data test용
        if loginrequestdata.access_token == "dummy_access_token":
            print("더미 데이터 반환")
            login_response = LoginResponseData(
                user_key="kakao",
                access_token="abc123def456",
                is_login_success=True,
                is_new_user=False,
                login_message="로그인 성공",
                user_info="사용자 상세정보"
            )
            print(login_response.get_json())
            await self.send_json(login_response.get_json())

        # 각 login_type에 따른 처리
        if loginrequestdata.login_type == "kakao":
            await self.process_kakao(loginrequestdata)
        elif loginrequestdata.login_type == "google":
            await self.process_google(loginrequestdata)
        else:
            await self.send_json({"error": f"알 수 없는 login_type: {loginrequestdata.login_type}"})

    async def process_kakao(self, loginrequestdata):
        # Kakao 로그인 처리 로직 (예시)
        print(f"[Kakao] 사용자 {loginrequestdata.user_id}의 로그인 처리 중...")

        login_response: LoginResponseData
        try:
            user: CustomUser = CustomUser.objects.get(user_id="testuser123")
            if user.access_token == loginrequestdata.access_token:
                login_response = LoginResponseData(
                    user_key=user.user_key,
                    access_token=user.access_token,
                    is_login_success=True,
                    is_new_user=False,
                    login_message="login_success",
                    user_info=user.user_name
                )
            else:
                login_response = LoginResponseData(
                    user_key=user.user_key,
                    access_token=user.access_token,
                    is_login_success=False,
                    is_new_user=False,
                    login_message="Invalid access token",
                    user_info=user.user_name
                )
        except CustomUser.DoesNotExist:
            login_response = LoginResponseData(
                user_key="",
                access_token="",
                is_login_success=False,
                is_new_user=False,
                login_message="Unknown User ID",
                user_info=""
            )
        print(login_response.get_json())
        await self.send_json(login_response.get_json())

    async def process_google(self, user_id):
        # Google 로그인 처리 로직 (예시)
        print(f"[Google] 사용자 {user_id}의 로그인 처리 중...")
        login_response = LoginResponseData(
            user_key="kakao",
            access_token="abc123def456",
            is_login_success=True,
            is_new_user=False,
            login_message="로그인 성공",
            user_info="사용자 상세정보"
        )
        print(login_response.get_json())
        await self.send_json(login_response.get_json())

class UserRegisterResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserRegisterRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            print("데이터 처리 오류:", e)
            responseData = UserRegisterResponseData(
                user_key="",
                access_token="",
                is_registered=False,
                register_message="Missing data: " + e,
                user_info=""
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        users = CustomUser.objects.filter(
            Q(user_id=requestData.user_ID)
        )
        if users.exists():
            responseData = UserRegisterResponseData(
                user_key="",
                access_token="",
                is_registered=False,
                register_message="Duplicated User ID",
                user_info=""
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        users = CustomUser.objects.filter(
            Q(access_token=requestData.access_token)
        )
        if users.exists():
            responseData = UserRegisterResponseData(
                user_key="",
                access_token="",
                is_registered=False,
                register_message="Duplicated Access Token",
                user_info=""
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        new_user = CustomUser.objects.create_user(
            user_id=requestData.user_ID,
            user_name=requestData.user_ID,
            password=requestData.user_PW,
            access_token = requestData.access_token,
            login_type=requestData.login_type,  # extra_fields로 전달
            birth_date=requestData.user_birth_date,  # 선택 필드
            education_level=requestData.user_education_level,  # 선택 필드
            desired_company=requestData.desired_company,  # 선택 필드
            desired_job=requestData.desired_job,  # 선택 필드
            job_prep_period_year = requestData.job_prep_period_year,
            job_prep_period_month = requestData.job_prep_period_month,
            job_prep_status = requestData.job_prep_status,
            job_difficulties = requestData.job_difficulties,
            interested_routine = requestData.interested_routine,
            profile_image = "",
            bio = "",
            subscription_status = False
        )

        responseData = UserRegisterResponseData(
            user_key=new_user.user_key,
            access_token=new_user.access_token,
            is_registered=True,
            register_message="register_success",
            user_info=new_user.user_name
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class UserInfoResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserInfoRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            responseData = UserInfoResponseData(
                user_key="",
                user_name="",
                desired_company=0,
                desired_job="",
                is_subscribed=False
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData):
        print(f"사용자 데이터 응답중...")
        responseData: UserInfoResponseData
        try:
            user: CustomUser = CustomUser.objects.get(user_key=requestData.user_key)
            responseData = UserInfoResponseData(
                user_key=user.user_key,
                user_name=user.user_name,
                desired_company=user.desired_company,
                desired_job=user.desired_job,
                is_subscribed=user.subscription_status
            )
        except CustomUser.DoesNotExist:
            responseData = UserInfoResponseData(
                user_key="",
                user_name="",
                desired_company=0,
                desired_job="",
                is_subscribed=False
            )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class UserRoutineResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserRoutineRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            responseData = UserRoutineResponseData(
                user_key="",
                user_name="",
                request_date=date(1, 1, 1),
                task_list=[]
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        try:
            user: CustomUser = CustomUser.objects.get(user_key=requestData.user_key)
        except CustomUser.DoesNotExist:
            responseData = UserRoutineResponseData(
                user_key="",
                user_name="",
                request_date=date(1, 1, 1),
                task_list=[]
            )
            await self.send_json(responseData.get_json())
            return

        selected_date = requestData.request_date

        # 해당 사용자의 RoutineTask를, 시작일이 selected_date보다 작거나 같고,
        # (종료일이 없거나 selected_date보다 크거나 같은) 조건으로 조회
        tasks = RoutineTask.objects.filter(
            user=user,
            start_date__lte=selected_date
        ).filter(
            Q(end_date__gte=selected_date) | Q(end_date__isnull=True)
        )

        tasks_for_date = []
        # 요일 매핑: 영어 요일을 한글 약어로 변환 (예: 'Mon' -> '월')
        weekday_mapping = {
            'Mon': '월',
            'Tue': '화',
            'Wed': '수',
            'Thu': '목',
            'Fri': '금',
            'Sat': '토',
            'Sun': '일'
        }
        selected_weekday_korean = weekday_mapping[selected_date.strftime('%a')]

        for task in tasks:
            if task.repeat_type == 'once':
                # 한 번 실행하는 Task는 시작일과 정확히 일치해야 함
                if task.start_date == selected_date:
                    tasks_for_date.append(task)
            elif task.repeat_type == 'weekly':
                # 주간 반복 Task는 선택한 요일이 execute_days에 포함되어야 함
                # execute_days는 예를 들어 "월//수//금" 형태로 저장된다고 가정
                if selected_weekday_korean in task.execute_days:
                    tasks_for_date.append(task)
            else:
                # 다른 반복 유형은 기본적으로 범위에 포함되면 반환 (필요에 따라 조건 추가 가능)
                tasks_for_date.append(task)

        # RoutineTask의 데이터를 TaskData 형태로 변환
        task_data_list = []
        for task in tasks_for_date:
            completed = await sync_to_async(RoutineTaskAchievement.objects.filter)(task=task, achieved_date=selected_date).exists()
            task_data = TaskData(
                task_id=str(task.task_id),
                task_name=task.task_name,
                task_category=task.task_category,
                execute_description=task.execute_description,
                execute_time=task.execute_time,
                completed=completed,
                use_timer=task.use_timer,
                time_filter=task.time_filter
            )
            task_data_list.append(task_data)

        responseData = UserRoutineResponseData(
            user_key=str(user.user_key),
            user_name=user.user_name,
            request_date=selected_date,
            task_list=task_data_list
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

    async def process_response_dummy(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        dummy_task1 = TaskData(
            task_id="task_001",
            task_name="Daily Workout",
            task_category="Health",
            execute_description="Do a 30-minute workout",
            execute_time=time(6, 30),  # 오전 6시 30분
            completed=False,
            use_timer=True,
            time_filter=15
        )

        dummy_task2 = TaskData(
            task_id="task_002",
            task_name="Read News",
            task_category="Information",
            execute_description="Read the daily news articles",
            execute_time=time(8, 0),  # 오전 8시
            completed=True,
            use_timer=False,
            time_filter=0
        )

        responseData = UserRoutineResponseData(
            user_key="user_dummy_001",
            user_name="Alice",
            request_date=date(2025, 3, 19),
            task_list=[dummy_task1, dummy_task2]
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class AddRoutineResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = AddRoutineRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            responseData = AddRoutineResponseData(
                uers_key=requestData.uers_key,
                task_id="",
                is_added=False,
                routine_message=f"Missing data: " + e
            )
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        # 사용자 조회: requestData.uers_key를 통해 CustomUser 검색 (비동기 ORM 호출)
        try:
            user: CustomUser = await sync_to_async(CustomUser.objects.get)(user_key=requestData.uers_key)
        except CustomUser.DoesNotExist:
            responseData = AddRoutineResponseData(
                uers_key=requestData.uers_key,
                task_id="",
                is_added=False,
                routine_message="Unknown User ID"
            )
            await self.send_json(responseData.get_json())
            return

        # RoutineTask 생성 (비동기 ORM 호출)
        new_task = await sync_to_async(RoutineTask.objects.create)(
            user=user,
            task_name=requestData.task_name,
            task_category=requestData.task_category,
            repeat_type=requestData.repeat_type,
            execute_days=requestData.execute_days,
            execute_description=requestData.execute_description,
            execute_time=requestData.execute_time,
            use_timer=requestData.use_timer,
            time_filter=requestData.time_filter,
            start_date=requestData.start_date,
            end_date=None  # 종료 날짜가 없으면 None 처리
        )

        responseData = AddRoutineResponseData(
            uers_key=requestData.uers_key,
            task_id=str(new_task.task_id),
            is_added=True,
            routine_message="add_success"
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class SuccessRoutineResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = SuccessRoutineRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            print("데이터 처리 오류:", e)
            await self.send_json({"error": "잘못된 데이터 형식입니다."})
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        dummy_success_routine = SuccessRoutineData(
            task_id="task_001",
            task_name="Complete Assignment",
            task_category="Study",
            execute_description="Complete math assignment by 5 PM",
            execute_time=time(17, 0),  # 오후 5시
            time_filter=15
        )

        responseData = SuccessRoutineResponseData(
            uers_key="dummy_user_003",
            user_name="홍길동",
            success_user_id="success_id_003",
            success_users_name="성공사용자 홍길동",
            current_company="Dummy Inc.",
            current_position="Senior Developer",
            profile_image="https://example.com/profile.jpg",
            university="Dummy University",
            major="Computer Engineering",
            graduation_year="2018",
            previous_job="Junior Developer",
            linkedin_url="https://www.linkedin.com/in/dummyuser",
            likes=100,
            routine_date=date(2025, 3, 19),
            user_routine=[dummy_success_routine]
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class SuccessLikeResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = SuccessLikeRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            print("데이터 처리 오류:", e)
            await self.send_json({"error": "잘못된 데이터 형식입니다."})
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")

        responseData = SuccessLikeResponseData(
            uers_key="dummy_user_001",
            user_name="홍길동",
            success_user_id="success_id_001",
            likes=100
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class SuccessRoutineCopyResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = SuccessRoutineCopyRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            print("데이터 처리 오류:", e)
            await self.send_json({"error": "잘못된 데이터 형식입니다."})
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")

        responseData = SuccessRoutineCopyResponseData(
            uers_key="dummy_user_004",
            copied_tasks=3
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class UserRoutineWeeklyStatisticsResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserRoutineWeeklyStatisticsRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            responseData = UserRoutineWeeklyStatisticsResponseData(
                user_key="",
                statistics_type="",
                start_date=date(1, 1, 1),
                end_date=date(1, 1, 1),
                total_completed=0,
                praise_days=0,
                weekly_data=[]
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData: UserRoutineWeeklyStatisticsRequestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        '''
        dummy_weekly_routine1 = Weekly_Routine_Data(
            task_name="Exercise",
            completed_days=["Monday", "Wednesday", "Friday"]
        )

        dummy_weekly_routine2 = Weekly_Routine_Data(
            task_name="Study",
            completed_days=["Tuesday", "Thursday"]
        )

        responseData = UserRoutineWeeklyStatisticsResponseData(
            user_key="dummy_user_weekly_001",
            statistics_type="weekly",
            start_date=date(2025, 3, 1),
            end_date=date(2025, 3, 7),
            total_completed=5,
            praise_days=2,
            weekly_data=[dummy_weekly_routine1, dummy_weekly_routine2]
        )
        '''
        # 1. 사용자 조회
        try:
            user: CustomUser = await sync_to_async(CustomUser.objects.get)(user_key=requestData.user_key)
        except CustomUser.DoesNotExist:

            responseData = UserRoutineWeeklyStatisticsResponseData(
                user_key=requestData.user_key,
                statistics_type="",
                start_date=date(1, 1, 1),
                end_date=date(1, 1, 1),
                total_completed=0,
                praise_days=0,
                weekly_data=[]
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        start_date = requestData.start_date
        end_date = requestData.end_date

        # 2. 주간 기간 내 해당 사용자의 RoutineTask 조회
        tasks = await sync_to_async(list)(RoutineTask.objects.filter(user=user,start_date__lte=end_date).filter
            (
                Q(end_date__gte=start_date) | Q(end_date__isnull=True)
            )
        )

        total_completed = 0
        unique_achievement_days = set()  # 주간 달성 날짜(중복 제거)
        weekly_data_list = []

        # 3. 각 RoutineTask에 대해, 주간 기간 내 달성 기록 조회
        for task in tasks:
            achievements = await sync_to_async(list)(
                RoutineTaskAchievement.objects.filter(
                    task=task,
                    achieved_date__gte=start_date,
                    achieved_date__lte=end_date
                )
            )
            if achievements:
                # 각 Task의 달성 기록 수를 total_completed에 누적
                total_completed += len(achievements)
                # 각 achievement의 날짜를 unique set에 추가
                for ach in achievements:
                    unique_achievement_days.add(ach.achieved_date)
                # 각 Task별 달성 요일(예: "Monday") 목록 구성 (중복 제거)
                completed_days = list({ach.achieved_date.strftime("%A") for ach in achievements})
                weekly_data = Weekly_Routine_Data(
                    task_name=task.task_name,
                    completed_days=completed_days
                )
                weekly_data_list.append(weekly_data)

        praise_days = len(unique_achievement_days)

        responseData = UserRoutineWeeklyStatisticsResponseData(
            user_key=str(user.user_key),
            statistics_type="weekly",
            start_date=start_date,
            end_date=end_date,
            total_completed=total_completed,
            praise_days=praise_days,
            weekly_data=weekly_data_list
        )


        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class UserRoutineMonthlyStatisticsResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserRoutineMonthlyStatisticsRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            responseData = UserRoutineMonthlyStatisticsResponseData(
                user_key="",
                statistics_type="",
                month=date(1, 1, 1),
                total_completed=1,
                praise_days=1,
                monthly_data=[]
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData: UserRoutineMonthlyStatisticsRequestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        '''
        dummy_monthly_routine1 = Monthly_Routine_Data(
            routine_date=date(2025, 3, 1),
            completion_rate=80,
            status="Completed"
        )

        dummy_monthly_routine2 = Monthly_Routine_Data(
            routine_date=date(2025, 3, 15),
            completion_rate=90,
            status="Completed"
        )

        responseData = UserRoutineMonthlyStatisticsResponseData(
            user_key="dummy_user_monthly_001",
            statistics_type="monthly",
            month=date(2025, 3, 1),
            total_completed=10,
            praise_days=4,
            monthly_data=[dummy_monthly_routine1, dummy_monthly_routine2]
        )
        '''
        # 1. 사용자 조회
        try:
            user: CustomUser = await sync_to_async(CustomUser.objects.get)(user_key=requestData.user_key)
        except CustomUser.DoesNotExist:
            responseData = UserRoutineMonthlyStatisticsResponseData(
                user_key=requestData.user_key,
                statistics_type="",
                month=date(1, 1, 1),
                total_completed=1,
                praise_days=1,
                monthly_data=[]
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        # 2. 해당 월의 시작일과 종료일 계산
        month_date = requestData.month  # 예: 2025-03-01
        year = month_date.year
        month = month_date.month
        last_day = calendar.monthrange(year, month)[1]
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        # 3. 해당 월에 유효한 RoutineTask들을 조회
        tasks = await sync_to_async(list)(
            RoutineTask.objects.filter(
                user=user,
                start_date__lte=end_date
            ).filter(
                Q(end_date__gte=start_date) | Q(end_date__isnull=True)
            )
        )

        # Helper: 특정 날짜에 Task가 적용되는지 판별하는 함수
        def task_applies_on(task, current_day):
            if task.repeat_type == 'once':
                return task.start_date == current_day
            elif task.repeat_type == 'weekly':
                # task.execute_days는 예: "월//수//금" 형식으로 저장됨
                weekday_mapping = {
                    'Mon': '월',
                    'Tue': '화',
                    'Wed': '수',
                    'Thu': '목',
                    'Fri': '금',
                    'Sat': '토',
                    'Sun': '일'
                }
                current_weekday = weekday_mapping[current_day.strftime('%a')]
                return current_weekday in task.execute_days
            else:
                # 기타 반복 유형: 단순히 해당 날짜가 Task 기간 내에 있는 경우 적용
                return True

        monthly_data_list = []
        total_completed = 0
        praise_days = 0

        # 4. 해당 월의 각 날짜에 대해 통계 산출
        current_day = start_date
        while current_day <= end_date:
            # 해당 날짜에 적용되는 Task 선정
            scheduled_tasks = [task for task in tasks if task_applies_on(task, current_day)]
            scheduled_count = len(scheduled_tasks)
            achieved_count = 0

            # 각 Task별 달성 기록 체크 (달성 기록의 achieved_date가 current_day와 일치)
            for task in scheduled_tasks:
                exists_coro = sync_to_async(RoutineTaskAchievement.objects.filter(task=task, achieved_date=current_day).exists)
                if await exists_coro():
                    achieved_count += 1

            if scheduled_count > 0:
                completion_rate = int((achieved_count / scheduled_count) * 100)
                status = "Completed" if completion_rate == 100 else "Incomplete"
            else:
                completion_rate = 0
                status = "No Task"

            # 해당 날짜에 예정된 Task가 있다면 통계 데이터에 추가
            if scheduled_count > 0:
                monthly_data = Monthly_Routine_Data(
                    routine_date=current_day,
                    completion_rate=completion_rate,
                    status=status
                )
                monthly_data_list.append(monthly_data)
                total_completed += achieved_count
                if completion_rate == 100:
                    praise_days += 1

            current_day += timedelta(days=1)

        responseData = UserRoutineMonthlyStatisticsResponseData(
            user_key=str(user.user_key),
            statistics_type="monthly",
            month=start_date,  # 월의 시작일을 month 필드에 사용
            total_completed=total_completed,
            praise_days=praise_days,
            monthly_data=monthly_data_list
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class UserBioInfoResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserBioInfoRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            responseData = UserBioInfoResponseData(
                user_key="",
                users_name="",
                profile_image="",
                bio="",
                subscription_status=False
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData: UserBioInfoResponseData
        try:
            user: CustomUser = CustomUser.objects.get(user_key=requestData.user_key)
            responseData = UserBioInfoResponseData(
                user_key=user.user_key,
                users_name=user.user_name,
                profile_image=user.profile_image,
                bio=user.bio,
                subscription_status=user.subscription_status
            )
        except CustomUser.DoesNotExist:
            responseData = UserBioInfoResponseData(
                user_key="",
                users_name="",
                profile_image="",
                bio="",
                subscription_status=False
            )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())

class UserBioInfoUpdateResponser(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        try:
            requestData = UserBioInfoUpdateRequestData(**content)
            print(requestData.get_json())
        except (json.JSONDecodeError, ValidationError) as e:
            print("데이터 처리 오류:", e)
            responseData = UserBioInfoUpdateResponseData(
                user_key="",
                status="fail",
                message="Missing data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response(requestData)

    async def process_response(self, requestData):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData: UserBioInfoUpdateResponseData
        try:
            user: CustomUser = CustomUser.objects.get(user_key=requestData.user_key)
            user.user_name = requestData.user_name
            user.profile_image = requestData.profile_image
            user.bio = requestData.bio
            responseData = UserBioInfoUpdateResponseData(
                user_key=requestData.user_key,
                status="Success",
                message="update_success"
            )
        except CustomUser.DoesNotExist:
            responseData = UserBioInfoUpdateResponseData(
                user_key=requestData.user_key,
                status="fail",
                message="Unknown user key"
            )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())
