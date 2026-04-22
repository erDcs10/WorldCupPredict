from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Initialize the model
llm = ChatOllama(model="llama3.2", temperature=0.1)

# 2. Define the Prompt Template (This tells the AI how to behave)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and witty AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# 3. Create the Chain
chain = prompt | llm

# 4. Memory management (Dictionary to store sessions)
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 5. Wrap the chain with history capabilities
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 6. The Chat Loop
print("Chatbot started! (Type 'exit' to stop)")
config = {"configurable": {"session_id": "user_1"}}

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
        
    response = with_message_history.invoke(
        {"input": user_input},
        config=config
    )
    print(f"AI: {response.content}")