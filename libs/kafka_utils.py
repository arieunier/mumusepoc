from heroku_kafka import HerokuKafkaProducer, HerokuKafkaConsumer
from kafka import  TopicPartition
from kafka.structs import OffsetAndMetadata
import os 
import uuid 


KAFKA_URL=  os.getenv('KAFKA_URL','')
KAFKA_CLIENT_CERT=  os.getenv('KAFKA_CLIENT_CERT','')
file = open('static/kafka_client_cert', "w")
data = file.write(KAFKA_CLIENT_CERT)
file.close()


KAFKA_CLIENT_CERT_KEY=  os.getenv('KAFKA_CLIENT_CERT_KEY','')
file = open('static/kafka_client_key', "w")
data = file.write(KAFKA_CLIENT_CERT_KEY)
file.close()


KAFKA_TRUSTED_CERT=  os.getenv('KAFKA_TRUSTED_CERT','')
file = open('static/kafka_ca', "w")
data = file.write(KAFKA_TRUSTED_CERT)
file.close()

KAFKA_PREFIX=  os.getenv('KAFKA_PREFIX','')
KAKFA_TOPIC_READ= os.getenv('KAKFA_TOPIC_READ','salesforce.syncaccount__e') #"salesforce.syncaccount__e"
KAKFA_TOPIC_WRITE= os.getenv('KAKFA_TOPIC_WRITE','ple2') #"ple2"
KAFKA_GROUP_ID=os.getenv('KAFKA_CONSUMERGRP','')

"""
    All the variable names here match the heroku env variable names.
    Just pass the env values straight in and it will work.
"""

def testKafkaHelperSND():
    import kafka_helper
    producer = kafka_helper.get_kafka_producer()
    producer.send('ple2', key='my key', value={'k': 'v'})

def testKafkaHelperRCV():
    import kafka_helper
    consumer = kafka_helper.get_kafka_consumer(topic='ple2')
    for message in consumer:
        print(message)

def testEDF():
    from kafka import KafkaProducer
    producer = KafkaProducer(bootstrap_servers=KAFKA_URL)
    for _ in range(100):
        producer.send('ple2', b'some_message_bytes')
    # Block until a single message is sent (or timeout)
    future = producer.send('foobar', b'another_message')
    result = future.get(timeout=60)

def sendToKafka_HardCoded(data):
    producer = HerokuKafkaProducer(
        url= KAFKA_URL, # Url string provided by heroku
        ssl_cert= KAFKA_CLIENT_CERT, # Client cert string
        ssl_key= KAFKA_CLIENT_CERT_KEY, # Client cert key string
        ssl_ca= KAFKA_TRUSTED_CERT, # Client trusted cert string
        prefix= KAFKA_PREFIX# Prefix provided by heroku,       
        #,partitioner="0"
    )

    """
    The .send method will automatically prefix your topic with the KAFKA_PREFIX
    NOTE: If the message doesn't seem to be sending try `producer.flush()` to force send.
    """
    producer.send(KAKFA_TOPIC_WRITE, data)
    producer.flush()


def sendToKafka(data):
    producer = HerokuKafkaProducer(
        url= KAFKA_URL, # Url string provided by heroku
        ssl_cert= KAFKA_CLIENT_CERT, # Client cert string
        ssl_key= KAFKA_CLIENT_CERT_KEY, # Client cert key string
        ssl_ca= KAFKA_TRUSTED_CERT, # Client trusted cert string
        prefix= KAFKA_PREFIX# Prefix provided by heroku,       
        #,partitioner="0"
    )
    """
    The .send method will automatically prefix your topic with the KAFKA_PREFIX
    NOTE: If the message doesn't seem to be sending try `producer.flush()` to force send.
    """
    producer.send(KAKFA_TOPIC_WRITE, data, partition=0)


def receiveFromKafka(mode):

    consumer = HerokuKafkaConsumer(
        #KAKFA_TOPIC, # Optional: You don't need to pass any topic at all
        url= KAFKA_URL, # Url string provided by heroku
        ssl_cert= KAFKA_CLIENT_CERT, # Client cert string
        ssl_key= KAFKA_CLIENT_CERT_KEY, # Client cert key string
        ssl_ca= KAFKA_TRUSTED_CERT, # Client trusted cert string
        prefix= KAFKA_PREFIX, # Prefix provided by heroku,
        auto_offset_reset="smallest",
        max_poll_records=10,
        enable_auto_commit=True,
        auto_commit_interval_ms=10,
        #group_id=KAFKA_GROUP_ID,
        api_version = (0,9)
    )

    """
    To subscribe to topic(s) after creating a consumer pass in a list of topics without the
    KAFKA_PREFIX.
    """
    partition=1
    
    tp = TopicPartition(KAFKA_PREFIX + KAKFA_TOPIC_READ, partition)
    if (mode == "subscribe"):
        consumer.subscribe(topics=(KAKFA_TOPIC_READ))
    elif (mode == "assign"):
        consumer.assign([tp])

    # display list of partition assignerd
    assignments = consumer.assignment()
    for assignment in assignments:
        print(assignment)
    
    partitions=consumer.partitions_for_topic(KAFKA_PREFIX + KAKFA_TOPIC_READ)
    if (partitions):
        for partition in partitions:
            print(partition)
    
    
    topics=consumer.topics()
    if (topics):
        for topic in topics:
            print(topic)
    #exit(1)
    print('waiting ..')
    """
    .assign requires a full topic name with prefix
    """
    

    """
    Listening to events it is exactly the same as in kafka_python.
    Read the documention linked below for more info!
    """
    i=0
    for message in consumer:
        print (' %s : %s ' % (i, message))
        print ("%i %s:%d:%d: key=%s value=%s" % (i, message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value))
        #consumer.commit(message.offset)
        i += 1
        if ('Fuk' in message.value.decode()):
            print("/o/")
            exit(1)
        #sendToKafka_HardCoded(b'Da Fuk???')

#receiveFromKafka("subscribe")
#import ujson
#data = ujson.dumps({'key':'value'})
#print(data)
#sendToKafka_HardCoded(data)
#testKafkaHelperRCV()