# your_app/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .JsonClassis import *

class LoginConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 클라이언트와 연결되면 연결 승인
        await self.accept()
        print("WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료됨")

    async def receive_json(self, content, **kwargs):
        """
        클라이언트로부터 JSON 데이터를 수신하면 호출됩니다.
        content는 이미 dict 형태로 파싱되어 전달됩니다.
        """
        print(f"Test")
        login_type = content.get("login_type")
        user_id = content.get("user_id")
        user_pw = content.get("user_pw")
        access_token = content.get("access_token")

        # 각 login_type에 따른 처리
        if login_type == "kakao":
            await self.process_kakao(user_id)
        elif login_type == "google":
            await self.process_google(user_id)
        else:
            await self.send_json({"error": f"알 수 없는 login_type: {login_type}"})

    async def process_kakao(self, user_id):
        # Kakao 로그인 처리 로직 (예시)
        print(f"[Kakao] 사용자 {user_id}의 로그인 처리 중...")
        print(f"test2")
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

    async def process_google(self, user_id):
        # Google 로그인 처리 로직 (예시)
        print(f"[Google] 사용자 {user_id}의 로그인 처리 중...")
        await self.send_json({"message": f"Google 로그인 처리 완료: {user_id}"})