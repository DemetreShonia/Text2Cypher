# 🤖 Text2Cypher: Claude Opus 4.0 Evaluation Framework

> **Bachelor Thesis Project** - Evaluating Claude Opus 4.0's Performance in Natural Language to Cypher Query Translation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0+-green.svg)](https://neo4j.com)
[![Claude](https://img.shields.io/badge/Claude-Opus%204.0-orange.svg)](https://anthropic.com)

## 📋 Overview

Text2Cypher is a comprehensive evaluation framework designed to assess Claude Opus 4.0's capabilities in translating natural language queries to Neo4j Cypher queries. This bachelor thesis project evaluates the model's performance across 100 carefully crafted test cases, examining both retrieval-augmented and non-retrieval approaches.

## 🎯 Project Goals

- **Evaluate Claude Opus 4.0** performance in NL-to-Cypher translation
- **Compare retrieval vs non-retrieval strategies** for query generation
- **Assess semantic accuracy** across different query complexity levels
- **Generate comprehensive metrics** for academic evaluation
- **Provide interactive tools** for test case management and analysis

## 🏗️ Architecture

The project consists of four specialized applications, each serving a distinct purpose in the evaluation pipeline:

### 📊 **Benchmark Application** (`app-benchmark/`)

The core evaluation engine that runs comprehensive tests on Claude Opus 4.0.

**Key Features:**

- Automated test case execution with 100 curated scenarios
- Support for both retrieval-augmented and non-retrieval strategies
- Real-time Neo4j query execution and result validation
- Comprehensive metrics calculation (accuracy, syntax correctness, execution success)
- Interactive dashboard with detailed analytics and visualizations
- Export capabilities for CSV and Markdown reports

**Technologies:** Streamlit, Anthropic API, Neo4j, Plotly, Pandas

### 🗄️ **Data Generator** (`app-data-generator/`)

Creates realistic graph data for testing and evaluation scenarios.

**Key Features:**

- Generates multi-generational family trees with complex relationships
- Creates educational and professional networks
- Produces location-based data with geographical relationships
- Supports both simple and detailed schema configurations
- Exports Neo4j database dumps for consistent testing

**Technologies:** Faker, Neo4j, Python

### 🔍 **Interactive RAG** (`app-interactive-rag/`)

Interactive tool for testing retrieval-augmented generation with real-time feedback.

**Key Features:**

- Real-time Cypher query generation from natural language
- Schema-aware query construction
- Context retrieval and visualization
- Query history logging and analysis
- Support for custom schema configurations

**Technologies:** Streamlit, LangChain, Google Generative AI, Neo4j

### 📝 **Test Case Manager** (`app-test-case-manager/`)

Web-based interface for creating, managing, and organizing test cases.

**Key Features:**

- Intuitive form-based test case creation
- Category and difficulty classification
- JSON-based expected results validation
- Bulk test case management and editing
- Export capabilities for test case collections

**Technologies:** Streamlit, JSON

## 📈 Evaluation Results

The framework has generated comprehensive evaluation results stored in the `Results/` directory:

### Simple Schema Results

- **Simple-No-Retrieval.csv/md** - Baseline performance without retrieval
- **Simple-Retrieval.csv/md** - Performance with retrieval augmentation

### Detailed Schema Results

- **Detailed-No-Retrieval.csv/md** - Complex schema without retrieval
- **Detailed-Retrieval.csv/md** - Complex schema with retrieval augmentation

Each result file contains:

- Individual test case performance metrics
- Overall accuracy statistics
- Token usage analysis
- Execution success rates
- Detailed error categorization

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Neo4j Database (5.0+)
- Anthropic API Key
- Google Generative AI API Key (for RAG application)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Text2Cypher.git
   cd Text2Cypher
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Neo4j Database**

   ```bash
   # Start Neo4j (adjust credentials as needed)
   # Default: neo4j://localhost:7687
   # Username: neo4j
   # Password: thesis2025
   ```

4. **Generate test data**

   ```bash
   cd app-data-generator
   python data-generator.py
   ```

5. **Run the benchmark application**
   ```bash
   cd app-benchmark
   streamlit run app-final.py
   ```

## 📊 Usage Guide

### Running the Benchmark Evaluation

1. **Configure API Keys**

   - Set your Anthropic API key in the application
   - Configure Neo4j connection parameters

2. **Select Evaluation Strategy**

   - Choose between retrieval-augmented or non-retrieval approaches
   - Select schema complexity (simple vs detailed)

3. **Execute Test Cases**

   - Run all 100 test cases automatically
   - Monitor real-time progress and metrics

4. **Analyze Results**
   - View interactive dashboards and charts
   - Export detailed reports in CSV/Markdown format

### Interactive RAG Testing

1. **Launch the RAG application**

   ```bash
   cd app-interactive-rag
   streamlit run interactive-rag.py
   ```

2. **Configure connections**

   - Set Neo4j database credentials
   - Configure Google Generative AI API

3. **Test queries interactively**
   - Enter natural language queries
   - View generated Cypher queries
   - Examine retrieved context and results

### Managing Test Cases

1. **Launch the test case manager**

   ```bash
   cd app-test-case-manager
   streamlit run testcase-manager.py
   ```

2. **Create new test cases**

   - Fill out the comprehensive form
   - Validate JSON expected results
   - Categorize by difficulty and type

3. **Organize existing cases**
   - Filter by category and difficulty
   - Edit and update test cases
   - Export test case collections

## 🔬 Research Methodology

### Test Case Categories

- **Graph Recursion** - Complex hierarchical queries
- **Filtering** - Conditional data selection
- **Path Finding** - Relationship traversal patterns
- **Aggregation** - Statistical and grouping operations
- **Pattern Matching** - Complex graph pattern recognition

### Difficulty Levels

- **Easy** - Basic queries with simple patterns
- **Medium** - Moderate complexity with multiple relationships
- **Hard** - Complex queries requiring advanced Cypher features

### Evaluation Metrics

- **Semantic Accuracy** - Correctness of query results
- **Syntactic Correctness** - Valid Cypher syntax
- **Execution Success** - Successful database execution
- **Token Usage** - Efficiency analysis
- **Response Time** - Performance benchmarking

## 📚 Academic Context

This project serves as a comprehensive evaluation framework for assessing Large Language Model performance in graph database query generation. The research contributes to:

- **LLM Evaluation Methodologies** - Systematic assessment approaches
- **Graph Database Accessibility** - Natural language interfaces
- **Retrieval-Augmented Generation** - Context-aware query generation
- **Database Query Translation** - NL-to-query conversion accuracy

## 🤝 Contributing

This is a bachelor thesis project, but suggestions and feedback are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍🎓 Authors

This project was built by Demetre Shonia with help of amazing teammates, Nino Sharvashidze and Giorgi Kochiashvili!

**Bachelor Thesis Project** 
_Evaluating Claude Opus 4.0 for Natural Language to Cypher Query Translation_

---

<div align="center">

**Built with ❤️ for academic research**

[![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Database-green)](https://neo4j.com)
[![Claude](https://img.shields.io/badge/Claude-Opus%204.0-orange)](https://anthropic.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)](https://streamlit.io)

</div>
