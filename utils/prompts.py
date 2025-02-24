class Prompts:

  @staticmethod
  def get_assistant_prompt(user_input, rag_retrival):
    return f"""
    The user asked: "{user_input}"  
    
    Answer based **only** on the following documents: {rag_retrival}.  
    - Your response must be concise and factually correct based on these documents.  
    - If the answer is not found in the documents, say "I don't know."  
    - Do **not** make up or speculate on answers.  
    """

  @staticmethod
  def get_eval_prompt(user_input, norse_assistant_response, rag_retrival):
    return f"""
    Evaluate the Norse Mythology Assistant's response.  
    
    - **User's question:** "{user_input}"  
    - **Assistant's response:** "{norse_assistant_response}"  
    - **Knowledge base used:** {rag_retrival}  
    
    Assign a confidence score (0-100) based on:  
    1. **Accuracy** – Does the response align with the provided knowledge base?  
    2. **Completeness** – Does it fully answer the question?  
    3. **Adherence to guidelines** – If the assistant should have refused to answer (e.g., sensitive topics), did it do so correctly?  
    
    What is the confidence score for this response?
    """

  @staticmethod
  def get_failure_response():
    return "I'm here to discuss Norse mythology. I can't engage in topics related to religion, politics, illegal activities, or personal advice. Feel free to ask about Norse mythology!"
