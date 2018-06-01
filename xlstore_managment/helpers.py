import re
from django import template
from django.conf import settings
from django.template import defaultfilters
from django.utils.translation import gettext as _, ngettext
from decimal import Decimal
from django.utils.encoding import force_text
from django.utils.formats import number_format


intword_converters = (
    (6, lambda number: (
        ngettext('%(value).1f m', '%(value).1f m', number),
        ngettext('%(value)s m', '%(value)s m', number),
    )),
    (9, lambda number: (
        ngettext('%(value).1f b', '%(value).1f b', number),
        ngettext('%(value)s b', '%(value)s b', number),
    )),
    (12, lambda number: (
        ngettext('%(value).1f t', '%(value).1f t', number),
        ngettext('%(value)s t', '%(value)s t', number),
    )),
    (15, lambda number: (
        ngettext('%(value).1f quad', '%(value).1f quad', number),
        ngettext('%(value)s quad', '%(value)s quad', number),
    )),
    (18, lambda number: (
        ngettext('%(value).1f quint', '%(value).1f quint', number),
        ngettext('%(value)s quint', '%(value)s quint', number),
    )),
    (21, lambda number: (
        ngettext('%(value).1f sext', '%(value).1f sext', number),
        ngettext('%(value)s sext', '%(value)s sext', number),
    )),
    (24, lambda number: (
        ngettext('%(value).1f sept', '%(value).1f sept', number),
        ngettext('%(value)s sept', '%(value)s sept', number),
    )),
    (27, lambda number: (
        ngettext('%(value).1f oct', '%(value).1f oct', number),
        ngettext('%(value)s oct', '%(value)s oct', number),
    )),
    (30, lambda number: (
        ngettext('%(value).1f non', '%(value).1f non', number),
        ngettext('%(value)s non', '%(value)s non', number),
    )),
    (33, lambda number: (
        ngettext('%(value).1f dec', '%(value).1f dec', number),
        ngettext('%(value)s dec', '%(value)s dec', number),
    )),
    (100, lambda number: (
        ngettext('%(value).1f googol', '%(value).1f googol', number),
        ngettext('%(value)s googol', '%(value)s googol', number),
    )),
)



def intword(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000000:
        return value

    def _check_for_i18n(value, float_formatted, string_formatted):

        if settings.USE_L10N:
            value = defaultfilters.floatformat(value, 1)
            template = string_formatted
        else:
            template = float_formatted
        return template % {'value': value}

    for exponent, converters in intword_converters:
        large_number = 10 ** exponent
        if value < large_number * 1000:
            new_value = value / float(large_number)
            return _check_for_i18n(new_value, *converters(new_value))
    return value


def intcomma(value, use_l10n=True):
    
    if settings.USE_L10N and use_l10n:
        try:
            if not isinstance(value, (float, Decimal)):
                value = int(value)
        except (TypeError, ValueError):
            return intcomma(value, False)
        else:
            return number_format(value, force_grouping=True)
    orig = force_text(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new, use_l10n)
