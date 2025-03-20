# your_app/routing.py
from django.urls import path
from . import WebResponser

websocket_urlpatterns = [
    path('api/auth/login', WebResponser.LoginResponser.as_asgi()),
    path('api/register', WebResponser.UserRegisterResponser.as_asgi()),
    path('api/user-info', WebResponser.UserInfoResponser.as_asgi()),
    path('api/routine_list', WebResponser.UserRoutineResponser.as_asgi()),
    path('api/task/add', WebResponser.AddRoutineResponser.as_asgi()),
    path('api/success_routine', WebResponser.SuccessRoutineResponser.as_asgi()),
    path('api/success_routine_like', WebResponser.SuccessLikeResponser.as_asgi()),
    path('api/success_routine_copy', WebResponser.SuccessRoutineCopyResponser.as_asgi()),
    path('api/statistic/weekly', WebResponser.UserRoutineWeeklyStatisticsResponser.as_asgi()),
    path('api/statistic/monthly', WebResponser.UserRoutineMonthlyStatisticsResponser.as_asgi()),
    path('api/user/profile', WebResponser.UserBioInfoResponser.as_asgi()),
    path('api/user/profile/update', WebResponser.UserBioInfoUpdateResponser.as_asgi()),
]