import datetime
import json
from pydantic import BaseModel, ValidationError
from datetime import date, time

class LoginRequestData(BaseModel):
    login_type: str  # "kakao" 또는 "google"
    user_id: str
    user_pw: str
    access_token: str

    @classmethod
    def from_json(cls, json_str: str) -> "LoginRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class LoginResponseData(BaseModel):
    user_key: str  # "kakao" 또는 "google"
    access_token: str
    is_login_success: bool
    is_new_user:bool
    login_message: str
    user_info: str

    @classmethod
    def from_json(cls, json_str: str) -> "LoginResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserRegisterRequestData(BaseModel):
    login_type: str               # "kakao" 또는 "google"
    user_name: str                # 예: "홍길동"
    user_ID: str                  # 예: "Hongildon@kakao.com"
    user_PW: str                  # 예: ""
    access_token: str             # 예: "sdfjklweru38249"
    user_birth_date: date         # 예: "1996-03-04"
    user_education_level: int     # 예: 2
    desired_company: int          # 예: 0
    desired_job: str              # 예: "dev_2//3//5"
    job_prep_period_year: int     # 예: 1
    job_prep_period_month: int    # 예: 5
    job_prep_status: str          # 예: "0//1//5"
    job_difficulties: str         # 예: "3//6//8//9//10"
    interested_routine: bool      # 예: True

    @classmethod
    def from_json(cls, json_str: str) -> "UserRegisterRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserRegisterResponseData(BaseModel):
    user_key: str
    access_token: str
    is_registered: bool
    register_message: str
    user_info: str

    @classmethod
    def from_json(cls, json_str: str) -> "UserRegisterResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserInfoRequestData(BaseModel):
    user_key: str
    user_name: str

    @classmethod
    def from_json(cls, json_str: str) -> "UserInfoRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserInfoResponseData(BaseModel):
    user_key: str
    user_name: str
    desired_company: int
    desired_job: str
    is_subscribed: bool

    @classmethod
    def from_json(cls, json_str: str) -> "UserInfoResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserRoutineRequestData(BaseModel):
    user_key: str
    user_name: str
    request_date: date

    @classmethod
    def from_json(cls, json_str: str) -> "UserRoutineRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class TaskData(BaseModel):
    task_id: str
    task_name: str
    task_category: str
    execute_description: str
    execute_time: time
    completed: bool
    use_timer: bool
    time_filter: int

class UserRoutineResponseData(BaseModel):
    user_key: str
    user_name: str
    request_date: date
    task_list: list[TaskData]

    @classmethod
    def from_json(cls, json_str: str) -> "UserRoutineResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class AddRoutineRequestData(BaseModel):
    uers_key: str
    task_name: str
    task_category: str
    repeat_type: str
    execute_days: list[str]
    execute_description:str
    execute_time: time
    use_timer: bool
    time_filter: int
    start_date: date

    @classmethod
    def from_json(cls, json_str: str) -> "AddRoutineRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class AddRoutineResponseData(BaseModel):
    uers_key: str
    task_id: str
    is_added: bool
    routine_message: str

    @classmethod
    def from_json(cls, json_str: str) -> "AddRoutineResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class SuccessRoutineRequestData(BaseModel):
    uers_key: str
    user_name: str
    success_user_id: str

    @classmethod
    def from_json(cls, json_str: str) -> "SuccessRoutineRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class SuccessRoutineData(BaseModel):
    task_id: str
    task_name: str
    task_category: str
    execute_description: str
    execute_time: time
    time_filter: int

class SuccessRoutineResponseData(BaseModel):
    uers_key: str
    user_name: str
    success_user_id: str
    success_users_name: str
    current_company: str
    current_position: str
    profile_image: str
    university: str
    major: str
    graduation_year: str
    previous_job: str
    linkedin_url: str
    likes: int
    routine_date: date
    user_routine: list[SuccessRoutineData]

    @classmethod
    def from_json(cls, json_str: str) -> "SuccessRoutineResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class SuccessLikeRequestData(BaseModel):
    uers_key: str
    user_name: str
    success_user_id: str
    liked: bool

    @classmethod
    def from_json(cls, json_str: str) -> "SuccessLikeRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class SuccessLikeResponseData(BaseModel):
    uers_key: str
    user_name: str
    success_user_id: str
    likes: int

    @classmethod
    def from_json(cls, json_str: str) -> "SuccessLikeResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class SuccessRoutineCopyRequestData(BaseModel):
    uers_key: str
    success_user_id: str
    copy_type: str

    @classmethod
    def from_json(cls, json_str: str) -> "SuccessRoutineCopyRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class SuccessRoutineCopyResponseData(BaseModel):
    uers_key: str
    copied_tasks: int

    @classmethod
    def from_json(cls, json_str: str) -> "SuccessRoutineCopyResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserRoutineWeeklyStatisticsRequestData(BaseModel):
    user_key: str
    statistics_type: str
    start_date: date
    end_date: date

    @classmethod
    def from_json(cls, json_str: str) -> "UserRoutineWeeklyStatisticsRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class Weekly_Routine_Data(BaseModel):
    task_name: str
    completed_days: list[str]

class UserRoutineWeeklyStatisticsResponseData(BaseModel):
    user_key: str
    statistics_type: str
    start_date: date
    end_date: date
    total_completed: int
    praise_days: int
    weekly_data: list[Weekly_Routine_Data]

    @classmethod
    def from_json(cls, json_str: str) -> "UserRoutineWeeklyStatisticsResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserRoutineMonthlyStatisticsRequestData(BaseModel):
    user_key: str
    statistics_type: str
    month: date #달 저장시 문제가 생길 수 있음, 필요에 따라 변수 타입 변경 필요

    @classmethod
    def from_json(cls, json_str: str) -> "UserRoutineMonthlyStatisticsRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class Monthly_Routine_Data(BaseModel):
    routine_date: date
    completion_rate: int
    status: str

class UserRoutineMonthlyStatisticsResponseData(BaseModel):
    user_key: str
    statistics_type: str
    month: date
    total_completed: int
    praise_days: int
    monthly_data: list[Monthly_Routine_Data]

    @classmethod
    def from_json(cls, json_str: str) -> "UserRoutineMonthlyStatisticsResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserBioInfoRequestData(BaseModel):
    user_key: str
    user_name: str

    @classmethod
    def from_json(cls, json_str: str) -> "UserBioInfoRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserBioInfoResponseData(BaseModel):
    user_key: str
    users_name: str
    profile_image: str
    bio: str
    subscription_status: bool

    @classmethod
    def from_json(cls, json_str: str) -> "UserBioInfoResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserBioInfoUpdateRequestData(BaseModel):
    user_key: str
    user_name: str
    profile_image: str
    bio: str

    @classmethod
    def from_json(cls, json_str: str) -> "UserBioInfoUpdateRequestData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()

class UserBioInfoUpdateResponseData(BaseModel):
    user_key: str
    status: str
    message: str

    @classmethod
    def from_json(cls, json_str: str) -> "UserBioInfoUpdateResponseData":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            print("JSON 파싱 오류:", e)
            raise
        except ValidationError as e:
            print("데이터 유효성 검사 실패:", e)
            raise

    def get_json(self):
        return self.model_dump_json()






