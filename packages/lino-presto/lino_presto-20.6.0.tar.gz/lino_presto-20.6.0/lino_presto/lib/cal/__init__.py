# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Extends :mod:`lino_xl.lib.cal` for :ref:`presto`.

.. autosummary::
   :toctree:

    fixtures.std
    fixtures.demo2

"""


from lino_xl.lib.cal import Plugin


class Plugin(Plugin):

    extends_models = ['Event', 'Room']
    partner_model = 'contacts.Worker'  # TODO: rename to "guest_model"

    def setup_main_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)

        m.add_action('cal.MyEntries')  # string spec to allow overriding
        m.add_action('cal.OverdueAppointments')
        m.add_action('cal.MyUnconfirmedAppointments')
        m.add_action('cal.MyOverdueAppointments')

        # m.add_separator('-')
        # m  = m.add_menu("tasks",_("Tasks"))
        m.add_action('cal.MyTasks')
        # m.add_action(MyTasksToDo)
        m.add_action('cal.GuestsNeedingReplacement')
        # m.add_action('cal.MyPresences')
        # m.add_action('cal.DailyPlanner')

    def get_dashboard_items(self, user):
        for i in super(Plugin, self).get_dashboard_items(user):
            yield i
        yield self.site.models.cal.GuestsNeedingReplacement
