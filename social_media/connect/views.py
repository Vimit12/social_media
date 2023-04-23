# Import necessary modules
from http import HTTPStatus
import copy
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils import timezone
from utils.constants import USER_NAME_EXISTS, USER_NAME_AVAILABLE, USER_CREATED, RESPONSE_DATA, USER_NOT_FOUND, \
    USER_AUTH_FAIL
from utils.jsonvalidator.json_validator import CustomJsonValidator
from utils.serializers import connect_serializer
from .models import ConnectMeUser
from utils.authenticate.authentication import TokenGeneration
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


# Define an API view for username
class UserNameAPI(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        # Get the request data
        _data = request.data
        print(_data)

        # Define a response data dictionary with default values
        response_data = RESPONSE_DATA

        try:
            _user_obj = ConnectMeUser.objects.filter(user__username=_data.get("username"))

            if _user_obj.count():
                response_data.update(
                    {"message": USER_NAME_EXISTS, "status_code": HTTPStatus.CONFLICT}
                )
            else:
                # Update the response data with whether username is available
                response_data.update(
                    {"message": USER_NAME_AVAILABLE, "status_code": HTTPStatus.OK}
                )

        except Exception as e:
            response_data.update(
                {"error": str(e), "status_code": HTTPStatus.INTERNAL_SERVER_ERROR}
            )

        # Return a JsonResponse with the response data
        return JsonResponse(response_data)


# Define an API view for sign up
class SignUp(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        # Get the request data
        _data = request.data
        print(_data)

        # Define a response data dictionary with default values
        response_data = RESPONSE_DATA

        try:
            with transaction.atomic():
                # Create a savepoint for the transaction
                savepoint_id = transaction.savepoint()

                # Define the schema file name
                schema_file_name = "sign_up.json"
                # Validate the JSON data using the CustomJsonValidator
                obj = CustomJsonValidator(schema_file_name, _data)
                schema_status, msg = obj.flag, obj.message

                # If the JSON data is valid according to the schema
                if schema_status:
                    # Extract the name field from the data and split it into first and last name
                    name = _data.pop("name").split(" ")
                    _data.update(
                        {"first_name": name[0], "last_name": " ".join(name[1:])}
                    )

                    # Serialize the data using the UserSerializer
                    serializer = connect_serializer.UserSerializer(data=_data)
                    # If the data is valid according to the serializer
                    if serializer.is_valid():
                        # Save the user object
                        user = serializer.save()
                        print(user)

                        # Update the response data with a success message and status code
                        response_data.update(
                            {
                                "message": USER_CREATED,
                                "status_code": HTTPStatus.OK,
                            }
                        )
                    else:
                        # Update the response data with validation errors
                        # and a status code indicating a bad request
                        print(serializer.errors)
                        response_data.update(
                            {
                                "error": serializer.errors,
                                "status_code": HTTPStatus.BAD_REQUEST,
                            }
                        )
                else:
                    # Update the response data with the validation error message
                    # and a status code indicating a bad request
                    response_data.update(
                        {"error": msg, "status_code": HTTPStatus.BAD_REQUEST}
                    )

        except Exception as e:
            # Rollback the transaction to the savepoint in case of an exception
            transaction.savepoint_rollback(savepoint_id)

            # Log the error
            print(f"An error occurred: {str(e)}")
            response_data.update(
                {"error": str(e), "status_code": HTTPStatus.INTERNAL_SERVER_ERROR}
            )
        else:
            # Commit the transaction if no exceptions occurred
            transaction.commit()

        # Return a JsonResponse with the response data
        return JsonResponse(response_data)


# Define LoginAPI after user creation
@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request) -> RESPONSE_DATA:
        # Get the request data
        _data = request.data
        print(_data)

        # Define a response data dictionary with default values
        response_data = RESPONSE_DATA

        try:
            with transaction.atomic():
                # Create a savepoint for the transaction
                savepoint_id = transaction.savepoint()

                # Define the schema file name
                schema_file_name = "login.json"
                # Validate the JSON data using the CustomJsonValidator
                obj = CustomJsonValidator(schema_file_name, _data)
                schema_status, msg = obj.flag, obj.message

                # If the JSON data is valid according to the schema
                if schema_status:

                    user = authenticate(username=_data.get("username"), password=_data.get("password"))
                    if user:
                        _user_obj = ConnectMeUser.objects.get(user__username=_data.get("username"),
                                                              deleted_at=None)
                        if _user_obj:
                            access_token = TokenGeneration.generate_access_token()
                            refresh_token = TokenGeneration.generate_refresh_token()

                            _user_obj.access_token = access_token
                            _user_obj.refresh_token = refresh_token
                            _user_obj.updated_at = timezone.now()
                            _user_obj.save()

                            _user_data = _user_obj._get_detail

                            response_data.update(
                                {"message": _user_data, "status_code": HTTPStatus.OK}
                            )
                        else:
                            response_data.update(
                                {"error": USER_NOT_FOUND, "status_code": HTTPStatus.NOT_FOUND}
                            )
                    else:
                        response_data.update(
                            {"error": USER_AUTH_FAIL, "status_code": HTTPStatus.UNAUTHORIZED}
                        )
                else:
                    # Update the response data with the validation error message
                    # and a status code indicating a bad request
                    response_data.update(
                        {"error": msg, "status_code": HTTPStatus.BAD_REQUEST}
                    )

        except Exception as e:
            # Rollback the transaction to the savepoint in case of an exception
            transaction.savepoint_rollback(savepoint_id)

            # Log the error
            print(f"An error occurred: {str(e)}")
            response_data.update(
                {"error": str(e), "status_code": HTTPStatus.INTERNAL_SERVER_ERROR}
            )
        else:
            # Commit the transaction if no exceptions occurred
            transaction.commit()

        # Return a JsonResponse with the response data
        return JsonResponse(response_data)
