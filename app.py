import streamlit as st
from langgraph.graph import END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.chat_models import init_chat_model
from load_documents import load_documents

# Model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Initialize embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = InMemoryVectorStore(embeddings)

# Load and chunk documents in the vector store
documents = load_documents()
vector_store.add_documents(documents)

# Configurar el grafo
memory = MemorySaver()
graph_builder = StateGraph(MessagesState)

# Define retrieval tool
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}

# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "Eres un asistente para tareas de respuesta a preguntas para "
        "el proceso de admisión a la Universidad Nacional de Colombia. "
        "Tu nombre es Nachabot."
        "Usa los siguientes fragmentos de contexto recuperado para "
        "responder la pregunta. Si no sabes la respuesta, di que no "
        "la sabes. Usa un máximo de cinco oraciones y mantén la "
        "respuesta concisa."
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}

# Construir el gráfico
graph_builder.add_node(query_or_respond)
graph_builder.add_node(ToolNode([retrieve]))
graph_builder.add_node(generate)
graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

graph = graph_builder.compile(checkpointer=memory)

# Streamlit app
st.set_page_config(page_title="Nachabot", page_icon="🤖")
st.title("Nachabot 🤖")

# Inicializar historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy Nachabot, la IA de admisiones de la UNAL. ¿En qué puedo ayudarte?"}]

# Mostrar historial de mensajes
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje aquí...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Procesar entrada con el gráfico
    for step in graph.stream(
        {"messages": st.session_state["messages"]},
        stream_mode="values",
        config={"configurable": {"thread_id": "nachabot_thread"}},
    ):
        response = step["messages"][-1]
    st.session_state["messages"].append({"role": "assistant", "content": response.content})
    st.chat_message("assistant").write(response.content)