from competitions.models import Competition
from django.http import HttpResponse
from django.views.generic import TemplateView
from web.models import Organizer, Partner

from bullet.utils.email import send_email


class BranchSpecificTemplateMixin:
    def get_template_names(self):
        previous = super().get_template_names()

        if self.request.BRANCH is None:
            return previous

        templates = []
        for template in previous:
            templates.append(f"{self.request.BRANCH.identifier}/{template}")
            templates.append(template)
        return templates


class HomepageView(BranchSpecificTemplateMixin, TemplateView):
    template_name = "web/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.branch = self.request.BRANCH

        try:
            context[
                "open_competition"
            ] = Competition.objects.currently_running_registration().get(
                branch=self.branch
            )
        except Competition.DoesNotExist:
            pass

        context["partners"] = Partner.objects.filter(branch=self.branch).all()
        context["organizers"] = Organizer.objects.filter(branch=self.branch).all()

        return context


def test(request):
    send_email(
        request.BRANCH,
        "adam@zahradnik.xyz",
        "Registrácia tímu",
        "mail/messages/registration.html",
        "mail/messages/registration.txt",
        {},
    )
    return HttpResponse("417")
