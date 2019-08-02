from django.db.models import Q
from django.urls import reverse,reverse_lazy
from django.utils import timezone

from communication.forms import MessageForm
from communication.models import Messages
from django.views.generic import ListView, DetailView, RedirectView, FormView

from django.contrib.auth import get_user_model
User = get_user_model()

class MessagesListView(ListView):
    model = Messages
    context_object_name = 'message_list'
    template_name = "communication/messages_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        qs =  Messages.objects.filter(receiver=self.request.user).values_list("sender",flat=True).distinct().annotate()
        o = User.objects.filter(pk__in=qs)  
        context = {'senders': o}
        return context
         
class MessagesDetailView(ListView):
    model = Messages
    template_name = "communication/messages_detail.html"
    
    def get_queryset(self):
        super().get_queryset().filter(
            Q(sender_id=self.kwargs["user_id"], receiver=self.request.user) & Q(seen__isnull=True)
        ).update(seen=timezone.now())
        query =super().get_queryset().filter(
            Q(sender_id=self.kwargs["user_id"], receiver=self.request.user) |
            Q(receiver_id=self.kwargs["user_id"], sender=self.request.user)
        ).order_by("created")
        total = query.count()
        limit = 50
        offset = total - limit if total - limit > 0 else 0
        return query[offset:]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["other_user"] = User.objects.get(id=self.kwargs["user_id"])
        context["form"] = MessageForm()
        return context


class MessagesSendView(FormView):
    form_class = MessageForm
    template_name="communication/send_message.html"
    
    def get_success_url(self):
        return reverse_lazy("communication:messages_detail", kwargs={"user_id": self.kwargs["user_id"]})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.kwargs["user_id"]
        return context
    
    def form_valid(self, form):
        Messages.objects.create(
            sender=self.request.user,
            receiver_id=self.kwargs["user_id"],
            message=form.cleaned_data["message"],
            file=form.cleaned_data["file"]
        )
        return super().form_valid(form)
