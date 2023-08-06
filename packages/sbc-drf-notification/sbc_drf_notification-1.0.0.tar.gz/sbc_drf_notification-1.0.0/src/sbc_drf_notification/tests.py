from sbc_drf.tests import TestCase, SetupUserTestCaseMixin

from .factories import NotificationFactory


class NotificationTest(SetupUserTestCaseMixin, TestCase):
    ENDPOINT = '/notifications'

    def test_create_simple_email(self):
        notification = NotificationFactory(kind='generic', to_users=[self.user])
        notification.send()
