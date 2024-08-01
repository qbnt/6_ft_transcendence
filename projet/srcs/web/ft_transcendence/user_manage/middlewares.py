import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = now()
        last_activity = request.session.get('last_activity')

        if last_activity:
            last_activity_time = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=current_time.tzinfo)
            if (current_time - last_activity_time).seconds > settings.SESSION_COOKIE_AGE:
                request.user.is_onsite = False
                request.user.save()
                messages.warning(request, 'You have been logged out due to inactivity.')
                logout(request)
        else:
            request.user.is_onsite = True
            request.user.save()

        request.session['last_activity'] = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')