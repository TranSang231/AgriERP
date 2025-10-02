import threading
from .implement import Twilio

class SMSThread(threading.Thread):
    def __init__(
        self,
        messages=None,
        fail_callback=None
    ):
        self.executer = Twilio()
        self.messages =  messages
        self.fail_callback =  fail_callback
        threading.Thread.__init__(self)

    def run(self):
        for message in self.messages:
            try:
                self.executer.send_sms(message.get("to"), message.get("content"));
            except Exception as e:
                # TODO: Add a log right here
                print(str(e))
                if self.fail_callback:
                    self.fail_callback(message)


class SMS:
    @staticmethod
    def asyn_send_messages(messages):
        SMSThread(messages=messages).start()

    @staticmethod
    def asyn_send_message(message):
        SMSThread(messages=[message]).start()

