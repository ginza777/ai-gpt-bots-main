from django.db import models
from base.models import BaseModel



class Message(BaseModel):
    telegram_user = models.ForeignKey("base.TelegramUser", on_delete=models.PROTECT)
    thread_id = models.CharField(max_length=100, verbose_name="Thread ID", null=True, blank=True)
    run_id = models.CharField(max_length=100, verbose_name="Run ID", null=True, blank=True)
    telegram_message_id = models.CharField(max_length=100, verbose_name="Telegram Message ID", null=True)

    input_message = models.TextField(verbose_name="Message", null=True, blank=True)
    input_file = models.FileField(verbose_name="File", null=True, blank=True)

    response_message = models.TextField(verbose_name="Response Message", null=True, blank=True)
    cost = models.PositiveIntegerField(verbose_name="Cost", default=50)
    is_on_process = models.BooleanField(default=False, verbose_name="On Process")
    is_finished = models.BooleanField(default=False, verbose_name="Finished")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


