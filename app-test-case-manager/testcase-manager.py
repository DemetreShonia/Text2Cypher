import streamlit as st
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Test Case Manager",
    page_icon="📊",
    layout="wide"
)

# Define the path to the JSON file
BENCHMARK_FILE = "cypher_benchmarks2.json"

# Function to load existing benchmarks
def load_benchmarks():
    if os.path.exists(BENCHMARK_FILE):
        try:
            with open(BENCHMARK_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error(f"Error parsing {BENCHMARK_FILE}. Creating a new benchmark file.")
            return []
    return []

# Function to save benchmarks
def save_benchmarks(benchmarks):
    with open(BENCHMARK_FILE, 'w') as f:
        json.dump(benchmarks, f, indent=2)

# Initialize session state
if 'benchmarks' not in st.session_state:
    st.session_state.benchmarks = load_benchmarks()

# App title and description
st.title("📊 Test Case Manager")
st.markdown("""
This tool allows you to easily create and manage benchmark test cases for Cypher queries.
Add new test cases with proper formatting and view existing benchmarks.
""")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Add New Test Case", "View Test Cases", "Edit Test Cases"])

# Tab 1: Add New Test Case
with tab1:
    st.header("Add New Test Case")
    
    # Form to add a new test case
    with st.form("add_test_case_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            test_id = st.text_input("ID", placeholder="unique_test_id")
            category = st.selectbox(
                "Category",
                options=["graph_recursion", "filtering", "path_finding", "aggregation", "pattern_matching", "other"],
                index=None,
                placeholder="Select a category"
            )
            if category == "other":
                category = st.text_input("Specify category")
            
            
        
        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                options=["easy", "medium", "hard"],
                index=None,
                placeholder="Select difficulty"
            )

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.text_input("Created At", value=created_at, disabled=True)
        
        nl_query = st.text_area(
            "Natural Language Query", 
            height=100,
            placeholder="Enter the natural language query to test"
        )
        
        # Use a monospace font for code inputs
        st.markdown("### Ground Truth Cypher Query")
        cypher_query = st.text_area(
            "Enter the correct Cypher query",
            height=200,
            placeholder="MATCH (n)-[r]->(m) WHERE n.property = 'value' RETURN n, r, m",
            key="cypher_textarea"
        )
        
        st.markdown("### Expected Results (JSON)")
        expected_results = st.text_area(
            "Enter the expected results in JSON format",
            height=200,
            placeholder='''[
  {
    "n": {"id": 123, "labels": ["Person"], "properties": {"name": "John"}},
    "r": {"id": 456, "type": "KNOWS", "properties": {"since": 2020}},
    "m": {"id": 789, "labels": ["Person"], "properties": {"name": "Jane"}}
  }
]''',
            key="results_textarea"
        )
        
        explanation = st.text_area(
            "Explanation",
            height=100,
            placeholder="Explain what this test case is testing"
        )
        
        submitted = st.form_submit_button("Add Test Case")
    
    if submitted:
        # Validate inputs
        if not test_id:
            st.error("Test ID is required")
        elif not category:
            st.error("Category is required")
        elif not difficulty:
            st.error("Difficulty is required")
        elif not nl_query:
            st.error("Natural language query is required")
        elif not cypher_query:
            st.error("Ground truth Cypher query is required")
        else:
            # Validate JSON format for expected results
            try:
                expected_results_json = json.loads(expected_results) if expected_results else []
            except json.JSONDecodeError:
                st.error("Expected results must be valid JSON")
                st.stop()
            
            # Create the test case object
            test_case = {
                "id": test_id,
                "category": category,
                "difficulty": difficulty,
                "natural_language_query": nl_query,
                "ground_truth_cypher": cypher_query,
                "expected_results": expected_results_json,
                "explanation": explanation,
                "created_at": created_at,
            }
            
            # Check for duplicate ID
            ids = [case["id"] for case in st.session_state.benchmarks]
            if test_id in ids:
                st.error(f"Test ID '{test_id}' already exists. Please use a unique ID.")
            else:
                # Add the test case and save
                st.session_state.benchmarks.append(test_case)
                save_benchmarks(st.session_state.benchmarks)
                st.success(f"Test case '{test_id}' added successfully!")
                # Clear the form using a rerun trick
                st.rerun()

# Tab 2: View Benchmarks
with tab2:
    st.header("View Benchmarks")
    
    if not st.session_state.benchmarks:
        st.info("No benchmark test cases found. Add some in the 'Add New Test Case' tab.")
    else:
        # Add filters
        col1, col2 = st.columns(2)
        with col1:
            filter_category = st.multiselect(
                "Filter by Category",
                options=list(set(case["category"] for case in st.session_state.benchmarks)),
                default=None
            )
        with col2:
            filter_difficulty = st.multiselect(
                "Filter by Difficulty",
                options=["easy", "medium", "hard"],
                default=None
            )
        
        # Filter benchmarks
        filtered_benchmarks = st.session_state.benchmarks
        if filter_category:
            filtered_benchmarks = [case for case in filtered_benchmarks if case["category"] in filter_category]
        if filter_difficulty:
            filtered_benchmarks = [case for case in filtered_benchmarks if case["difficulty"] in filter_difficulty]
        
        # Display benchmark count
        st.write(f"Showing {len(filtered_benchmarks)} of {len(st.session_state.benchmarks)} benchmarks")
        
        # Display benchmarks
        for i, case in enumerate(filtered_benchmarks):
            with st.expander(f"{case['id']} - {case['category']} ({case['difficulty']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**ID:** {case['id']}")
                    st.markdown(f"**Category:** {case['category']}")
                    st.markdown(f"**Difficulty:** {case['difficulty']}")
                    st.markdown(f"**Created At:** {case.get('created_at', 'N/A')}")
                
                st.markdown("### Natural Language Query")
                st.write(case["natural_language_query"])
                
                st.markdown("### Ground Truth Cypher Query")
                st.code(case["ground_truth_cypher"], language="cypher")
                
                st.markdown("### Expected Results")
                st.json(case["expected_results"])
                
                if case.get("explanation"):
                    st.markdown("### Explanation")
                    st.write(case["explanation"])

# Tab 3: Edit Benchmarks
with tab3:
    st.header("Edit Benchmarks")
    
    if not st.session_state.benchmarks:
        st.info("No benchmark test cases found. Add some in the 'Add New Test Case' tab.")
    else:
        # Select a test case to edit
        test_ids = [case["id"] for case in st.session_state.benchmarks]
        selected_id = st.selectbox("Select a test case to edit", options=test_ids)
        
        # Find the selected test case
        selected_case = next((case for case in st.session_state.benchmarks if case["id"] == selected_id), None)
        
        if selected_case:
            with st.form("edit_test_case_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    category = st.selectbox(
                        "Category",
                        options=["graph_recursion", "filtering", "path_finding", "aggregation", "pattern_matching", "other"],
                        index=["graph_recursion", "filtering", "path_finding", "aggregation", "pattern_matching", "other"].index(selected_case["category"]) if selected_case["category"] in ["graph_recursion", "filtering", "path_finding", "aggregation", "pattern_matching"] else 5
                    )
                    if category == "other":
                        category = st.text_input("Specify category", value=selected_case["category"] if selected_case["category"] not in ["graph_recursion", "filtering", "path_finding", "aggregation", "pattern_matching"] else "")
                    
                    difficulty = st.selectbox(
                        "Difficulty",
                        options=["easy", "medium", "hard"],
                        index=["easy", "medium", "hard"].index(selected_case["difficulty"])
                    )
                
                with col2:
                    created_at = st.text_input("Created At", value=selected_case.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")), disabled=True)
                
                nl_query = st.text_area(
                    "Natural Language Query", 
                    height=100,
                    value=selected_case["natural_language_query"]
                )
                
                st.markdown("### Ground Truth Cypher Query")
                cypher_query = st.text_area(
                    "Enter the correct Cypher query",
                    height=200,
                    value=selected_case["ground_truth_cypher"],
                    key="edit_cypher_textarea"
                )
                
                st.markdown("### Expected Results (JSON)")
                expected_results = st.text_area(
                    "Enter the expected results in JSON format",
                    height=200,
                    value=json.dumps(selected_case["expected_results"], indent=2),
                    key="edit_results_textarea"
                )
                
                explanation = st.text_area(
                    "Explanation",
                    height=100,
                    value=selected_case.get("explanation", "")
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button("Update Test Case")
                with col2:
                    delete_button = st.form_submit_button("Delete Test Case", type="primary", use_container_width=True)
            
            if update_button:
                # Validate JSON format for expected results
                try:
                    expected_results_json = json.loads(expected_results) if expected_results else []
                except json.JSONDecodeError:
                    st.error("Expected results must be valid JSON")
                    st.stop()
                
                # Update the test case
                index = test_ids.index(selected_id)
                st.session_state.benchmarks[index].update({
                    "category": category,
                    "difficulty": difficulty,
                    "natural_language_query": nl_query,
                    "ground_truth_cypher": cypher_query,
                    "expected_results": expected_results_json,
                    "explanation": explanation,
                })
                
                save_benchmarks(st.session_state.benchmarks)
                st.success(f"Test case '{selected_id}' updated successfully!")
                st.rerun()
            
            if delete_button:
                # Delete the test case
                st.session_state.benchmarks = [case for case in st.session_state.benchmarks if case["id"] != selected_id]
                save_benchmarks(st.session_state.benchmarks)
                st.success(f"Test case '{selected_id}' deleted successfully!")
                st.rerun()

# Add a footer
st.markdown("---")
st.markdown(f"Currently managing {len(st.session_state.benchmarks)} benchmark test cases. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Add export option
if st.button("Export Benchmarks to JSON"):
    st.download_button(
        label="Download JSON File",
        data=json.dumps(st.session_state.benchmarks, indent=2),
        file_name="cypher_benchmarks_export.json",
        mime="application/json"
    )
