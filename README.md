# kafka_to_elastic

Ferramenta para importar dados do kafka para o Elasticsearch.

## Criação do ambiente

Para este teste simples é importante que o ambiente do python possua todos os pacotes necessários.

Para criar um ambiente python com os pacotes necessários.

Criar o ambiente no Anaconda

```
conda create -n elastic_env
conda activate elastic_env
conda install python
pip install elasticsearch
pip install pandas
pip install confluent_kafka
```

|Nome da variável|Definição|
|--------|---------|
|KAFKA_TOPIC|Nome do topico. ex.: ml-train|
|KAFKA_GROUP_ID|Nome do grupo do kafka. Ex.: ml-group|
|KAFKA_OFFSET_RESET|Kafka offset reset do kafka. ex.:earliest|
|INDEX_ELK|Nome do index|
|URL_ELK|URL do elasticsearch. Ex.: localhost:9200|
|USER_ELK|Usuário do elasticsearch|
|PWD_ELK|Senha do elasticsearch|
|BULK_SIZE|Tamanho do bulk do Elasticsearch.|

### Exemplos do envio para Kafka

Criar topico

```
./kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 10 --config cleanup.policy=delete --topic topic-test
```

```
./kafka-console-producer.sh --topic topic-test --bootstrap-server kafka:9092
```

```
{"campo_1":"Texto de exemplo","date_value":"2021-01-26T15:00:00.000Z","metric": -150}
```

```
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic-test --from-beginning
```

```
./kafka-topics.sh --zookeeper zookeeper:2181 --delete --topic topic-test
```

## Build

```
docker build -f ./Dockerfile -t marcelonunesalves/kafka_to_elasic:latest .
docker push marcelonunesalves/kafka_to_elasic:latest
```