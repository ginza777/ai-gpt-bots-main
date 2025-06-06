from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Language(models.TextChoices):
    Uzbek = "uz", _("Uzbek")
    Russian = "ru", _("Russian")
    English = "en", _("English")


class TelegramUser(BaseModel):
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True, db_index=True)
    full_name = models.CharField(verbose_name="Full Name", max_length=255, null=True, blank=True)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=25, null=True, blank=True)
    first_name = models.CharField(verbose_name="First Name", max_length=255, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=255, null=True, blank=True)
    username = models.CharField(verbose_name="Username", max_length=255, null=True, blank=True)
    language = models.CharField(verbose_name="Language", max_length=255, choices=Language, null=True, blank=True,
                                db_index=True)
    referal_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    number_of_referals = models.PositiveIntegerField(verbose_name="Number of Referals", default=0)
    registred_date = models.DateTimeField(verbose_name="Registred Date", null=True, blank=True)
    balance = models.PositiveIntegerField(verbose_name="Balance", default=300)

    class Meta:
        verbose_name = _("Telegram User")
        verbose_name_plural = _("Telegram Users")

    def get_thread_id(self, bot_username):
        try:
            bot_user = TelegramBotUser.objects.get(telegram_user=self, bot=bot_username)
        except TelegramBotUser.DoesNotExist:
            bot_user = TelegramBotUser.objects.create(telegram_user=self, bot=bot_username)
        if not bot_user.openai_thread_id:
            openai_client = settings.OPENAI_CLIENT
            thread = openai_client.beta.threads.create()
            bot_user.openai_thread_id = thread.id
            bot_user.save(
                update_fields=["openai_thread_id"],
            )
        return bot_user.openai_thread_id

    def __str__(self):
        return self.full_name if self.full_name else f"{self.first_name} {self.last_name}"


class TelegramBotUser(BaseModel):
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name=_("Telegram User"),
    )
    bot = models.CharField(verbose_name="Bot", max_length=255, db_index=True)
    openai_thread_id = models.CharField(verbose_name="OpenAI Thread ID", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Telegram Bot User")
        verbose_name_plural = _("Telegram Bot Users")
