from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    """
    limit ten requests to login per five minutes
    """

    scope = "login"

    def parse_rate(self, rate):
        return 10, 300
