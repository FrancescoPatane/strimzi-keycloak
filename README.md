quay.io/strimzi/kafka:0.49.1-kafka-4.1.1

kubectl -n kafka run kafka-oauth-consumer -ti --rm --restart=Never \
  --image=quay.io/strimzi/kafka:0.49.1-kafka-4.1.1 -- \
  bin/kafka-console-consumer.sh \
    --bootstrap-server my-cluster-dual-role-0.my-cluster-kafka-brokers.kafka.svc:9093 \
    --topic a_topic \
    --from-beginning \
    --consumer-property security.protocol=SASL_PLAINTEXT \
    --consumer-property sasl.mechanism=OAUTHBEARER \
    --consumer-property ssl.endpoint.identification.algorithm= \
	 --consumer-property group.id=a_test_group \
    --consumer-property sasl.login.callback.handler.class=io.strimzi.kafka.oauth.client.JaasClientOauthLoginCallbackHandler \
    --consumer-property sasl.jaas.config="org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required oauth.client.id=\"team-a-client\" oauth.client.secret=\"team-a-client-secret\" oauth.token.endpoint.uri=\"http://10.111.165.225:8080/realms/kafka-authz/protocol/openid-connect/token\";"




kubectl -n kafka run kafka-oauth-producer -ti --rm --restart=Never  \
--image=quay.io/strimzi/kafka:0.49.1-kafka-4.1.1 \
--   bin/kafka-console-producer.sh   \
--bootstrap-server my-cluster-dual-role-0.my-cluster-kafka-brokers.kafka.svc:9093   \
--topic a_topic \
--producer-property security.protocol=SASL_PLAINTEXT \
--producer-property sasl.mechanism=OAUTHBEARER   \
--producer-property ssl.endpoint.identification.algorithm=  \
--producer-property enable.idempotence=false \
--producer-property sasl.login.callback.handler.class=io.strimzi.kafka.oauth.client.JaasClientOauthLoginCallbackHandler   \
--producer-property sasl.jaas.config="org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required oauth.client.id=\"team-a-client\" oauth.client.secret=\"team-a-client-secret\" oauth.token.endpoint.uri=\"http://10.111.165.225:8080/realms/kafka-authz/protocol/openid-connect/token\";"   


 kubectl port-forward svc/keycloak 8080:8080 -n keycloak

 kubectl -n kafka run kafka-oauth-consumer -ti --rm --restart=Never \
  --image=quay.io/strimzi/kafka:0.49.1-kafka-4.1.1 -- \
  bin/kafka-console-consumer.sh \
    --bootstrap-server my-cluster-dual-role-0.my-cluster-kafka-brokers.kafka.svc:9093 \
    --topic 1_topic \
    --from-beginning \
    --consumer-property security.protocol=SASL_PLAINTEXT \
    --consumer-property sasl.mechanism=OAUTHBEARER \
    --consumer-property ssl.endpoint.identification.algorithm= \
	 --consumer-property group.id=a_test_group \
    --consumer-property sasl.login.callback.handler.class=io.strimzi.kafka.oauth.client.JaasClientOauthLoginCallbackHandler \
    --consumer-property sasl.jaas.config="org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required oauth.client.id=\"kafka\" oauth.client.secret=\"kafka-secret\" oauth.token.endpoint.uri=\"http://10.111.165.225:8080/realms/kafka-authz/protocol/openid-connect/token\";"