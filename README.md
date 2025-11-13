# Company Information Investigator

An automated agent that investigates companies and gathers information including industry, LinkedIn profile, and website. The agent uses AI-powered browsing to search the internet and compile results into a CSV file.

## Features

- Reads company names from a CSV file
- Uses AI agent with browser automation (Playwright) to research companies
- Gathers company information: industry, LinkedIn profile, and website
- Outputs results to a structured CSV file
- Persistent and intelligent browsing (handles cookies, popups, etc.)

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Node.js and npm (for Playwright MCP server)

## Setup

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=company-investigator
```

Note: Get your LangSmith API key from [smith.langchain.com](https://smith.langchain.com/)

3. Sync dependencies:
```bash
uv sync
```

4. Create a `sandbox` directory for file operations:
```bash
mkdir sandbox
```

## Usage

Run the script with a CSV file containing company names:

```bash
uv run company_info.py company_names.csv
```

### Input CSV Format

The input CSV should have company names in the first column:

```csv
Company Name
Disco
Molinos
Arcor
Coto
Easy
```

The header row will be automatically skipped.

### Output

The agent will create a `company_info.csv` file in the `sandbox` directory with the following information for each company:
- Company name
- Industry
- LinkedIn profile URL
- Website URL

## How It Works

1. The script reads company names from the provided CSV file
2. Initializes AI agent with browser automation capabilities (Playwright) and file system access
3. The agent browses the internet to find information about each company
4. Results are compiled and saved to a CSV file
5. All agent interactions are traced in LangSmith for debugging and observability

## LangSmith Tracing

This project uses [LangSmith](https://smith.langchain.com/) for tracing and monitoring agent execution. LangSmith provides:

- **Full trace visibility**: See all agent steps, tool calls, and decisions
- **Performance monitoring**: Track latency and token usage
- **Debugging**: Identify issues in agent behavior
- **Run history**: Review past executions

To view traces:
1. Run the script with your LangSmith credentials configured in `.env`
2. Visit [smith.langchain.com](https://smith.langchain.com/)
3. Navigate to your project (default: `company-investigator`)
4. Browse traces for each run

## Project Structure

```
kk_company_info/
├── company_info.py          # Main script
├── company_names.csv        # Input file with company names
├── .env                     # Environment variables (API keys)
├── sandbox/                 # Output directory for generated files
└── README.md               # This file
```
