# -*- coding: UTF-8 -*-
# Copyright 2018-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _

rt.models.system.SiteConfigs.detail_layout = """
site_company next_partner_id:10
default_build_method simulate_today
site_calendar default_event_type
max_auto_events hide_events_before
"""

# if False:
#     rt.models.calview.WeekDetail.main = "body workers"
#     rt.models.calview.WeekDetail.workers = dd.Panel("""
#     navigation_panel:15 contacts.WorkersByWeek:85
#     """, label=_("Workers"))
# else:
#     # rt.models.calview.WeekDetail.main = "body contacts.WorkersByWeek"
#     rt.models.calview.WeekDetail.body = "navigation_panel:15 contacts.WorkersByWeek:85"
