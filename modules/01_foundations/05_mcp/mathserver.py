from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
def add(a:int, b:int) -> int:
    """_summary_
    add two numbers
    """
    return a+b

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """_sumamry_
    Multiply two numbers
    """
    return a*b

if __name__ == "__main__":
    ## stdio: the server talks to the client through standard input/output (stdin/stdout)
    ## - no need to start it yourself: the client launches this file as a subprocess
    ## - one client per server, on the same machine only, and it stops when the client stops
    ## - good for local tools, no port or URL needed
    mcp.run(transport="stdio")