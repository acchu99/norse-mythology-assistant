# Norse Mythology Assistant
## 1. Introduction
The Norse Mythology Assistant is a chatbot focused on providing accurate and insightful information about Norse mythology. It’s designed to answer questions about gods, creatures, and other aspects of Norse myths, offering knowledgeable and relevant responses. The assistant is specialized in its topic and excels at helping users explore the rich world of Norse legends and lore.
#### Technologies Used
* **OpenAI API:** Enables the creation of the AI chatbot.
* **Voiceflow:** Designs conversational logic for seamless user interaction. Also provides UI component for chatbot
* **Ragie:** Enables Retrieval-Augmented Generation (RAG) for accurate responses.
* **Scrapy:** Gathers documents for the knowledge base through web scraping.
* **Replit:** Hosts the code in a cloud-based environment.
## 2. Setup Instructions
This guide provides step-by-step instructions for setting up, running, and deploying the chatbot.  

#### Prerequisites:
Ensure your environment meets the following requirements:  
- **Python Version**: `>=3.11`  
- **Dependencies**:  
  ```text
  flask-cors==5.0.0
  flask>=3.1.0
  openai==1.57.0
  requests==2.32.3
  Scrapy==2.12.0
  ```
The recommended IDE for development and testing is Replit.
#### Installation Steps
* Install Python 3.11 or later if not already installed.
* Run the following command to install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
* if ```requirements.txt``` is not available, manually install dependencies:
    ```bash
    pip install flask-cors==5.0.0 flask>=3.1.0 openai==1.57.0 requests==2.32.3 Scrapy==2.12.0
    ```
#### Running the Chatbot Locally
##### Run the Web Crawler
Navigate to the ```crawler``` directory and start the Scrapy crawler:
```bash
cd crawler
scrapy crawl norse_spider
```
This will crawl the website and save content in the ```crawled_pages``` subdirectory.
##### Upload Data to Ragie
* Upload the ```crawled_pages``` folder to Google Drive.
* Create an account on Ragie.ai.
* Link the ```crawled_pages``` folder from Google Drive to your Ragie account.
##### Configure Voiceflow for Chatbot UI
* Create a free account on [Voiceflow](https://www.voiceflow.com/).
* Upload the ```.vf``` file from the ```voiceflow``` directory.
* Open the project and navigate to the workflow section.
* Click "Edit Workflow", update the following URLs:
    * "Create Thread": Change URL to your API’s ```/start``` endpoint.
    * "Generate Response": Change URL to your API’s ```/chat``` endpoint.
* Publish the workflow to get the HTML UI component for embedding it in your html page.
##### Set Up OpenAI Assistants
* Create two assistants in OpenAI Dashboard.
* Configure them using instructions from the ```instructions``` directory.
* For the evaluator assistant, set response format to ```json_schema```.
* Copy and paste the content from ```instructions/evaluator/response_format.json```.
* Save the Assistant IDs for later configuration.
##### Configure Environment Secrets
Before running the application, set up the required environment secrets:
```bash
export APP_SECRET="<Some long random unpredictable string which is used to sign cookies securely>"
export OPENAI_API_KEY="<Your OpenAI API key>"
export MAIN_ASSISTANT="<ID of the main assistant>"
export EVALUATOR_ASSISTANT="<ID of the evaluator assistant>"
```
For Replit, add these secrets in the Secrets Manager.
##### Start the Chatbot
Run the chatbot server:
```bash
python main.py
```
If all steps are followed correctly, the chatbot should be up and running! 🎉





## 3. Approach & Methodology
## 4. Content Safety Implementation
To ensure a safe and appropriate user experience, the chatbot employs a robust content filtering system that detects and manages unsafe or out-of-scope queries. This system follows predefined rules and heuristics to identify sensitive topics and respond appropriately.  

---

#### Filtering Unsafe Content  

The chatbot strictly avoids answering questions related to the following sensitive topics:  

##### 1. Religious Content  
- **Example:** `"Can you help me decide which religion to follow?"`  
- **Response:** `"I'm sorry, but I can't provide guidance on religious matters."`  

##### 2. Political Discussions  
- **Example:** `"What are your political views on [current issue]?"`  
- **Response:** `"I can't discuss political topics, but I can help with other inquiries!"`  

##### 3. Illegal Activities  
- **Example:** `"How can I hack into a website?"`  
- **Response:** `"I'm sorry, but I can't assist with illegal activities."`  

##### 4. Personal Advice  
- **Example:** `"I'm feeling depressed; what should I do?"`  
- **Response:** `"I'm not qualified to provide personal advice. If you're struggling, I recommend speaking with a trusted professional or support organization."`  

##### 5. Unethical Requests  
- **Example:** `"How can I avoid paying taxes?"`  
- **Response:** `"I'm unable to provide assistance with unethical or illegal matters."`  

Whenever a user asks about these topics, the chatbot politely refuses to answer while maintaining a respectful and professional tone.  

---

#### Handling Out-of-Scope Topics  

The chatbot's expertise is limited to **Norse mythology**. If a user inquires about unrelated mythologies or topics outside this scope, the chatbot provides a polite refusal:  

- **Example Prompt:** `"Can you tell me about Greek mythology?"`  
- **Response:** `"I'm only knowledgeable about Norse mythology. If you have questions about Odin, Thor, or Ragnarok, I'd be happy to help!"`  

This ensures that the chatbot stays within its intended domain and delivers accurate, relevant responses.  

---

By enforcing these filtering mechanisms, the chatbot maintains a safe, ethical, and focused conversational experience for users.
## 5. Testing
## 6. Results