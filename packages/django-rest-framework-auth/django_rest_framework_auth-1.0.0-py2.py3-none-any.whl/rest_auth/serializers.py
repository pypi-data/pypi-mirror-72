# -*- coding: utf-8 -*-
"""Serializer implementations for authentication.
"""
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model, login, password_validation
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Serializer for loggin in.
    It checks username and password are correct for settings.AUTH_USER_MODEL.

    After validating it, ``user`` instance created for authenticated user.
    View methods should persist this user.
    (through ``django.contrib.auth.login``)

    :param username: ``USERNAME_FIELD`` for AUTH_USER_MODEL
    :param password: user's password
    """
    username = serializers.CharField(
        label=_('Username'), max_length=254,
    )

    password = serializers.CharField(
        label=_('Password'), write_only=True,
        style={'input_type': 'password'},
    )

    default_error_messages = {
        'invalid_login': _(
            'Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }

    def validate(self, data):
        """Checks username & password.
        uses ``django.contrib.auth.authenticate``

        :param data: validated data from ``Serializer.validate``
        :return: validated_data
        :exception VaildationError: if username or password are incorrect
        """
        username = data['username']
        password = data['password']

        self.user = auth.authenticate(username=username, password=password)
        if self.user is None:
            raise serializers.ValidationError(
                self.error_messages['invalid_login'], code='invalid_login',
            )

        self.confirm_login_allowed(self.user)

        return data

    def confirm_login_allowed(self, user):
        """Checks if validated user is allowed for website.

        Override this method if you use custom authentication method
        and have additional methods for allowing login.

        :exception VaildationError: if user are not allowed
        """

    def create(self, validated_data):
        """persist a authenticated user in this step.

        :param validated_data: validated_data should contains ``request``.\
        You should pass request to serialzer.save.
        """
        user = self.get_user()
        request = validated_data.get('request')
        self.perform_login(request, user)

        return user

    def perform_login(self, request, user):
        """Persist a user. Override this method if you do more than
        persisting user.
        """
        login(request, user)

    def get_user(self):
        """
        :return: ``user`` instance created after ``self.validate``
        """
        return self.user


class PasswordResetSerializer(serializers.Serializer):
    """Sends a website link for resetting password.
    It uses django's ``PasswordResetForm`` directly because
    there is just one required field, `email`, and form implemented
    its business logic nicely.

    :param email: email address to receive password-reset-link.
    """
    email = serializers.EmailField(
        label=_('Email'), max_length=254,
    )

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        """
        :exception VaildationError: ``rest_framework``'s field validation
        :exception VaildationError: ``django``'s field vaildation
        """
        self.form = self.password_reset_form_class(data=self.initial_data)
        if not self.form.is_valid():
            if 'email' in self.form.errors:
                messages = self.form.errors['email']
            else:
                # XXX non email errors should be catched & re-raised
                # (if django's PasswordResetForm add new fields)
                messages = self.form.errors

            raise serializers.ValidationError(messages)

        return value

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=True, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """sends a email, which contains link for resetting password
        """
        return self.form.save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name, use_https=use_https,
            token_generator=token_generator, from_email=from_email,
            request=request, html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context,
        )


class SetPasswordSerializer(serializers.Serializer):
    """This serializer resets password of a given user.
    Please be VERY CAREFUL for using this any given user's password
    can be changed.

    Setting permission IsAdminUser is recommended.

    :param new_password1: new password
    :param new_password2: new password confirmation.
    """
    new_password1 = serializers.CharField(
        label=_('New password'),
        validators=[password_validation.validate_password],
        help_text=password_validation.password_validators_help_text_html(),
        write_only=True,
        style={'input_type': 'password'},
    )

    new_password2 = serializers.CharField(
        label=_('New password confirmation'),
        help_text=_('Enter the same password as before, for verification.'),
        write_only=True,
        style={'input_type': 'password'},
    )

    default_error_messages = {
        'password_mismatch': _('2 passwords should be equal'),
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        """
        :exception VaildationError: if two given passwords are different.
        """
        password1 = data.get('new_password1')
        password2 = data.get('new_password2')

        data['new_password2'] =\
            self._validate_new_password2(password1, password2)

        return data

    def _validate_new_password2(self, password1, password2):
        if password1 != password2:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def create(self, validated_data):
        """resets password
        """
        password = validated_data['new_password1']
        self.user.set_password(password)
        self.user.save()

        return self.user


class PasswordChangeSerializer(SetPasswordSerializer):
    """resets password of user.
    Resetting password is done if old_password is correct and
    two new passwords are equals.

    :param old_password: old_password
    :param new_password1: new password
    :param new_password2: new password confirmation.
    """
    old_password = serializers.CharField(
        label=_('Old password'),
        write_only=True,
        style={'input_type': 'password'},
    )

    default_error_messages = {
        'password_incorrect': _('Your old password was entered incorrectly. '
                                'Please enter it again.'),
    }

    def validate_old_password(self, old_password):
        """
        :exception ValidationError: if old_password is not correct
        """
        if not self.user.check_password(old_password):
            raise serializers.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect'
            )

        return old_password


class SignupSerializer(serializers.ModelSerializer):
    """Signup serializer for rest_framework & AUTH_USER_MODEL.

    Fields & methods are built on a django's defualt ``User`` model.
    Extend this serializer if you need your custom user model.

    (Even if ``AUTH_USER_MODEL`` is can be customized, this is recommended
    that You don't change & use customized user model.
    using custom user model is very complex.)

    :param username: ``USERNAME_FIELD`` of ``AUTH_USER_MODEL``
    :param email: ``User.get_email_field_name()``
    :param password1: password of a user (write_only, used only when created)
    :param password2: password confirmation (write_only)

    :TODO: Serializer Only implements creating. list/get are need to be implmtd
    """
    password1 = serializers.CharField(
        label=_('Password'),
        validators=[password_validation.validate_password],
        help_text=password_validation.password_validators_help_text_html(),
        write_only=True,
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        label=_('Password Confirmation'),
        help_text=_('Enter the same password as before, for verification.'),
        write_only=True,
        style={'input_type': 'password'},
    )

    default_error_messages = {
        'password_mismatch': _('2 passwords should be equal'),
    }

    EMAIL_FIELD_NAME = UserModel.get_email_field_name()

    class Meta:
        model = UserModel
        fields = (
            UserModel.USERNAME_FIELD, UserModel.get_email_field_name(),
            'password1', 'password2',
        )

        extra_kwargs = {
            UserModel.get_email_field_name(): {
                'required': True,
                'allow_blank': False,
            },
        }

    def validate(self, data):
        """Vaildates if two passwords are equal.

        :exception ValidationError: when 2 passwds are different
        """
        password1 = data.get('password1')
        password2 = data.get('password2')

        data['password2'] = self._validate_password2(password1, password2)

        return data

    def _validate_password2(self, password1, password2):
        if password1 != password2:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def create(self, validated_data):
        """Creates user instance

        CAVEAT:

        A clear difference between django's ``ModelForm`` and rest_framework's
        ``ModelSerializer`` is that, model serializer's ``save`` method doesn't
        respect form's ``commit=True``.

        Inside ``super().create``, a query is fired to create user,
        and inside this, additional query is fired to save hashed password.
        It's because ``ModelSerializer``'s ``create`` method uses
        default manager's create function, ``Model._default_manager.create()``

        (User model creation is recommended by calling ``UserManager``'s
        ``create_user`` method)

        :param validated_data: validated data created after ``self.vaildate``
        """
        password = validated_data.pop('password1')
        email_opts = validated_data.pop('email_opts', {})
        validated_data.pop('password2')

        # NOTE We should set user's password manually because
        # ModelSerializer.create calls model._default_manager.save().
        user = super(SignupSerializer, self).create(validated_data)
        user.set_password(password)

        # user activation through email confirmation.
        require_email_confirmation =\
            settings.REST_AUTH_SIGNUP_REQUIRE_EMAIL_CONFIRMATION

        update_fields = ['password']
        if require_email_confirmation:
            user, new_update_fields = self.set_user_as_unverified(user)
            update_fields.extend(new_update_fields)
            self.send_mail(user, **email_opts)

        user.save(update_fields=update_fields)

        return user

    def set_user_as_unverified(self, user):
        user.is_active = False
        return user, ['is_active']

    def send_mail(self, user, domain_override=None,
                  subject_template_name='registration/verify_email.txt',
                  email_template_name='registration/verify_email.html',
                  use_https=False, token_generator=default_token_generator,
                  from_email=None, request=None, html_email_template_name=None,
                  extra_email_context=None):
        """Send verification mail to newbie.
        """
        email = self.validated_data[self.EMAIL_FIELD_NAME]

        if domain_override:
            site_name = domain = domain_override
        else:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain

        protocol = 'https' if use_https else 'http'
        context = {
            'email': email, 'domain': domain, 'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user), 'protocol': protocol,
        }
        if extra_email_context is not None:
            context.update(extra_email_context)

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [email]
        )
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name, context
            )
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
