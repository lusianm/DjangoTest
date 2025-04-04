import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .JsonClassis import *

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

        # 각 login_type에 따른 처리
        if loginrequestdata.login_type == "kakao":
            await self.process_kakao(loginrequestdata.user_id)
        elif loginrequestdata.login_type == "google":
            await self.process_google(loginrequestdata.user_id)
        else:
            await self.send_json({"error": f"알 수 없는 login_type: {loginrequestdata.login_type}"})

    async def process_kakao(self, user_id):
        # Kakao 로그인 처리 로직 (예시)
        print(f"[Kakao] 사용자 {user_id}의 로그인 처리 중...")
        login_response = LoginResponseData(
            user_key="kakao",
            access_token="abc123def456",
            is_login_success=True,
            is_new_user=False,
            login_message="로그인 성공",
            user_info="사용자 상세정보",
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

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData = UserRegisterResponseData(
            user_key="dummy_key_001",
            access_token="dummy_token_001",
            is_registered=True,
            register_message="Registration successful.",
            user_info="Sample user information."
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
            print("데이터 처리 오류:", e)
            responseData = UserInfoResponseData(
                user_key="",
                user_name="",
                desired_company=0,
                desired_job="",
                is_subscribed=False,
                message="Missing data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData = UserInfoResponseData(
            user_key="dummy_key_002",
            user_name="홍길동",
            desired_company=123,
            desired_job="Software Engineer",
            is_subscribed=True,
            message="Success"
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
            print("데이터 처리 오류:", e)
            responseData = UserRoutineResponseData(
                user_key="",
                user_name="",
                request_date=date(1, 1, 1),
                task_list=[],
                message="Missing data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
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
            task_list=[dummy_task1, dummy_task2],
            message="Success"
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
            print("데이터 처리 오류:", e)
            responseData = AddRoutineResponseData(
                uers_key=requestData.uers_key,
                task_id="",
                is_added=False,
                routine_message=f"Missing data: " + e
            )
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData = AddRoutineResponseData(
            uers_key="dummy_user_001",
            task_id="dummy_task_001",
            is_added=True,
            routine_message="Routine added successfully."
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
            responseData = SuccessRoutineResponseData(
                uers_key="",
                user_name="",
                success_user_id="",
                success_users_name="",
                current_company="",
                current_position="",
                profile_image="",
                university="",
                major="",
                graduation_year="",
                previous_job="",
                linkedin_url="",
                likes=0,
                routine_date=date(1, 1, 1),
                user_routine=[],
                message="Missing data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
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
            user_routine=[dummy_success_routine],
            message="Success"
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
            responseData = SuccessLikeResponseData(
                uers_key="",
                user_name="",
                success_user_id="",
                likes=0,
                message="Missing Data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")

        responseData = SuccessLikeResponseData(
            uers_key="dummy_user_001",
            user_name="홍길동",
            success_user_id="success_id_001",
            likes=100,
            message="Success"
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
            responseData = SuccessRoutineCopyResponseData(
                uers_key="",
                copied_tasks=0,
                message="Missing data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")

        responseData = SuccessRoutineCopyResponseData(
            uers_key="dummy_user_004",
            copied_tasks=3,
            message="Success"
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
            print("데이터 처리 오류:", e)
            responseData = UserRoutineWeeklyStatisticsResponseData(
                user_key="",
                statistics_type="",
                start_date=date(1, 1, 1),
                end_date=date(1, 1, 1),
                total_completed=0,
                praise_days=0,
                weekly_data=[],
                message="Missing Data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")

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
            weekly_data=[dummy_weekly_routine1, dummy_weekly_routine2],
            message="Success"
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
            print("데이터 처리 오류:", e)
            responseData = UserRoutineMonthlyStatisticsResponseData(
                user_key="",
                statistics_type="",
                month=date(1, 1, 1),
                total_completed=1,
                praise_days=1,
                monthly_data=[],
                message="Missing Data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")

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
            monthly_data=[dummy_monthly_routine1, dummy_monthly_routine2],
            message="Success"
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
            print("데이터 처리 오류:", e)
            responseData = UserBioInfoResponseData(
                user_key="",
                users_name="",
                profile_image="",
                bio="",
                subscription_status=False,
                message="Missing Data: " + e
            )
            print(responseData.get_json())
            await self.send_json(responseData.get_json())
            return

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData = UserBioInfoResponseData(
            user_key="dummy_user_bio_001",
            users_name="홍길동",
            profile_image="https://example.com/profile.jpg",
            bio="This is a sample bio for testing.",
            subscription_status=True,
            message="Success"
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

        await self.process_response()

    async def process_response(self):
        # Kakao 로그인 처리 로직 (예시)
        print(f"사용자 데이터 응답중...")
        responseData = UserBioInfoUpdateResponseData(
            user_key="dummy_user_update_001",
            status="Success",
            message="update_success"
        )
        print(responseData.get_json())
        await self.send_json(responseData.get_json())
