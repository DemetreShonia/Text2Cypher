# app.py
# LLM Text-to-Cypher Translation Evaluation System - v2.3 (Robustness Update)

# --- IMPORTS ---
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json
import time
from datetime import datetime
import re
from pathlib import Path
from fpdf import FPDF
import numpy as np
import anthropic
from neo4j import GraphDatabase

# --- INITIAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CypherGen-Eval",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FILE PATHS ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TESTCASES_FILE = DATA_DIR / "testcases.json"
SIMPLE_SCHEMA_FILE = DATA_DIR / "simple_schema.txt"
DETAILED_SCHEMA_FILE = DATA_DIR / "detailed_schema.txt"
BASE_CONTEXT_FILE = DATA_DIR / "prompt_templates" / "base_context.txt"
BASE_NO_CONTEXT_FILE = DATA_DIR / "prompt_templates" / "base_no_context.txt"
RETRIEVAL_PROMPT_FILE = DATA_DIR / "prompt_templates" / "retrieval_prompt.txt"
PROMPT_TEMPLATE_FILE = DATA_DIR / "prompt_templates" / "base_prompt.txt"

# --- HELPER CLASSES AND FUNCTIONS ---
class APIRateLimiter:
    def __init__(self, requests_per_minute=30, delay_between_requests=1.0):
        self.rpm = requests_per_minute
        self.delay = delay_between_requests
        self.last_request_time = 0
        self.request_count = 0
        self.window_start = time.time()

    def wait_if_needed(self):
        current_time = time.time()
        if current_time - self.window_start >= 60:
            self.request_count = 0
            self.window_start = current_time
        if self.request_count >= self.rpm:
            sleep_time = 60 - (current_time - self.window_start)
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.request_count = 0
            self.window_start = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.delay:
            time.sleep(self.delay - time_since_last)
        self.request_count += 1
        self.last_request_time = time.time()

def call_claude_api(prompt, model, api_key):
    if not api_key:
        raise ValueError("API Key is missing.")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0,
            system="You are an expert Neo4j Cypher query translator. Return ONLY the Cypher query, with no explanations or markdown formatting.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()
    except Exception as e:
        raise Exception(f"Claude API Error: {str(e)}")

def track_token_usage(prompt, response, provider):
    # Estimate token usage based on character count (rough approximation)
    return int(len(prompt) / 4 + len(response) / 4)

def get_db_driver(uri, auth):
    if not uri or not auth[0] or not auth[1]:
        return None
    return GraphDatabase.driver(uri, auth=auth)

def test_db_connection(uri, username, password):
    if not uri or not username or not password:
        return False, "Connection failed: Missing credentials."
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            session.run("RETURN 1")
        driver.close()
        return True, "Connection successful!"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def execute_cypher_query(driver, query, timeout=10):
    if not driver:
        return {'success': False, 'error': 'Database not connected.', 'infinite_loop': False}
    
    try:
        with driver.session() as session:
            result = session.run(query, timeout=timeout)
            return {'success': True, 'results': [dict(record) for record in result], 'infinite_loop': False}
    except Exception as e:
        error_str = str(e).lower()
        is_timeout = "timeout" in error_str
        return {'success': False, 'error': str(e), 'infinite_loop': is_timeout}

def normalize_item(item):
    if isinstance(item, dict):
        return {k: normalize_item(v) for k, v in item.items()}
    if isinstance(item, list):
        try:
            return sorted([normalize_item(i) for i in item])
        except TypeError:
            return frozenset(json.dumps(normalize_item(i), sort_keys=True) for i in item)
    if isinstance(item, float) and item.is_integer():
        return int(item)
    return item

def compare_results(expected, actual, manual_override=None):
    if manual_override is not None:
        return {'semantic_accurate': manual_override}
    if not isinstance(expected, list) or not isinstance(actual, list):
        return {'semantic_accurate': False}
    
    norm_expected = normalize_item(expected)
    norm_actual = normalize_item(actual)
    semantic_match = frozenset(json.dumps(d, sort_keys=True) for d in norm_expected) == frozenset(json.dumps(d, sort_keys=True) for d in norm_actual)
    return {'semantic_accurate': semantic_match}

def calculate_strategy_metrics(eval_data):
    total_cases = len(eval_data.get('test_cases', []))
    if total_cases == 0: return {'strategy': eval_data.get('strategy', 'N/A'), 'accuracy': 0, 'syntax_ok': 0, 'exec_ok': 0, 'total_tokens': 0, 'avg_tokens': 0, 'total_cases': 0}
    correct_count, syntax_ok_count, exec_ok_count = 0, 0, 0
    for res in eval_data['test_cases']:
        is_correct = res['manual_override'] if res['manual_override'] is not None else res['semantic_accurate']
        if is_correct: correct_count += 1
        if res['syntactic_correct']: syntax_ok_count += 1
        if res['execution_success']: exec_ok_count += 1
    accuracy = (correct_count / total_cases) * 100; syntax_ok_pct = (syntax_ok_count / total_cases) * 100
    exec_ok_pct = (exec_ok_count / total_cases) * 100; avg_tokens = eval_data.get('token_usage', 0) / total_cases if total_cases > 0 else 0
    return {'strategy': eval_data['strategy'], 'accuracy': accuracy, 'syntax_ok': syntax_ok_pct, 'exec_ok': exec_ok_pct, 'total_tokens': eval_data.get('token_usage', 0), 'avg_tokens': avg_tokens, 'total_cases': total_cases}

# Initialize rate limiter
api_rate_limiter = APIRateLimiter(requests_per_minute=20, delay_between_requests=1.5)

class TestCase:
    def __init__(self, data):
        self.id = data.get('id', 'N/A')
        self.category = data.get('category', 'Uncategorized')
        self.difficulty = data.get('difficulty', 'normal')
        self.question = data.get('natural_language_query', '')
        self.cypher = data.get('ground_truth_cypher', '')
        self.expected_result = data.get('expected_results', [])
        self.explanation = data.get('explanation', '')
        self.created_at = data.get('created_at', '')
        self.tags = data.get('tags', [])

# --- FILE LOADING FUNCTIONS ---
@st.cache_data
def load_text_file(file_path):
    try:
        return file_path.read_text()
    except Exception as e:
        st.error(f"Failed to load file: {file_path}. Error: {e}")
        return ""

@st.cache_data
def load_test_cases(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [TestCase(tc) for tc in data]
    except FileNotFoundError:
        st.error(f"Test cases file not found: {file_path}. The application cannot run without it.")
        return []
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {file_path}. Please check the file for syntax errors.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred while loading test cases: {e}")
        return []


def serialize_neo4j_object(obj):
    if hasattr(obj, '_properties'):  # Neo4j Node/Relationship
        result = dict(obj._properties)
        if hasattr(obj, 'labels'):  # Node
            result['_labels'] = list(obj.labels)
        if hasattr(obj, 'type'):  # Relationship
            result['_type'] = obj.type
        return result
    elif isinstance(obj, dict):
        return {k: serialize_neo4j_object(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_neo4j_object(item) for item in obj]
    else:
        return obj

# --- CORE EVALUATION LOGIC ---
def execute_test_case(test_case, strategy_name, db_driver, llm_config, schemas):
    start_time = time.time()
    schema_type, retrieval_method = strategy_name.split(' + ')
    schema_content = schemas.get('detailed', '') if schema_type == "Detailed" else schemas.get('simple', '')
    retrieval_cypher = None
    context = ""
    try:
        if retrieval_method == "Retrieval":
            # Step 1: Generate context-retrieval Cypher
            retrieval_prompt = load_text_file(RETRIEVAL_PROMPT_FILE)
            retrieval_prompt = retrieval_prompt.format(
                schema=schema_content,
                question=test_case.question
            )
            api_rate_limiter.wait_if_needed()
            retrieval_cypher = call_claude_api(retrieval_prompt, llm_config['model'], llm_config['api_key'])
            # Step 2: Run context-retrieval Cypher
            context_result = execute_cypher_query(db_driver, retrieval_cypher)
            if not context_result['success']:
                # If context retrieval fails, record error and skip final Cypher generation
                return {
                    'test_case_id': test_case.id,
                    'test_case_obj': test_case,
                    'strategy_name': strategy_name,
                    'retrieval_cypher': retrieval_cypher,
                    'context': None,
                    'ground_truth_cypher': test_case.cypher,
                    'generated_cypher': None,
                    'gt_query_result': None,
                    'gen_query_result': None,
                    'tokens_used': 0,
                    'syntactic_correct': False,
                    'execution_success': False,
                    'execution_error': f"Context retrieval failed: {context_result.get('error')}",
                    'semantic_accurate': False,
                    'infinite_loop': context_result.get('infinite_loop', False),
                    'manual_override': None
                }
            # Convert Neo4j objects to string representation
            serialized_results = serialize_neo4j_object(context_result['results'])
            context = str(serialized_results)
            # Step 3: Generate final Cypher using context
            prompt = load_text_file(BASE_CONTEXT_FILE)
            prompt = prompt.format(
                schema=schema_content,
                context=context,
                question=test_case.question
            )
        else:
            # No-Retrieval: Direct Cypher generation
            prompt = load_text_file(BASE_NO_CONTEXT_FILE)
            prompt = prompt.format(
                schema=schema_content,
                question=test_case.question
            )
        # Step 4: Generate final Cypher
        api_rate_limiter.wait_if_needed()
        generated_cypher = call_claude_api(prompt, llm_config['model'], llm_config['api_key'])
        tokens_used = track_token_usage(prompt, generated_cypher, llm_config['provider'])
        # Step 5: Validate and execute the generated Cypher
        is_syntactic_correct = bool(re.match(r'^\s*(MATCH|MERGE|CREATE|CALL)\b', generated_cypher.strip(), re.IGNORECASE))
        gt_result = execute_cypher_query(db_driver, test_case.cypher)
        gen_result = execute_cypher_query(db_driver, generated_cypher) if is_syntactic_correct else {'success': False, 'error': 'Skipped execution due to syntax error.', 'infinite_loop': False}
        semantic_comparison = compare_results(gt_result.get('results', []), gen_result.get('results', [])) if gt_result.get('success') and gen_result.get('success') else {'semantic_accurate': False}
        return {
            'test_case_id': test_case.id,
            'test_case_obj': test_case,
            'strategy_name': strategy_name,
            'retrieval_cypher': retrieval_cypher,
            'context': context if retrieval_method == "Retrieval" else None,
            'ground_truth_cypher': test_case.cypher,
            'generated_cypher': generated_cypher,
            'gt_query_result': gt_result.get('results', []),
            'gen_query_result': gen_result.get('results', []),
            'tokens_used': tokens_used,
            'syntactic_correct': is_syntactic_correct,
            'execution_success': gen_result['success'],
            'execution_error': gen_result.get('error'),
            'semantic_accurate': semantic_comparison['semantic_accurate'],
            'infinite_loop': gen_result.get('infinite_loop', False),
            'manual_override': None,
            'execution_time': round(time.time() - start_time, 2) 
        }
    except Exception as e:
        return {
            'test_case_id': test_case.id,
            'test_case_obj': test_case,
            'strategy_name': strategy_name,
            'retrieval_cypher': retrieval_cypher,
            'context': context if retrieval_method == "Retrieval" else None,
            'ground_truth_cypher': test_case.cypher,
            'generated_cypher': None,
            'gt_query_result': None,
            'gen_query_result': None,
            'tokens_used': 0,
            'syntactic_correct': False,
            'execution_success': False,
            'execution_error': f"Error in test case execution: {str(e)}",
            'semantic_accurate': False,
            'infinite_loop': False,
            'manual_override': None,
            'execution_time': round(time.time() - start_time, 2)
        }

# --- REPORTING & EXPORT FUNCTIONS ---
def generate_run_csv(evaluation_data):
    records = []
    for res in evaluation_data.get('test_cases', []):
        is_correct = res['manual_override'] if res['manual_override'] is not None else res.get('semantic_accurate', False)
        records.append({
            "Test Case ID": res.get('test_case_id', 'N/A'), "Category": getattr(res.get('test_case_obj'), 'category', 'N/A'),
            "Difficulty": getattr(res.get('test_case_obj'), 'difficulty', 'N/A'), "Question": getattr(res.get('test_case_obj'), 'question', 'N/A'),
            "Ground Truth Cypher": res.get('ground_truth_cypher', ''), "Generated Cypher": res.get('generated_cypher', ''),
            "Syntactic Correct": res.get('syntactic_correct', False), "Execution Success": res.get('execution_success', False),
            "Semantic Accurate": res.get('semantic_accurate', False), "Manual Override": res.get('manual_override', None),
            "Final Correctness": is_correct, "Tokens Used": res.get('tokens_used', 0),
            "Execution Time (s)": res.get('execution_time', 0),
            "Execution Error": res.get('execution_error', ''), "Context Used": bool(res.get('context'))
        })
    df = pd.DataFrame(records)
    return df.to_csv(index=False).encode('utf-8')

import json
from datetime import datetime

def generate_run_markdown(evaluation_data):
    """Generate a clean markdown evaluation report suitable for PDF conversion"""
    
    markdown_content = []
    
    # Title and Header
    strategy = evaluation_data.get('strategy', 'N/A')
    markdown_content.append(f"# Evaluation Report: {strategy}")
    markdown_content.append("")
    
    timestamp = evaluation_data.get('timestamp', '')
    if timestamp:
        formatted_time = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        markdown_content.append(f"**Run Time:** {formatted_time}")
        markdown_content.append("")
    
    # Summary Metrics
    summary = calculate_strategy_metrics(evaluation_data)
    markdown_content.append("## Summary Metrics")
    markdown_content.append("")
    markdown_content.extend([
        f"- **Total Cases:** {summary['total_cases']}",
        f"- **Overall Accuracy:** {summary['accuracy']:.2f}%",
        f"- **Syntactic Correctness:** {summary['syntax_ok']:.2f}%",
        f"- **Execution Success:** {summary['exec_ok']:.2f}%",
        f"- **Total Tokens:** {summary['total_tokens']:,}",
        ""
    ])
    
    # Test Cases
    markdown_content.append("## Test Cases")
    markdown_content.append("")
    
    for i, res in enumerate(evaluation_data.get('test_cases', [])):
        # Test case passes if semantically accurate (with manual override if present)
        is_semantically_correct = res['manual_override'] if res['manual_override'] is not None else res.get('semantic_accurate', False)
        
        # Determine status - PASS means semantically correct
        if res.get('error'):
            status = "ERROR"
        elif is_semantically_correct:
            status = "PASS"
        else:
            status = "FAIL"
        
        test_case_id = res.get('test_case_id', 'N/A')
        markdown_content.append(f"### Test Case {i+1}: {test_case_id}")
        markdown_content.append(f"**Status:** {status}")
        markdown_content.append("")
        
        # Question
        question = getattr(res.get('test_case_obj'), 'question', 'N/A')
        markdown_content.append("#### Natural Language Query")
        markdown_content.append("```")
        markdown_content.append(str(question))
        markdown_content.append("```")
        markdown_content.append("")
        
        # Ground Truth Cypher
        ground_truth = res.get('ground_truth_cypher', '')
        markdown_content.append("#### Ground Truth Cypher")
        markdown_content.append("```cypher")
        markdown_content.append(str(ground_truth))
        markdown_content.append("```")
        markdown_content.append("")
        
        # Generated Cypher
        generated = res.get('generated_cypher', '')
        markdown_content.append("#### Generated Cypher")
        markdown_content.append("```cypher")
        markdown_content.append(str(generated))
        markdown_content.append("```")
        markdown_content.append("")
        
        # Error Analysis (if present)
        if res.get('execution_error'):
            markdown_content.append("#### Error Analysis")
            markdown_content.append("```")
            markdown_content.append(str(res['execution_error']))
            markdown_content.append("```")
            markdown_content.append("")
        
        # Results Comparison
        markdown_content.append("#### Results Comparison")
        markdown_content.append("")
        
        # Expected Results
        markdown_content.append("**Expected Results:**")
        markdown_content.append("```json")
        expected = json.dumps(res.get('gt_query_result', []), indent=2, ensure_ascii=False)
        markdown_content.append(str(expected))
        markdown_content.append("```")
        markdown_content.append("")
        
        # Actual Results
        markdown_content.append("**Actual Results:**")
        markdown_content.append("```json")
        actual = json.dumps(res.get('gen_query_result', []), indent=2, ensure_ascii=False)
        markdown_content.append(str(actual))
        markdown_content.append("```")
        markdown_content.append("")
        
        # Additional Information
        markdown_content.append("#### Additional Information")
        markdown_content.append("")
        
        # Get test case attributes safely
        test_case_obj = res.get('test_case_obj')
        category = getattr(test_case_obj, 'category', 'N/A') if test_case_obj else 'N/A'
        difficulty = getattr(test_case_obj, 'difficulty', 'N/A') if test_case_obj else 'N/A'
        
        # Boolean indicators
        syntax_indicator = "Yes" if res.get('syntactic_correct') else "No"
        exec_indicator = "Yes" if res.get('execution_success') else "No"
        loop_indicator = "Yes" if res.get('infinite_loop') else "No"
        
        markdown_content.extend([
            f"- **Category:** {category}",
            f"- **Difficulty:** {difficulty}",
            f"- **Tokens Used:** {res.get('tokens_used', 0):,}",
            f"- **Execution Time:** {res.get('execution_time', 0):.2f}s",
            f"- **Syntactic Correct:** {syntax_indicator}",
            f"- **Execution Success:** {exec_indicator}",
            f"- **Test Case Passed:** {'Yes' if status == 'PASS' else 'No'}",
            f"- **Infinite Loop:** {loop_indicator}",
            ""
        ])
        
        # Add separator between test cases
        markdown_content.append("---")
        markdown_content.append("")
    
    # Ensure all content is string before joining
    markdown_content = [str(item) for item in markdown_content]
    return "\n".join(markdown_content)

def save_run_markdown(evaluation_data, filename="evaluation_report.md"):
    """Save markdown report to file"""
    markdown_content = generate_run_markdown(evaluation_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return filename

def generate_summary_markdown(evaluation_data):
    """Generate a condensed summary version"""
    markdown_content = []
    
    strategy = evaluation_data.get('strategy', 'N/A')
    markdown_content.append(f"# 📊 {strategy} - Summary")
    markdown_content.append("")
    
    # Summary table
    summary = calculate_strategy_metrics(evaluation_data)
    markdown_content.extend([
        "| Metric | Value |",
        "|--------|-------|",
        f"| 📋 Total Cases | {summary['total_cases']} |",
        f"| 🎯 Overall Accuracy | {summary['accuracy']:.2f}% |",
        f"| ✅ Syntactic Correctness | {summary['syntax_ok']:.2f}% |",
        f"| 🚀 Execution Success | {summary['exec_ok']:.2f}% |",
        f"| 🔢 Total Tokens | {summary['total_tokens']:,} |",
        ""
    ])
    
    # Quick test results overview
    markdown_content.append("## 🧪 Test Results Overview")
    markdown_content.append("")
    
    passed = failed = errored = 0
    for res in evaluation_data.get('test_cases', []):
        is_correct = res['manual_override'] if res['manual_override'] is not None else res.get('semantic_accurate', False)
        if res.get('error'):
            errored += 1
        elif is_correct:
            passed += 1
        else:
            failed += 1
    
    markdown_content.extend([
        f"- ✅ **Passed:** {passed}",
        f"- ❌ **Failed:** {failed}",
        f"- ⚠️ **Errors:** {errored}",
        ""
    ])
    
    return "\n".join(markdown_content)

 
# --- MAIN STREAMLIT APPLICATION ---
def initialize_state():
    if 'initialized' in st.session_state:
        return
    st.session_state.evaluation_results = {}
    st.session_state.current_evaluation_id = None
    st.session_state.neo4j_config = {'uri': 'bolt://localhost:7687', 'user': 'neo4j', 'pass': 'thesis2025'}
    st.session_state.llm_config = {'provider': 'Claude', 'model': 'claude-3-5-sonnet-20240620', 'api_key': "ENTER YOUR API KEY HERE, use .env file to store it."}

    st.session_state.neo4j_connected = False
    st.session_state.db_driver = None
    
    st.session_state.test_cases = load_test_cases(TESTCASES_FILE)
    st.session_state.schemas = {
        "simple": load_text_file(SIMPLE_SCHEMA_FILE),
        "detailed": load_text_file(DETAILED_SCHEMA_FILE)
    }
    st.session_state.initialized = True

def render_dashboard():
    st.image("https://dist.neo4j.com/wp-content/uploads/20210423042456/neo4j-social-share-21.png", width=200)
    st.title("LLM Text-to-Cypher Translation Evaluation System")
    st.markdown("---")
    st.subheader("System Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.get('neo4j_connected', False): st.success("🟢 **Database Connected**")
        else: st.error("🔴 **Database Disconnected**")
        st.markdown("Configure in `⚙️ Configuration`")
    with col2:
        if st.session_state.llm_config.get('api_key'): st.success("🟢 **LLM API Configured**")
        else: st.error("🔴 **No API Key**")
        st.markdown(f"Provider: `{st.session_state.llm_config.get('provider', 'N/A')}`")
    with col3:
        test_count = len(st.session_state.get('test_cases', []))
        st.info(f"📋 **Test Cases Loaded: {test_count}**")
        st.markdown("Manage in `🗃️ Test Case Management`")
    st.markdown("---")
    st.subheader("Recent Activity")
    if not st.session_state.evaluation_results:
        st.info("No evaluations run yet. Go to `🚀 Run Evaluation` to start.")
    else:
        df_summary = pd.DataFrame([calculate_strategy_metrics(v) for v in st.session_state.evaluation_results.values()])
        st.dataframe(df_summary, use_container_width=True)

def render_test_case_management():
    st.title("🗃️ Test Case Management")
    st.markdown("Overview of the loaded test cases for evaluation.")
    test_cases = st.session_state.get('test_cases', [])
    if not test_cases:
        st.warning("No test cases loaded. Please check your `testcases-mine.json` file.")
        return

    # Group test cases by category
    test_cases_by_category = {}
    for tc in test_cases:
        if tc.category not in test_cases_by_category:
            test_cases_by_category[tc.category] = []
        test_cases_by_category[tc.category].append(tc)

    # Display statistics
    col1, col2 = st.columns(2)
    with col1:
        category_counts = Counter([tc.category for tc in test_cases])
        if category_counts:
            fig_category = px.pie(values=list(category_counts.values()), 
                                names=list(category_counts.keys()), 
                                title="Test Cases by Category", 
                                hole=0.3)
            fig_category.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_category, use_container_width=True)
    with col2:
        difficulty_counts = Counter([tc.difficulty for tc in test_cases])
        if difficulty_counts:
            colors = {'easy': '#2ca02c', 'medium': '#ff7f0e', 'hard': '#d62728'}
            difficulty_order = ['easy', 'medium', 'hard']
            x_data = [d for d in difficulty_order if d in difficulty_counts]
            y_data = [difficulty_counts[d] for d in x_data]
            fig_difficulty = px.bar(x=x_data, y=y_data, color=x_data, 
                                  color_discrete_map=colors,
                                  labels={'x': 'Difficulty', 'y': 'Count'}, 
                                  title="Test Cases by Difficulty")
            fig_difficulty.update_layout(showlegend=False)
            st.plotly_chart(fig_difficulty, use_container_width=True)

    # Display test cases by category
    for category, category_test_cases in test_cases_by_category.items():
        st.subheader(f"📁 {category.title()} Test Cases")
        
        for tc in category_test_cases:
            with st.expander(f"ID: {tc.id} - {tc.question[:100]}... ({tc.difficulty.title()})"):
                st.markdown("**Question:**")
                st.info(tc.question)
                
                st.markdown("**Ground Truth Cypher:**")
                st.code(tc.cypher, language="cypher")
                
                if tc.explanation:
                    st.markdown("**Explanation:**")
                    st.info(tc.explanation)
                
                st.markdown("**Expected Results:**")
                st.json(tc.expected_result)
                
                if tc.tags:
                    st.markdown("**Tags:**")
                    st.write(", ".join(tc.tags))

def render_configuration():
    st.title("⚙️ Configuration")
    with st.expander("Neo4j Database Configuration", expanded=True):
        uri = st.text_input("Neo4j URI", value=st.session_state.neo4j_config['uri'])
        username = st.text_input("Username", value=st.session_state.neo4j_config['user'])
        password = st.text_input("Password", type="password", value=st.session_state.neo4j_config['pass'])
        if st.button("Test & Save Connection"):
            with st.spinner("Testing connection..."):
                is_success, message = test_db_connection(uri, username, password)
                if is_success:
                    st.success(f"✅ {message}"); st.session_state.neo4j_config = {'uri': uri, 'user': username, 'pass': password}
                    st.session_state.neo4j_connected = True; st.session_state.db_driver = get_db_driver(uri, (username, password))
                else:
                    st.error(f"❌ {message}"); st.session_state.neo4j_connected = False; st.session_state.db_driver = None
    with st.expander("LLM Configuration", expanded=True):
        provider = st.selectbox("Provider", ["Claude", "Gemini"], index=["Claude", "Gemini"].index(st.session_state.llm_config['provider']))
        
        model_options = {
            "Claude 4 Opus": "claude-opus-4-20250514",
            "Claude 4 Sonnet": "claude-sonnet-4-20250514",
            "Claude 3.7 Sonnet": "claude-3-7-sonnet-20250219",
            "Claude 3.5 Sonnet v2": "claude-3-5-sonnet-20241022",
            "Claude 3.5 Sonnet": "claude-3-5-sonnet-20240620",
            "Claude 3.5 Haiku": "claude-3-5-haiku-20241022",
            "Claude 3 Opus": "claude-3-opus-20240229",
            "Claude 3 Sonnet": "claude-3-sonnet-20240229",
            "Claude 3 Haiku": "claude-3-haiku-20240307",
        }
        if provider == "Claude": model = st.selectbox("Model", list(model_options.values()))
        else: model = st.selectbox("Model", ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"])
        api_key = st.text_input("API Key", type="password", value=st.session_state.llm_config.get('api_key', 'Use your API KEY'))
        if st.button("Save LLM Configuration"):
            st.session_state.llm_config = {'provider': provider, 'model': model, 'api_key': api_key}
            st.success("LLM configuration saved!"); st.rerun()

def display_individual_results():
    evaluation_id = st.session_state.current_evaluation_id
    results_data = st.session_state.evaluation_results.get(evaluation_id)
    if not results_data:
        st.error("Could not find the results for the current evaluation. Please re-run.")
        return

    st.header(f"Results for: {results_data['strategy']}")
    
    st.subheader("Export This Run")
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(label="📥 Download Results (CSV)", 
                         data=generate_run_csv(results_data),
                         file_name=f"evaluation_run_{evaluation_id}.csv",
                         mime="text/csv",
                         use_container_width=True)
    with dl_col2:
        st.download_button(label="📄 Download Report (Markdown)",
                         data=generate_run_markdown(results_data),
                         file_name=f"evaluation_report_{evaluation_id}.md", 
                         mime="text/markdown",
                         use_container_width=True)
    st.markdown("---")

    # Group test cases by category
    test_cases_by_category = {}
    for result in results_data.get('test_cases', []):
        category = getattr(result.get('test_case_obj'), 'category', 'Uncategorized')
        if category not in test_cases_by_category:
            test_cases_by_category[category] = []
        test_cases_by_category[category].append(result)

    # Display test cases by category
    for category, test_cases in test_cases_by_category.items():
        st.subheader(f"📁 {category.title()} Test Cases")
        
        for result in test_cases:
            is_correct = result['manual_override'] if result['manual_override'] is not None else result.get('semantic_accurate', False)
            status_icon = '✅' if is_correct else '❌'
            if result.get('error'): 
                status_icon = '⚠️'
            
            with st.expander(f"{status_icon} Test Case {result.get('test_case_id', 'N/A')} - {getattr(result.get('test_case_obj'), 'question', 'N/A')[:100]}..."):
                st.markdown("### Question")
                st.info(getattr(result.get('test_case_obj'), 'question', 'N/A'))
                
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Syntactic", "✅" if result.get('syntactic_correct') else "❌")
                m_col2.metric("Execution", "✅" if result.get('execution_success') else "❌")
                m_col3.metric("Semantic", "✅" if result.get('semantic_accurate') else "❌")
                # Loop: Only show warning if infinite_loop is True, otherwise show red cross
                if result.get('infinite_loop'):
                    m_col4.metric("Loop", "⚠️", "Timeout")
                else:
                    m_col4.metric("Loop", "❌")

                st.markdown("### Query Comparison")
                q_col1, q_col2 = st.columns(2)
                with q_col1:
                    st.markdown("**Ground Truth Cypher**")
                    st.code(result.get('ground_truth_cypher', ''), language='cypher')
                with q_col2:
                    st.markdown("**Generated Cypher**")
                    st.code(result.get('generated_cypher', ''), language='cypher')

                if result.get('execution_error'):
                    st.markdown("### Error Analysis")
                    st.error(f"**Execution Error:** {result['execution_error']}")
                
                st.markdown("### Result Comparison")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("**Expected Result**")
                    st.json(result.get('gt_query_result', []), expanded=False)
                with res_col2:
                    st.markdown("**Actual Result**")
                    st.json(result.get('gen_query_result', []), expanded=False)

                st.markdown("### Additional Information")
                info_col1, info_col2, info_col3 = st.columns(3) 
                with info_col1:
                    st.metric("Tokens Used", f"{result.get('tokens_used', 0):,}")
                with info_col2:
                    st.metric("Execution Time", f"{result.get('execution_time', 0):.2f}s")
                with info_col3:  
                    st.metric("Difficulty", getattr(result.get('test_case_obj'), 'difficulty', 'N/A').title())

                st.markdown("### Manual Override")
                # Create unique keys for each button using test case ID
                test_case_id = result.get('test_case_id', 'N/A')
                override_key_base = f"override_{evaluation_id}_{test_case_id}"
                current_override_status = result.get('manual_override')
                status_text = "Current Status: **Auto-Graded**"
                if current_override_status is True:
                    status_text = "<span style='color:green;'>**Manually Marked Correct**</span>"
                elif current_override_status is False:
                    status_text = "<span style='color:red;'>**Manually Marked Incorrect**</span>"
                st.markdown(status_text, unsafe_allow_html=True)
                
                o_col1, o_col2, o_col3 = st.columns(3)
                with o_col1:
                    if st.button("Mark as Correct",
                                key=f"correct_{override_key_base}",
                                use_container_width=True):
                        # Find and update the correct test case in the original results
                        for tc in st.session_state.evaluation_results[evaluation_id]['test_cases']:
                            if tc.get('test_case_id') == test_case_id:
                                tc['manual_override'] = True
                                break
                        st.rerun()
                with o_col2:
                    if st.button("Mark as Incorrect",
                                key=f"incorrect_{override_key_base}",
                                use_container_width=True):
                        # Find and update the correct test case in the original results
                        for tc in st.session_state.evaluation_results[evaluation_id]['test_cases']:
                            if tc.get('test_case_id') == test_case_id:
                                tc['manual_override'] = False
                                break
                        st.rerun()
                with o_col3:
                    if st.button("Reset to Auto",
                                key=f"auto_{override_key_base}",
                                use_container_width=True):
                        # Find and update the correct test case in the original results
                        for tc in st.session_state.evaluation_results[evaluation_id]['test_cases']:
                            if tc.get('test_case_id') == test_case_id:
                                tc['manual_override'] = None
                                break
                        st.rerun()

def render_run_evaluation():
    st.title("🚀 Run Evaluation")
    if not st.session_state.get('neo4j_connected') or not st.session_state.get('llm_config', {}).get('api_key'):
        st.error("Please configure your Database and LLM in `⚙️ Configuration` first.")
        return
    st.subheader("1. Filter Test Cases")
    f_col1, f_col2 = st.columns(2)
    test_cases = st.session_state.get('test_cases', [])
    categories = ['All'] + sorted({tc.category for tc in test_cases})
    selected_category = f_col1.selectbox("Filter by Category", options=categories)
    difficulties = ['All'] + sorted({tc.difficulty for tc in test_cases}, key=lambda d: ('easy', 'medium', 'hard').index(d) if d in ('easy', 'medium', 'hard') else 99)
    selected_difficulty = f_col2.selectbox("Filter by Difficulty", options=difficulties)
    filtered_test_cases = test_cases
    if selected_category != 'All': filtered_test_cases = [tc for tc in filtered_test_cases if tc.category == selected_category]
    if selected_difficulty != 'All': filtered_test_cases = [tc for tc in filtered_test_cases if tc.difficulty == selected_difficulty]
    st.info(f"**{len(filtered_test_cases)}** test cases selected.")
    st.subheader("2. Select Prompting Strategy")
    s_col1, s_col2 = st.columns(2)
    schema_type = s_col1.radio("Schema Type", ["Simple", "Detailed"])
    retrieval_method = s_col2.radio("Retrieval Method", ["No-Retrieval", "Retrieval"])
    strategy_name = f"{schema_type} + {retrieval_method}"
    st.subheader("3. Execute")
    if st.button(f"Start Evaluation for '{strategy_name}'", type="primary", use_container_width=True, disabled=not filtered_test_cases):
        evaluation_id = f"{strategy_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.current_evaluation_id = evaluation_id
        st.session_state.evaluation_results[evaluation_id] = {'strategy': strategy_name, 'test_cases': [], 'summary_metrics': {}, 'token_usage': 0, 'timestamp': datetime.now().isoformat()}
        progress_bar = st.progress(0, text="Initializing...")
        for i, test_case in enumerate(filtered_test_cases):
            progress_bar.progress((i + 1) / len(filtered_test_cases), text=f"Processing {i+1}/{len(filtered_test_cases)}: {test_case.id}")
            result = execute_test_case(test_case, strategy_name, st.session_state.db_driver, st.session_state.llm_config, st.session_state.schemas)
            st.session_state.evaluation_results[evaluation_id]['test_cases'].append(result)
            st.session_state.evaluation_results[evaluation_id]['token_usage'] += result.get('tokens_used', 0)
        progress_bar.empty()
        st.success(f"Evaluation run '{evaluation_id}' completed!")
    if st.session_state.current_evaluation_id:
        st.markdown("---")
        display_individual_results()

def create_error_distribution_chart(all_results):
    st.subheader("🔬 Error Distribution by Strategy")
    error_data = []
    for eval_id, eval_data in all_results.items():
        strategy = eval_data['strategy']
        error_counts = Counter()
        for res in eval_data.get('test_cases', []):
            error_type = "Correct"
            if not res.get('syntactic_correct'): error_type = "Syntax Error"
            elif not res.get('execution_success'): error_type = "Execution Error / Timeout"
            elif not (res['manual_override'] if res['manual_override'] is not None else res.get('semantic_accurate')):
                error_type = "Semantic Mismatch"
            error_counts[error_type] += 1
        
        for error_type, count in error_counts.items():
            error_data.append({'strategy': strategy, 'error_type': error_type, 'count': count})
            
    if error_data:
        df_errors = pd.DataFrame(error_data)
        fig = px.bar(df_errors, x='strategy', y='count', color='error_type',
                     title="Outcome Distribution Across Strategies",
                     labels={'count': 'Number of Test Cases', 'strategy': 'Strategy', 'error_type': 'Outcome'},
                     barmode='stack', text_auto=True)
        fig.update_layout(yaxis_title="Number of Test Cases", xaxis_title="Evaluation Strategy")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No results to analyze.")

def render_results_analysis():
    st.title("📊 Results Analysis")
    if not st.session_state.get('evaluation_results'):
        st.info("No evaluation results to analyze. Please run an evaluation first.")
        return

    all_evaluations = st.session_state.evaluation_results
    all_summaries = [calculate_strategy_metrics(data) for data in all_evaluations.values()]
    df_strategies = pd.DataFrame(all_summaries)

    # --- NEW: Summary Section for All Strategies ---
    st.subheader("📝 Strategy Summaries")
    for eval_id, eval_data in all_evaluations.items():
        st.markdown(generate_summary_markdown(eval_data), unsafe_allow_html=True)
        st.markdown("---")

    st.subheader("📊 Strategy Performance Comparison")
    col1, col2 = st.columns(2)
    with col1:
        fig_accuracy = px.bar(df_strategies, x='strategy', y='accuracy', title="Accuracy Comparison", color='strategy', text_auto='.2f')
        fig_accuracy.update_traces(texttemplate='%{y:.2f}%', textposition='outside'); st.plotly_chart(fig_accuracy, use_container_width=True)
    with col2:
        fig_tokens = px.bar(df_strategies, x='strategy', y='total_tokens', title="Total Token Usage", color='strategy', text_auto=True)
        fig_tokens.update_traces(texttemplate='%{y:,}', textposition='outside'); st.plotly_chart(fig_tokens, use_container_width=True)

    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Error Analysis", "Confusion Matrices", "Performance Heatmap"])
    
    with tab1:
        create_error_distribution_chart(all_evaluations)
    
    with tab2:
        st.subheader("🔍 Confusion Matrices")
        for eval_id, eval_data in all_evaluations.items():
            st.write(f"**Strategy: {eval_data['strategy']}**")
            test_cases = eval_data.get('test_cases', [])
            if not test_cases: continue
            # --- FIX: Simplified and more robust confusion matrix logic ---
            y_pred = [(res['manual_override'] if res['manual_override'] is not None else res.get('semantic_accurate', False)) for res in test_cases]
            tp = sum(1 for p in y_pred if p is True)
            fn = len(y_pred) - tp
            z = [[tp, fn], [0, 0]]; x = ['Predicted Correct', 'Predicted Incorrect']; y = ['Actually Correct', '']
            fig = go.Figure(data=go.Heatmap(z=z, x=x, y=y, hoverongaps=False, colorscale='Blues', text=[[f"TP: {tp}", f"FN: {fn}"], ["", ""]], texttemplate="%{text}", showscale=False))
            fig.update_layout(title=f"Confusion Matrix for '{eval_data['strategy']}'"); st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🔥 Performance Heatmap (Category vs. Difficulty)")
        heatmap_data = [{'strategy': eval_data['strategy'], 'category': getattr(res.get('test_case_obj'), 'category', 'N/A'), 'difficulty': getattr(res.get('test_case_obj'), 'difficulty', 'N/A'), 'correct': 1 if (res['manual_override'] if res['manual_override'] is not None else res.get('semantic_accurate', False)) else 0} for eval_id, eval_data in all_evaluations.items() for res in eval_data.get('test_cases', [])]
        if heatmap_data:
            df = pd.DataFrame(heatmap_data)
            all_strategies = list(all_evaluations.keys())
            if all_strategies:
                selected_strategy = st.selectbox("Select a strategy", options=all_strategies, format_func=lambda x: all_evaluations[x]['strategy'])
                df_strategy = df[df['strategy'] == all_evaluations[selected_strategy]['strategy']]
                if not df_strategy.empty:
                    pivot = df_strategy.pivot_table(index='category', columns='difficulty', values='correct', aggfunc='mean') * 100
                    pivot = pivot.reindex(columns=['easy', 'medium', 'hard'])
                    fig = px.imshow(pivot, text_auto='.1f', aspect="auto", color_continuous_scale='RdYlGn', range_color=[0, 100], labels=dict(x="Difficulty", y="Category", color="Accuracy (%)"), title=f"Accuracy Heatmap for '{all_evaluations[selected_strategy]['strategy']}'")
                    fig.update_traces(texttemplate="%{z:.1f}%"); st.plotly_chart(fig, use_container_width=True)

# --- Main App Logic ---
initialize_state()
st.sidebar.title("CypherGen-Eval")
st.sidebar.markdown("A tool to evaluate LLM performance on Text-to-Cypher tasks.")
PAGES = {"🏠 Dashboard Overview": render_dashboard, "🗃️ Test Case Management": render_test_case_management, "⚙️ Configuration": render_configuration, "🚀 Run Evaluation": render_run_evaluation, "📊 Results Analysis": render_results_analysis}
selection = st.sidebar.radio("Navigation", list(PAGES.keys()))
if selection:
    page = PAGES[selection]
    page()
st.sidebar.markdown("---")
st.sidebar.info("v2.3 - Robustness Update")