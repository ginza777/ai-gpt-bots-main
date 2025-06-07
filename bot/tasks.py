from django.conf import settings
from core import celery_app as app
from .models import Message
from celery.exceptions import Retry


@app.task(bind=True, max_retries=None, default_retry_delay=0.5)
def check_message_result_with_message_id(self, message_id):
    try:
        message = Message.objects.get(id=message_id)
        if message.is_finished:
            return message

        open_ai_client = settings.OPENAI_CLIENT
        run = open_ai_client.beta.threads.runs.retrieve(thread_id=message.thread_id, run_id=message.run_id)
        bot = settings.AI_BOT

        if run.status != 'completed':
            message.run_id = run.id
            message.is_on_process = False
            message.save()
            # Javob kelmagan, 1 sekunddan keyin qayta urinib ko'rish
            raise self.retry()  # retry delay=1 sekunddan keyin
        elif run.status == "completed":
            response = \
            open_ai_client.beta.threads.messages.list(thread_id=message.thread_id, order="desc").data[0].content[
                0].text.value
            bot.editMessageText(
                message_id=message.telegram_message_id,
                chat_id=message.telegram_user.telegram_id,
                text=response,
            )
            message.is_finished = True
            message.response_message = response
            message.save(update_fields=["is_finished", "response_message"])
            return run.status
    except Retry:
        raise
    except Exception as exc:
        # Xatolik yuz bersa 5 sekunddan keyin qayta urinadi
        raise self.retry(exc=exc, countdown=1)


@app.task
def check_all_messages():
    messages_ids = Message.objects.filter(is_finished=False).values_list("id", flat=True)
    for message_id in messages_ids:
        check_message_result_with_message_id.apply_async(args=[message_id])
    return len(messages_ids)