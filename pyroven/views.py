import urllib

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from pyroven import UserNotAuthorised

from pyroven.utils import setting, HttpResponseSeeOther

def raven_return(request):
    # Get the token which the Raven server sent us - this should really
    # have a try/except around it to catch KeyError
    token = request.GET['WLS-Response']

    # See if this is a valid token
    try:
        user = authenticate(response_str=token)
    except UserNotAuthorised:
        return setting('PYROVEN_NOT_AUTHORISED',
                       default=HttpResponseForbidden("Authentication successful but you are not authorised "
                                                     "to access this site"))

    if user is None:
        return redirect(setting('PYROVEN_LOGOUT_REDIRECT', default='/'))
    else:
        login(request, user)
    
    # Redirect somewhere sensible
    return HttpResponseRedirect('/')


def raven_login(request):
    # Get the Raven object and return a redirect to the Raven server
    login_url = setting('PYROVEN_LOGIN_URL')
    encoded_return_url = urllib.quote(setting('PYROVEN_RETURN_URL'))
    return HttpResponseSeeOther("%s?ver=%d&url=%s" % (login_url, 3, encoded_return_url))


def raven_logout(request):
    logout(request)
    return redirect(setting('PYROVEN_LOGOUT_REDIRECT', default='/'))
