import json
import configparser

config = configparser.ConfigParser()
cfg = config.read('/usr/local/config.ini')
# a = config['DEFAULT']['topicIds']
# a = config['DEFAULT']['appToken']
a = config.get('DEFAULT', 'topicIds')

print(a)
