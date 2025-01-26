# Log Analyzer with Kafka, Python, AI, and MongoDB

This project is a **Log Analyzer** that streams logs, uses AI to analyze them, and stores insights in a MongoDB database. Logs are produced and consumed using **Kafka**, and **OpenAI's GPT-based AI models** are leveraged for real-time log analysis.

---

## **Features**

1. **Log Generation**:
   - A Python-based log generator simulates logs with details like:
     - IP addresses.
     - Log levels (INFO, WARNING, ERROR, DEBUG).
     - Services (e.g., `auth-service`, `payment-service`, `user-service`).
   - Logs are sent to a Kafka topic (`app-logs`) for real-time streaming.

2. **Log Consumption**:
   - A Kafka consumer fetches logs in real-time and passes them for AI analysis.

3. **AI-Powered Analysis**:
   - OpenAI's GPT models are used to:
     - Classify logs (e.g., INFO, WARNING, ERROR).
     - Identify anomalies or critical issues.
     - Suggest potential fixes for detected issues.

4. **MongoDB Integration**:
   - Logs and their AI-analyzed insights are stored in a MongoDB database (`log_monitoring`) for historical analysis and debugging.

---

## **Technologies Used**
- **Python**: Core programming language for log generation and processing.
- **Kafka**: Message queue for log streaming.
- **OpenAI API**: AI-powered log analysis.
- **MongoDB**: Database for storing logs and insights.
- **dotenv**: Manage environment variables securely.

---

## **How It Works**

### **1. Log Producer**
- The `producer.py` script generates simulated logs and streams them to a Kafka topic (`app-logs`).
- Each log contains:
  - A timestamp.
  - IP address.
  - HTTP resource accessed.
  - Log level and service name.
  - User-agent and referer details.

### **2. Log Consumer with AI Analysis**
- The `consumer.py` script consumes logs from Kafka and sends them to the OpenAI API for analysis.
- The analysis includes:
  - Classification of logs.
  - Detection of anomalies.
  - Recommendations for resolving issues.
- Processed logs and AI insights are stored in MongoDB.

### **3. MongoDB Storage**
- Each log entry is saved in a `logs` collection in MongoDB with the following structure:
  ```json
  {
      "log_message": "Sample log message",
      "analysis": {
          "classification": "ERROR",
          "anomaly_detected": true,
          "suggestion": "Check authentication configuration."
      },
      "timestamp": "2025-01-26T12:34:56"
  }
