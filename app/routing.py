# your_app/routing.py
from django.urls import path
from . import WebResponser
from . import DummyWebResponser

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

    path('dummy_api/auth/login', DummyWebResponser.LoginResponser.as_asgi()),
    path('dummy_api/register', DummyWebResponser.UserRegisterResponser.as_asgi()),
    path('dummy_api/user-info', DummyWebResponser.UserInfoResponser.as_asgi()),
    path('dummy_api/routine_list', DummyWebResponser.UserRoutineResponser.as_asgi()),
    path('dummy_api/task/add', DummyWebResponser.AddRoutineResponser.as_asgi()),
    path('dummy_api/success_routine', DummyWebResponser.SuccessRoutineResponser.as_asgi()),
    path('dummy_api/success_routine_like', DummyWebResponser.SuccessLikeResponser.as_asgi()),
    path('dummy_api/success_routine_copy', DummyWebResponser.SuccessRoutineCopyResponser.as_asgi()),
    path('dummy_api/statistic/weekly', DummyWebResponser.UserRoutineWeeklyStatisticsResponser.as_asgi()),
    path('dummy_api/statistic/monthly', DummyWebResponser.UserRoutineMonthlyStatisticsResponser.as_asgi()),
    path('dummy_api/user/profile', DummyWebResponser.UserBioInfoResponser.as_asgi()),
    path('dummy_api/user/profile/update', DummyWebResponser.UserBioInfoUpdateResponser.as_asgi()),
]