from django.contrib.auth.backends import ModelBackend


def create_identity(user, password, superuser_identities):
    from django_pgpy.models import Identity

    if user and user.is_authenticated and not Identity.objects.exists_for_user(user):
        Identity.objects.create(user, password, list(superuser_identities))


def add_superusers_to_identity(user, password, superuser_identities):
    from django_pgpy.models import Identity

    if user and user.is_authenticated:
        identity = Identity.objects.get(user=user)

        if list(identity.encrypters.all().order_by('user__id')) != list(superuser_identities.all().order_by('user__id')):
            identity.add_restorers(password, list(superuser_identities.all().order_by('user__id')))


def process_key_recovery_requests(user, password):
    from django_pgpy.models import RequestKeyRecovery
    if user and user.is_authenticated and user.is_superuser and hasattr(user, 'pgp_identity'):
        open_requests = RequestKeyRecovery.objects.filter(reset_by=None)
        for request in open_requests:
            request.reset_password(user.pgp_identity, password)


class ModelUserWithIdentityBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        from django_pgpy.models import Identity

        user = super().authenticate(request, username, password, **kwargs)

        superuser_identities = Identity.objects.filter(user__is_superuser=True).exclude(user=user)
        create_identity(user, password, superuser_identities)

        return user


class ModelUserWithIdentityAndSuperuserRestorersBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        from django_pgpy.models import Identity

        user = super().authenticate(request, username, password, **kwargs)
        superuser_identities = Identity.objects.filter(user__is_superuser=True).exclude(user=user)

        create_identity(user, password, superuser_identities)
        add_superusers_to_identity(user, password, superuser_identities)
        process_key_recovery_requests(user, password)

        return user


class IdentityLoginAction:

    def run(self, request, user, username, password=None, **kwargs):
        from django_pgpy.models import Identity

        if user and user.is_authenticated:
            superuser_identities = Identity.objects.filter(user__is_superuser=True).exclude(user=user)

            create_identity(user, password, superuser_identities)
            add_superusers_to_identity(user, password, superuser_identities)
            process_key_recovery_requests(user, password)
