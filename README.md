# AI Agent Project

An AI-powered coding agent that uses Google's Gemini API to interact with a calculator application through natural language and function calling.

## Quick Start

### Prerequisites
- Python 3.11+
- [pipx](https://pipx.pypa.io/) (recommended for global installation)
- Google Gemini API key

### Installation

#### Using pipx (recommended)

1. Install pipx if you haven't already:
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

2. Install the AI agent:
```bash
pipx install git+https://github.com/ManoloEsS/ai_agent.git
```

3. Set up your API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```
Or create a `.env` file in your working directory:
```
GEMINI_API_KEY=your-api-key-here
```

#### Alternative: Using pip (local development)

If you prefer to use pip for local development:

1. Clone the repository:
```bash
git clone https://github.com/ManoloEsS/ai_agent.git
cd ai_agent
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up your API key as shown above.

### Usage

Run the AI agent with natural language commands:

```bash
# After installing with pipx, you can run from anywhere
ai-agent "list files in the calculator directory"
```

More examples:

```bash
# Run the calculator
ai-agent "run the calculator with expression 3 + 5"

# Read a file
ai-agent "read the calculator.py file"

# Enable verbose mode for detailed logging
ai-agent --verbose "explain how the calculator works"
```

### Direct Calculator Usage

You can also run the calculator directly:

```bash
cd calculator
python3 main.py "3 + 5"
python3 tests.py
```

## Project Structure

```
.
├── main.py                      # AI agent entry point
├── config.py                    # Configuration and constants
├── functions/                   # Agent function tools
│   ├── call_function.py        # Function router
│   ├── get_files_info.py       # List directory contents
│   ├── get_file_content.py     # Read files
│   ├── write_file.py           # Create/modify files
│   └── run_python_file.py      # Execute Python scripts
└── calculator/                  # Demo calculator application
    ├── main.py                 # Calculator CLI
    ├── tests.py                # Unit tests
    └── pkg/
        ├── calculator.py       # Calculator logic
        └── render.py           # Output formatting
```

## Documentation

For a comprehensive explanation of each function and their role in the program, see:

**[FUNCTION_DOCUMENTATION.md](FUNCTION_DOCUMENTATION.md)**

This detailed documentation includes:
- Complete function descriptions and their responsibilities
- Parameter explanations and return values
- Security features and design patterns
- Program flow and workflow examples
- Usage examples and best practices

## Key Features

- **AI-Driven Interaction**: Use natural language to interact with code
- **Function Calling**: AI automatically determines which functions to call
- **Security**: Path traversal protection and working directory constraints
- **File Operations**: List, read, and write files safely
- **Code Execution**: Run Python scripts with arguments
- **Multi-Step Tasks**: Agent can chain multiple operations
- **Verbose Logging**: Debug mode for detailed execution traces

## How It Works

1. User provides a natural language prompt
2. AI agent analyzes the request
3. Agent calls appropriate functions (file operations, code execution)
4. Results are returned to the AI
5. AI generates a human-readable response

The agent can perform multiple operations in sequence to accomplish complex tasks.

## Examples

### Example 1: Exploring the Project
```bash
ai-agent "what files are in the calculator directory?"
```

### Example 2: Running Code
```bash
ai-agent "run the calculator tests"
```

### Example 3: Reading and Explaining Code
```bash
ai-agent "read calculator.py and explain how it works"
```

### Example 4: Modifying Code
```bash
ai-agent "add support for exponentiation to the calculator"
```

## Security

The agent includes multiple security layers:
- Operations are restricted to the `./calculator` working directory
- Path traversal protection prevents access to parent directories
- File operations validate paths before execution
- Script execution has a 30-second timeout
- File reading is limited to 10,000 characters

## Testing

Run the calculator tests:
```bash
cd calculator
python3 tests.py
```

## License

This project is provided as-is for educational and demonstration purposes.

## Contributing

This is a demonstration project showing AI agent capabilities with function calling.

---

For detailed technical documentation, see [FUNCTION_DOCUMENTATION.md](FUNCTION_DOCUMENTATION.md)
