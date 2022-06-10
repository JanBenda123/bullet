from countries.models import BranchCountry
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

_country_cache = dict()


def get_country_cache() -> dict[int, dict[str, list[str]]]:
    if not len(_country_cache):
        countries = BranchCountry.objects.all()

        for c in countries:
            if c.branch not in _country_cache:
                _country_cache[c.branch] = dict()
            _country_cache[c.branch][c.country.code.lower()] = list(c.languages)

    return _country_cache


@receiver(post_save, sender=BranchCountry)
@receiver(post_delete, sender=BranchCountry)
def reset_cache(*args, **kwargs):
    _country_cache.clear()
