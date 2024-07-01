from django.urls import path

from api.views import (
RegisterAppView, RegisterIterator, CreateTableView, CreateStudentView, StudentSetStatusView, GetNextLine
)


urlpatterns = [
    path('register_app/', RegisterAppView.as_view()),
    path('register_iterator/', RegisterIterator.as_view()),
    path('register_table/', CreateTableView.as_view()),
    path('register_student/', CreateStudentView.as_view()),
    path('set_status/', StudentSetStatusView.as_view()),
    path('get_next_line/', GetNextLine.as_view()),
]