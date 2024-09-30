from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from blogs.models import Blog
from mailing.cron import send_mailing
from mailing.form import ClientForm, MailingForm, MailingManagerForm, MessageForm
from mailing.models import Client, Mailing, MailingLog, Message


class OwnerPermissionMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class ManagerPermissionMixin:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)

        if user.has_perm("mailing.set_active_status"):
            return queryset
        return queryset.filter(owner=user)


class FormValidMixin:
    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class ClientListView(ManagerPermissionMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(name="Manager").exists()
        return context


class ClientDetailView(OwnerPermissionMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class ClientUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("mailing:client_detail", args=[self.kwargs.get("pk")])


class ClientDeleteView(OwnerPermissionMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")


class MessageListView(ManagerPermissionMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(name="Manager").exists()
        return context


class MessageDetailView(OwnerPermissionMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(OwnerPermissionMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MailingListView(ManagerPermissionMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(name="Manager").exists()
        # context['mailings'] = get_mailings_from_cache()
        return context


class MailingDetailView(DetailView):
    model = Mailing

    # def post(self, request, *args, **kwargs):
    #     mailing = self.get_object()
    #     send_mailing(mailing)
    #     logs = MailingLog.objects.filter(mailing=mailing).order_by("-last_mailing")
    #
    #     if logs:
    #         messages.success(request, "Рассылка завершена")
    #     else:
    #         messages.error(
    #             request, "Не удалось выполнить рассылку. Проверьте настройки."
    #         )
    #
    #     return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        mailing = self.get_object()
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all()
        context["clients"] = mailing.clients.all()
        logs = MailingLog.objects.filter(mailing=self.object).order_by("-last_mailing")
        context["last_log"] = mailing.logs.first()
        context["user"] = mailing.owner
        context["is_manager"] = self.request.user.groups.filter(name="Manager").exists()
        return context

    def get_success_url(self):
        return reverse("mailing:mailing_detail", args=[self.kwargs.get("pk")])


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_success_url(self):
        return reverse("mailing:mailing_detail", args=[self.object.pk])


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_success_url(self):
        return reverse("mailing:mailing_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm("mailing.set_active_status"):
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(OwnerPermissionMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


class MainPageView(TemplateView):
    def get_template_names(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return ["mailing/main_manager_page.html"]
        return ["mailing/main_page.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_blog"] = Blog.objects.order_by("?")[:3]
        context["mailing_count"] = Mailing.objects.all().count()
        context["active_mailing_count"] = Mailing.objects.filter(
            mailing_status=Mailing.STARTED
        ).count()
        context["clients_count"] = Client.objects.all().count()
        # context['user_email'] = self.request.user.email
        return context

        # @cache_page(60 * 15)
        # def get_queryset(self, *args, **kwargs):
        #     queryset = super().get_queryset(*args, **kwargs)
        #     queryset = queryset.order_by('?')
        #     return queryset[:3]


def get_mailinglog_view(request):
    user = request.user
    if user.has_perm("mailing.set_active_status"):
        mailing_logs = MailingLog.objects.all()
    elif user.is_authenticated:
        mailing_logs = MailingLog.objects.filter(owner=request.user)
        print(mailing_logs)
    else:
        mailing_logs = Mailing.objects.none()
    return render(
        request, "mailing/mailinglog_list.html", {"object_list": mailing_logs}
    )
