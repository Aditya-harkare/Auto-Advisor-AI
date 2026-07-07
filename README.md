# 🚗 AutoAdvisor AI

> An Agentic AI-powered automobile purchase consultant that recommends the most suitable vehicle based on user requirements using a multi-agent workflow built with LangGraph.

---

## Overview

Buying a car involves balancing multiple factors such as:

- Budget
- Performance
- Reliability
- Safety
- Comfort
- Fuel efficiency
- Family requirements

Instead of relying on a single LLM prompt, AutoAdvisor AI decomposes the problem into multiple specialized AI agents, each responsible for one stage of the decision-making process.

This modular architecture improves reasoning quality, transparency, maintainability, and scalability.

---

## Features

- Multi-agent workflow using LangGraph
- Intelligent requirement extraction
- Repository-based vehicle filtering
- LLM-powered candidate selection
- Comparative vehicle evaluation
- Final recommendation with reasoning
- Personalized ownership & purchase advisory
- Structured outputs using Pydantic
- Automatic retry mechanism with exponential backoff
- Rich terminal report generation

---

## Workflow

User Query
↓
Requirement Agent
↓
Vehicle Repository
↓
Candidate Selection Agent
↓
Evaluation Agent
├──────────────┐
│              │
↓              ↓
Recommendation Purchase Advisory
Agent          Agent
│              │
└───────┬──────┘
        ↓
Response Composer
        ↓
Final Report

---

## Multi-Agent Architecture

### Requirement Agent

Extracts user preferences such as:

- Budget
- Fuel type
- Seating capacity
- Body type
- Priorities
- Transmission

---

### Repository

Filters the complete vehicle database using hard constraints before involving the LLM.

This significantly reduces token usage and improves recommendation quality.

---

### Candidate Selection Agent

Shortlists the most suitable vehicle models for further analysis.

Uses:

- Specifications
- User constraints
- Diversity
- Overall suitability

---

### Evaluation Agent

Performs detailed comparison of shortlisted vehicles.

Evaluates:

- Performance
- Reliability
- Comfort
- Safety
- Practicality
- Ownership suitability

---

### Recommendation Agent

Chooses the best vehicle.

Produces:

- Recommendation summary
- Key reasons
- Trade-offs
- Alternative vehicles

---

### Purchase Advisory Agent

Generates personalized ownership guidance.

Includes:

- Insurance advice
- Financing suggestions
- Delivery checklist
- Ownership tips
- Useful accessories

---

### Response Composer

Combines outputs from multiple agents into a single consultation report.

---

## Failure Handling

The project includes a retry middleware.

Features:

- Automatic retries
- Exponential backoff
- Validation-aware retries
- Structured output validation
- Graceful failure handling

---

## Tech Stack

Python

LangGraph

LangChain

Gemini / Groq

Pydantic

Pandas

Rich

dotenv

---

## Project Structure

```
AutoAdvisor-AI/

agents/
graph/
schemas/
utils/

main.py
```

---

## Installation

```bash
git clone <repository-url>

cd AutoAdvisor-AI

python -m venv .venv

source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file

```env
GOOGLE_API_KEY=your_key

# or

GROQ_API_KEY=your_key
```

---

## Run

```bash
python main.py
```

---

## Example Query

```
Budget 18 lakh

Automatic petrol SUV

Family of five

Reliability is top priority
```

---

## Example Recommendation

Toyota Urban Cruiser Hyryder

Reasons

- Excellent reliability
- Strong resale value
- Spacious cabin
- Fuel efficient
- Wide service network

Trade-offs

- Average performance
- Standard warranty

---

## Why Multi-Agent Instead of a Single LLM?

A single LLM prompt must perform every task simultaneously:

- Understand requirements
- Search candidates
- Compare vehicles
- Evaluate trade-offs
- Recommend a car
- Generate ownership advice

AutoAdvisor AI decomposes the problem into specialized agents, making the reasoning process more transparent, scalable, and easier to maintain.

---

## Future Improvements

- Streamlit Web UI
- Conversation memory
- Live vehicle pricing APIs
- RAG-based automobile knowledge base
- Multi-language support
- Voice assistant integration

---

## License

MIT License