# Yet-Another-Kafka
**Collaborators:** Atul Krishnan, Gowri Nandana PK, Atharv Anant Athavale, Atharva Anil Chanda

# INTRODUCTION #
Language used: Python3 

In this project, we have implemented the kafka interface along with the zookeeper,broker,producer and consumers respectively using socket programming. Infinite number of producers and consumers can connect with the broker to publish and subscribe to a topic. Multiple brokers will be running simultaneously for fault tolerence. The leader of the "brokers" will be elected on a "First Come First Server" algorithm if a fault occurs. The broker has it's own file system where it maintains a record of all topics. These topics have been partitioned to ensure efficient memory management. The broker also maintains a log of producter-consumer transactions.
The zookeeper monitors the health of the broker by checking it's heartbeat at a 10s time interval. 

# GETTING STARTED #
LET'S GO

1. To start our implementation of kafka, first run 'zookeeper.py' on the terminal in the same directory as :
```python3 zookeeper.py```
2. Now, start the broker, which runs 'broker.py' in the same directory as the zookeeper on the terminal:
```python3 broker.py```
3. Now open ```2``` new terminals and do the above commands in each of the terminals. This is to ensure backups are available for the zookeeper to assign, in case of failure. 
4. Now open "another" terminal in the same directory. To run the producer file on this terminal, use the following command: 
```python3 producer.py```
5. In the "PRODUCER" terminal, you can enter a topic and then enter a message which you can publish to the topic. You can open as many terminals as you want and produce to infinite number of topics :)
6. Now open "another" terminal in the same directory. To run the consumer file on this terminal, use the following command: 
```python3 consumer.py```
7. In the "CONSUMER" terminal, you can enter a topic which you wish to subscribe to. There are 2 options provided: Using the flag ```--beginning``` you can receive all the messages since the origin of the topic. Or write ```no``` to receive all messages since the time of subscription to the topic. 
8. You can open "as many terminals as you want" and run the above command to have infinite number of consumers ;)
