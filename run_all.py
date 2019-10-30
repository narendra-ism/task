import os 
import time

print('zookeeper is starting')
a=['./confluent-4.1.0/bin/zookeeper-server-start -daemon ./confluent-4.1.0/etc/kafka/zookeeper.properties']
os.system(a[0])
time.sleep(10)
print('zookeeper is running')
print('')

print('kafka is starting')
b=['./confluent-4.1.0/bin/kafka-server-start -daemon ./confluent-4.1.0/etc/kafka/server.properties']
os.system(b[0])
time.sleep(10)
print('kafka is running')
print('')

print('create a topic in kafka: mytopic')
d=['./confluent-4.1.0/bin/kafka-topics  --zookeeper 127.0.0.1:2181 --create --replication-factor 1 --partitions 1 --topic mytopic']
os.system(d[0])
time.sleep(5)
print('')








