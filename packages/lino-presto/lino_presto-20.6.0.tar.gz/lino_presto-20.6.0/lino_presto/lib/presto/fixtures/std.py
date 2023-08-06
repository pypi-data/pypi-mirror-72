# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Demo data for Lino Presto.

- Create two additional non-primary excerpt types for Orders.

"""
from django.conf import settings

from lino.api import dd, rt, _

def objects():
    ExcerptType = rt.models.excerpts.ExcerptType
    Order = rt.models.orders.Order
    Worker = rt.models.contacts.Worker
    ContentType = rt.models.contenttypes.ContentType

    yield ExcerptType(
        template="estimate.weasy.html",
        build_method='weasy2pdf',
        content_type=ContentType.objects.get_for_model(Order),
        **dd.str2kw('name', _("Cost estimate")))

    yield ExcerptType(
        template="sheet.weasy.html",
        build_method='weasy2pdf',
        content_type=ContentType.objects.get_for_model(Order),
        **dd.str2kw('name', _("Order sheet")))

    yield ExcerptType(
        template="week_planner.weasy.html",
        build_method='weasy2pdf',
        content_type=ContentType.objects.get_for_model(Worker),
        **dd.str2kw('name', _("Week planner")))
