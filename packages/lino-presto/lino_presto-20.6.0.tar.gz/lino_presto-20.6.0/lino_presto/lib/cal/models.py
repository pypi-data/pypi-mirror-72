# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from etgen.html import E, iselement
from etgen.html2rst import html2rst

from django.utils.translation import ugettext_lazy as _
from lino.core.gfks import gfk2lookup
from lino.core.fields import make_remote_field

from lino_xl.lib.cal.models import *
from lino_xl.lib.cal.choicelists import EntryStates, GuestStates

from lino.modlib.users.choicelists import UserTypes

# from lino_xl.lib.courses.choicelists import EnrolmentStates
from lino_xl.lib.invoicing.mixins import InvoiceGenerator

# courses = dd.resolve_app('courses')

# from lino.modlib.office.roles import OfficeUser
from lino_presto.lib.contacts.models import PrintRoster
from lino.modlib.printing.mixins import Printable


class Room(Room, Referrable, Printable):

    ref_max_length = 5

    class Meta(Room.Meta):
        abstract = dd.is_abstract_model(__name__, 'Room')
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    event_type = dd.ForeignKey('cal.EventType',blank=True, null=True)
    guest_role = dd.ForeignKey("cal.GuestRole", blank=True, null=True)
    invoicing_area = dd.ForeignKey('invoicing.Area', blank=True, null=True)

    print_roster = PrintRoster()

    @dd.displayfield(_("Print"))
    def print_actions(self, ar):
        if ar is None:
            return ''
        elems = [
            ar.instance_action_button(
                self.print_roster)]
        return E.p(*join_elems(elems, sep=", "))



class RoomDetail(dd.DetailLayout):
    main = """
    ref name id print_actions
    invoicing_area event_type guest_role display_color
    company contact_person contact_role
    cal.EntriesByRoom contacts.MembershipsByRoom
    """


class Rooms(Rooms):
    column_names = "name event_type *"


#
class Event(Event, InvoiceGenerator):

    class Meta(Event.Meta):
        abstract = dd.is_abstract_model(__name__, 'Event')

    summary_show_user = False

    # invoiceable_date_field = 'start_date'
    invoiceable_partner_field = 'project'

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super(Event, cls).get_request_queryset(ar, **filter)
        pv = ar.param_values
        #
        #
        # @classmethod
        # def calendar_param_filter(cls, qs, pv):
        # qs = super(Event, cls).calendar_param_filter(qs, pv)
        if pv.project__municipality:  # failed when the field isn't mentioned in params_layout
        # if pv.get('project__municipality'):
            places = pv.project__municipality.whole_clan()
            # print("20200425", places)
            qs = qs.filter(project__isnull=False, project__city__in=places)
        return qs

    def get_event_summary(self, ar):
        pv = ar.param_values
        if self.project:
            yield str(self.project) + " "
            if self.project.city:
                yield self.project.city.name + " "
        # if not pv.event_type and self.event_type:
        #     t.append(str(self.event_type))
        if self.room and self.room.ref:
            yield self.room.ref + " "
        if self.summary:
            yield self.summary + " "

    def obj2href(self, ar, txt=None, *args, **kwargs):
        if txt is None:
            txt = str(self)
        if iselement(txt):
            kwargs.setdefault('title', html2rst(txt))
        else:
            kwargs.setdefault('title', txt)
        return super(Event, self).obj2href(ar, txt, *args, **kwargs)

    def get_invoiceable_partner(self):
        ord = self.owner
        if isinstance(ord, rt.models.orders.Order):
            return ord.invoice_recipient or ord.project

    def get_invoiceable_product(self, max_date=None):
        par = self.get_invoiceable_partner()
        # par = self.project
        # if self.project_id is None:
        if par is None:
            return None
        return rt.models.products.Product.get_ruled_price(par, self.event_type)

    def get_invoiceable_qty(self):
        qty = self.get_duration()
        if qty is not None:
            return Duration(qty)
        if self.event_type_id:
            return self.event_type.default_duration or self.default_invoiceable_qty
        return self.default_invoiceable_qty

    # def get_event_summary(self, ar):
    #     # Overrides lino_xl.lib.cal.Event.get_event_summary
    #     if self.owner is None:
    #         return self.summary
    #     else:
    #         return str(self.owner)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        # pre-select all Event objects that potentially will generate
        # an invoice.

        qs = cls.objects.all()
        qs = qs.filter(state=EntryStates.took_place)
        if plan.area_id:
            qs = qs.filter(room__invoicing_area=plan.area)

        if plan.order is not None:
            qs = qs.filter(**gfk2lookup(cls.owner, plan.order))

        # dd.logger.info("20181113 c %s", qs)

        if partner is None:
            partner = plan.partner

        if partner is None:
            # only courses with a partner (because only these get invoiced
            # per course).
            qs = qs.filter(project__isnull=False)
        else:
            q1 = models.Q(
                project__salesrule__invoice_recipient__isnull=True,
                project=partner)
            q2 = models.Q(
                project__salesrule__invoice_recipient=partner)
            qs = qs.filter(models.Q(q1 | q2))

        # dd.logger.info("20190328 %s (%d rows)", qs.query, qs.count())
        return qs.order_by('id')

    # def __str__(self):
    #     if self.owner is None:
    #         if six.PY2:
    #             return super(Event, self).__unicode__()
    #         else:
    #             return super(Event, self).__str__()
    #         # a simple super() fails because of
    #     owner = self.owner._meta.verbose_name + " #" + str(self.owner.pk)
    #     return "%s %s" % (owner, self.summary)

    # def suggest_guests(self):
    #     # print "20130722 suggest_guests"
    #     for g in super(Event, self).suggest_guests():
    #         print("20190328 suggesting super {}".format(g))
    #         yield g
    #     order = self.owner
    #     if not isinstance(order, rt.models.orders.Order):
    #         # e.g. None or RecorrentEvent
    #         return
    #     Guest = settings.SITE.models.cal.Guest
    #     for obj in order.enrolments_by_order.all():
    #         if obj.worker:
    #             print("20190328 suggesting worker {}".format(obj.worker))
    #             yield Guest(event=self,
    #                         partner=obj.worker,
    #                         role=obj.guest_role)

    def get_invoice_items(self, info, invoice, ar):
        # dd.logger.info("20181116a %s", self)
        for i in super(Event, self).get_invoice_items(info, invoice, ar):
            # print(i.qty)
            yield i
            for oi in self.owner.items.all():
                kwargs = dict(
                    invoiceable=self,
                    product=oi.product,
                    qty=oi.qty)
                yield invoice.add_voucher_item(**kwargs)


    @classmethod
    def setup_parameters(cls, params):
        super(Event, cls).setup_parameters(params)
        params['presence_guest'].verbose_name = _("Worker")
        params['project__municipality'] = make_remote_field(cls, 'project__municipality')


dd.update_field(Event, 'description', format="plain")
dd.update_field(EventType, 'all_rooms', verbose_name=_("Locks all teams"))

# dd.update_field(Guest, 'state', default='present')
# dd.update_field(Guest, 'state', default=GuestStates.present.as_callable())

class EventDetail(EventDetail):
    main = "general more"
    general = dd.Panel("""
    room event_type summary user
    start end
    owner:30 project workflow_buttons:30
    cal.GuestsByEvent description
    """, _("General"))

    more = dd.Panel("""
    id created:20 modified:20 state
    priority access_class transparent #rset
    # outbox.MailsByController  notes.NotesByOwner
    invoicing.InvoicingsByGenerator
    """, _("More"))


class MyEntries(MyEntries):
    column_names = 'when_text summary room owner workflow_buttons *'


class GuestsByEvent(GuestsByEvent):
    column_names = 'partner role workflow_buttons remark *'


class EntriesByProject(EntriesByProject):
    column_names = 'when_text owner summary workflow_buttons *'

# dd.update_field(Guests, 'event_summary', verbose_name="Description")
# doesn't work as i expected

class GuestsNeedingReplacement(Guests):
    label = _("Deployments needing replacement")
    required_roles = dd.login_required(OfficeUser)
    welcome_message_when_count = 0
    order_by = ['event__start_date', 'event__start_time']
    column_names = ("event__start_date event__start_time partner "
                    "event_summary #role workflow_buttons remark *")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(GuestsNeedingReplacement, self).param_defaults(ar, **kw)
        # kw.update(user=ar.get_user())
        # kw.update(event_state=EntryStates.draft)
        kw.update(guest_state=GuestStates.needs)
        kw.update(start_date=dd.today())
        return kw


class FindReplacement(dd.ChangeStateAction):
    """Find another worker to replace this one.
    """
    label = _("Find replacement")
    icon_name = None
    show_in_workflow = True
    # no_params_window = True
    parameters = dict(
        new_partner=dd.ForeignKey(dd.plugins.cal.partner_model),
        comment=models.CharField(_("Comment"), max_length=200, blank=True))

    params_layout = """
    new_partner
    comment
    """

    required_states = "needs"

    @dd.chooser()
    def new_partner_choices(self):
        return rt.models.contacts.Worker.objects.all()

    # def get_action_permission(self, ar, obj, state):
    #     if state == GuestStates.needs:
    #         return super(FindReplacement, self).get_action_permission(ar, obj, state)
    #     return False

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        pv = ar.action_param_values
        obj.partner = pv.new_partner
        obj.state = GuestStates.invited
        obj.remark = pv.comment
        obj.full_clean()
        obj.save()
        ar.success(refresh=True)


dd.inject_action('cal.Guest', find_replacement=FindReplacement(GuestStates.invited))



PlannerColumns.clear()
add = PlannerColumns.add_item
add('10', _('External'), 'external')
add('20', _('Internal'), 'internal')
add('30', _('Craftsmen'), 'craftsmen')
add('40', _('Care staff'), 'care_staff')
add('50', _('Garden'), 'garden')

AllEntries.column_names = 'start_date project summary event_type id project__city project__municipality *'
AllEntries.params_layout = """
start_date end_date observed_event state project project__municipality event_type room
"""
# Events.params_layout = 'event_type room project__municipality project presence_guest'
# Events.params_layout = 'event_type room project presence_guest'
