from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User


class ProfileOwnershipVerificationMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user_id = User.objects.get(pk=self.request.user.pk).id
        profile_user_id = User.objects.get(pk=self.kwargs['pk']).id
        return user_id == profile_user_id
