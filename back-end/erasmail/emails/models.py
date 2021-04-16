from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from .managers import (NewsletterQuerySet, EmailStatsQuerySet, EmailHeadersQuerySet, AttachmentQuerySet, )
from .utils.pollution import emailPollution, getYearlyCarbonForecast

User = get_user_model()

class EmailStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mailbox_size = models.PositiveIntegerField(null=False)
    carbon_eq_at_creation = models.FloatField(null=False, validators=[MinValueValidator(0.0)])
    carbon_eq = models.FloatField(null=False, default=0, validators=[MinValueValidator(0.0)])
    emails_count  =  models.PositiveIntegerField(null=False)
    emails_seen_count = models.PositiveIntegerField(null=False)
    emails_received_count = models.PositiveIntegerField(null=False)
    months_since_creation = models.FloatField(null=False, validators=[MinValueValidator(0.0)])
    saved_co2 = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    # connected_count = models.PositiveIntegerField(default=0, help_text="Number of times the user connected to ErasMail")
    deleted_emails_count = models.PositiveIntegerField(default=0, help_text="Number of deleted emails")
    badges_shared = models.PositiveIntegerField(default=0, help_text="The user has shared his badges on social media")
    stats_shared = models.PositiveIntegerField(default=0, help_text="The user has shared his stats on social media")
    unsubscribed_newsletters_count = models.PositiveIntegerField(default=0, help_text="Number of newsletters that have been unsubscribed using ErasMail") #TODO: on calcule déjà cette valeur faut juste l'insérer.
    newsletters_deleted_emails_count = models.PositiveIntegerField(default=0, help_text="Number of newsletters related emails deleted")
    deleted_emails_olderF_count = models.PositiveIntegerField(default=0, help_text="Number of deleted emails using the older than filter")
    deleted_emails_largerF_count = models.PositiveIntegerField(default=0, help_text="Number of deleted emails using the larger than filter")
    deleted_emails_useless_count = models.PositiveIntegerField(default=0, help_text="Number of deleted useless emails")
    threads_deleted_emails_count = models.PositiveIntegerField(default=0, help_text="Number of threads related emails deleted")
    deleted_attachments_count = models.PositiveIntegerField(default=0, help_text="Number of deleted attachments")





    objects = EmailStatsQuerySet.as_manager()

    def add(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, F(k) + v)


    def update_deleted_email(self, emails):
        self.deleted_emails_count = F('deleted_emails_count') + emails.get('emails_count', 0)
        self.emails_count = F('emails_count') - emails.get('emails_count', 0)
        self.emails_received_count = F('emails_received_count') - emails.get('emails_received_count', 0)
        self.emails_seen_count = F('emails_seen_count') - emails.get('emails_seen_count', 0)
        self.mailbox_size = F('mailbox_size') - emails.get('mailbox_size', 0)
        self.saved_co2 = F('saved_co2') + emails.get('carbon_eq', 0)
        self.carbon_eq = F('carbon_eq') - emails.get('carbon_eq', 0)

    def update_deleted_attachments(self, attachments_stats):
        self.saved_co2 = F('saved_co2') + attachments_stats['generated_carbon_tot']
        self.carbon_eq = F('carbon_eq') - attachments_stats['generated_carbon_tot']
        self.mailbox_size = F('mailbox_size') - attachments_stats['attachment_size_tot']

    def save(self, *args, **kwargs):
        if not self.carbon_eq_at_creation:
            self.carbon_eq_at_creation = self.carbon_eq
        super(EmailStats, self).save(*args, **kwargs)


class Newsletter(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    list_unsubscribe = models.CharField(max_length=5000)
    one_click = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)
    sender_email = models.EmailField()
    objects = NewsletterQuerySet.as_manager()
    
    def get_latest_email(self):
        return self.email_headers.latest('received_at')

    def __str__(self) -> str:
        return f'pk: {self.pk}  sender: {self.sender_email}'



class EmailHeaders(models.Model):
    uid = models.IntegerField()
    seen = models.BooleanField(default=False)
    subject = models.CharField(max_length=5000, blank=True)
    sender_name = models.CharField(max_length=5000, blank=True)
    sender_email = models.EmailField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField(null=True)
    message_id = models.CharField(max_length=5000)
    folder = models.CharField(max_length=5000)
    thread_id = models.IntegerField(null=True)
    generated_carbon = models.FloatField(validators=[MinValueValidator(0.0)])
    carbon_yforecast = models.FloatField(validators=[MinValueValidator(0.0)])
    is_received = models.BooleanField(default=False)

    unsubscribe = models.ForeignKey(Newsletter, related_name='email_headers', on_delete=models.CASCADE, blank=True, null=True) # change newsletters to emailheaders

    objects = EmailHeadersQuerySet.as_manager()

    def update_deleted_attachments(self, attachments_stats):
        self.size = F('size') - attachments_stats['attachment_size_tot']
        self.generated_carbon = F('generated_carbon') - attachments_stats['generated_carbon_tot']

    def __str__(self):
        return f'from: {self.sender_email}\nto: {self.receiver}\nsubject: {self.subject}'


    def save(self, *args, **kwargs):
        self.generated_carbon=emailPollution(self.size, self.received_at)
        self.carbon_yforecast=getYearlyCarbonForecast(self.size, self.received_at)
        super(EmailHeaders, self).save(*args, **kwargs)


class Attachment(models.Model):
    email_header = models.ForeignKey(EmailHeaders, related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    size = models.IntegerField()

    objects = AttachmentQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} {self.size}'

