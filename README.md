GrowthOS 🚀
Autonomous AI Growth & Agentic Commerce Platform
GrowthOS is an AI-powered growth engine designed to identify customer
purchase opportunities, decide what growth action should be taken,
execute that action, measure the business outcome, and learn from
historical performance.

Core stack
React + Vite frontend

Python + FastAPI backend

PostgreSQL database

SQLAlchemy ORM

AI growth agent

Opportunity detection

Decision engine

Growth action execution

Outcome analytics

Strategy learning

Project status: Core GrowthOS engine and dashboard are implemented
and pushed to GitHub. Production deployment is the next stage.

1. What is GrowthOS?
GrowthOS is designed to make e-commerce growth proactive instead of
purely reactive.

It analyzes customer behavior such as product views and cart activity,
calculates purchase intent, detects growth opportunities, selects a
strategy using current intent and historical outcomes, creates a
personalized growth action, records the result, and feeds that result
back into the learning layer.

The central loop is:

Observe → Detect → Decide → Act → Measure → Learn → Act better

Customer behavior
        ↓
Opportunity detection
        ↓
Intent scoring
        ↓
Decision engine
        ↓
AI growth action
        ↓
Execution
        ↓
Outcome + revenue
        ↓
Learning
        ↓
Better future decisions
2. Why GrowthOS?
A business may have many customers showing different levels of buying
intent. Manually analyzing every customer and deciding what action to
take does not scale.

GrowthOS automates that workflow:

Customer behavior
      ↓
GrowthOS detects opportunity
      ↓
GrowthOS decides strategy
      ↓
GrowthOS generates action
      ↓
GrowthOS executes action
      ↓
GrowthOS records outcome
      ↓
GrowthOS learns
3. Main Capabilities
Opportunity Detection
GrowthOS scans customer/product activity and classifies purchase intent
as:

HIGH

MEDIUM

LOW

Example:

Customer: Customer 1
Product: Wireless Headphones
Product views: 8
Product currently in cart: Yes
Intent score: 80
Intent: HIGH
Growth Actions
Examples implemented in the project include:

Personalized cart recovery

Personalized product recommendation

High-intent abandoned-cart recovery

Example message:

Hi Customer 1! You left Wireless Headphones in your cart.
Complete your purchase today and get 10% off for a limited time.
Decision Engine
The current decision logic combines:

Current intent score: 60%

Historical conversion rate: 40%

For a matching historical strategy:

confidence =
    intent_score × 0.6
    +
    historical_conversion_rate × 0.4
Example:

Intent score = 80
Historical conversion rate = 100%

Confidence = 80 × 0.6 + 100 × 0.4
           = 88
Outcome Analytics
The system tracks:

Total actions

Total outcomes

Conversions

Conversion rate

Revenue generated

Average revenue per conversion

Strategy performance

Strategy Learning
GrowthOS groups historical outcomes by strategy and calculates:

Total outcomes
Conversions
Conversion rate
Revenue
The learning layer exposes the best-performing historical strategy.

4. Complete Architecture
flowchart TB
    UI[React Frontend]
    API[FastAPI Backend]
    DB[(PostgreSQL)]
    AI[AI Growth Agent]

    OP[Opportunity Engine]
    DEC[Decision Engine]
    ACT[Growth Action Engine]
    OUT[Outcome Analytics]
    LEARN[Learning Engine]

    UI --> API
    API --> OP
    API --> DEC
    API --> ACT
    API --> OUT
    API --> LEARN

    OP --> DB
    DEC --> DB
    ACT --> DB
    OUT --> DB
    LEARN --> DB

    DEC --> AI
    AI --> ACT
5. Full GrowthOS Flow
flowchart TD
    A[Customer Activity] --> B[PostgreSQL Database]
    B --> C[Opportunity Engine]
    C --> D{Purchase Intent}

    D -->|HIGH| E[High Priority]
    D -->|MEDIUM| F[Medium Priority]
    D -->|LOW| G[Low Priority]

    E --> H[Decision Engine]
    F --> H
    G --> H

    H --> I[Historical Strategy Analysis]
    I --> J[Recommended Strategy]
    J --> K[AI Growth Agent]
    K --> L[Generate Growth Action]
    L --> M[Action Pipeline]

    M --> N{Execute Action}
    N -->|Success| O[Outcome]
    N -->|Failure| P[Failed Execution]

    O --> Q{Customer Converts?}
    Q -->|YES| R[Revenue Generated]
    Q -->|NO| S[No Conversion]

    R --> T[Learning Engine]
    S --> T
    P --> T

    T --> U[Strategy Performance]
    U --> H
6. Database Architecture
Main entities:

users
products
browsing_events
cart_items
orders
order_items
growth_actions
action_outcomes
action_logs
erDiagram
    USERS ||--o{ BROWSING_EVENTS : performs
    PRODUCTS ||--o{ BROWSING_EVENTS : receives

    USERS ||--o{ CART_ITEMS : owns
    PRODUCTS ||--o{ CART_ITEMS : contains

    USERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : purchased

    GROWTH_ACTIONS ||--o{ ACTION_OUTCOMES : produces
    GROWTH_ACTIONS ||--o{ ACTION_LOGS : records

    PRODUCTS ||--o{ GROWTH_ACTIONS : targets
    USERS ||--o{ GROWTH_ACTIONS : targets
Models
User

id
name
email
created_at
Product

id
name
category
description
price
stock
rating
image_url
BrowsingEvent

id
user_id
product_id
event_type
created_at
CartItem

id
user_id
product_id
quantity
created_at
Order

id
user_id
total_amount
status
created_at
OrderItem

id
order_id
product_id
quantity
price
GrowthAction

Stores an AI-generated action targeted at a customer/product
opportunity.

ActionOutcome

Stores the result of an executed action, including conversion and
generated revenue.

ActionLog

Stores execution-related action information.

7. Project Structure
GrowthOS/
│
├── Backend/
│   ├── .env.example
│   ├── requirements.txt
│   ├── seed.py
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       │
│       ├── actions/
│       │   ├── __init__.py
│       │   └── growth_actions.py
│       │
│       ├── agents/
│       │   └── growth_agent.py
│       │
│       ├── models/
│       │   ├── user.py
│       │   ├── product.py
│       │   ├── cart.py
│       │   ├── event.py
│       │   ├── order.py
│       │   ├── order_item.py
│       │   ├── growth_action.py
│       │   ├── action_outcome.py
│       │   └── action_log.py
│       │
│       ├── routes/
│       │   ├── opportunities.py
│       │   ├── agent.py
│       │   ├── actions.py
│       │   ├── decision.py
│       │   ├── learning.py
│       │   ├── dashboard.py
│       │   └── auto_growth.py
│       │
│       └── services/
│           ├── opportunity_service.py
│           ├── decision_service.py
│           └── learning_service.py
│
└── Frontend/
    └── src/
        ├── App.jsx
        └── App.css
8. API Architecture
Current API route groups:

/opportunities
/agent
/actions
/learning
/dashboard
/decision
/auto_growth
FastAPI interactive documentation:

http://127.0.0.1:8000/docs
Root
GET /
Example:

{
  "project": "GrowthOS",
  "message": "Autonomous AI Growth Engine is running 🚀"
}
Health
GET /health
Example:

{
  "status": "healthy",
  "database": "connected"
}
Growth Decision
GET /decision/{user_id}/{product_id}
Example:

GET /decision/1/1
Example result:

{
  "success": true,
  "decision": {
    "customer": "Customer 1",
    "product": "Wireless Headphones",
    "intent_score": 80,
    "intent": "HIGH",
    "opportunity_type": "Send personalized cart recovery offer",
    "recommended_strategy": "Cart Recovery",
    "confidence": 88,
    "historical_conversion_rate": 100,
    "reason": "Cart Recovery matches the current growth opportunity and has a historical conversion rate of 100.0%.",
    "recommended_action": "Send personalized cart recovery offer"
  }
}
9. Decision Engine Flow
flowchart TD
    A[Request user_id + product_id]
    --> B[Calculate Current Opportunities]

    B --> C{Opportunity Found?}

    C -->|No| D[Return 404]
    C -->|Yes| E[Load Historical Outcomes]

    E --> F[Group Outcomes by Strategy]
    F --> G[Calculate Historical Conversion Rate]
    G --> H[Read Current Intent Score]

    H --> I{Matching Historical Strategy?}

    I -->|Yes| J[Intent 60% + Historical 40%]
    I -->|No| K[Intent-Based Confidence]

    J --> L[Recommend Historical Strategy]
    K --> M[Recommend Current Opportunity Action]

    L --> N[Return Decision]
    M --> N
10. Learning Engine
flowchart TD
    A[Growth Actions]
    B[Action Outcomes]

    A --> C[Count Total Actions]
    B --> D[Count Total Outcomes]
    B --> E[Count Conversions]
    B --> F[Sum Revenue]

    D --> G[Conversion Rate]
    E --> G

    F --> H[Average Revenue per Conversion]
    E --> H

    A --> I[Group by Strategy]
    B --> I

    I --> J[Strategy Performance]
    J --> K[Best Strategy]

    C --> L[Learning Insights]
    G --> L
    H --> L
    J --> L
    K --> L
Current formulas:

conversion_rate =
    total_conversions / total_outcomes × 100

average_revenue_per_conversion =
    total_revenue / total_conversions
11. Action Lifecycle
stateDiagram-v2
    [*] --> Detected
    Detected --> Classified
    Classified --> ReadyForDecision
    ReadyForDecision --> StrategySelected
    StrategySelected --> ActionCreated
    ActionCreated --> Ready
    Ready --> Executing
    Executing --> Completed
    Executing --> Failed
    Completed --> Converted
    Completed --> NoConversion
    Converted --> Learning
    NoConversion --> Learning
    Failed --> Learning
    Learning --> FutureDecision
12. Example End-to-End Customer Journey
Customer 1
    ↓
Views Wireless Headphones 8 times
    ↓
Product is in cart
    ↓
Opportunity detected
    ↓
Intent score = 80
    ↓
Intent = HIGH
    ↓
Decision Engine
    ↓
Historical Cart Recovery performance = 100%
    ↓
Confidence = 88
    ↓
Cart Recovery selected
    ↓
AI generates personalized message
    ↓
Action enters execution pipeline
    ↓
Customer converts or does not convert
    ↓
Outcome recorded
    ↓
Revenue recorded when applicable
    ↓
Learning Engine
    ↓
Historical strategy performance updated
13. Dashboard
The GrowthOS dashboard provides a single view of the growth engine.

It includes:

Growth overview

Opportunities

Growth actions

Outcome analytics

Strategy learning

Conversion statistics

Revenue statistics

Action execution pipeline

Example development dataset:

Opportunities:       105
High intent:           2
Medium intent:         1
Low intent:          102

Growth actions:       21
Ready:                12
Executing:             1
Completed:             6
Failed:                2

Outcomes:              4
Conversions:           4
Conversion rate:     100%
Revenue generated: ₹64,996
These are development/demo results, not guaranteed production
performance.

14. AI Agent
The AI agent is located at:

Backend/app/agents/growth_agent.py
The project is configured to use a Gemini API key through:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
Never commit the real API key.

15. Local Setup
Requirements
Install:

Python

PostgreSQL

Node.js

npm

Git

Clone
git clone https://github.com/akshay-9191-git/GROWTHOS.git
cd GROWTHOS
Backend
cd Backend
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
Environment
Create:

Backend/.env
Example:

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:8543/growthos
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
PostgreSQL
Create a PostgreSQL database named:

growthos
The current development configuration uses port:

8543
Update the connection string for your own environment.

Seed data
From the backend directory:

python seed.py
Start backend
uvicorn app.main:app --reload
Backend:

http://127.0.0.1:8000
Docs:

http://127.0.0.1:8000/docs
Start frontend
Open another terminal:

cd GrowthOS\Frontend
npm install
npm run dev
Vite will show the frontend URL, commonly:

http://localhost:5173
16. Run the Full System
Terminal 1:

cd GrowthOS\Backend
.venv\Scriptsctivate
uvicorn app.main:app --reload
Terminal 2:

cd GrowthOS\Frontend
npm run dev
Then:

Browser
   ↓
React Frontend
   ↓
FastAPI
   ↓
GrowthOS Services
   ↓
PostgreSQL
17. Testing
Open:

http://127.0.0.1:8000/docs
Use Swagger UI to test the API.

Example:

GET /health
and:

GET /decision/1/1
18. Security
Never commit:

Backend/.env
Never expose:

GEMINI_API_KEY
DATABASE_URL
Database passwords
API tokens
Use:

Backend/.env.example
as the safe configuration template.

If credentials are accidentally committed, rotate/revoke them
immediately and remove them from repository history.

19. Git Workflow
git status
git add .
git commit -m "Describe your change"
git push
Before committing, verify that secrets are not included.

The repository is:

https://github.com/akshay-9191-git/GROWTHOS

20. Production Architecture
The intended production architecture can evolve toward:

flowchart TB
    USER[Customer / Business User]
    WEB[Production React App]
    API[Production FastAPI]
    DB[(Managed PostgreSQL)]
    AI[AI Provider]
    WORKER[Background Workers]
    MSG[Messaging / Commerce Integrations]
    MON[Monitoring]

    USER --> WEB
    WEB --> API
    API --> DB
    API --> AI
    API --> WORKER
    WORKER --> MSG
    WORKER --> DB
    API --> MON
    WORKER --> MON
Production deployment is a separate stage from the current local
development setup.

21. Future Evolution
Potential future engineering work includes:

More growth strategies

Better intent scoring

More sophisticated strategy ranking

Real email/SMS/WhatsApp integrations

Real-time event ingestion

Scheduled autonomous campaigns

A/B testing

Customer segmentation

Budget-aware incentives

Outreach frequency limits

Authentication and role-based access

Managed production PostgreSQL

Background job processing

Observability and monitoring

Deployment automation

More advanced AI decision-making

Strategy experimentation and optimization

These are future extensions, not claims about the current
implementation.

22. Design Philosophy
GrowthOS is built around an agentic loop:

SENSE
  ↓
THINK
  ↓
ACT
  ↓
MEASURE
  ↓
LEARN
  ↓
REPEAT
SENSE --- Understand customer behavior.

THINK --- Determine purchase intent and choose a strategy.

ACT --- Generate and execute a personalized growth action.

MEASURE --- Track conversion and revenue.

LEARN --- Use historical performance to influence future decisions.

REPEAT --- Continuously identify and act on new opportunities.

23. Current Limitations
This is a development-stage system.

Current implementation includes simplified components:

Historical strategy matching is based on strategy naming/type.

Decision confidence is rule-based.

The learning dataset is relatively small.

Action execution is represented through the project's action
pipeline rather than a full production messaging network.

PostgreSQL is currently configured for local development.

Production authentication, queues, observability, and deployment
infrastructure are not yet the focus of this stage.

These limitations define clear areas for future engineering work.

24. Contributing
Fork the repository.

Create a feature branch.

Make your changes.

Test backend and frontend.

Do not commit secrets.

Commit your changes.

Push the branch.

Open a pull request.

Example:

git checkout -b feature/new-growth-strategy
git add .
git commit -m "Add new growth strategy"
git push origin feature/new-growth-strategy
25. License
Add the project's chosen license before enabling external contribution.

26. Project
GrowthOS --- Autonomous AI Growth & Agentic Commerce Platform

GitHub:

https://github.com/akshay-9191-git/GROWTHOS

Core concept
Customer Behavior
       ↓
Opportunity Detection
       ↓
Intent Scoring
       ↓
Decision Engine
       ↓
AI Growth Agent
       ↓
Growth Action
       ↓
Execution
       ↓
Outcome
       ↓
Conversion + Revenue
       ↓
Learning
       ↓
Better Strategy
       ↺
GrowthOS --- Sense. Decide. Act. Measure. Learn. Grow. 🚀

