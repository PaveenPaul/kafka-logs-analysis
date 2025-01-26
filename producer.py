#!/usr/bin/python3
import time
import datetime
import random
from kafka import KafkaProducer

try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        retries=5 
    )
    print("Kafka Producer initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Kafka Producer: {e}")
    exit(1)


ips = [
    "123.221.14.56", "16.180.70.237", "10.182.189.79",
    "218.193.16.244", "198.122.118.164", "114.214.178.92",
    "233.192.62.103", "244.157.45.12", "81.73.150.239", "237.43.24.118"
]
referers = [
    "-", "http://www.casualcyclist.com",
    "http://bestcyclingreviews.com/top_online_shops",
    "http://bleater.com", "http://searchengine.com"
]
resources = [
    "/handle-bars", "/stems", "/wheelsets",
    "/forks", "/seatposts", "/saddles", "/shifters",
    "/Store/cart.jsp?productID="
]
useragents = [
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40)",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X)",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
]
log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
services = ['auth-service', 'payment-service', 'user-service']

start_time = datetime.datetime.now()


try:
    print("Generating logs and sending them to Kafka...")
    while True:
        log_time = datetime.datetime.now()
        ip = random.choice(ips)
        log_level = random.choice(log_levels)
        service = random.choice(services)
        resource = random.choice(resources)
        if "Store" in resource:
            resource += str(random.randint(1000, 1500))
        useragent = random.choice(useragents)
        referer = random.choice(referers)
        response_size = random.randint(2000, 5000)
        

        log_message = (
            f"{ip} - - [{log_time.strftime('%d/%b/%Y:%H:%M:%S %z')}] "
            f"\"GET {resource} HTTP/1.0\" 200 {response_size} "
            f"\"{referer}\" \"{useragent}\" [SERVICE: {service} | LEVEL: {log_level}]"
        )

  
        producer.send('app-logs', value=log_message.encode('utf-8'))
        print(f"Sent to Kafka: {log_message}")

        
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping log generation...")
except Exception as e:
    print(f"Error while sending logs: {e}")
finally:
    producer.close()
    print("Kafka Producer closed.")
