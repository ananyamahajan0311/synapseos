**# SynapseOS – AI Operating System**



**SynapseOS is a full-stack AI-powered operating system that allows users to interact with multiple digital services through natural-language commands.**



**Instead of manually opening different applications, users can give a single instruction and SynapseOS determines which tools are required, creates an execution plan, and performs the requested actions.**



**## 🚀 Key Features**



**- Natural-language command processing**

**- AI-powered task planning using Google Gemini**

**- Planner–Executor agent architecture**

**- Gmail integration**

&#x20; **- Read emails**

&#x20; **- Search emails**

&#x20; **- Generate emails using AI**

&#x20; **- Send emails**

**- Google Calendar integration**

&#x20; **- Create events**

&#x20; **- View upcoming events**

&#x20; **- Delete events**

**- Multi-tool workflows**

&#x20; **- Send an email and schedule a calendar event from one command**

**- Calculator tool**

**- Date and time tool**

**- Browser integration**

**- Google Docs integration**

**- Google Sheets integration**

**- Memory support for conversational context**

**- Secure Google OAuth authentication**

**- REST API backend**

**- React-based frontend**



**## 🧠 How SynapseOS Works**



**The system follows a Planner–Executor architecture:**



**User Command**

&#x20;      **↓**

**React Frontend**

&#x20;      **↓**

**FastAPI Backend**

&#x20;      **↓**

**Planner Agent**

&#x20;      **↓**

**Execution Plan**

&#x20;      **↓**

**Executor Agent**

&#x20;      **↓**

**Tools / Services**

&#x20;      **↓**

**Result**

&#x20;      **↓**

**User**



**The Planner analyzes the user's natural-language request and determines which tool or sequence of tools should be executed.**



**The Executor then runs the selected tools and returns the results to the user.**



**## 🤖 AI Integration**



**SynapseOS uses Google Gemini for:**



**- Understanding natural-language requests**

**- Generating execution plans**

**- Generating email content**

**- Extracting meeting details**

**- Generating document content**

**- Handling requests that do not match predefined tool rules**



**This allows the system to combine rule-based task routing with LLM-powered intelligence.**



**## 🛠️ Technology Stack**



**### Frontend**

**- React.js**

**- Vite**

**- JavaScript**

**- HTML**

**- CSS**



**### Backend**

**- Python**

**- FastAPI**

**- REST APIs**

**- SQLAlchemy**

**- SQLite**



**### AI**

**- Google Gemini API**



**### Authentication \& Services**

**- Google OAuth**

**- Gmail API**

**- Google Calendar API**

**- Google Docs API**

**- Google Sheets API**



**### Development Tools**

**- Git**

**- GitHub**

**- VS Code**



**## 🔧 Available Tools**



**| Tool | Function |**

**|------|----------|**

**| Calculator | Performs mathematical calculations |**

**| DateTime | Provides current date and time |**

**| Gmail Read | Reads recent emails |**

**| Gmail Search | Searches emails |**

**| Gmail Send | Generates and sends emails |**

**| Calendar Create | Creates calendar events |**

**| Calendar List | Displays upcoming events |**

**| Calendar Delete | Deletes calendar events |**

**| Browser | Opens/searches web resources |**

**| Google Docs | Creates documents |**

**| Google Sheets | Creates spreadsheets |**



**## 💬 Example Commands**



**### Calculator**



**Calculate 25 \* 8 + 10**



**### Date \& Time**



**What is the current date and time?**



**### Gmail**



**Show my latest emails**



**Search my emails about meeting**



**Mail my friend about tomorrow's meeting**



**### Calendar**



**Schedule a meeting tomorrow at 3 PM**



**Show my upcoming events**



**### Multi-Tool Workflow**



**Mail my friend about the meeting tomorrow at 3 PM and also schedule it on my calendar.**



**SynapseOS can identify that both Gmail and Calendar tools are required and execute them as part of the same request.**



**## 📁 Project Structure**



**```text**

**SynapseOS/**

**│**

**├── backend/**

**│   ├── agents/**

**│   │   ├── planner.py**

**│   │   ├── executor.py**

**│   │   └── llm.py**

**│   │**

**│   ├── api/**

**│   ├── config/**

**│   ├── memory/**

**│   ├── prompts/**

**│   ├── services/**

**│   ├── tools/**

**│   ├── utils/**

**│   ├── database.py**

**│   ├── models.py**

**│   └── main.py**

**│**

**├── frontend/**

**│   ├── src/**

**│   ├── public/**

**│   ├── package.json**

**│   └── vite.config.js**

**│**

**├── .gitignore**

**└── README.md# SynapseOS – AI Operating System**



**SynapseOS is a full-stack AI-powered operating system that allows users to interact with multiple digital services through natural-language commands.**



**Instead of manually opening different applications, users can give a single instruction and SynapseOS determines which tools are required, creates an execution plan, and performs the requested actions.**



**## 🚀 Key Features**



**- Natural-language command processing**

**- AI-powered task planning using Google Gemini**

**- Planner–Executor agent architecture**

**- Gmail integration**

&#x20; **- Read emails**

&#x20; **- Search emails**

&#x20; **- Generate emails using AI**

&#x20; **- Send emails**

**- Google Calendar integration**

&#x20; **- Create events**

&#x20; **- View upcoming events**

&#x20; **- Delete events**

**- Multi-tool workflows**

&#x20; **- Send an email and schedule a calendar event from one command**

**- Calculator tool**

**- Date and time tool**

**- Browser integration**

**- Google Docs integration**

**- Google Sheets integration**

**- Memory support for conversational context**

**- Secure Google OAuth authentication**

**- REST API backend**

**- React-based frontend**



**## 🧠 How SynapseOS Works**



**The system follows a Planner–Executor architecture:**



**User Command**

&#x20;      **↓**

**React Frontend**

&#x20;      **↓**

**FastAPI Backend**

&#x20;      **↓**

**Planner Agent**

&#x20;      **↓**

**Execution Plan**

&#x20;      **↓**

**Executor Agent**

&#x20;      **↓**

**Tools / Services**

&#x20;      **↓**

**Result**

&#x20;      **↓**

**User**



**The Planner analyzes the user's natural-language request and determines which tool or sequence of tools should be executed.**



**The Executor then runs the selected tools and returns the results to the user.**



**## 🤖 AI Integration**



**SynapseOS uses Google Gemini for:**



**- Understanding natural-language requests**

**- Generating execution plans**

**- Generating email content**

**- Extracting meeting details**

**- Generating document content**

**- Handling requests that do not match predefined tool rules**



**This allows the system to combine rule-based task routing with LLM-powered intelligence.**



**## 🛠️ Technology Stack**



**### Frontend**

**- React.js**

**- Vite**

**- JavaScript**

**- HTML**

**- CSS**



**### Backend**

**- Python**

**- FastAPI**

**- REST APIs**

**- SQLAlchemy**

**- SQLite**



**### AI**

**- Google Gemini API**



**### Authentication \& Services**

**- Google OAuth**

**- Gmail API**

**- Google Calendar API**

**- Google Docs API**

**- Google Sheets API**



**### Development Tools**

**- Git**

**- GitHub**

**- VS Code**



**## 🔧 Available Tools**



**| Tool | Function |**

**|------|----------|**

**| Calculator | Performs mathematical calculations |**

**| DateTime | Provides current date and time |**

**| Gmail Read | Reads recent emails |**

**| Gmail Search | Searches emails |**

**| Gmail Send | Generates and sends emails |**

**| Calendar Create | Creates calendar events |**

**| Calendar List | Displays upcoming events |**

**| Calendar Delete | Deletes calendar events |**

**| Browser | Opens/searches web resources |**

**| Google Docs | Creates documents |**

**| Google Sheets | Creates spreadsheets |**



**## 💬 Example Commands**



**### Calculator**



**Calculate 25 \* 8 + 10**



**### Date \& Time**



**What is the current date and time?**



**### Gmail**



**Show my latest emails**



**Search my emails about meeting**



**Mail my friend about tomorrow's meeting**



**### Calendar**



**Schedule a meeting tomorrow at 3 PM**



**Show my upcoming events**



**### Multi-Tool Workflow**



**Mail my friend about the meeting tomorrow at 3 PM and also schedule it on my calendar.**



**SynapseOS can identify that both Gmail and Calendar tools are required and execute them as part of the same request.**



**## 📁 Project Structure**



**```text**

**SynapseOS/**

**│**

**├── backend/**

**│   ├── agents/**

**│   │   ├── planner.py**

**│   │   ├── executor.py**

**│   │   └── llm.py**

**│   │**

**│   ├── api/**

**│   ├── config/**

**│   ├── memory/**

**│   ├── prompts/**

**│   ├── services/**

**│   ├── tools/**

**│   ├── utils/**

**│   ├── database.py**

**│   ├── models.py**

**│   └── main.py**

**│**

**├── frontend/**

**│   ├── src/**

**│   ├── public/**

**│   ├── package.json**

**│   └── vite.config.js**

**│**

**├── .gitignore**

**└── README.md# SynapseOS – AI Operating System**



**SynapseOS is a full-stack AI-powered operating system that allows users to interact with multiple digital services through natural-language commands.**



**Instead of manually opening different applications, users can give a single instruction and SynapseOS determines which tools are required, creates an execution plan, and performs the requested actions.**



**## 🚀 Key Features**



**- Natural-language command processing**

**- AI-powered task planning using Google Gemini**

**- Planner–Executor agent architecture**

**- Gmail integration**

&#x20; **- Read emails**

&#x20; **- Search emails**

&#x20; **- Generate emails using AI**

&#x20; **- Send emails**

**- Google Calendar integration**

&#x20; **- Create events**

&#x20; **- View upcoming events**

&#x20; **- Delete events**

**- Multi-tool workflows**

&#x20; **- Send an email and schedule a calendar event from one command**

**- Calculator tool**

**- Date and time tool**

**- Browser integration**

**- Google Docs integration**

**- Google Sheets integration**

**- Memory support for conversational context**

**- Secure Google OAuth authentication**

**- REST API backend**

**- React-based frontend**



**## 🧠 How SynapseOS Works**



**The system follows a Planner–Executor architecture:**



**User Command**

&#x20;      **↓**

**React Frontend**

&#x20;      **↓**

**FastAPI Backend**

&#x20;      **↓**

**Planner Agent**

&#x20;      **↓**

**Execution Plan**

&#x20;      **↓**

**Executor Agent**

&#x20;      **↓**

**Tools / Services**

&#x20;      **↓**

**Result**

&#x20;      **↓**

**User**



**The Planner analyzes the user's natural-language request and determines which tool or sequence of tools should be executed.**



**The Executor then runs the selected tools and returns the results to the user.**



**## 🤖 AI Integration**



**SynapseOS uses Google Gemini for:**



**- Understanding natural-language requests**

**- Generating execution plans**

**- Generating email content**

**- Extracting meeting details**

**- Generating document content**

**- Handling requests that do not match predefined tool rules**



**This allows the system to combine rule-based task routing with LLM-powered intelligence.**



**## 🛠️ Technology Stack**



**### Frontend**

**- React.js**

**- Vite**

**- JavaScript**

**- HTML**

**- CSS**



**### Backend**

**- Python**

**- FastAPI**

**- REST APIs**

**- SQLAlchemy**

**- SQLite**



**### AI**

**- Google Gemini API**



**### Authentication \& Services**

**- Google OAuth**

**- Gmail API**

**- Google Calendar API**

**- Google Docs API**

**- Google Sheets API**



**### Development Tools**

**- Git**

**- GitHub**

**- VS Code**



**## 🔧 Available Tools**



**| Tool | Function |**

**|------|----------|**

**| Calculator | Performs mathematical calculations |**

**| DateTime | Provides current date and time |**

**| Gmail Read | Reads recent emails |**

**| Gmail Search | Searches emails |**

**| Gmail Send | Generates and sends emails |**

**| Calendar Create | Creates calendar events |**

**| Calendar List | Displays upcoming events |**

**| Calendar Delete | Deletes calendar events |**

**| Browser | Opens/searches web resources |**

**| Google Docs | Creates documents |**

**| Google Sheets | Creates spreadsheets |**



**## 💬 Example Commands**



**### Calculator**



**Calculate 25 \* 8 + 10**



**### Date \& Time**



**What is the current date and time?**



**### Gmail**



**Show my latest emails**



**Search my emails about meeting**



**Mail my friend about tomorrow's meeting**



**### Calendar**



**Schedule a meeting tomorrow at 3 PM**



**Show my upcoming events**



**### Multi-Tool Workflow**



**Mail my friend about the meeting tomorrow at 3 PM and also schedule it on my calendar.**



**SynapseOS can identify that both Gmail and Calendar tools are required and execute them as part of the same request.**



**## 📁 Project Structure**



**```text**

**SynapseOS/**

**│**

**├── backend/**

**│   ├── agents/**

**│   │   ├── planner.py**

**│   │   ├── executor.py**

**│   │   └── llm.py**

**│   │**

**│   ├── api/**

**│   ├── config/**

**│   ├── memory/**

**│   ├── prompts/**

**│   ├── services/**

**│   ├── tools/**

**│   ├── utils/**

**│   ├── database.py**

**│   ├── models.py**

**│   └── main.py**

**│**

**├── frontend/**

**│   ├── src/**

**│   ├── public/**

**│   ├── package.json**

**│   └── vite.config.js**

**│**

**├── .gitignore**

**└── README.md**

