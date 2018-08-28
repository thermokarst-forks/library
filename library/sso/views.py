import uuid
import base64
import hashlib
import hmac

from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.conf import settings
from django.urls import reverse

User = get_user_model()


def sso_redirect_to_provider(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.GET.get('next', '/'))

    nonce = uuid.uuid4().hex
    secret = settings.DISCOURSE_SSO_SECRET.encode('utf8')
    provider = settings.DISCOURSE_SSO_PROVIDER

    request.session['sso_nonce'] = nonce

    params = request.GET.copy()
    try:
        del params['sso']
        del params['sig']
    except KeyError:
        pass
    if params:
        params = '?' + params.urlencode()
    else:
        params = ''

    return_path = reverse('sso_callback') + params
    return_url = request.build_absolute_uri(return_path)

    payload = QueryDict(mutable=True)
    payload['nonce'] = nonce
    payload['return_sso_url'] = return_url
    payload = base64.b64encode(payload.urlencode().encode('utf8'))

    signature = hmac.new(
        secret, msg=payload, digestmod=hashlib.sha256).hexdigest()

    provider_url = 'https://%s/session/sso_provider?sso=%s&sig=%s' % (
        provider, payload.decode('utf8'), signature)

    return HttpResponseRedirect(provider_url)


def sso_client_callback(request):
    try:
        payload = request.GET['sso'].encode('utf8')
        signature = request.GET['sig']
    except KeyError:
        return HttpResponse('This request was not signed.', status=422)

    secret = settings.DISCOURSE_SSO_SECRET.encode('utf8')
    exp_signature = hmac.new(
        secret, msg=payload, digestmod=hashlib.sha256).hexdigest()
    if exp_signature != signature:
        return HttpResponse('Request signature does not match expected.', status=422)

    payload = QueryDict(base64.b64decode(payload).decode('utf8'))
    nonce = payload['nonce']
    try:
        exp_nonce = request.session.pop('sso_nonce')
    except KeyError:
        return HttpResponse('Invalid session.', status=422)
    if nonce != exp_nonce:
        return HttpResponse('Login replay detected.', status=422)

    user, user_was_created = User.objects.update_or_create(
        forum_external_id=payload['external_id'],
        defaults={
            'username': payload['username'],
            'email': payload['email'],
            'full_name': payload['name'],
            'forum_external_id': payload['external_id'],
            'forum_avatar_url': payload['avatar_url'],
            # TODO: come up with better casting here
            'forum_is_admin': payload['admin'] == 'true',
            'forum_is_moderator': payload['moderator'] == 'true',
        }
    )
    if user_was_created:
        user.set_unusable_password()
        user.save()

    users_groups = []
    for group in [g.strip() for g in payload['groups'].split(',')]:
        user_group, _ = Group.objects.get_or_create(name=group)
        users_groups.append(user_group)

    user.groups.add(*users_groups)

    update_session_auth_hash(request, user)
    login(request, user)

    return HttpResponseRedirect(request.GET.get('next', '/'))


def sso_client_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))
