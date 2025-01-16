import logging
import time
from collections import defaultdict
from datetime import datetime
from django.http import HttpResponseForbidden
from django.urls import resolve


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # configure logging to write request.log
        logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(message)s")
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "No Authorization Header")
        print(f"DEBUG: Authorization header: {auth_header}")
        # log request details
        user = request.user if request.user.is_authenticated else "Anonymous"
        print(f"DEBUG: User is_authenticated={request.user.is_authenticated}, User={user}")
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        
        # restrict hours (9pm to 6am)
        restricted_hours = (21 <= current_hour or current_hour < 6)
        if restricted_hours:
            return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Acess to this server is restricted during the hours of 9 PM to 6 AM.</p>")
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # dictionary to track message counts and timestamps by IP
        self.ip_message_tracker = defaultdict(list)

        # set message limits
        self.message_limit = 5
        self.time_window = 60

    def __call__(self, request):
        if request.method == "POST":
            # get user's ip
            user_ip = self.get_client_ip(request)
            current_time = time.time()

            # clean up old timestamps outside the time window
            message_times = self.ip_message_tracker[user_ip] # all messages by user's IP
            self.ip_message_tracker[user_ip] = [
                timestamp for timestamp in message_times
                if current_time - timestamp < self.time_window
            ] # filter/retain only recent (60s) messages

            # check if the limit is exceeded
            if len(self.ip_message_tracker[user_ip]) > self.message_limit:
                return HttpResponseForbidden("<h1>403 Forbidden</h1><p>You have exceeded the allowed message limit. Please wait a moment and try again</p>")

            # add the current timestamp
            self.ip_message_tracker[user_ip].append(current_time)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """
        Extract the client's IP address from the request.
        Handles cases where a reverse proxy might be in use.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class RolePermissionMiddleware:
    def __init__(self, get_reponse):
        self.get_response = get_reponse

    def __call__(self, request):
        """
        Check if the user has the required role before proceeding with the request.
        Allowed roles: 'admin', 'host'
        """

        # List public routes that dont require authentication or role checking
        public_routes = ['register', 'login']

        # get current route
        current_route = resolve(request.path_info).url_name

        # skip role checks for public routes
        if current_route in public_routes:
            return self.get_response(request)

        # skip role check for unauthenticated users
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access denied: You must be logged in to perform this action.</p>"
            )

        # check if the user has the required role
        allowed_roles = ['admin', 'host']
        if request.user.role not in allowed_roles:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access denied: Your role does not have permissions to perform this action.</p>"
            )
        
        response = self.get_response(request)
        return response
    