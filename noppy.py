import configparser
import logging
import threading
import random
import time

from Legobot.Connectors.IRC import IRC
from Legobot.Lego import Lego
from Legobot.Legos.Help import Help
from database import greetings, are_answers, generic, how_answers, what_answers, when_answers, who_answers, why_answers


def bot_setup():
    global config, logger
    config = configparser.ConfigParser()
    config.read('config.ini')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)


def bot_init():
    global baseplate_proxy
    # Initialize lock and baseplate
    lock = threading.Lock()
    baseplate = Lego.start(None, lock)
    baseplate_proxy = baseplate.proxy()
    # Add children


bot_init()
bot_setup()


def check_greetings(message, greetings_list):
    for greeting in greetings_list:
        for word in message.split(" "):
            if greeting == word or greeting + "." == word or greeting + "?" == word or greeting + "!" == word:
                return True


def get_random_greeting(greetings_list):
    return str(greetings_list[random.randint(0, len(greetings_list) - 1)])


def reply_sleep(message):
    time.sleep(len(message) * 0.3)


def read_sleep(message):
    time.sleep(len(message) * 0.2)


class Greet(Lego):
    def listening_for(self, message):
        if "noppy" in message['text'].lower() and check_greetings(message["text"].lower() + " ", greetings.db):
            return True

    def handle(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        text = get_random_greeting(greetings.db)
        read_sleep(message["text"])
        reply_sleep(text)
        self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)

    def get_name(self):
        return 'helloworld'

    def get_help(self):
        help_text = "Say hello! Usage: !helloworld"
        return help_text


class Question(Lego):
    def listening_for(self, message):
        if "noppy" in message['text'].lower() and message['text'].endswith("?"):
            return True

    def handle(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        for word in message["text"].split(" "):
            if word == "why":
                self.get_fitting_response(message, opts, why_answers.db)
                break
            if word == "when":
                self.get_fitting_response(message, opts, when_answers.db)
                break
            if word == "what":
                self.get_fitting_response(message, opts, what_answers.db)
                break
            if word == "who":
                self.get_fitting_response(message, opts, who_answers.db)
                break
            if word == "are" or word == "is":
                self.get_fitting_response(message, opts, are_answers.db)
                break
            if word == "how":
                self.get_fitting_response(message, opts, how_answers.db)
                break
            if word.endswith("?"):
                self.get_fitting_response(message, opts, generic.db)
                break

    def get_fitting_response(self, message, opts, question_type):
        text = get_random_greeting(question_type)
        read_sleep(message["text"])
        reply_sleep(text)
        self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)

    def get_name(self):
        return 'helloworld2'

    def get_help(self):
        help_text = "Say hello! Usage: !helloworld"
        return help_text


baseplate_proxy.add_child(IRC,
                          channels=[channel.strip() for channel in config.get(
                              "irc1", "channel").split(",")],
                          nickname=config['irc1']['username'],
                          server=config['irc1']['host'],
                          port=int(config['irc1']['port']),
                          use_ssl=config.getboolean('irc1', 'ssl'),
                          username=config['irc1']['username'],
                          password=config['irc1']['password'])
baseplate_proxy.add_child(Greet)
baseplate_proxy.add_child(Question)
