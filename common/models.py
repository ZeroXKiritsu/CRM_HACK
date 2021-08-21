import arrow
import binascii
import datetime
import os
import time
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from common.templatetags.document_tag import (
    is_image,
    is_audio,
    is_video,
    is_pdf,
    is_text,
    is_sheet,
    is_archive
)
from django.utils import timezone
from django.conf import settings

def get_image_url(filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)

class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    address = models.TextField(blank=True, default="")
    sub_domain = models.CharField(max_length=30)
    user_limit = models.IntegerField(default=5)
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)

class User(AbstractBaseUser, PermissionsMixin):
    file_prepend = "users/profile_pics"
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(("date joined"), auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLES)
    profile_pic = models.FileField(max_length=1000, upload_to=get_image_url, null=True, blank=True)
    has_sales_access = models.BooleanField(default=False)
    has_marketing_access = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def documents(self):
        return self.document_uploaded.all()

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + ' ' + self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    @property
    def on_arrow(self):
        return arrow.get(self.date_joined).humanize()

    class Meta:
        ordering = ['-is_active']

    def __str__(self):
        return self.email

class Address(models.Model):
    address = models.CharField(max_length=255, blank=True, default='')
    street = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=255, blank=True, default='')
    state = models.CharField(max_length=255, blank=True, default='')
    postcode = models.CharField(max_length=64, blank=True, default='')
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)

    def __str__(self):
        return self.city if self.city else ''

    def get_full_address(self):
        address = ""
        if self.address:
            address += self.address
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.get_country_display()
            else:
                address += self.get_country_display()
        return address

class Comment(models.Model):
    case = models.ForeignKey(
        'cases.Case',
        blank=True,
        null=True,
        related_name='cases',
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=255)
    is_commented = models.DateTimeField(auto_now_add=True)
    commented_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey('accounts.Account', blank=True, null=True, on_delete=models.CASCADE)
    lead = models.ForeignKey('leads.Lead', blank=True, null=True, on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunity.Opportunity', blank=True, null=True, on_delete=models.CASCADE)
    contact = models.ForeignKey('contacts.Contact', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey('tasks.Task', blank=True, null=True, on_delete=models.CASCADE)
    invoice = models.ForeignKey('invoices.Invoice', blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', blank=True, null=True, on_delete=models.CASCADE)

    def get_files(self):
        return Files.objects.filter(comment_id=self)

    @property
    def commented_on_arrow(self):
        return arrow.get(self.commented_on).humanize()

class Files(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files", default="")

class Attachments(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    file_name = models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(max_length=1001, upload_to="attachments/%Y/%m/")
    lead = models.ForeignKey("leads.Lead",null=True,blank=True,on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Account', blank=True, null=True, on_delete=models.CASCADE)
    contact = models.ForeignKey('contacts.Contact', blank=True, null=True, on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunity.Opportunity', blank=True, null=True, on_delete=models.CASCADE)
    case = models.ForeignKey('cases.Case', blank=True,null=True,related_name='cases',on_delete=models.CASCADE)
    task = models.ForeignKey('tasks.Task', blank=True, null=True, on_delete=models.CASCADE)
    invoice = models.ForeignKey('invoices.Invoice', blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', blank=True, null=True, on_delete=models.CASCADE)

    def get_file_type(self):
        extensions_list = self.attachment.url.split('.')
        if len(extensions_list) > 1:
            extensions = extensions_list[int(len(extensions_list) - 1)]
            if is_audio(extensions):
                return ("audio", "fa fa-file-audio")
            if is_video(extensions):
                return ("video", "fa fa-file-video")
            if is_image(extensions):
                return ("image", "fa fa-file-image")
            if is_pdf(extensions):
                return ("pdf", "fa fa-file-pdf")
            if is_text(extensions):
                return ("text", "fa fa-file-alt")
            if is_sheet(extensions):
                return ("sheet", "fa fa-file-excel")
            if is_archive(extensions):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def get_file_type_display(self):
        if self.attachment:
            return self.get_file_type()[1]
        return None

    @property
    def on_arrow(self):
        return arrow.get(self.created_on).humanize()

def get_document_path(filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)

class Document(models.Model):
    pass