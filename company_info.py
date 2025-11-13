import os
import csv
import argparse
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from langsmith import traceable

load_dotenv(override=True)

# Enable LangSmith tracing
os.environ.setdefault("LANGSMITH_TRACING", "true") 


def read_company_names(csv_file):
    """Read company names from CSV file."""
    company_names = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        # Skip header if present
        header = next(reader, None)
        for row in reader:
            if row:  # Skip empty rows
                company_names.append(row[0])
    return company_names


@traceable(name="investigate_companies")
async def investigate_companies(agent, company_list):
    """Run the agent investigation with LangSmith tracing."""
    prompt = f"""For each company name in the provided list:
    Find and confirm:
        The company’s primary industry (e.g., Fintech, Retail, Software).
        The company’s official LinkedIn profile URL (must be a LinkedIn page for organizations, not individuals or groups).
        The company’s official website homepage (ex: www.company.com).

        Instructions:
            Use direct LinkedIn and web search (Google or Bing).
            Use site:linkedin.com/company "COMPANY NAME".
            If multiple companies have similar names, use web sources to verify the correct LinkedIn profile—prefer the global parent organization if ambiguous.
            Only accept LinkedIn URLs that begin with https://www.linkedin.com/company/....
            For industry, use LinkedIn’s or the official website’s stated category, or trusted business databases if unclear.
            Validate the website by cross-checking with LinkedIn and other authoritative sources.
        Output:
            Create a single company_info.csv file with columns:
            company_name
            industry
            linkedin_url
            website_url

            Fill in all rows with accurate data; do not leave columns blank unless truly unavailable after exhaustive search.
            
            Example Output Row:
            Acme Corp, Software, https://www.linkedin.com/company/acme-corp, https://www.acmecorp.com
            
            Fallback logic:
                If no LinkedIn company page is found, state "Not found" in the linkedin_url column, and log attempted queries.

            Audit:
                Double-check each LinkedIn URL resolves to a real company profile and is accessible.

            Ensure the industry and website are consistent across sources.
                                    Company List Names: {company_list}"""
    result = await Runner.run(agent, prompt)
    return result


async def main(csv_file):
    # Read company names from CSV
    company_names = read_company_names(csv_file)
    company_list = ",\n                                        ".join(company_names) + ","

    fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}

    async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
        fetch_tools = await server.list_tools()

    playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"]}

    async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
        playwright_tools = await server.list_tools()

    sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
    files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}

    async with MCPServerStdio(params=files_params,client_session_timeout_seconds=60) as server:
        file_tools = await server.list_tools()

    instructions = """
You browse the internet to accomplish your instructions.
You are highly capable at browsing the internet independently to accomplish your task,
including accepting all cookies and clicking 'not now' as
appropriate to get to the content you need. If one website isn't fruitful, try another.
Be persistent until you have solved your assignment,
trying different options and sites as needed.
"""

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
            agent = Agent(
                name="investigator",
                instructions=instructions,
                model="gpt-4o-mini",
                mcp_servers=[mcp_server_files, mcp_server_browser]
                )
            result = await investigate_companies(agent, company_list)
            print(result.final_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Investigate companies and gather information.')
    parser.add_argument('csv_file', help='Path to CSV file containing company names')
    args = parser.parse_args()

    asyncio.run(main(args.csv_file))
