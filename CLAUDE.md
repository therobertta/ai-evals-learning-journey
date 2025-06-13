# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a Recipe Chatbot system built for the AI Evals course. It serves as a foundation for learning AI evaluation techniques through incrementally added features across multiple homework assignments.

### Core Components

- **FastAPI Backend** (`backend/`): REST API serving the chat interface and agent logic
- **Frontend** (`frontend/`): Simple HTML/CSS/JS chat interface with Markdown rendering
- **LLM Integration**: Uses LiteLLM for model-agnostic LLM interactions
- **Retrieval System**: BM25-based recipe retrieval with query rewriting capabilities
- **Evaluation Framework**: Comprehensive evaluation utilities for measuring system performance

### Key Architecture Patterns

- **RAG Pipeline**: Query rewrite → BM25 retrieval → LLM generation
- **Evaluation-First Development**: Each feature includes comprehensive evaluation metrics
- **Modular Design**: Each homework assignment builds upon previous components
- **Concurrent Processing**: Parallel query processing and batch evaluation capabilities

## Development Commands

### Running the Application

```bash
# Start the web application (FastAPI + Frontend)
uvicorn backend.main:app --reload

# Access the chat interface at http://127.0.0.1:8000
```

### Testing and Evaluation

```bash
# Bulk test against query dataset
python scripts/bulk_test.py

# Custom CSV file for testing
python scripts/bulk_test.py --csv path/to/queries.csv

# Run retrieval evaluation (HW4)
python homeworks/hw4/scripts/evaluate_retrieval.py

# Generate synthetic queries for evaluation
python homeworks/hw4/scripts/generate_queries.py

# Evaluate with query rewriting agent
python homeworks/hw4/scripts/evaluate_retrieval_with_agent.py
```

### Data Processing

```bash
# Process raw recipe data (HW4)
python homeworks/hw4/scripts/process_recipes.py

# Generate failure analysis traces (HW5)
python homeworks/hw5/scripts/generate_failure_traces.py

# Analyze failure mode transitions
python homeworks/hw5/scripts/analyze_failure_traces.py
```

### Homework-Specific Commands

```bash
# HW3: LLM-as-Judge evaluation
python homeworks/hw3/scripts/develop_judge.py
python homeworks/hw3/scripts/evaluate_judge.py
python homeworks/hw3/scripts/run_full_evaluation.py

# HW5: Failure analysis with visualizations
python homeworks/hw5/analysis/transition_heatmaps.py
```

## Key Configuration

### Environment Setup

1. Create `.env` file from `env.example`
2. Set `MODEL_NAME` with provider prefix (e.g., `openai/gpt-4o-mini`, `anthropic/claude-3-haiku`)
3. Set corresponding API key (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)

### System Prompt Location

- Main system prompt: `backend/utils.py` → `SYSTEM_PROMPT` constant
- Must be crafted for recipe-specific responses with proper Markdown formatting

## Evaluation Framework

### Core Evaluation Classes

- `BaseRetrievalEvaluator` (`backend/evaluation_utils.py`): Standard IR metrics (Recall@k, MRR)
- `QueryRewriteAgent` (`backend/query_rewrite_agent.py`): LLM-powered query optimization
- `RecipeRetriever` (`backend/retrieval.py`): BM25 indexing and search

### Evaluation Patterns

All major features follow this evaluation approach:
1. Generate synthetic test data with LLM
2. Implement baseline system
3. Measure performance with standard metrics
4. Enhance system (query rewriting, better prompts, etc.)
5. Compare systems and analyze improvements

### Results Storage

- Bulk test results: `results/` directory with timestamped CSV files
- Homework results: `homeworks/hwN/results/` with JSON evaluation outputs
- Visualizations: `homeworks/hwN/results/visualizations/` for charts and heatmaps

## Project Structure Conventions

- **Homework Isolation**: Each `homeworks/hwN/` is self-contained with its own scripts, data, and results
- **Shared Backend**: Core functionality in `backend/` is shared across all assignments
- **Data Management**: Raw data stays in homework directories, processed data gets versioned
- **Concurrent Processing**: Use ThreadPoolExecutor for batch operations (query processing, evaluation)

## Development Notes

### Query Processing Pipeline

1. **Original Query** → **Query Rewrite Agent** → **Enhanced Query**
2. **Enhanced Query** → **BM25 Retrieval** → **Top-K Recipes**
3. **Recipes + Query** → **LLM Generation** → **Final Response**

### Testing Philosophy

- Generate realistic edge cases with LLM assistance
- Measure both retrieval quality (Recall@k) and response quality (LLM-as-Judge)
- Compare systems statistically with proper evaluation methodology
- Focus on specific failure modes (dietary adherence, cooking accuracy, etc.)

### Code Style

- Use type hints consistently
- Parallel processing with `ThreadPoolExecutor` and `tqdm` progress bars
- Rich console output for better development experience
- Comprehensive error handling with fallbacks

## Dependencies

Key libraries used across the project:
- `fastapi`, `uvicorn`: Web framework
- `litellm`: Model-agnostic LLM interface
- `rank-bm25`: BM25 retrieval implementation
- `judgy`: LLM-as-Judge evaluation framework
- `rich`, `tqdm`: Enhanced CLI experience
- `pandas`, `numpy`: Data processing
- `matplotlib`, `seaborn`: Visualization