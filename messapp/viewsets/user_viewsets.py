from rest_framework import viewsets
from messapp.models import User
from messapp.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
import tempfile #to create temporary csv file of students.csv
from messapp.utils.parse_students import parse_students

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'hostel', 'roll_no']


    #Custom API to update a user's profile picture
    @action(detail=True, methods=['patch'])
    def updateprofilepic(self, request, pk=None):
        user= request.user()
        
        None


    @action(detail=False,methods=['POST'])
    def bulk_students(self, request, pk=None):
        csv_file= request.FILES.get("file")
        print("Inside Bulk Students")
        if not csv_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            for chunk in csv_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        # Parse the CSV
        student_data = parse_students(tmp_path)
        print(student_data)
        # Save data into DB
        try: 
            for entry in student_data:
                print(entry,'\n')
                User.objects.update_or_create(
                    username= entry['Roll Number'],
                    name=entry['Name'],
                    password= str(entry['Roll Number']+'@123'),
                    hostel=entry['Hostel'],
                    roll_no=entry['Roll Number'],
                    role='student',
                )
            return Response({"message": "Students created successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

         