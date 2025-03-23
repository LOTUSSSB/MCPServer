from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


# Initialize FastMCP server
mcp = FastMCP("algomd")


@mcp.tool()
async def read_algo() -> dict:
    """Read the content of all .cpp files in D:\\code\\luogu directory."""
    # Set the target path
    cpp_files_path = Path("D:\\code\\luogu")
    
    # Check if the path exists
    if not cpp_files_path.exists():
        return {"error": f"Path {cpp_files_path} does not exist"}
    
    # Dictionary to store file paths and their contents
    cpp_files_content = {}
    
    # Find all .cpp files
    cpp_files = list(cpp_files_path.glob("**/*.cpp"))
    
    # Process files
    for i, cpp_file in enumerate(cpp_files):
        try:
            # 直接使用 print 或日志记录进度，不再使用 ctx
            print(f"Reading file ({i+1}/{len(cpp_files)}): {cpp_file}")
            
            # Read the content of each file with UTF-8 encoding
            with open(cpp_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # Store the file path as string and its content
                cpp_files_content[str(cpp_file)] = content
        except Exception as e:
            # Handle potential errors (like encoding issues)
            cpp_files_content[str(cpp_file)] = f"Error reading file: {str(e)}"
    
    return cpp_files_content

@mcp.tool()
def save_to_markdown(
    content: str, 
    prompt: Optional[str] = None,
    filename: Optional[str] = None
) -> dict:
    """
    Save LLM-generated content to a markdown file.
    
    Args:
        content: The text content to save in the markdown file
        prompt: Optional prompt that generated the content
        filename: Optional custom filename (without extension)
        
    Returns:
        Dictionary with status information
    """
    # 固定的保存路径
    save_dir = Path("D:/code/ai_outputs")
    
    # 创建目录（如果不存在）
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名（如果未提供）
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"llm-output-{timestamp}"
    
    # 确保文件名有.md扩展名
    if not filename.endswith(".md"):
        filename = f"{filename}.md"
    
    # 完整的文件路径
    file_path = save_dir / filename
    
    try:
        # 准备文件内容
        file_content = []
        
        # 添加元数据部分
        file_content.append("---")
        file_content.append(f"created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        file_content.append(f"user: {os.getenv('USERNAME') or 'LOTUSSSB'}")
        
        if prompt:
            file_content.append(f"prompt: |\n  {prompt.replace(chr(10), chr(10) + '  ')}")
        
        file_content.append("---")
        file_content.append("")  # 空行分隔元数据和内容
        
        # 添加正文内容
        file_content.append(content)
        
        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(file_content))
        
        return {
            "success": True,
            "file_path": str(file_path),
            "file_size": os.path.getsize(file_path),
            "message": f"Content successfully saved to {file_path}"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to save content: {str(e)}"
        }


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

    #   "algomd": {
    #       "command": "uv",
    #       "args": [
    #           "--directory",
    #           "D:\\code\\mcp\\algomd",
    #           "run",
    #           "algomd.py"
    #       ]
    #   },