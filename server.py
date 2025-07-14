from fastmcp import FastMCP
import os
from pathlib import Path
import subprocess
import uvicorn
import requests
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
from urllib.parse import unquote

mcp = FastMCP('manim-mcp-server', json_response=True, stateless_http=True)

@mcp.tool
def get_context(docs_list_str: str) -> str:
    """Retrieve context for a given query."""
    docs_list = docs_list_str.split(",")
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

    manim_cmd = [".venv/bin/python", "-m", "manim", "-qm", "main.py", "Main"]
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
    
    return FileResponse(
        file_path,
        media_type='video/mp4',
        filename=filename
    )
    
download_route = Route('/download/{filename}', download_file, methods=['GET'])
app.routes.append(download_route)

def main():
    uvicorn.run(app, host='0.0.0.0', port=8000)
    
if __name__ == "__main__":
    main()