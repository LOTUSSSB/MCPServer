from typing import Any
import httpx
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务器
mcp = FastMCP("phygen")

# 常量
CONVERT_API_URL = "CLOUDFLARE_WORKER_URL"  # 云端转换服务的URL
DEFAULT_INPUT_FILE = "input.pdf"  # 当前目录下的默认输入文件
AUTH_PASSWORD = "PASSWD"  # 在这里设置您的密码

@mcp.tool()
async def convert_pdf_to_markdown() -> str:
    """将当前目录下的input.pdf转换为Markdown格式。"""
    # 检查input.pdf是否存在
    input_file = Path(DEFAULT_INPUT_FILE)
    if not input_file.exists():
        return f"错误: 当前目录下未找到 '{DEFAULT_INPUT_FILE}'。请确保文件存在。"
    
    try:
        # 准备文件数据
        files = [
            ("files", (input_file.name, open(input_file, "rb"), "application/pdf"))
        ]
        
        # 设置请求头
        headers = {
            "Cookie": f"auth={AUTH_PASSWORD}"
        }

        # 发送请求
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CONVERT_API_URL,
                headers=headers,
                files=files
            )
            
            # 关闭文件
            files[0][1][1].close()
                
            # 检查响应状态
            if response.status_code != 200:
                return f"转换失败: HTTP 状态码 {response.status_code}, 响应: {response.text}"
            
            # 解析响应
            result = response.json()
            if "markdowns" not in result:
                return f"转换失败: 响应格式不正确 - {result}"
            
            # 同时保存结果到文件
            output_texts = []
            for item in result["markdowns"]:
                markdown_content = item["markdown"]
                output_texts.append(f"## 文件: {item['name']}\n\n{markdown_content}")
                
                # 保存到output.md文件
                with open("output.md", "w", encoding="utf-8") as output_file:
                    output_file.write(markdown_content)
                
            return "已成功转换PDF并保存到output.md\n\n" + "\n\n".join(output_texts)
    except Exception as e:
        return f"转换过程中发生错误: {str(e)}"
    
@mcp.tool()
async def save_llm_content(
    content: str, 
    prompt: str = None
) -> dict:
    """
    将LLM生成的内容保存到当前目录下的Markdown文件中。
    
    参数:
        content: 要保存的文本内容
        prompt: 可选的生成该内容的提示词
        
    返回:
        包含状态信息的字典
    """
    # 固定的保存路径为当前目录，固定的文件名
    file_path = Path("result.md")
    
    try:
        # 直接写入内容，不添加额外的元数据
        with open(file_path, "w", encoding="utf-8") as f:
            # 如果有提示词，可以在文件开头添加一个简单的注释
            if prompt:
                f.write(f"<!-- 提示词: {prompt} -->\n\n")
            
            # 写入主要内容
            f.write(content)
        
        return {
            "success": True,
            "file_path": str(file_path),
            "file_size": os.path.getsize(file_path),
            "message": f"内容已成功保存到 {file_path}"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"保存内容失败: {str(e)}"
        }

@mcp.tool()
async def convert_to_docx(
    input_file: str = "result.md",
    output_file: str = "result.docx",
    template_file: str = "template.docx"
) -> str:
    """
    使用 pandoc 将 Markdown 文件转换为 Word 文档。
    
    参数:
        input_file: 输入的 Markdown 文件名
        output_file: 输出的 Word 文档文件名
        template_file: 参考模板文档（用于样式）
    """
    import subprocess
    import os
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        return f"错误: 输入文件 '{input_file}' 不存在"
    
    # 构建 pandoc 命令
    command = f"pandoc {input_file} -o {output_file}"
    
    # 如果模板文件存在，添加参考文档参数
    if os.path.exists(template_file):
        command += f" --reference-doc={template_file}"
    else:
        return f"警告: 模板文件 '{template_file}' 不存在，将使用默认样式"
    
    try:
        # 执行命令
        result = subprocess.run(
            command, 
            shell=True,
            capture_output=True, 
            text=True
        )
        
        # 检查命令是否成功执行
        if result.returncode == 0:
            if os.path.exists(output_file):
                return f"成功将 {input_file} 转换为 {output_file}"
            else:
                return f"命令执行成功，但未找到输出文件 {output_file}"
        else:
            return f"命令执行失败: {result.stderr}"
    
    except Exception as e:
        return f"执行过程中发生错误: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

#pandoc test.md -o test.docx --reference-doc=template.docx    
# {
#   "mcpServers": {
#       "phygen": {
#           "command": "uv",
#           "args": [
#               "--directory",
#               "D:\\code\\mcp\\phygen",
#               "run",
#               "phygen.py"
#           ]
#       }
#   }
# }