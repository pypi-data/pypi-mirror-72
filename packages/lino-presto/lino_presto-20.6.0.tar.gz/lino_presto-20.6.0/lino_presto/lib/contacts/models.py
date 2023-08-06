# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import datetime
from django.db.models import Q
from django.conf import settings
from etgen.html import E

from lino.api import dd, rt, _
from lino.utils.quantities import ZERO_DURATION
from lino.utils import SumCollector
# from lino.utils import ONE_WEEK
# from lino.core.utils import comma

from lino_xl.lib.contacts.models import *
from lino_xl.lib.contacts.roles import ContactsUser
# from lino_xl.lib.courses.mixins import Enrollable
from lino_xl.lib.beid.mixins import SSIN
# from lino_xl.lib.calview.ui import WeeklyView
# from lino_xl.lib.calview.ui import WeeklySlave
from lino_xl.lib.calview.mixins import Plannable
from lino.modlib.printing.actions import DirectPrintAction
from lino.mixins.periods import Weekly

# from lino_xl.lib.calview.models import ParameterClone
from lino_xl.lib.calview.models import EventsParameters
from lino_xl.lib.calview.models import WeeklySlaveBase, DailySlaveBase
from lino_xl.lib.calview.models import Planners, CalendarView, InsertEvent


class PrintRoster(DirectPrintAction):
    help_text = _("Print a roster of calendar events")
    # combo_group = "creacert"
    label = _("Roster")
    tplname = "roster"
    build_method = "weasy2pdf"
    icon_name = None
    show_in_bbar = False
    parameters = Weekly(
        show_remarks=models.BooleanField(
            _("Show remarks"), default=False),
        overview=models.BooleanField(
            _("Overview"), default=True))
    params_layout = """
    start_date
    end_date
    overview
    show_remarks
    """
    # keep_user_values = True




class Partner(Partner, mixins.CreatedModified):

    class Meta(Partner.Meta):
        app_label = 'contacts'
        # verbose_name = _("Partner")
        # verbose_name_plural = _("Partners")
        abstract = dd.is_abstract_model(__name__, 'Partner')

    # isikukood = models.CharField(
    #     _("isikukood"), max_length=20, blank=True)
    #
    hidden_columns = 'created modified'

    faculty = None
    """Required by :mod:`lino_xl.lib.working`.
    """

    # def get_overview_elems(self, ar):
    #     # In the base classes, Partner must come first because
    #     # otherwise Django won't inherit `meta.verbose_name`. OTOH we
    #     # want to get the `get_overview_elems` from AddressOwner, not
    #     # from Partner (i.e. AddressLocation).
    #     elems = super(Partner, self).get_overview_elems(ar)
    #     elems += AddressOwner.get_overview_elems(self, ar)
    #     return elems


class PartnerDetail(PartnerDetail):

    main = "general #contact invoicing ledger #misc"

    general = dd.Panel("""
    overview:20 general2:20
    remarks:40 sepa.AccountsByPartner
    # notes.NotesByPartner orders.OrdersByPartner
    """, label=_("General"))

    general2 = """
    id
    language
    created
    modified
    """

    # contact = dd.Panel("""
    # sepa.AccountsByPartner
    # """, label=_("Contact"))
    #
    ledger = dd.Panel("""
    sales.InvoicesByPartner
    vat.VouchersByPartner ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)

    invoicing = dd.Panel("""
    invoicing_left:30 invoicing2 #orders.OrdersByProject:50
    sales.InvoicesByPartner
    """, label=_("Invoicing"))

    invoicing_left = """
    pf_income
    salesrule__invoice_recipient
    payment_term salesrule__paper_type
    """

    invoicing2 = """
    vat_regime
    vat_id
    purchase_account
    """


    # purchases = dd.Panel("""
    # purchase_account vat_regime vat_id
    # ana.InvoicesByPartner
    # """, label=_("Purchases"))

    # misc = dd.Panel("""
    # created modified
    # """, label=_("Miscellaneous"))

Partners.detail_layout = 'contacts.PartnerDetail'

class Person(Partner, Person):
    """
    Represents a physical person.
    """

    class Meta(Person.Meta):
        app_label = 'contacts'
        # verbose_name = _("Person")
        # verbose_name_plural = _("Persons")
        #~ ordering = ['last_name','first_name']
        abstract = dd.is_abstract_model(__name__, 'Person')

    print_roster = PrintRoster()

    @dd.displayfield(_("Print"))
    def print_actions(self, ar):
        if ar is None:
            return ''
        elems = [
            ar.instance_action_button(
                self.print_roster)]
        return E.p(*join_elems(elems, sep=", "))

    @classmethod
    def get_user_queryset(cls, user):
        qs = super(Person, cls).get_user_queryset(user)
        return qs.select_related('country', 'city')

    def get_print_language(self):
        "Used by DirectPrintAction"
        return self.language

    def cal_entries_by_guest(self):
        return rt.models.cal.Event.objects.filter(guest__partner=self)

dd.update_field(Person, 'first_name', blank=False)
# dd.update_field(Person, 'last_name', blank=False)

# class PersonDetail(PersonDetail, PartnerDetail):
class PersonDetail(PartnerDetail):

    main = "general contact humanlinks misc cal_tab"

    general = dd.Panel("""
    overview:20 general2:40 #general3:40
    contacts.RolesByPerson:20
    """, label=_("General"))

    contact = dd.Panel("""
    # lists.MembershipsByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    humanlinks = dd.Panel("""
    humanlinks.LinksByHuman:30
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Human Links"))

    misc = dd.Panel("""
    url
    created modified
    # notes.NotesByPartner
    """, label=_("Miscellaneous"))

    cal_tab = dd.Panel("""
    print_actions
    #cal.GuestsByPartner cal.EntriesByGuest
    """, label=_("Calendar"))

    general2 = """
    title first_name:15 middle_name:15
    last_name
    gender:10 birth_date age:10
    id language
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """


Persons.insert_layout = """
first_name last_name
phone gsm
gender email
"""


class Company(Partner, Company):
    class Meta(Company.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Company')

    # class Meta:
    #     verbose_name = _("Organisation")
    #     verbose_name_plural = _("Organisations")

    # vat_id = models.CharField(_("VAT id"), max_length=200, blank=True)


class CompanyDetail(PartnerDetail):

    main = "general contact invoicing misc"

    ledger = dd.Panel("""
    vat.VouchersByPartner
    ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)

    general = dd.Panel("""
    overview:20 general2:40 general3:40
    contacts.RolesByCompany
    """, label=_("General"))

    general2 = """
    prefix:20 name:40
    type vat_id
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    # lists.MembershipsByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    # tickets = "tickets.SponsorshipsByPartner"

    misc = dd.Panel("""
    id language
    created modified
    # notes.NotesByPartner
    """, label=_("Miscellaneous"))


Companies.insert_layout = """
name
phone gsm
#language:20 email:40
type #id
"""

class Worker(Person, SSIN, Plannable):
    class Meta:
        app_label = 'contacts'
        verbose_name = _("Worker")
        verbose_name_plural = _("Workers")
        abstract = dd.is_abstract_model(__name__, 'Worker')

    plannable_header_row_label = _("All workers")

    @classmethod
    def setup_parameters(cls, fields):
        fields.setdefault(
            'room', dd.ForeignKey('cal.Room',
                blank=True,
                help_text=_("Show only workers of this team.")))
        super(Worker, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(Worker, self).get_request_queryset(ar, **filter)
        pv = ar.param_values
        if pv.room:
            qs = qs.filter(team_memberships__room=pv.room)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Worker, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.room:
            yield str(pv.room)

    def get_weekly_chunks(self, ar, entries, today):
        sums = SumCollector()
        for e in entries:  # .filter(guest__partner=self).distinct():
            yield e.obj2href(ar, ar.actor.get_calview_div(e, ar))
            sums.collect(e.event_type, e.get_duration())
        for k, v in sums.items():
            yield _("{} : {}").format(k, str(v))
            # need to explicitly call str(v) because otherwise __format__() is
            # used, which would render it like a Decimal

    @classmethod
    def get_plannable_entries(cls, obj, qs, ar):

        # The header row in a workers calendar view shows entries that
        # are for everybody, e.g. holidays.  This is when
        # cal.EventType.locks_user is True.
        # print("20200303 get_plannable_entries", cls, obj, ar)
        # Event = rt.models.cal.Event
        if obj is None:
            return qs.none()
        User = rt.models.users.User
        # qs = Event.objects.all()
        if obj is cls.HEADER_ROW:
            qs = qs.filter(event_type__locks_user=False)
        else:
            # entries where the worker is either a guest or the author
            # qs = qs.filter(event_type__locks_user=True)
            try:
                u = User.objects.get(partner=obj)
                # print(u)
                qs = qs.filter(Q(user=u) | Q(guest__partner=obj)).distinct()
            except Exception:
                qs = qs.filter(guest__partner=obj).distinct()
        return qs
        # return Event.calendar_param_filter(qs, ar.param_values)


class WorkerDetail(PersonDetail):

    main = "general contact"

    general = dd.Panel("""
    overview:20 cal_panel:40
    contacts.MembershipsByPartner orders.EnrolmentsByWorker
    """, label=_("General"))

    cal_panel = """
    national_id  print_actions
    cal.EntriesByGuest
    """


class Workers(Persons):
    model = 'contacts.Worker'
    # detail_layout = WorkerDetail()
    detail_layout = 'contacts.WorkerDetail'
    params_layout = 'room gender observed_event start_date end_date'


class Membership(dd.Model):

    class Meta:
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Membership')
        verbose_name = _("Team membership")
        verbose_name_plural = _("Team memberships")
        unique_together = ['room', 'partner']

    quick_search_fields = "partner__name remark"
    show_in_site_search = False

    room = dd.ForeignKey('cal.Room', related_name="workers")
    partner = dd.ForeignKey('contacts.Worker', related_name="team_memberships")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def __str__(self):
        return _("{} is member of {}").format(self.partner, self.room)

    @dd.chooser()
    def room_choices(self, partner):
        existing = rt.models.contacts.Membership.objects.filter(partner=partner).values('room')
        return rt.models.cal.Room.objects.exclude(id__in=existing)

    @dd.chooser()
    def partner_choices(self, room):
        existing = rt.models.contacts.Membership.objects.filter(room=room).values('partner')
        return rt.models.contacts.Worker.objects.exclude(id__in=existing)


class Memberships(dd.Table):
    required_roles = dd.login_required(ContactsUser)
    model = 'contacts.Membership'
    detail_layout = dd.DetailLayout("""
    room
    partner
    remark
    """, window_size=(60, 'auto'))


class MembershipsByRoom(Memberships):
    label = _("Members")
    master_key = 'room'
    # order_by = ['seqno']
    order_by = ['partner__name']
    if dd.is_installed("phones"):
        column_names = "partner remark partner__address_column partner__contact_details *"
    else:
        column_names = "partner remark partner__address_column partner__email partner__gsm *"

    display_mode = "summary"
    # summary_sep = comma
    insert_layout = """
    partner
    remark
    """

    @classmethod
    def summary_row(cls, ar, obj, **kwargs):
        if ar is None:
            yield str(obj.partner)
        else:
            yield ar.obj2html(obj, str(obj.partner))


class MembershipsByPartner(Memberships):
    label = _("Teams")
    master_key = 'partner'
    column_names = "room remark *"
    order_by = ['room__name']
    display_mode = "summary"
    # summary_sep = comma
    insert_layout = """
    room
    remark
    """

    @classmethod
    def summary_row(cls, ar, obj, **kwargs):
        if ar is None:
            yield str(obj.room)
        else:
            yield ar.obj2html(obj, str(obj.room))



class AllMemberships(Memberships):
    required_roles = dd.login_required(ContactsStaff)



# class WorkersParameters(ParameterClone):
class WorkersParameters(EventsParameters):

    abstract = True
    # clone_from = "contacts.Workers"

    @classmethod
    def get_dayslave_rows(cls, ar):
        return rt.models.contacts.Worker.objects.all()

    @classmethod
    def unused_get_calview_chunks(cls, obj, ar):
        pv = ar.param_values
        # if pv.user:
        # if pv.assigned_to:
        # if settings.SITE.project_model is not None and pv.project:
        # if pv.event_type:
        if obj.start_time:
            yield str(obj.start_time)[:5] + " "
        # elif not pv.start_date:
            # t.append(str(self.start_date))
        # if not pv.user and self.user:
        #     t.append(str(self.user))
        if obj.project:
            yield str(obj.project) + " "
            if obj.project.city:
                yield obj.project.city.name + " "
        # if not pv.event_type and self.event_type:
        #     t.append(str(self.event_type))
        if obj.room and obj.room.ref:
            yield obj.room.ref + " "
        if obj.summary:
            yield obj.summary + " "

    def get_header_chunks(obj, ar, entries, today):

        # unlike the library version, this does not have an insert button and
        # does not show only whole-day events.

        # entries = entries.filter(start_time__isnull=True)
        txt = str(today.day)
        if today == dd.today():
            txt = E.b(txt)

        yield E.p(txt, align="center")
        for e in entries:
            yield e.obj2href(ar, ar.actor.get_calview_div(e, ar))

    @dd.displayfield(_("Worker"))
    def name_column(cls, obj, ar):
        # x1 = str([o.obj2href(ar) for o in ar.selected_rows])
        d = ar.master_instance.date
        d -= datetime.timedelta(days=d.weekday())  # start at first day of week
        ba = obj.print_roster
        if ba is None:
            return E.p(obj.obj2href(ar))

        pv = dict(start_date=d, end_date=d + datetime.timedelta(days=6))
        # print("20200417", pv)
        # lbl = "🖨" # unicode 1f5a8 printer
        lbl = "🖶" # unicode 1f5b6 printer icon
        btn = ar.instance_action_button(ba, lbl,
            request_kwargs=dict(action_param_values=pv))
        return E.p(obj.obj2href(ar), " ", btn)


class WeeklySlave(WorkersParameters, WeeklySlaveBase, Workers):
# 20200430 class WeeklySlave(Workers, WeeklySlaveBase):
    column_names_template = "name_column:20 {vcolumns}"
    hide_top_toolbar = False


class DailySlave(WorkersParameters, DailySlaveBase, Workers):
# 20200430 class DailySlave(Workers, DailySlaveBase):
    column_names_template = "name_column:20 {vcolumns}"
    # display_mode = "html"
    navigation_mode = 'day'

class WeeklyView(WorkersParameters, CalendarView):
    label = _("Weekly view")
    detail_layout = 'contacts.WeekDetail'
    navigation_mode = "week"
    # params_layout = ""

class DailyView(WorkersParameters, CalendarView):
    label = _("Daily view")
    detail_layout = 'contacts.DayDetail'
    navigation_mode = "day"
    insert_event = InsertEvent()

class WeekDetail(dd.DetailLayout):
    main = "body"
    body = "navigation_panel:15 contacts.WeeklySlave:85"

class DayDetail(dd.DetailLayout):
    main = "body"
    body = "navigation_panel:15 contacts.DailySlave:85"



add = Planners.add_item
add("contacts", _("Workers planner"), "contacts.DailyView", "contacts.WeeklyView", "")
