import httpx
from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather")

@mcp.tool()
async def get_weather(location:str) -> str:
    """Get the current weather for a location (city name, e.g. "London")"""

    try:
        ## wttr.in: free weather API, no API key needed, returns one line of text
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"https://wttr.in/{location}",
                params={"format": "%l: %C %t (feels %f), humidity %h, wind %w"}
            )
            response.raise_for_status()
            return response.text.strip()

    except Exception as e:
        return f"Weather lookup failed for {location}: {str(e)}"


if __name__ == "__main__":
    ## streamable-http: the server runs as a web server and talks to clients over HTTP
    ## - start it yourself first: python weather.py (runs on http://127.0.0.1:8000/mcp)
    ## - clients connect by URL, so many clients (or other machines) can share one server
    ## - good for remote or shared tools that should keep running on their own
    mcp.run(transport="streamable-http")