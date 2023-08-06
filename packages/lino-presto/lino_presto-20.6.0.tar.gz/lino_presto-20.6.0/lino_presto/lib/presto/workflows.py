# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for the :ref:`presto` applications.

Extends :mod:`lino_xl.lib.cal.workflows.voga` and
:mod:`lino_xl.lib.courses.workflows`.

"""

from lino.api import _


# If we want to change the text and/or button_text of a state, we must
# do this *before* workflow modules are loaded because transition
# actions would otherwise get the unchanged text or button_text.

from lino_xl.lib.cal.choicelists import EntryStates
EntryStates.cancelled.button_text = "⚕"
EntryStates.cancelled.text = _("Called off")
EntryStates.draft.text = _("Scheduled")


from lino_xl.lib.cal.workflows.voga import *
from lino_xl.lib.courses.workflows import *

EntryStates.ignore_required_states = True

add = EntryStates.add_item
add('60', _("Missed"), 'missed', fixed=True,
    help_text=_("Client missed the appointment."),
    button_text="☉", noauto=True)  # \u2609 SUN

EntryStates.missed.add_transition(
    required_states='cancelled suggested draft took_place')

# Do not check guest states when marking an entry as took place
# calendar entry can have taken place even though there are invited workers.
EntryStates.took_place.transition.refuse_guest_states = None

    

# print("20181107b", EntryStates.draft.button_text)

GuestStates.clear()
add = GuestStates.add_item
# add('10', _("Suggested"), 'suggested', button_text="?")
add('10', _("Present"), 'invited', button_text="☑")
# add('20', _("Present"), 'present', afterwards=True, button_text="☑")
# add('30', _("Done"), 'done', afterwards=True, button_text="☑")
# add('40', _("Cancelled"), 'cancelled', button_text="C")
add('50', _("Needs replacement"), 'needs', afterwards=True, button_text="⚕")
add('60', _("Found replacement"), 'found', button_text="☉")
# add('10', "☐", 'invited')
# add('40', "☑", 'present', afterwards=True)
# add('50', "☉", 'missing', afterwards=True)
# add('60', "⚕", 'excused')

GuestStates.clear_transitions()
# GuestStates.ignore_required_states = True
GuestStates.invited.add_transition(required_states='needs found')
GuestStates.needs.add_transition(required_states='invited found')
GuestStates.found.add_transition(required_states='invited needs')
