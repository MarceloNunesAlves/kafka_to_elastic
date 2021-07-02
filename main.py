from confluent_kafka import Consumer, KafkaError, KafkaException
from json import loads
import data_elastic
import traceback
import logging
import os
import sys
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)
logger.addHandler(console_handler)

# Ambos os valores serão separado por virgula
topic = os.environ.get('KAFKA_TOPIC', 'topic-test')
group_id = os.environ.get('KAFKA_GROUP_ID', 'group-test')
offset_reset = os.environ.get('KAFKA_OFFSET_RESET', 'earliest')
index = os.environ.get('INDEX_ELK', 'test-index')
bulk_size = os.environ.get('BULK_SIZE', 10)

conf = {'bootstrap.servers': 'localhost',
        'group.id': group_id,
        'auto.offset.reset': offset_reset,
        'max.poll.interval.ms': 600000}

consumer = Consumer(conf)
running = True

def leitura():
    try:
        db = data_elastic.ManagerElastic()
        envios = ''
        count = 0

        consumer.subscribe([topic])

        while running:
            message = consumer.poll(timeout=-1)
            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.error('%% %s [%d] fim do offset %d\n' %
                                 (message.topic(), message.partition(), message.offset()))
                    continue
                elif message.error():
                    raise KafkaException(message.error())
            else:
                logger.debug("Recebimento da mensagem")
                try:
                    message = loads(message.value().decode('utf-8'))
                except Exception as e:
                    logger.error('Mensagem invalida: {}'.format(message))
                    continue

                try:
                    envios += '{ "index" : { "_index" : "' + index + '" } }\n'
                    envios += json.dumps(message) + '\n'
                    count += 1

                    if count > bulk_size:
                        logger.info("Envio para o Elasticsearch...")
                        db.sendBulkElastic(envios)
                        envios = ''
                        count = 0

                except Exception as e:
                    stack_trace_string = traceback.format_exc()
                    logger.error('Erro na execução. motivo {}\n{}'.format(str(e), stack_trace_string))

                logger.debug('Processo concluido!')
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
        db.sendBulkElastic(envios)

if __name__ == '__main__':
    leitura()