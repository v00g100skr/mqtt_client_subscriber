import paho.mqtt.client as mqtt

import logging, json, os

from pymemcache.client import base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

host = os.environ.get('MEMCHACHED_HOST') or 'memcached'
port = os.environ.get('MEMCHACHED_PORT') or 11211
mhost = os.environ.get('MQTT_HOST') or '10.2.0.40'
login = os.environ.get('MQTT_LOGIN') or 'zigstar'
password = os.environ.get('MQTT_PASSWORD') or 'zigstar'

cache = base.Client((host, port))

# This is the Subscriber


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))
    client.subscribe("zigbee2mqtt_lan/geiger_counter")


def on_message(client, userdata, msg):
    data = json.loads(str(msg.payload.decode("utf-8")))
    logging.info("received message: %s" % json.dumps(data))
    try:
        cached_data = {
            'last_seen': data['last_seen'],
            'radiation_dose_per_hour': data['radiation_dose_per_hour'],
            'radioactive_events_per_minute': data['radioactive_events_per_minute']
        }
        cache.set('geiger_counter', json.dumps(data))
        logging.info("caching message: %s" % cached_data)
    except Exception as e:
        logging.error("caching fail: %s" % e)


logging.info('start subscriber %s:%s %s:%s' % (host, port, login, password))
client = mqtt.Client()
client.username_pw_set(login, password)
client.connect(mhost, 1883, 60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()