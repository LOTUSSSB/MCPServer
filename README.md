# AlgoMD

AlgoMD 是一个基于 MCP (Model Control Protocol) 的工具集，旨在简化算法代码分析与文档生成的流程。

## 功能特点

AlgoMD 提供了以下主要功能：

- **代码读取**：自动读取指定目录下所有 C++ 算法代码文件
- **内容保存**：将大语言模型(LLM)生成的内容保存为结构化的 Markdown 文件
- **元数据管理**：自动添加时间戳、用户信息和提示词等元数据到输出文件中

## 安装要求

- Python 3.7+
- uv
- 安装以下依赖：
  - mcp
  - httpx

```bash
uv add mcp[cli] httpx
```

## 设置与配置

1. 克隆此仓库到本地
2. 在 `algomd.py` 中设置以下路径（根据需要调整）：
   - 算法文件目录：默认为 `D:\code\luogu`
   - 输出文件目录：默认为 `D:\code\ai_outputs`

## 使用方法

### 配置 MCP 服务器

在 Claude Desktop 的设置中添加以下配置：

```json
{
  "mcpServers": {
    "algomd": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\code\\mcp\\algomd", // AlgoMD 的路径
        "run",
        "algomd.py"
      ]
    }
  }
}
```

### 读取算法代码

调用 `read_algo()` 函数，它将：

1. 递归扫描 `D:\code\luogu` 目录下的所有 `.cpp` 文件
2. 读取每个文件的内容
3. 返回一个字典，键为文件路径，值为文件内容

```python
code_files = await read_algo()
```

### 保存 LLM 内容

```python
await save_to_markdown(
    content="# 算法分析\n\n这是对冒泡排序的分析...",
    prompt="解释这段排序算法的时间复杂度",
    filename="bubble_sort_analysis"
)
```

此函数将：
1. 在 `D:\code\ai_outputs` 目录下创建 Markdown 文件
2. 添加包含创建时间、用户和提示词的元数据头
3. 保存 LLM 生成的内容
4. 返回文件保存状态信息

## 工作流示例

1. 使用 `read_algo()` 读取算法代码文件
2. 将代码传递给 LLM 进行分析
3. 让 LLM 生成算法解释、复杂度分析或优化建议
4. 使用 `save_to_markdown()` 将分析结果保存为结构化文档

```python
# 工作流示例
code_files = await read_algo()
algorithm_code = code_files["D:\\code\\luogu\\sorting\\bubble_sort.cpp"]

# 使用 LLM 分析代码（这部分在 Claude 中完成）
analysis = "# 冒泡排序分析\n\n## 算法原理\n\n冒泡排序通过重复遍历要排序的数列，比较相邻元素并交换它们的位置...\n\n## 时间复杂度\n\n- 最坏情况：O(n²)\n- 最好情况：O(n)"

# 保存分析结果
result = await save_to_markdown(
    content=analysis,
    prompt="分析这段冒泡排序代码的原理和复杂度",
    filename="bubble_sort_analysis"
)

print(f"文档已保存至 {result['file_path']}")
```

## 输出示例

生成的 Markdown 文件包含以下结构：

```markdown
---
created: 2025-03-24 15:30:45
user: LOTUSSSB
prompt: |
  分析这段冒泡排序代码的原理和复杂度
---

# 冒泡排序分析

## 算法原理

冒泡排序通过重复遍历要排序的数列，比较相邻元素并交换它们的位置...

## 时间复杂度

- 最坏情况：O(n²)
- 最好情况：O(n)
```

# PhyGen

PhyGen 是一个基于 MCP (Model Control Protocol) 的工具集，旨在简化物理学或其他学科报告的生成和处理流程。

## 功能特点

PhyGen 提供了以下主要功能：

- **PDF 转 Markdown**：自动将 PDF 文档转换为结构化的 Markdown 格式
- **内容保存**：将大语言模型(LLM)生成的内容保存为 Markdown 文件
- **Markdown 转 Word**：使用 pandoc 将 Markdown 内容转换为格式化的 Word 文档

## 安装要求

- Python 3.7+
- uv
- 安装以下依赖：
  - mcp
  - httpx
  - pandoc (命令行工具)

```bash
uv add mcp[cli] httpx
```

同时确保系统中已安装 [pandoc](https://pandoc.org/installing.html)。

## 设置与配置

1. 克隆此仓库到本地
2. 在 `phygen.py` 中设置以下常量：
   - `CONVERT_API_URL`: 云端 PDF 转换服务的 URL(使用cloudflare的markdown[转换服务](https://developers.cloudflare.com/workers-ai/markdown-conversion/#tomarkdowndocumentresult-definition)，为了使用方便，建议使用此方式[部署](https://github.com/xxnuo/serverless-markdown-converto))
   - `AUTH_PASSWORD`: 访问转换服务的密码

## 使用方法

### 配置 MCP 服务器

在 Claude Desktop 的设置中添加以下配置：

```json
{
  "mcpServers": {
    "phygen": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\code\\mcp\\phygen", // PhyGen 的路径
        "run",
        "phygen.py"
      ]
    }
  }
}
```

### PDF 转 Markdown

1. 将要转换的 PDF 文件放在工作目录下，并命名为 `input.pdf`
2. 调用 `convert_pdf_to_markdown()` 函数
3. 转换结果将保存为 `output.md`

```python
result = await convert_pdf_to_markdown()
print(result)  # 显示转换状态和摘要
```

### 保存 LLM 内容

```python
await save_llm_content(
    content="# 我的报告\n\n这是由 LLM 生成的内容...",
    prompt="生成一份关于量子力学的报告"
)
```

保存的内容将位于 `result.md` 文件中。

### Markdown 转 Word 文档

```python
await convert_to_docx(
    input_file="result.md",
    output_file="final_report.docx",
    template_file="template.docx"
)
```

此功能使用 pandoc 将 Markdown 转换为 Word 文档，并可应用自定义模板样式。

## 工作流示例

1. 将实验手册或文献保存为 PDF 并命名为 `input.pdf`
2. 使用 `convert_pdf_to_markdown()` 将其转换为 Markdown
3. 准备template.docx文件来实现你想要的模板，用于生成最终的word文档
3. 让 LLM 生成或修改内容并通过 `save_llm_content()` 保存
4. 最后使用 `convert_to_docx()` 将结果转换为格式化的 Word 文档

```python
# 转换PDF到Markdown
pdf_result = await convert_pdf_to_markdown()

# LLM处理内容（在Claude中进行）
# ...

# 保存LLM生成的内容
save_result = await save_llm_content(
    content="# 实验报告\n\n## 引言\n\n本实验旨在测量...",
    prompt="基于PDF内容生成标准实验报告"
)

# 转换为Word文档
docx_result = await convert_to_docx(
    input_file="result.md",
    output_file="实验报告.docx",
    template_file="template.docx"
)

print(f"Word文档已生成: {docx_result}")
```



