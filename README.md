# AI Dev

Agentic coding assistant that turns natural language programming requests into working code. Parses the request, plans an implementation, writes files iteratively, and runs the code to verify output — without manual intervention.

## How it works

1. You describe what you want to build in plain English.
2. The agent breaks the request into subtasks using an LLM planner.
3. A code-writing loop generates each file, runs it, reads the output, and fixes errors automatically.
4. When all subtasks pass, the session is done.

The agent maintains a project context across prompts — you can say "now add unit tests" or "refactor the main loop" and it knows what exists.

## Tech stack

| Component | Role |
|---|---|
| OpenAI GPT-4o | Planning and code generation |
| Python subprocess | Running generated code and capturing output |
| File I/O | Writing, reading, and patching files in the project directory |

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key

### Install

```bash
git clone https://github.com/quinnhasse/AIDevTest.git
cd AIDevTest
pip install -r requirements.txt
```

### Configure

Create a `.env` file:

```env
OPENAI_API_KEY=your_key_here
```

### Run

```bash
python main.py
```

Enter your request at the prompt. The agent will print each step as it works.

## Example session

```
> Build a CLI todo app that stores tasks in a JSON file

[Agent] Planning: file_io.py, todo.py, cli.py
[Agent] Writing file_io.py...
[Agent] Writing todo.py...
[Agent] Writing cli.py...
[Agent] Running cli.py --help...
[Agent] Output: usage: cli.py [-h] {add,list,done,remove} ...
Done.
```

## Project structure

```
AIDevTest/
├── main.py            # Entry point and REPL
├── planner.py         # Task decomposition via LLM
├── coder.py           # File generation and patching
├── runner.py          # Subprocess execution and error capture
├── context.py         # Session state (files, history)
├── requirements.txt
└── .env.example
```

## Requirements

```
openai
python-dotenv
```
