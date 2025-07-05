import streamlit as st
import re
import json
from datetime import datetime
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import GraphCypherQAChain

def initialize_neo4j_graph(uri, username, password):
    """
    Initialize the Neo4j graph connection.
    
    Args:
        uri (str): Neo4j database URI
        username (str): Neo4j username
        password (str): Neo4j password
    
    Returns:
        Neo4jGraph: Initialized Neo4j graph object
    """
    return Neo4jGraph(
        url=uri,  
        username=username, 
        password=password, 
    )

def initialize_llm_with_schema(model_name, api_key, schema):
    """
    Initialize the Language Model with schema preamble.
    
    Args:
        model_name (str): Name of the Google model
        api_key (str): Google API key
        schema (str): Graph schema for preamble
    
    Returns:
        GoogleGenerativeAIModel: Initialized language model
    """
    # Step 1: Send schema as preamble to initialize LLM
    preamble_prompt = f"""
    You are a Neo4j Cypher query expert. You have access to a graph database with the following schema:
    
    {schema}
    
    Your task is to generate accurate Cypher queries based on natural language questions.
    Always use the provided schema to understand the available nodes, relationships, and properties.
    """
    llm = ChatGoogleGenerativeAI(model=model_name, api_key=api_key)
    
    # Initialize the model with schema context
    try:
        llm.invoke(preamble_prompt)
        st.success("✅ LLM initialized with graph schema preamble")
    except Exception as e:
        st.warning(f"Schema preamble initialization failed: {e}")
    
    return llm

def create_cypher_generation_prompt():
    """
    Create a prompt template for Cypher query generation.
    
    Returns:
        PromptTemplate: Configured prompt template for Cypher query generation
    """
    return PromptTemplate(
        input_variables=["question", "schema"],
        template="""
        Generate a Cypher query that answers the question based on the provided graph schema.
        Use the following rules:
        1. If the question asks about relationships between nodes, use the relationship types provided in the schema.
        2. If the question asks about node properties, use the node labels and property names provided in the schema.
        3. When dealing with variable length paths, and filtering relationship types within those paths, use the any() function.
        4. Return ONLY the cypher query. Do not return any explanation.
        5. Ensure the query retrieves sufficient context to answer the question completely.
        
        Question: {question}
        Schema: {schema}
        Cypher:
        """,
    )

def initialize_graph_cypher_qa_chain(llm, graph, cypher_prompt):
    """
    Initialize the GraphCypherQAChain.
    
    Args:
        llm (ChatGoogleAI): Language model
        graph (Neo4jGraph): Neo4j graph connection
        cypher_prompt (PromptTemplate): Cypher generation prompt template
    
    Returns:
        GraphCypherQAChain: Configured graph Cypher QA chain
    """
    return GraphCypherQAChain.from_llm(
        llm,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,
        cypher_prompt=cypher_prompt,
        return_intermediate_steps=True,  # This helps us see the retrieved context
    )

def log_query_and_response(query, cypher_query, response, retrieved_context=None):
    """
    Log user query and generated response (Step 6 from diagram).
    
    Args:
        query (str): User's natural language query
        cypher_query (str): Generated Cypher query
        response (str): Final answer
        retrieved_context (str): Context retrieved from database
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_query": query,
        "generated_cypher": cypher_query,
        "retrieved_context": retrieved_context,
        "final_answer": response
    }
    
    # Initialize query history in session state
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    st.session_state.query_history.append(log_entry)
    
    # Display log confirmation
    st.success("✅ Query logged successfully")

def execute_cypher_and_get_context(graph, cypher_query):
    """
    Execute Cypher query and retrieve context from Neo4j (Step 4).
    
    Args:
        graph (Neo4jGraph): Neo4j graph connection
        cypher_query (str): Cypher query to execute
    
    Returns:
        tuple: (context_data, formatted_context)
    """
    try:
        # Execute the query
        context_data = graph.query(cypher_query)
        
        # Format the context for display
        if context_data:
            formatted_context = json.dumps(context_data, indent=2, ensure_ascii=False)
        else:
            formatted_context = "No data retrieved from the database."
            
        return context_data, formatted_context
    
    except Exception as e:
        error_msg = f"Error executing Cypher query: {str(e)}"
        return None, error_msg

def process_query_with_full_rag(chain, query, graph, custom_schema=None):
    """
    Process the user's query following the complete RAG workflow.
    
    Args:
        chain (GraphCypherQAChain): Graph Cypher QA chain
        query (str): User's natural language query (Step 2)
        graph (Neo4jGraph): Neo4j graph connection
        custom_schema (str): Optional custom schema
    
    Returns:
        dict: Complete workflow results
    """
    try:
        # Step 2: User asks for a NL query (already received as parameter)
        
        # Step 3: LLM generates a retrieval Cypher
        schema_to_use = custom_schema if custom_schema else str(graph.schema)
        cypher_query = chain.cypher_generation_chain.run(
            question=query, 
            schema=schema_to_use
        )
        
        # Clean the cypher query
        cypher_query = re.sub(r"^```(\w+)?|\n```$", "", cypher_query, flags=re.MULTILINE).strip()
        
        # Step 4: Run Cypher on Neo4j DB, retrieve context
        context_data, formatted_context = execute_cypher_and_get_context(graph, cypher_query)
        
        # Step 5: Feed LLM with context retrieved from the DB & LLM generates final answer
        if context_data is not None:
            response = chain.run(query)
        else:
            response = f"Unable to retrieve data from the database. Error: {formatted_context}"
        
        # Step 6: Log user NL query and generated Query
        log_query_and_response(query, cypher_query, response, formatted_context)
        
        return {
            "response": response,
            "cypher_query": cypher_query,
            "retrieved_context": formatted_context,
            "context_data": context_data
        }
    
    except Exception as e:
        error_response = f"An error occurred while processing the query: {e}"
        log_query_and_response(query, "ERROR", error_response, str(e))
        raise RuntimeError(error_response)

def main():
    """
    Main function to set up and run the Streamlit application.
    """
    st.set_page_config(page_title="Knowledge Graph RAG Assistant", layout="wide")
    
    st.title("🔍 Knowledge Graph RAG Assistant")
    st.markdown("**Following the complete RAG workflow: Schema → Query → Cypher → Retrieve → Answer → Log**")
    
    with st.sidebar:
        st.header("Configuration")
        
        # Database Connection Settings
        st.subheader("Database Connection")
        with st.expander("Neo4j Connection Details", expanded=True):
            neo4j_uri = st.text_input("Neo4j URI", value="bolt://localhost:7687", key="uri")
            neo4j_user = st.text_input("Neo4j Username", value="neo4j", key="username")
            neo4j_password = st.text_input("Neo4j Password", value="thesis2025", type="password", key="password")

        # Model Settings
        st.subheader("LLM Configuration")
        model_options = {
                "Gemini 1.5 Flash": "gemini-1.5-flash",
                "Gemini 1.5 Pro": "gemini-1.5-pro",
                "Gemini 2.0 Flash": "gemini-2.0-flash",
                "Gemini 2.0 Flash-Lite": "gemini-2.0-flash-lite",
            }
        selected_model = st.selectbox("Select Model", options=list(model_options.keys()), key="model")
        api_key = st.text_input("Google API Key", type="password", key="api_key", value="YOUR API KEY HERE")

        # Connect button
        connect_button = st.button("🔌 Connect to Database")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Query", "📊 Custom Schema", "📝 Query History"])
    
    # Initialize session state
    if 'graph' not in st.session_state:
        st.session_state.graph = None
    if 'chain' not in st.session_state:
        st.session_state.chain = None
    if 'custom_schema' not in st.session_state:
        st.session_state.custom_schema = None
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    if 'schema_initialized' not in st.session_state:
        st.session_state.schema_initialized = False
    
    # Try to connect when button is pressed
    if connect_button:
        try:
            with st.spinner("Connecting to Neo4j database..."):
                st.session_state.graph = initialize_neo4j_graph(neo4j_uri, neo4j_user, neo4j_password)
                
                # Get schema for LLM initialization
                schema = str(st.session_state.graph.schema)
                model_name = model_options[selected_model]
                
                # Step 1: Initialize LLM with schema preamble
                st.session_state.llm = initialize_llm_with_schema(model_name, api_key, schema)
                
                cypher_prompt = create_cypher_generation_prompt()
                st.session_state.chain = initialize_graph_cypher_qa_chain(
                    st.session_state.llm, st.session_state.graph, cypher_prompt
                )
                st.session_state.schema_initialized = True
                st.sidebar.success("🎉 Connected successfully! LLM initialized with schema.")
        except Exception as e:
            st.sidebar.error(f"❌ Connection failed: {str(e)}")
    
    # Custom Schema Tab
    with tab2:
        st.header("📊 Custom Graph Schema")
        st.markdown("""
        Provide your own graph schema to override the database schema. 
        This is useful for testing or when working with hypothetical graph structures.
        """)
        
        custom_schema = st.text_area(
            "Enter custom graph schema:",
            height=300,
            placeholder="Enter nodes, relationships and their properties..."
        )
        
        upload_schema = st.file_uploader("Or upload schema file:", type=["txt"])
        
        if upload_schema is not None:
            custom_schema = upload_schema.getvalue().decode("utf-8")
            st.text_area("Uploaded schema:", value=custom_schema, height=300, disabled=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Apply Custom Schema"):
                if custom_schema:
                    st.session_state.custom_schema = custom_schema
                    # Re-initialize LLM with new schema
                    if st.session_state.llm and api_key:
                        model_name = model_options[selected_model]
                        st.session_state.llm = initialize_llm_with_schema(model_name, api_key, custom_schema)
                    st.success("✅ Custom schema applied! LLM re-initialized with new schema.")
                else:
                    st.error("Please enter or upload a schema first.")
        
        with col2:
            if st.button("🗑️ Clear Custom Schema"):
                st.session_state.custom_schema = None
                # Re-initialize with database schema
                if st.session_state.graph and st.session_state.llm and api_key:
                    model_name = model_options[selected_model]
                    schema = str(st.session_state.graph.schema)
                    st.session_state.llm = initialize_llm_with_schema(model_name, api_key, schema)
                st.success("✅ Custom schema cleared. Using database schema.")
    
    # Query Tab
    with tab1:
        st.header("🔍 Natural Language Query")
        
        # Show RAG workflow status
        if st.session_state.schema_initialized:
            st.success("🎯 RAG Pipeline Ready: Schema → Query → Cypher → Retrieve → Answer → Log")
        else:
            st.warning("⚠️ Please connect to database first to initialize the RAG pipeline")
        
        query = st.text_input("💬 Enter your natural language query about the graph:")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.button("🚀 Submit Query")
        
        with col2:
            if st.session_state.graph is None:
                st.info("Please connect to the database first using the sidebar.")
        
        if submit_button and st.session_state.graph and st.session_state.chain:
            if not query.strip():
                st.error("Please enter a query first.")
            else:
                with st.spinner("Processing your query through RAG pipeline..."):
                    try:
                        # Process query with full RAG workflow
                        result = process_query_with_full_rag(
                            st.session_state.chain, 
                            query, 
                            st.session_state.graph,
                            st.session_state.custom_schema
                        )
                        
                        # Step 7: Display the answer to user
                        st.subheader("📋 Final Answer")
                        st.write(result["response"])
                        
                        # Show intermediate steps
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            with st.expander("🔧 Generated Cypher Query (Step 3)"):
                                st.code(result["cypher_query"], language="cypher")
                        
                        with col2:
                            with st.expander("📊 Retrieved Context (Step 4)"):
                                if result["context_data"]:
                                    st.json(result["context_data"])
                                else:
                                    st.text("No data retrieved")
                        
                    except Exception as e:
                        st.error(f"❌ Error processing query: {str(e)}")
        
        # Show current schema in use
        st.subheader("📖 Current Graph Schema")
        with st.expander("📖 Current Graph Schema"):
            if st.session_state.custom_schema:
                st.text("Using custom schema:")
                st.text(st.session_state.custom_schema)
            elif st.session_state.graph:
                st.text("Using database schema:")
                st.text(str(st.session_state.graph.schema))
            else:
                st.info("No schema available. Please connect to the database.")
    
    # Query History Tab
    with tab3:
        st.header("📝 Query History & Logs")
        
        if 'query_history' in st.session_state and st.session_state.query_history:
            st.write(f"**Total Queries Logged:** {len(st.session_state.query_history)}")
            
            for i, log_entry in enumerate(reversed(st.session_state.query_history)):
                with st.expander(f"Query {len(st.session_state.query_history) - i}: {log_entry['user_query'][:50]}..."):
                    st.write(f"**Timestamp:** {log_entry['timestamp']}")
                    st.write(f"**User Query:** {log_entry['user_query']}")
                    st.write(f"**Generated Cypher:** {log_entry['generated_cypher']}")
                    st.write(f"**Final Answer:** {log_entry['final_answer']}")
                    
                    if log_entry.get('retrieved_context'):
                        st.write("**Retrieved Context:**")
                        st.text(log_entry['retrieved_context'])
            
            if st.button("🗑️ Clear Query History"):
                st.session_state.query_history = []
                st.success("Query history cleared!")
        else:
            st.info("No queries logged yet. Submit some queries to see the history here.")

if __name__ == "__main__":
    main()