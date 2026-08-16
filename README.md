# ScoutAgent Pro ⚽🛡️

AI-powered football scouting platform built for the Google Agent Development Kit Hackathon.

## Overview

ScoutAgent Pro is a multi-agent football scouting system that combines:

* Gemini-powered planning and reasoning
* MongoDB Atlas player database
* Streamlit analytics dashboard
* Transfer recommendation workflows
* Player comparison and scouting tools
* Agent activity tracing and memory

The platform helps clubs identify talent, compare players, build squads, and generate transfer recommendations using autonomous agent workflows.

---

## Features

### Scout

Search football players from a MongoDB database using:

* Position
* Age
* Rating
* Nationality
* Value filters

### Compare

Compare two players side-by-side using:

* Core attributes
* Ratings
* Strengths and weaknesses
* Statistical profiles

### Agent Planner

Natural language football scouting assistant.

Examples:

* Find a young Brazilian striker under €20M
* Recommend replacements for Harry Kane
* Show top U23 midfielders in Europe

The planner:

1. Understands user intent
2. Selects tools
3. Queries MongoDB
4. Synthesizes scouting recommendations

### Agent Activity

Displays:

* Planner reasoning
* Tool calls
* Retrieved data
* Agent execution traces

### Transfer Strategy

Generates transfer recommendations using:

* Club profile
* Budget
* Tactical style
* Squad requirements

### Squad Builder

Interactive squad planning tool powered by real player data.

### Memory Center

Stores scouting history and agent reasoning for future sessions.

---

## Architecture

Frontend (Streamlit)

↓

Backend Adapter

↓

Planner Agent (Gemini)

↓

Tool Layer

↓

MongoDB Atlas

---

## Tech Stack

### Frontend

* Streamlit
* Plotly
* Python

### Backend

* FastAPI
* Python

### AI

* Google Gemini

### Database

* MongoDB Atlas

---

## Project Structure

backend/

* agents/
* db/
* memory/
* tools/
* app.py

frontend/

* pages/
* services/
* state/
* visualizations/
* app.py

---

## Setup

### Clone

git clone https://github.com/abhinav0singh/scout-agent.git

cd scout-agent

### Install

pip install -r backend/requirements.txt

### Environment Variables

Create:

backend/.env

Add:

GEMINI_API_KEY=YOUR_KEY

MONGODB_URI=YOUR_URI

### Run Frontend

streamlit run frontend/app.py

---

## Demo Flow

1. Dashboard
2. Scout Players
3. Compare Players
4. Ask Agent
5. View Agent Trace
6. Transfer Strategy
7. Squad Builder
8. Memory Center

---

## Hackathon Submission

Built for the Google Agent Development Kit Hackathon.

Focus Areas:

* Agent Planning
* Tool Use
* Memory
* Reasoning
* Multi-Agent Architecture
* Real Football Data
