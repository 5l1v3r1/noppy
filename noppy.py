import configparser
import logging
import threading
import random
import time
from Legobot.Connectors.IRC import IRC
from Legobot.Lego import Lego
from Legobot.Legos.Help import Help

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

# Initialize lock and baseplate
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()
# Add children

def checkGreetings(message, greetings):
    for greeting in greetings:
        for word in message.split(" "):
            if greeting == word or greeting + "." == word or greeting + "?" == word or greeting + "!" == word:
                return True

def randomGreeting(greetings):
    return str(greetings[random.randint(0, len(greetings) -1)])

def replySleep(message):
    time.sleep(len(message) * 0.15)


greetings = ["hi", "hello", "sup", "whats up", "wassup", "zapp", "gucci", "yo", "pong"]
generic_answers = ["I dont want to talk about it", "I prefer to keep those things quiet",
"ask py, he knows me really well ;)", "Depends who\'s asking ;)",
"..."]

what_answers = ["69", "Your mum", "Your mum\'s mum", "py\'s mum", "a gram of weed", "its a tiny little reptile in your cup"]
who_answers = ["The pope", "Linus Torvalds", "Richard Branson\'s nanny", "pry0cc", "Kevin Mitnick"]
when_answers = ["1969", "the other day", "thursday", "6969", "no idea"]
are_answers = ["Yes", "absolutely", "100%", "not a chance", "um no...", "i cant believe you asked me that", "hmm maybe", "not sure really, could be anything", 
"NEVA", "lol, you\'re having a laugh mate", "get off those moon rocks, thats impossible"]
how_answers = ["You take a small suser, and put it in a jar, job done!", "dont ask me, im not a genius", 
"Google the mendles pee experiment, that might help", "you run around the room shouting 'I LOVE A DIDDY NOPPY', that should become pretty apparent."]




class Greet(Lego):
    def listening_for(self, message):
        if "noppy" in message['text'].lower() and checkGreetings(message["text"].lower() + " ", greetings):
            return True

    def handle(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        text = randomGreeting(greetings)
        replySleep(text)
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
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        for word in message["text"].split(" "):
            if word == "why":
                text = randomGreeting(generic_answers)
                replySleep(text)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            if word == "when":
                text = randomGreeting(when_answers)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            if word == "what":
                text = randomGreeting(what_answers)
                replySleep(text)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            if word == "who":
                text = randomGreeting(who_answers)
                replySleep(text)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            if word == "are" or word == "is":
                text = randomGreeting(are_answers)
                replySleep(text)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            if word == "how":
                text = randomGreeting(how_answers)
                replySleep(text)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            if word.endswith("?"):
                text = randomGreeting(generic_answers)
                replySleep(text)
                self.reply(message, str(message["metadata"]["source_username"]) + ": " + text, opts)
                break
            
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