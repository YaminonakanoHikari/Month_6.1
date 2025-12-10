from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # phone_number NOT required for normal users
        return self._create_user(email, password, phone_number, **extra_fields)

    def create_superuser(self, email, password, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError('Superuser must have a password.')
        # enforce phone_number for superuser
        if not phone_number:
            raise ValueError('Superuser must have a phone_number.')

        return self._create_user(email, password, phone_number, **extra_fields)
