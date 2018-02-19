import logging

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import User, UserSerializer

log = logging.getLogger('accounts.views')


def user_signup_view(request):
    return render(request, template_name='users/new.html')


def user_signup_create(request):
    log.info("Signup submitted ...")
    try:
        if request.POST.get('password') != request.POST.get('confirm_password'):
            log.info('New user passwords do not match.')
            return HttpResponseBadRequest()
        user = User.objects.create_user(request.POST.get('username'),
                                        request.POST.get('password'),
                                        request.POST.get('email'))
        login(request, user)
    except AttributeError:
        log.exception('Error while creating a new user.')
        return HttpResponseBadRequest()
    else:
        log.info("Signup successful.")
        return redirect('home')


# pylint: disable=missing-docstring
class LoginView(GenericAPIView):
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser,]
    template_name = 'index.html'

    def get(self, request):
        log.info('Loading home view...')
        if request.user.is_authenticated:
            return Response({'user': request.user}, template_name=self.template_name)
        else:
            return render(request, template_name='index.html')

    def post(self, request, *args, **kwargs):
        log.info('User logging in...')
        try:
            user = authenticate(request,
                                username=request.POST.get('username'),
                                password=request.POST.get('password'))
            login(request, user)
        except (AttributeError, Exception):
            log.exception("Login failed: %s", request.POST)
            return Response({"error": "Login failed."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'user': user}, template_name=self.template_name)


# pylint: disable=missing-docstring
class UserDashboardView(RetrieveUpdateDestroyAPIView):
    """
    User can view and edit: profile, cleanups, and participation.
    Use formsets.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'user': request.user, 'cleanups': request.user.cleanups.all()},
                        template_name='users/detail.html')


# pylint: disable=missing-docstring
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser,)


# pylint: disable=missing-docstring
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


# pylint: disable=missing-docstring
class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
