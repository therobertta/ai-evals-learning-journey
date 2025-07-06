# Claude Code Best Practices for AI-Native Development

## Executive Summary
This document establishes best practices for using Claude Code as an AI-native developer, combining systematic evaluation methodologies from your AI evals course with advanced Claude Code techniques to build production-ready AI systems.

## Core Philosophy: Evaluation-Driven Development

### The AI-Native Mindset
**Traditional Development**: Code → Test → Deploy
**AI-Native Development**: Evaluate → Analyze → Measure → Improve → Deploy

**Key Principle**: Every AI system starts with defining "good" behavior before implementation.

## Claude Code Mastery Framework

### 1. Systematic Codebase Navigation

#### Pattern: Concurrent Information Gathering
```bash
# GOOD: Parallel exploration
<function_calls>
<invoke name="Glob">
<parameter name="pattern">homeworks/hw2/**/*