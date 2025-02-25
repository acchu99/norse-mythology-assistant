import os
import json
from time import sleep
from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS, cross_origin
from utils.ragie import retrieve_chunks
from utils.prompts import Prompts

DEBUG = False
CONFIDENCE_THRESHOLD = 0.70

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")
CORS(app, supports_credentials=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
main_assistant_id = os.getenv("MAIN_ASSISTANT")
evaluator_assistant_id = os.getenv("EVALUATOR_ASSISTANT")


@app.route("/start", methods=["GET"])
def start_conversation():
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    return jsonify({"thread_id": thread.id})


@app.route("/chat", methods=["POST"])
@cross_origin(supports_credentials=True)
def chat():
    data = request.json
    thread_id = data.get("thread_id")
    user_input = data.get("message", "")

    # Error cases
    if not thread_id:
        print("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400
    if user_input == "":
        print("Error: Missing user input")
        return jsonify({"error": "Missing user input"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")

    # RAG retrieval
    rag_retrival = retrieve_chunks(user_input)

    # Send prompt to Norse Mythology Assistant
    user_input_with_instruction = Prompts.get_assistant_prompt(
        user_input, rag_retrival)

    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=user_input_with_instruction)

    run_norse = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=main_assistant_id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                       run_id=run_norse.id)

        print(f"Run status: {run_status.status}")

        if run_status.status == "completed":
            break
        elif run_status.status == 'failed':
            print("Run failed")
            break
        sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    norse_assistant_response = messages.data[0].content[0].text.value

    # Send prompt to Evaluator Assistant
    print("Evaluating response...")

    eval_prompt = Prompts.get_eval_prompt(user_input, norse_assistant_response,
                                          rag_retrival)

    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=eval_prompt)

    run_eval = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=evaluator_assistant_id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                       run_id=run_eval.id)

        print(f"Run status: {run_status.status}")

        if run_status.status == "completed":
            break
        elif run_status.status == 'failed':
            print("Run failed")
            break
        sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    eval_assistant_response = json.loads(
        messages.data[0].content[0].text.value)
    print(f"Evaluator Assistant Response: {eval_assistant_response}")

    # Prepare response based on confidence score
    score = eval_assistant_response["confidence_score"] / 100

    final_output = {
        "response": None,
        "confidence_score": eval_assistant_response["confidence_score"]
    }

    if score >= CONFIDENCE_THRESHOLD:
        final_output["response"] = norse_assistant_response
    else:
        final_output["response"] = Prompts.get_failure_response()

    print("Final Response: ", final_output)

    return jsonify(final_output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
