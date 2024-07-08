from rest_framework.response import Response
from rest_framework.request import Request, HttpRequest
from rest_framework.views import APIView
import jwt

from students.classes import Student
from tables.classes import TableManager, TableManagerInterface, TableInterface, TableFactory, TableFactoryInterface
from students.classes import StudentsIteratorManager, StudentsIteratorFactory
from students.interfaces import StudentIteratorInterface, StudentIteratorManagerInterface
from api.utils import authorization
from codefuture_bank.settings import SECRET_KEY
from apps.models import Apps


class RegisterAppView(APIView):

    def post(self, request):
        if request.headers.get("auth_token") != SECRET_KEY:
            return Response({"status": 403, "message": "permissions denied"})

        name = request.query_params.get("name")

        try:
            app = Apps.objects.get(name=name)
        except Apps.DoesNotExist:

            app = Apps(name=name)
            app.save()

        token = jwt.encode({"id": app.id,
                            "name": app.name},
                           SECRET_KEY)

        return Response({"status": 200, "message": "app successful created", "token": token})


class RegisterIterator(APIView):
    @authorization
    def post(self, request, *args, **kwargs):
        iter_name = request.query_params.get('iter_name')
        table_name = request.query_params.get('table_name')
        iter_type = request.query_params.get('iter_type')

        factory = StudentsIteratorFactory()
        table_manager = TableManager()

        table = table_manager.get(table_name)
        factory.create(iter_name, table, iter_type)

        return Response({"status": True, "message": None})


class CreateTableView(APIView):
    @authorization
    def post(self, request, *args, **kwargs):
        table_name = request.query_params.get('table_name')
        sheet_name = request.query_params.get('sheet_name')
        sheet_id = request.query_params.get('sheet_id')
        fcs_column = int(request.query_params.get('fcs_column'))
        status_column = int(request.query_params.get('status_column'))
        phone_column = int(request.query_params.get('phone_column'))

        factory = TableFactory()
        try:
            factory.create(table_name, sheet_id, sheet_name, fcs_column, status_column, phone_column)

            return Response({'status': True, "message": None})
        except ValueError:
            return Response({'status': False, 'message': f"table {table_name} already exists"})


class CreateStudentView(APIView):
    @authorization
    def post(self, request, *args, **kwargs):
        telegram_id = request.query_params.get('telegram_id')
        fcs = request.query_params.get('fcs')
        phone = request.query_params.get('phone')
        username = request.query_params.get('username')

        student = Student(telegram_id, fcs, phone, username)
        try:
            student.create_student()
            return Response({"status": True})

        except ValueError:
            return Response({"status": False})


class StudentSetStatusView(APIView):

    @authorization
    def post(self, request, *args, **kwargs):
        table_name = request.query_params.get('table_name')
        row = int(request.query_params.get('row'))
        status = request.query_params.get('status')

        table_manager: TableManagerInterface = TableManager()
        try:
            table: TableInterface = table_manager.get(table_name)
            table.set_status(row, status)
            return Response({"status": True, "message": None})
        except ValueError:
            return Response({"status": False, "message": f"table {table_name} does not exist"})


class GetNextLine(APIView):
    @authorization
    def get(self, request, *args, **kwargs):
        iterator_name = request.query_params.get('iterator_name')

        manager: StudentIteratorManagerInterface = StudentsIteratorManager()
        try:
            iterator: StudentIteratorInterface = manager.get(iterator_name)
            row: Student = iterator.next()
            return Response({"status": True, "message": "", "telegram_id": row.telegram_id, "username": row.username, "phone": row.phone, "fcs": row.fcs})
        except ValueError as error:
            return Response({"status": False, "message": f"iterator {iterator_name} does not exist"})




