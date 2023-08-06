class DjangoPgpyError(Exception):
    pass


class NoEncrypterFound(DjangoPgpyError):
    def __init__(self, encrypter_uid: 'django_pgpy.models.Identity', uid: 'django_pgpy.models.Identity'):
        super().__init__(f"The identity with ID={encrypter_uid.id} is not in the encrypter list of identity {uid.id}")