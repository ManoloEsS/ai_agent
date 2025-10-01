# AI Agent Project - Function Documentation

## Project Overview

This is an AI-powered coding agent that uses Google's Gemini API to interact with the files in a directory. The agent can perform file operations, execute Python code, and respond to natural language requests through function calling.

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
ai-agent "list files in the calculator directory"
ai-agent "run the calculator with expression 10 + 5"
ai-agent "read the calculator.py file"
```

### Verbose Mode
```bash
ai-agent --verbose "explain how the calculator works"
```

### Direct Calculator Usage
```bash
cd calculator
python3 main.py "3 + 5"
python3 tests.py
```

---

The calculator application serves as a demonstration of how the agent can interact with and manipulate Python projects through natural language instructions.
