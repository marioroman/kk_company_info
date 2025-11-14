# Company Information Investigator

An automated agent that investigates companies and gathers information including industry, LinkedIn profile, and website. The agent uses AI-powered browsing to search the internet and compile results into a CSV file.

## Features

- Reads company names from a CSV file
- Uses AI agent with browser automation (Playwright) to research companies
- Integrates BrightData MCP server for enhanced LinkedIn data extraction
- Prioritizes Argentinian companies when searching
- Gathers company information: industry, LinkedIn profile, and website
- Outputs results to a structured CSV file
- Persistent and intelligent browsing (handles cookies, popups, etc.)
- Full LangSmith tracing for observability

## Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Node.js and npm (for MCP servers: Playwright, BrightData, etc.)

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
BRIGHTDATA_API_KEY=your_brightdata_api_key_here
```

**API Keys:**
- OpenAI API key: [platform.openai.com](https://platform.openai.com/)
- LangSmith API key: [smith.langchain.com](https://smith.langchain.com/)
- BrightData API key (optional, for enhanced LinkedIn scraping): [brightdata.com](https://brightdata.com/)

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
Brastemp
Mondial
Colormaq
Suggar
Taiff
```

The header row will be automatically skipped.

### Output

The agent will create a `company_info.csv` file in the `sandbox` directory with the following columns:
- **company_name**: Name of the company
- **industry**: Primary industry (e.g., Retail, Software, Manufacturing)
- **linkedin_url**: Official LinkedIn company profile URL (format: https://www.linkedin.com/company/...)
- **website_url**: Official company website homepage

Example output:
```csv
company_name,industry,linkedin_url,website_url
Brastemp,Home Appliances,https://www.linkedin.com/company/brastemp,https://www.brastemp.com.br
Mondial,Consumer Electronics,https://www.linkedin.com/company/mondial-eletro,https://www.mondial.com.br
```

## How It Works

1. The script reads company names from the provided CSV file
2. Initializes AI agent with multiple MCP servers:
   - **Playwright**: Browser automation for web scraping
   - **BrightData**: Enhanced LinkedIn data extraction
   - **File System**: Writes results to CSV in sandbox directory
3. The agent intelligently searches for each company:
   - Prioritizes Argentinian companies first
   - Uses LinkedIn search with `site:linkedin.com/company` queries
   - Cross-validates information across multiple sources
   - Ensures LinkedIn URLs are valid organization pages
4. Results are compiled and saved to `sandbox/company_info.csv`
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
├── company_info.py          # Main script with agent logic
├── company_names.csv        # Input file with company names
├── pyproject.toml          # Project dependencies
├── .env                     # Environment variables (API keys)
├── .gitignore              # Git ignore rules
├── sandbox/                 # Output directory for generated files
│   └── company_info.csv    # Generated output (not in git)
└── README.md               # This file
```

## MCP Servers Used

This project leverages multiple Model Context Protocol (MCP) servers:

1. **@playwright/mcp**: Browser automation for general web scraping
2. **@brightdata/mcp**: Enhanced LinkedIn data extraction (requires API key)
3. **@modelcontextprotocol/server-filesystem**: File system operations in sandbox directory
4. **mcp-server-fetch**: HTTP fetching capabilities

## Notes

- The agent prioritizes finding Argentinian companies first in search results
- LinkedIn URLs are validated to ensure they point to organization pages (not individuals or groups)
- If no LinkedIn profile is found after exhaustive search, "Not found" is recorded
- All sources are cross-validated for accuracy
- Duplicate company names in the input are processed (as shown in the example CSV)
