import time
from datetime import datetime
from django.conf import settings
from django.contrib.auth import logout


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the session has a last_active timestamp
            last_active = request.session.get('last_active')
            if last_active is not None:
                # Check if the user has been inactive for longer than the configured time
                elapsed = time.time() - last_active
                if elapsed > settings.AUTO_LOGOUT_DELAY:
                    # Log the user out and delete the session
                    logout(request)
                    try:
                        del request.session['last_active']
                    except KeyError:
                        pass
            # Update the last_active timestamp in the session
            request.session['last_active'] = time.time()

        try:
            response = self.get_response(request)
        except KeyError as e:
            if str(e) == "'last_active'":
                # Handle the KeyError exception here
                request.session['last_active'] = datetime.now()
                response = self.get_response(request)
            else:
                raise e
            
        return response