import threading

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class MailingThread(threading.Thread):
    def __init__(
        self,
        messages=None,
        fail_callback=None
    ):
        self.messages = messages
        self.fail_callback =  fail_callback
        threading.Thread.__init__(self)

    def run(self):
        for message in self.messages:
            try:
                message.send()
            except Exception as e:
                # TODO: Add a log right here
                print(str(e))
                if self.fail_callback:
                    self.fail_callback(message)


class Mailing:
    @staticmethod
    def asyn_send_messages(messages):
        MailingThread(messages=messages).start()

    @staticmethod
    def asyn_send_message(message):
        MailingThread(messages=[message]).start()

    @classmethod
    def create_html_message(cls, data, attachment=None, headers=None):
        subject = data.get("subject")
        from_email=data.get("from") or settings.DEFAULT_FROM_EMAIL or "Alpha <noreply@pandosima.com>"
        to = data.get("to")

        html_content = render_to_string(
            data.get("template"), data.get("context")
        )
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject, text_content, from_email, to, headers
        )
        msg.attach_alternative(html_content, "text/html")
        if attachment:
            msg.attach(
                attachment.filename,
                attachment.content,
                attachment.mimetype,
            )
        # print('msg: ',msg)
        return msg
    
    @classmethod
    def create_text_message(cls, data, attachment=None, headers=None):
        subject = data.get("subject")
        from_email=data.get("from") or settings.DEFAULT_FROM_EMAIL or "Alpha <noreply@pandosima.com>"
        to = data.get("to")
        if not isinstance(to, list) and not isinstance(to, tuple):
            to = [to]
        reply_to = data.get("reply_to")
        if not isinstance(reply_to, list) and not isinstance(reply_to, tuple):
            reply_to = [reply_to]
        body = data.get("body")
        

        msg = EmailMessage(
            subject = subject,
            body = body, 
            from_email=from_email,
            to = to,
            headers = headers,
            reply_to = reply_to
        )
        if attachment is not None and isinstance (attachment, dict):
            filename = attachment.get("filename")
            content = attachment.get("content")
            minetype = attachment.get("minetype")
            msg.attach(filename,content,minetype)
        return msg

