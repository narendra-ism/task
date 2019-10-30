import os 
import time


print('kafka is stoping')
a=['./confluent-4.1.0/bin/kafka-server-stop -daemon ./confluent-4.1.0/etc/kafka/server.properties']
os.system(a[0])
time.sleep(5)
print('kafka is stopped')

print('zookeeper is stoping')
b=['./confluent-4.1.0/bin/zookeeper-server-stop -daemon ./etc/kafka/zookeeper.properties']
os.system(b[0])
time.sleep(5)

h=['pkill -9 -f kafka','pkill -9 -f zookeeper','pkill -9 -f Consumer','pkill -9 -f producer']
for i in range(len(h)):
    os.system(h[i])
    time.sleep(5)

