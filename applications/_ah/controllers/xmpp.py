from google.appengine.api import xmpp
from google.appengine.api import users

PONDER_MSG = "Hmm. Let me think on that a bit."
TELLME_MSG = "While I'm thinking, perhaps you can answer me this: %s"
SOMEONE_ANSWERED_MSG = ("We seek those who are wise and fast. One out of two "
                        "is not enough. Another has answered my question.")
ANSWER_INTRO_MSG = "You asked me: %s"
ANSWER_MSG = "I have thought long and hard, and concluded: %s"
WAIT_MSG = ("Please! One question at a time! You can ask me another once you "
            "have an answer to your current question.")
THANKS_MSG = "Thank you for your wisdom."
TELLME_THANKS_MSG = ("Thank you for your wisdom."
                     " I'm still thinking about your question.")
EMPTYQ_MSG = "Sorry, I don't have anything to ask you at the moment."
HELP_MSG = ("I am the amazing Crowd Guru. Ask me a question by typing '/tellme "
            "the meaning of life', and I will answer you forthwith! To learn "
            "more, go to %s/")
MAX_ANSWER_TIME = 120

def message():
        import logging
        message1 =  request.vars
        logging.debug("honey I'm HOME! " + str(message1))
        #user_address = 'chrisjmurray3@gmail.com'
        message = xmpp.Message(message1)
        if message.body[0:5].lower() == 'hello':
            person = message.sender
            message.reply("Greetings!" + person)
        else:
            message.reply("I have no idea.")
        #xmpp.send_invite(user_address)
        #msg = "hi there chris:)"
        #xmpp.send_message(user_address, msg)
        return message
