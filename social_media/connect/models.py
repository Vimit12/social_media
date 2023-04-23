import uuid

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
# from django_minio_storage.storage import MinioStorage
from utils.models.abstract_model import CommonItems

User = get_user_model()


class ProfilePicture(models.Model):
    profile = models.ForeignKey("ConnectMeUser", on_delete=models.CASCADE)
    # profile_picture = models.ImageField(storage=MinioStorage(), upload_to='profile_pics/',
    #                                     default='default_profile_pic.jpg')

    # Add any other fields for the profile picture here
    def __str__(self):
        return f'{self.profile.user.username} Profile Picture'

class ConnectMeUser(CommonItems):
    """
    Connect Me User model will inherit CommonItems and will have user model as one to one field.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_regex = RegexValidator(
        regex=r"^\+?\d{9,15}$",
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    mobile = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    access_token = models.JSONField(blank=True, null=True)

    refresh_token = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "connect_me_user"
        verbose_name = "Connect Me User"
        verbose_name_plural = "Connect Me Users"

    def __str__(self):
        return f"{self.id}"

    @property
    def _get_detail(self):
        _detail = {
            "id": str(self.id),
            "username": self.user.username,
            "name": self.user.first_name + " " + self.user.last_name,
            "email": self.user.email,
            "mobile": self.mobile,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "last_login": self.user.last_login
        }
        return _detail
