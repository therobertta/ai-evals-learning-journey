# Open Coding Web Interface Usage Guide

## Overview
This web interface allows SMEs to perform systematic open coding analysis on the 250 Recipe Bot traces generated for HW2.

## Features
- **Trace Navigation**: Browse through all 250 traces with Previous/Next buttons or direct selection
- **Failure Mode Annotation**: Check off applicable failure modes from the predefined taxonomy
- **Open Coding Notes**: Add detailed qualitative observations and insights
- **Progress Tracking**: Visual progress bar showing completion percentage
- **Auto-save**: Annotations are automatically saved when you click "Save Annotation"
- **CSV Export**: Export all annotations to CSV format matching the error analysis template

## How to Use

### 1. Start the Application
```bash
uvicorn backend.main:app --reload
```

### 2. Access the Interface
- Open your browser to `http://127.0.0.1:8000/coding`
- The interface will load all 250 traces automatically

### 3. Annotate Traces
1. **Review the trace**: Read the user query and bot response
2. **Check failure modes**: Select applicable failure modes from the 8 predefined categories
3. **Add open coding notes**: Write qualitative observations, patterns, and insights
4. **Save**: Click "Save Annotation" to store your work
5. **Navigate**: Use Previous/Next buttons or dropdown to move between traces

### 4. Export Results
- Click "Export to CSV" to download all annotations
- The CSV format matches the `error_analysis_template.csv` structure

## Failure Modes
The interface includes the 8 failure modes from the taxonomy:
1. **Missing Serving Size** - Bot fails to specify servings/portions
2. **Overcomplicated Simple Recipes** - Too many ingredients/steps for simple requests
3. **Inconsistent Time Estimates** - Doesn't match requested time constraints
4. **Missing Dietary Restriction Info** - Fails to address dietary restrictions properly
5. **Incomplete Ingredient Substitutions** - No alternatives provided
6. **Inconsistent Recipe Formatting** - Mixed measurements/formatting issues
7. **Missing Equipment Requirements** - Assumes specific tools without alternatives
8. **Inadequate Safety Information** - Missing temperature/safety guidelines

## Data Storage
- Annotations are stored in `homeworks/hw2/annotations.json`
- Progress is automatically tracked and displayed
- Data persists between sessions

## Tips for Effective Open Coding
1. **Be Descriptive**: Use detailed notes to capture nuanced observations
2. **Look for Patterns**: Note recurring issues across multiple traces
3. **Consider Context**: Evaluate responses based on the specific user query
4. **Stay Objective**: Focus on observable behaviors rather than assumptions
5. **Document Edge Cases**: Note unusual or particularly good/bad examples

## Troubleshooting
- If traces don't load, ensure the CSV file exists at `homeworks/hw2/hw2_bot_traces_20250613.csv`
- Refresh the page if you encounter loading issues
- Check browser console for any JavaScript errors