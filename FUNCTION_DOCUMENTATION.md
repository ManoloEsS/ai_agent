# AI Agent Project - Function Documentation

## Project Overview

This is an AI-powered coding agent that uses Google's Gemini API to interact with a calculator application. The agent can perform file operations, execute Python code, and respond to natural language requests through function calling.

## Architecture

The project consists of two main components:
1. **AI Agent System** (`main.py`, `functions/`, `config.py`) - The core agent that processes user requests
2. **Calculator Application** (`calculator/`) - A demonstration application that the agent can interact with

---

## Main Entry Point

### `main.py`

#### `main()` Function
**Purpose**: Entry point for the AI agent application. Orchestrates the entire agent workflow.

**Key Responsibilities**:
- **Environment Setup**: Loads environment variables using `load_dotenv()` to access the GEMINI_API_KEY
- **Argument Parsing**: 
  - Checks for `--verbose` flag to enable detailed logging
  - Extracts user prompt from command-line arguments
  - Validates that a prompt is provided
- **API Client Initialization**: Creates a Gemini API client with authentication
- **Message History**: Initializes conversation with user's prompt in the correct format
- **Iteration Loop**: 
  - Runs up to `MAX_ITERS` (20) iterations to handle multi-step tasks
  - Prevents infinite loops by enforcing iteration limit
  - Calls `generate_content()` repeatedly until a final response is obtained
- **Error Handling**: Catches and reports errors during content generation

**Flow**:
1. Parse command-line arguments
2. Initialize Gemini API client
3. Create initial message with user prompt
4. Loop until final response or max iterations:
   - Generate content (may trigger function calls)
   - If final response received, print and exit
5. Handle errors gracefully

---

#### `generate_content(client, messages, verbose)` Function
**Purpose**: Communicates with Gemini API to generate responses and execute function calls.

**Parameters**:
- `client`: Gemini API client instance
- `messages`: Conversation history (list of Content objects)
- `verbose`: Boolean flag for detailed logging

**Key Responsibilities**:
- **API Communication**: Sends messages to Gemini with system instructions and available tools
- **Token Tracking**: Reports token usage when verbose mode is enabled
- **Response Processing**: 
  - Appends AI responses to message history
  - Detects if response contains function calls or final text
- **Function Call Execution**:
  - Iterates through all function calls in response
  - Executes each function via `call_function()`
  - Validates function results
  - Appends function responses to message history
- **Return Value**: Returns final text response if no more function calls needed, otherwise returns None to continue the loop

**Flow**:
1. Call Gemini API with current message history
2. Log token usage (if verbose)
3. Add response to message history
4. If no function calls → return final text
5. If function calls present:
   - Execute each function call
   - Collect all function responses
   - Add responses to message history
   - Return None (continue iteration)

---

## Configuration

### `config.py`

**Constants**:
- `system_prompt`: Instructions for the AI agent, defining its role and capabilities
- `MAX_CHARS`: Maximum characters to read from a file (10,000)
- `WORKING_DIR`: Root directory for file operations (`"./calculator"`)
- `MAX_ITERS`: Maximum iteration limit to prevent infinite loops (20)

**Purpose**: Centralized configuration for security constraints and behavior settings.

---

## Function Call System

### `functions/call_function.py`

#### `available_functions` (Tool Declaration)
**Purpose**: Defines the schema of all functions available to the AI agent.

**Structure**: A `types.Tool` object containing function declarations:
- `schema_get_files_info`: List directory contents
- `schema_get_file_content`: Read file contents
- `schema_run_python_file`: Execute Python files
- `schema_write_file`: Create/modify files

**Role**: Informs the Gemini API about available tools so it can generate appropriate function calls.

---

#### `call_function(function_call_part, verbose)` Function
**Purpose**: Router that executes the appropriate function based on AI's request.

**Parameters**:
- `function_call_part`: Function call details from Gemini API (name and arguments)
- `verbose`: Boolean for detailed logging

**Key Responsibilities**:
- **Function Mapping**: Maps function names to actual function implementations
- **Security Injection**: Automatically adds `working_directory` parameter to constrain operations
- **Error Handling**: Returns error response for unknown functions
- **Logging**: Prints function calls with arguments (verbose) or just function names
- **Response Formatting**: Wraps function results in proper Content objects for Gemini API

**Security Feature**: Injects `WORKING_DIR` to prevent operations outside the calculator directory.

**Flow**:
1. Log function call
2. Validate function name exists
3. Extract arguments and inject working_directory
4. Execute function
5. Wrap result in Content object
6. Return to agent

---

## File Operation Functions

### `functions/get_files_info.py`

#### `get_files_info(working_directory, directory)` Function
**Purpose**: Lists files and directories with their metadata.

**Parameters**:
- `working_directory`: Base directory for operations (injected automatically)
- `directory`: Optional subdirectory to list (relative path)

**Security Features**:
- Path traversal protection: Validates target is within working directory
- Absolute path resolution to prevent "../" attacks

**Returns**: Formatted string with:
- File/directory names
- File sizes in bytes
- Directory flag (is_dir)

**Use Cases**: 
- Exploring project structure
- Finding files before reading/editing
- Understanding directory layout

---

### `functions/get_file_content.py`

#### `get_file_content(working_directory, file_path)` Function
**Purpose**: Safely reads file contents with size limits.

**Parameters**:
- `working_directory`: Base directory (injected)
- `file_path`: Target file path (relative)

**Security Features**:
- Path traversal protection
- File existence validation
- Regular file check (not directory)

**Size Limit**: Reads maximum `MAX_CHARS` (10,000) characters and appends truncation notice if file is longer.

**Returns**: 
- File contents (up to MAX_CHARS)
- Error messages for invalid paths or missing files

**Use Cases**:
- Reading source code
- Inspecting configuration files
- Understanding existing code before modifications

---

### `functions/write_file.py`

#### `write_file(working_directory, file_path, content)` Function
**Purpose**: Creates or overwrites files with provided content.

**Parameters**:
- `working_directory`: Base directory (injected)
- `file_path`: Target file path (relative)
- `content`: String content to write

**Security Features**:
- Path traversal protection
- Directory creation: Automatically creates parent directories if needed
- Directory check: Prevents writing to directories

**Returns**:
- Success message with character count
- Error messages for security violations or I/O errors

**Use Cases**:
- Creating new files
- Modifying existing code
- Generating configuration files

---

### `functions/run_python_file.py`

#### `run_python_file(working_directory, file_path, args)` Function
**Purpose**: Executes Python files with arguments and captures output.

**Parameters**:
- `working_directory`: Base directory (injected)
- `file_path`: Python file to execute (relative)
- `args`: Optional list of command-line arguments

**Security Features**:
- Path traversal protection
- File existence validation
- Python file extension check (.py)
- 30-second timeout to prevent infinite loops
- Executes in working directory context (cwd)

**Returns**: Combined output containing:
- STDOUT: Standard output from the program
- STDERR: Error messages
- Exit code (if non-zero)

**Use Cases**:
- Running calculator application
- Executing tests
- Testing code modifications

---

#### `schema_run_python_file` (and other schemas)
**Purpose**: Defines the function signature for the Gemini API.

**Structure**:
- `name`: Function identifier
- `description`: Natural language explanation of what the function does
- `parameters`: Schema defining input parameters with types and descriptions

**Role**: Enables the AI to understand when and how to call each function.

---

## Calculator Application

### `calculator/main.py`

#### `main()` Function
**Purpose**: Entry point for the calculator application.

**Responsibilities**:
- **Usage Instructions**: Displays help text when no arguments provided
- **Expression Parsing**: Combines command-line arguments into a single expression
- **Calculator Instantiation**: Creates Calculator instance
- **Evaluation**: Processes the mathematical expression
- **Rendering**: Formats output using the `render()` function
- **Error Handling**: Catches and displays evaluation errors

**Flow**:
1. Check for arguments
2. Join arguments into expression
3. Evaluate expression
4. Render result in a box
5. Print to console

---

### `calculator/pkg/calculator.py`

#### `Calculator` Class
**Purpose**: Evaluates mathematical expressions using infix notation.

**Components**:

##### `__init__()` Method
**Purpose**: Initializes calculator with operators and precedence rules.

**Attributes**:
- `operators`: Dictionary mapping symbols (+, -, *, /) to lambda functions
- `precedence`: Dictionary defining operator precedence (multiplication/division > addition/subtraction)

---

##### `evaluate(expression)` Method
**Purpose**: Main entry point for expression evaluation.

**Process**:
1. Validate expression (not empty or whitespace)
2. Tokenize by splitting on spaces
3. Call `_evaluate_infix()` for actual computation
4. Return result or None for empty expressions

---

##### `_evaluate_infix(tokens)` Method
**Purpose**: Implements the Shunting Yard algorithm for infix expression evaluation.

**Algorithm**:
1. Maintain two stacks: `values` (operands) and `operators`
2. For each token:
   - If operator: Apply higher/equal precedence operators from stack, then push current operator
   - If operand: Convert to float and push to values stack
3. After processing all tokens: Apply remaining operators
4. Validate single result remains
5. Return final value

**Error Handling**:
- Invalid tokens (non-numeric, non-operator)
- Malformed expressions
- Insufficient operands

---

##### `_apply_operator(operators, values)` Method
**Purpose**: Applies a single operator to two operands.

**Process**:
1. Pop operator from operators stack
2. Pop two values (b, then a) from values stack
3. Apply operator function: operator(a, b)
4. Push result back to values stack

**Error Handling**: Validates sufficient operands exist.

---

### `calculator/pkg/render.py`

#### `render(expression, result)` Function
**Purpose**: Creates a formatted ASCII box to display calculation results.

**Process**:
1. Format result (convert integers from floats)
2. Calculate box width based on longest string
3. Build box using Unicode box-drawing characters:
   - Top border (┌─┐)
   - Expression line
   - Blank line
   - Equals sign line
   - Blank line
   - Result line
   - Bottom border (└─┘)
4. Join lines and return

**Visual Output Example**:
```
┌──────────┐
│  3 + 5   │
│          │
│  =       │
│          │
│  8       │
└──────────┘
```

---

### `calculator/tests.py`

**Purpose**: Unit tests for the Calculator class.

**Test Cases**:
- `test_addition`: Verifies addition (3 + 5 = 8)
- `test_subtraction`: Verifies subtraction (10 - 4 = 6)
- `test_multiplication`: Verifies multiplication (3 * 4 = 12)
- `test_division`: Verifies division (10 / 2 = 5)
- `test_nested_expression`: Tests operator precedence (3 * 4 + 5 = 17)
- `test_complex_expression`: Complex precedence (2 * 3 - 8 / 2 + 5 = 7)
- `test_empty_expression`: Handles empty input
- `test_invalid_operator`: Catches invalid operators
- `test_not_enough_operands`: Catches malformed expressions

**Framework**: Python's `unittest` module

---

## Program Flow

### Complete Workflow Example

**User Command**: `python3 main.py "run calculator with expression 3 + 5"`

1. **main()**: 
   - Loads API key
   - Initializes Gemini client
   - Creates initial message

2. **generate_content()**: 
   - Sends prompt to Gemini
   - AI decides to call `run_python_file`
   - Returns function call (not text)

3. **call_function()**:
   - Routes to `run_python_file()`
   - Adds working_directory parameter
   - Executes function

4. **run_python_file()**:
   - Validates file path
   - Runs: `python3 calculator/main.py "3 + 5"`
   - Captures output

5. **calculator/main.py**:
   - Parses expression
   - Creates Calculator instance
   - Calls evaluate()

6. **Calculator.evaluate()**:
   - Tokenizes: ["3", "+", "5"]
   - Calls `_evaluate_infix()`

7. **_evaluate_infix()**:
   - Processes tokens using Shunting Yard algorithm
   - Returns: 8.0

8. **render()**:
   - Formats result in ASCII box

9. **Back to run_python_file()**:
   - Captures calculator output
   - Returns to call_function()

10. **Back to generate_content()**:
    - Adds function result to messages
    - Returns None (continue loop)

11. **main() loop continues**:
    - Calls generate_content() again

12. **generate_content() (second call)**:
    - Gemini sees function result
    - Generates final response
    - Returns text response

13. **main()**:
    - Prints final response
    - Exits

---

## Security Features

### Path Traversal Protection
All file operation functions validate that target paths remain within `WORKING_DIR`:
```python
if not target_file.startswith(absolute_working):
    return "Error: outside permitted directory"
```

### Automatic Directory Injection
`call_function()` automatically adds `working_directory` parameter, preventing AI from specifying arbitrary paths.

### Timeouts
`run_python_file()` enforces 30-second timeout to prevent infinite loops.

### File Size Limits
`get_file_content()` reads maximum 10,000 characters to prevent memory issues.

---

## Key Design Patterns

### 1. Function Calling (Agent Pattern)
The AI decides which functions to call based on user intent, enabling complex multi-step tasks.

### 2. Security by Design
All operations are constrained to a working directory with multiple validation layers.

### 3. Conversation History
Messages list maintains full context, allowing the AI to make informed decisions across multiple iterations.

### 4. Separation of Concerns
- Agent system (main.py) handles AI orchestration
- Functions (functions/) provide isolated capabilities
- Calculator app (calculator/) is a standalone demonstration

### 5. Schema-Driven Development
Function schemas inform the AI about available capabilities, enabling zero-shot tool use.

---

## Error Handling Strategy

### Graceful Degradation
- Unknown functions return error messages instead of crashing
- File operation errors are caught and returned as strings
- The iteration loop has a maximum limit to prevent infinite recursion

### Verbose Logging
The `--verbose` flag enables detailed debugging:
- Token usage tracking
- Function call arguments
- Function results

### Validation at Multiple Levels
1. **Application Level**: Command-line argument validation
2. **API Level**: Function existence checks
3. **File System Level**: Path validation, existence checks
4. **Security Level**: Working directory constraints

---

## Usage Examples

### Basic Usage
```bash
python3 main.py "list files in the calculator directory"
python3 main.py "run the calculator with expression 10 + 5"
python3 main.py "read the calculator.py file"
```

### Verbose Mode
```bash
python3 main.py --verbose "explain how the calculator works"
```

### Direct Calculator Usage
```bash
cd calculator
python3 main.py "3 + 5"
python3 tests.py
```

---

## Summary of Key Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `main()` | main.py | Agent orchestrator and CLI entry point |
| `generate_content()` | main.py | Gemini API communication and function execution |
| `call_function()` | functions/call_function.py | Function router with security injection |
| `get_files_info()` | functions/get_files_info.py | List directory contents |
| `get_file_content()` | functions/get_file_content.py | Read file contents safely |
| `write_file()` | functions/write_file.py | Create/modify files |
| `run_python_file()` | functions/run_python_file.py | Execute Python scripts |
| `Calculator.__init__()` | calculator/pkg/calculator.py | Initialize calculator with operators |
| `Calculator.evaluate()` | calculator/pkg/calculator.py | Main expression evaluation |
| `Calculator._evaluate_infix()` | calculator/pkg/calculator.py | Shunting Yard algorithm implementation |
| `Calculator._apply_operator()` | calculator/pkg/calculator.py | Apply single operation |
| `render()` | calculator/pkg/render.py | Format output in ASCII box |
| `main()` | calculator/main.py | Calculator CLI entry point |

---

## Conclusion

This AI agent system demonstrates:
- **Tool Use**: AI-driven function calling for file and code operations
- **Security**: Multi-layer protection against path traversal and malicious operations
- **Modularity**: Clean separation between agent infrastructure and application code
- **Extensibility**: Easy to add new functions by defining schemas and implementations
- **Robustness**: Comprehensive error handling and validation at every level

The calculator application serves as a demonstration of how the agent can interact with and manipulate Python projects through natural language instructions.
