from kafka import KafkaProducer
from kafka.sasl.oauth import AbstractTokenProvider
import requests
import time
import logging

logging.basicConfig(level=logging.DEBUG)

KEYCLOAK_TOKEN_URL = "http://10.111.165.225:8080/realms/alida/protocol/openid-connect/token"


class KeycloakTokenProvider(AbstractTokenProvider):
    def __init__(self):
        self._token = None
        self._expiry = 0

    def token(self):
        now = int(time.time())

        if self._token is None or now >= self._expiry - 30:
            r = requests.post(KEYCLOAK_TOKEN_URL, data={
                "grant_type": "password",
                "client_id": "kafka",
                "client_secret": "kafka-client",
                "username": "user1",
                "password": "password1"
            })
            r.raise_for_status()
            data = r.json()
            print(data['access_token'])
            self._token = data['access_token']
            self._expiry = now + data.get('expires_in', 3600)
        return self._token



producer = KafkaProducer(
    bootstrap_servers='my-cluster-dual-role-0.my-cluster-kafka-brokers.kafka.svc:9093',
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=KeycloakTokenProvider()
)

message = "Hello from alida user1 to topic a"
producer.send("a_topic", message.encode("utf-8"))

producer.flush()
print("message sent")