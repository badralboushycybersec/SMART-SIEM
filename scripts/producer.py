
#!/usr/bin/python3

import socket
from kafka import KafkaProducer
import json
from config import Wazuh_broadcasting_port
from config import kafka_bootstrap_server





def json_serializer(data):
    return json.dumps(data).encode("utf-8")
    

def recv_from_syslog(host,port):
    HOST = host
    PORT = port
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.bind((HOST,PORT))
        print(f"{HOST} Listening on port {PORT}")
        num_owasp = 1
        num_juice = 1
        while (True):
            data = s.recv(10*1024)
            datastr = data.decode("utf-8")
            print("recieved an alert")
            if"/home/sss/juice-shop_14.0.1/logs" in datastr:
                
                print("num of juice shop events",num_juice)
                num_juice +=1 
                producer.send("wazuh_alerts", datastr)
                
            elif '"id":"002"' in datastr and "/var/log/apache2/access.log" in datastr : 

                print("num of owasp events",num_owasp)
                num_owasp +=1 
                producer.send("wazuh_alerts", datastr)

            if not data:
                break
        




if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=[kafka_bootstrap_server],
                         value_serializer = json_serializer)
    
    if(producer.bootstrap_connected()):
        print("Producer Started")
        recv_from_syslog("0.0.0.0",Wazuh_broadcasting_port)
    else:
        print("producer Can't Connect to Kafka Server !!")
