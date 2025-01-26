from dotenv import load_dotenv
from kafka import KafkaConsumer
from openai import OpenAI
import pymongo
from datetime import datetime
from utilities import analyze_log_with_openai, extract_json_from_output
import os
load_dotenv()


def main():
    consumer = KafkaConsumer(
        'app-logs', 
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id='log-consumer-group',
        enable_auto_commit=True
    )
    client = OpenAI(
                api_key=os.getenv("OpenAI_Key"),
            )
    model_name = os.getenv("ModelName")
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["log_monitoring"]
    logs_collection = db["logs"]
    
    for message in consumer:
        log_message = message.value.decode('utf-8')
        print(f"Received: {log_message}")
        analysis = analyze_log_with_openai(client,model_name,log_message)
        print(f"AI Analysis:\n{analysis}")
        try:
            print("extract json")
            analysis = extract_json_from_output(analysis)
        except Exception as e:
            print(f"Error extracting JSON from output: {e}")
            pass
        print(f"AI Analysis:\n{analysis}")

        # Store log and analysis in MongoDB
        log_entry = {
            "log_message": log_message,
            "analysis": analysis,
            "timestamp": datetime.now()
        }
        logs_collection.insert_one(log_entry)
        print(f"Stored log in MongoDB: {log_entry}")
        

if __name__ == "__main__":
    main()
    
    
