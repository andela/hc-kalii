"""
Middle-ware for checking and adding failing checks if exists
This is will affect the behaviour of the unresolved checks button
"""
from hc.api.models import Check

class UnresolvedChecksMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            all_checks = list(Check.objects.filter(user=request.team.user).order_by("created"))
            failed = []
            for check in all_checks:
                try:
                    check.get_status()
                except TypeError:  # Raises type error if check is NoneType
                    continue
                else:
                    failed.append(check)
            if failed:
                request.has_unresolved_checks = True
                request.number_of_unresolved = len(failed)
            else:
                request.has_unresolved_checks = False

        return self.get_response(request)
