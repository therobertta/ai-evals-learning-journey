# AI Evals Learning Framework: From Theory to Practice

## Overview
This document provides a comprehensive learning framework for AI-native development using the **Analyze-Measure-Improve** lifecycle, grounded in your AI evals course curriculum and applied to the Recipe Chatbot project.

## Core Conceptual Framework

### Three Gulfs Model of LLM Development
The fundamental challenges in building effective LLM pipelines:

1. **Gulf of Comprehension** (Developer ↔ Data)
   - Understanding diverse input data patterns
   - Recognizing LLM behavior and failure modes
   - Challenge: Cannot manually review every input/output
   - **HW2 Focus**: Error analysis addresses this gulf

2. **Gulf of Specification** (Developer ↔ LLM Pipeline)
   - Translating intent into precise instructions (prompts)
   - Managing natural language ambiguity
   - Challenge: LLMs need explicit details
   - **Recipe Bot Example**: "Easy" needs definition (quick ingredients? few steps? simple techniques?)

3. **Gulf of Generalization** (Data ↔ LLM Pipeline)
   - Ensuring consistent behavior across inputs
   - Understanding foundation model capabilities
   - Challenge: LLMs fail on novel/unusual inputs
   - **Solution**: Systematic evaluation and improvement

### Analyze-Measure-Improve Lifecycle

#### 1. ANALYZE Phase
**Goal**: Understand failure modes through systematic error analysis

**HW2 Implementation**:
- **Open Coding**: Review interaction traces, assign descriptive labels without preconceived categories
- **Axial Coding**: Group observations into broader failure mode categories
- **Taxonomy Creation**: Structure failure modes with:
  - Clear title
  - Concise one-sentence definition
  - 1-2 illustrative examples from actual bot behavior

**Common Pitfalls**:
- Premature improvement
- Not examining enough examples
- Outsourcing annotation without understanding

#### 2. MEASURE Phase
**Goal**: Translate qualitative insights into quantitative metrics

**Key Decision**: Specification vs. Generalization Failures
- **Specification Failures**: Fix prompt first, don't build evaluators yet
- **Generalization Failures**: Prime candidates for automated evaluators

**HW3 Implementation - LLM-as-Judge**:
1. **Prompt Template Design** (4 components):
   - Clear task & evaluation criterion
   - Precise Pass/Fail definitions
   - Few-shot examples (2-3 pass, 2-3 fail)
   - Structured output format (JSON)

2. **Data Splitting Strategy**:
   - Training Set (10-20%): Examples for prompt few-shots
   - Dev Set (40%): Iterative prompt refinement
   - Test Set (40%): Final unbiased evaluation

3. **Validation Process**:
   - Target >80% TPR (True Positive Rate) and TNR (True Negative Rate)
   - Iterative prompt refinement based on dev set performance
   - Never include dev/test examples in prompt

4. **Bias Correction**:
   - Estimate true success rate: θ̂ = (p_obs + TNR - 1) / (TPR + TNR - 1)
   - Calculate 95% confidence intervals using bootstrap method
   - Account for judge imperfections in production metrics

#### 3. IMPROVE Phase
**Goal**: Refine prompts, models, and architecture based on analysis

**Systematic Approach**:
- Address specification failures first (prompt improvements)
- Use evaluation metrics to guide generalization improvements
- Continuous monitoring and iteration

## Architecture-Specific Evaluation Patterns

### RAG (Retrieval-Augmented Generation) - HW4
**Evaluation Strategy**: Separate retrieval and generation quality

**Retrieval Metrics**:
- Recall@k: Coverage of relevant information
- Precision@k: Accuracy of retrieved chunks
- MRR (Mean Reciprocal Rank): Speed of finding relevant info
- NDCG@k: Graded relevance ranking

**Generation Metrics** (ARES framework):
- **Answer Faithfulness**: Accurate reflection of retrieved context
- **Answer Relevance**: Direct relevance to original query

**Synthetic Data Generation**:
1. Chunk-level fact identification
2. Realistic query generation
3. Adversarial query creation (using similar chunks)
4. Quality filtering with LLM assistance

### Tool Calling Systems
**Evaluation Components**:
- Tool Selection: Correct tool for intent
- Argument Generation: Structural and semantic validity
- Execution Success: Runtime and silent failure detection
- Output Handling: Proper integration of tool responses

### Agentic Systems
**Agency Spectrum Definition**:
- High Agency: Independent problem-solving
- Medium Agency: Interactive clarification
- Low Agency: Strict instruction following

**Debugging Approach**:
- Comprehensive traceability logging
- Transition failure matrices
- Error attribution analysis

## Human-in-the-Loop Evaluation (Lesson 7)

### Custom Interface Design Principles
**10× Throughput Improvement**:
- Domain-native views (emails look like emails)
- Hotkeys & one-click tags
- Single-trace canvas with collapsible panels
- Progress indicators and batch operations

**Sampling Strategies**:
- Random sampling (20%): Unbiased quality check
- Uncertainty sampling (50%): Edge case detection
- Failure-driven sampling (30%): High-severity issues

**Closed-Loop Automation**:
- "Add to golden set" direct integration
- Automated label export
- Human-LLM disagreement flagging
- One-click prompt improvement

### Criteria Drift Management
**Key Insight**: Reviewers refine standards over time
**Solutions**:
- Editable rubrics and labels
- Versioned prompts and label history
- On-the-fly tag creation
- Real-time criterion refinement

## AI-Native Development Best Practices

### 1. Evaluation-First Development
- Design evaluation metrics before building features
- Use systematic failure analysis to guide improvements
- Build comprehensive test suites with diverse edge cases

### 2. Claude Code Mastery Patterns
- **Concurrent Tool Usage**: Batch operations for efficiency
- **Systematic Debugging**: Comprehensive error analysis
- **Proper Documentation**: Structured information architecture

### 3. Reproducible Workflows
- Version control for prompts and evaluation criteria
- Timestamped results with proper metadata
- Automated pipeline integration

### 4. Iterative Improvement Cycles
- Short feedback loops between analysis and improvement
- Continuous monitoring of production metrics
- Regular evaluation of evaluation systems themselves

## Recipe Bot Project Progression

### HW1: Foundation
- Initial system prompt design
- Role definition and output formatting
- Agency spectrum specification

### HW2: Error Analysis (Current Focus)
- Open and axial coding implementation
- Failure mode taxonomy development
- Qualitative pattern identification

### HW3: Automated Evaluation
- LLM-as-Judge for dietary adherence
- Statistical validation and bias correction
- Production metric estimation

### HW4: RAG Enhancement
- Retrieval evaluation dataset creation
- BM25 baseline performance measurement
- Multi-component pipeline evaluation

### HW5: Advanced Analysis
- Failure mode transition analysis
- Visualization and heatmap generation
- Complex pipeline debugging

## Connection to Epistemic Evals

### Belief-Centric Evaluation Framework
Your course foundation provides the perfect bridge to epistemic evaluation:

**Traditional AI Evals** → **Epistemic Evals**
- Task performance → Belief accuracy
- Output quality → Epistemic reliability
- Failure modes → Belief distortions
- Human alignment → Epistemic alignment

**Key Adaptation Areas**:
1. **Belief State Modeling**: Tracking agent beliefs vs. ground truth
2. **Epistemic Uncertainty**: Measuring confidence calibration
3. **Belief Update Mechanisms**: Evaluating learning from evidence
4. **Meta-Cognitive Monitoring**: Self-awareness of knowledge limitations

## Next Steps for Implementation

1. **Complete HW2**: Perfect your error analysis methodology
2. **Apply Framework**: Use this document as your reference guide
3. **Document Learnings**: Build your own evaluation cookbook
4. **Bridge to Epistemic**: Adapt patterns for belief-centric evaluation
5. **Scale Practices**: Apply to production systems

## Tools and Resources

### Essential Libraries
- `judgy`: LLM-as-Judge evaluation framework
- `litellm`: Model-agnostic LLM interface
- `rank-bm25`: Retrieval evaluation
- `rich`, `tqdm`: Enhanced CLI experience

### Evaluation Platforms
- Custom interfaces with Streamlit/Gradio
- EvalGen for rubric-based evaluation
- DocWrangler for document-level pipelines

### Statistical Tools
- Bootstrap confidence intervals
- TPR/TNR calculation and correction
- Bias-corrected success rate estimation

This framework provides the foundation for becoming an AI-native developer while mastering the systematic evaluation methodologies that will serve you throughout your career in AI development.