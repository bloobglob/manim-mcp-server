from fastmcp import FastMCP
import os
from pathlib import Path
import subprocess
import uvicorn
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
from urllib.parse import unquote
import sys

mcp = FastMCP('manim-mcp-server', json_response=True, stateless_http=True)

@mcp.tool
def get_context(docs_list_str: str) -> str:
    """Retrieve context for a given query.

    Args:
        docs_list_str (str): A list of docs to retrieve, separated by ",".

    Returns:
        str: A string of all concatenated documents.
    """
    docs_list = docs_list_str.strip("\n").split(",")
    ret = ""
    if os.getcwd().endswith("manimations"):
        os.chdir("..")
    for doc in docs_list:
        doc = doc.strip().strip(":").strip()
        with open(f"custom_docs/{doc}.txt", "r") as f:
            ret += f.read() + "\n\n"
    return ret
        
pairs = [('\a', '\\a'), (r"\x07", '\\a'), ('\b', '\\b'), ('\f', '\\f'), ('\r', '\\r'), ('\t', '\\t'), ('\v', '\\v')]        

@mcp.tool
def generate_video(code: str) -> str:
    """Generates video based on urllib.parse.quote'd code.

    Args:
        code (str): urllib.parse.quote'd code to generate video from.

    Returns:
        str: Empty string.
    """
    if os.getcwd().endswith("manimations"):
        os.chdir("..")
    print("running,", os.getcwd())
    code = unquote(code)
    print(code)
    code = code.replace("```python", "").replace("```", "")
    for og, rep in pairs:
        code = code.replace(og, rep)
    
    target_dir = Path("manimations")
    if not target_dir.exists():
        raise RuntimeError("Please create the manim project first")
    orig_dir = os.getcwd()
    os.chdir(target_dir)
    
    with open("main.py", "w") as f:
        f.write(code)

    manim_cmd = [sys.executable, "-m", "manim", "-qm", "main.py", "Main"]
    result = subprocess.run(manim_cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        raise RuntimeError(f"Manim command failed with error: {result.stderr}")

    print(orig_dir)
    os.chdir(orig_dir)
    print("Changed back to original directory:", os.getcwd())
    
    return ""
    
app = mcp.http_app()

async def download_file(request):
    if os.getcwd().endswith("manimations"):
        os.chdir("..")
    filename = request.path_params['filename']
    file_path = f'manimations/media/videos/main/720p30/{filename}'
    
    if not os.path.exists(file_path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    
    mtime = os.path.getmtime(file_path)
    
    return FileResponse(
        file_path,
        media_type='video/mp4',
        filename=filename,
        headers={
            "Cache-Control": "no-cache",  # Prevent caching of potentially changing files
            "ETag": f'"{mtime}"'  # Use modification time as ETag
        }
    )
    
download_route = Route('/download/{filename}', download_file, methods=['GET'])
app.routes.append(download_route)

def main():
    uvicorn.run(app, host='0.0.0.0', port=8000)
    
if __name__ == "__main__":
    main()