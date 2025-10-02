from uuid import UUID
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        password=None,
        first_name=None,
        last_name=None,
        is_superuser=False,
        is_staff=False,
        active=True,
        role_ids=[]
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have an password")
        user = self.model(email=self.normalize_email(email))
        user.fist_name = first_name
        user.last_name =  last_name
        user.is_superuser = is_superuser
        user.is_staff =  is_staff
        user.set_password(password)  # change user password
        user.active = active
        user.save(using=self._db)
        if role_ids is not None and len(role_ids) > 0:
            role_ids = [UUID(hex=item) if isinstance(item, str) else item for item in role_ids]
            user.roles.add(*role_ids)
        return user
