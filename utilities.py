
def analyze_log_with_openai(client,model_name,log_message):
    try:
        system_prompt = """
        You are an AI assistant specialized in log analysis. Your job is to:
        1. Classify the log level (INFO, WARNING, ERROR, DEBUG).
        2. Summarize the log message.
        3. Identify anomalies or critical issues in the log.
        4. Suggest potential fixes or actions if an issue is detected.
        5. Track the Anamoaly and report it.
        {
            "chainofthought":"Think over the log message and provide the best possible solution",
            "message": "Analyze the log message and provide a summary, classification, and potential issues or fixes.",
        }
        make sure to provide a json structure with the above keys and values.
        """
        messages = [{'role':'system','content':system_prompt}]
        messages.append({'role':'user','content':log_message})
        print("messages",messages)
        response = get_chatbot_response(client,model_name,messages)
        return response
    except Exception as e:
        return f"Error analyzing log with OpenAI: {e}"
    
def get_chatbot_response(client,model_name,messages,temperature=0):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000,
    ).choices[0].message.content
    print("response",response)
    return response

def extract_json_from_output(chatbot_output):
    import re
    import json

    json_match = re.search(r'```(?:json|write)\n(.*?)\n```', chatbot_output, re.DOTALL)

    if json_match:
        json_string = json_match.group(1)  
        try:
            json_data = json.loads(json_string)  
            return json_string
        except json.JSONDecodeError as e:
            return {"error": f"Failed to decode JSON: {e}"}
    else:
        return {"error": "No JSON found in the input."}