# ai — 智能命令行助手 / Intelligent Command Line Assistant

> 让终端更聪明：基于 ChatGPT 的交互式命令生成与执行工具  
> Make your terminal smarter: Interactive command generation and execution tool powered by ChatGPT

## 项目简介 / Project Overview

**ai** 是一款高度智能化的命令行工具，集成 OpenAI ChatGPT 接口。它能够：

* 自动生成符合需求的 Shell 命令
* 详细解析命令参数，并以友好样式呈现
* 支持即时执行或预览模式，安全可靠

适用于频繁需要查找和组合常用命令的开发者、运维工程师和终端达人。(才不是)  
适用于一时想不起该用什么指令的健忘的人

---

**ai** is a highly intelligent command-line tool integrated with OpenAI ChatGPT API. It can:

* Automatically generate Shell commands that meet your requirements
* Provide detailed parameter explanations with user-friendly formatting
* Support instant execution or preview mode, safe and reliable

Suitable for developers, DevOps engineers, and terminal enthusiasts who frequently need to look up and combine common commands. (Not really)  
Perfect for forgetful people who can't remember what command to use

---

## 核心功能 / Core Features

1. **config** — 配置并安全存储 ChatGPT API Key / Configure and securely store ChatGPT API Key
2. **ask** — 为目标提供可运行命令及参数说明，支持确认后执行 / Provide runnable commands with parameter explanations, execute after confirmation

---

## 安装指南 / Installation Guide

### 方法一 / Method 1
```bash
git clone https://github.com/kyuuseiryuu/ai-cmd.git
cd ai-cmd
uv tool install .
```

### 方法二 / Method 2
```bash
alias ai="uvx --from git+https://github.com/kyuuseiryuu/ai-cmd ai"
```

---

## 快速入门 / Quick Start

### 1. 配置 API Key / Configure API Key

**OpenAI API 配置 / OpenAI API Configuration:**
```bash
ai config --key sk-your-openai-api-key --model gpt-4o-mini
```

**Ollama 本地配置 / Ollama Local Configuration:**
```bash
ai config --endpoint http://localhost:11434/v1 --model llama3
```

首次使用前，你需要配置 API 信息。配置将被存储在 `~/.ai_cli_tool_config.json`。

Before first use, you need to configure the API information. The configuration will be stored in `~/.ai_cli_tool_config.json`.

### 2. 交互模式 (ask) / Interactive Mode (ask)

```bash
ai ask 查找当前目录下所有 Python 文件
# or
ai ask find all Python files in current directory
```

**流程 / Process:**
1. 显示建议命令及详细参数说明 / Display suggested command with detailed parameter explanations
2. 输入 `go` 确认后执行该命令 / Type `go` to confirm and execute the command

---

## 样例演示 / Example Demo

### 中文示例 / Chinese Example
```bash
$ ai ask 压缩当前目录为 archive.tar.gz

🤖 正在请求 AI 生成命令，请稍候...

✨ 建议命令:
   tar -czvf archive.tar.gz .

📖 命令说明:
* `tar`: 归档工具
* `-c`: 创建新的归档文件
* `-z`: 使用 gzip 压缩
* `-v`: 显示详细过程
* `-f`: 指定输出文件名
* `.`: 当前目录

⚠️  警告: 执行前请仔细检查命令，确保其安全无害。
输入 `go` 以执行, 按回车键取消: go

▶️  执行: tar -czvf archive.tar.gz .
# 执行并完成压缩
```

### English Example
```bash
$ ai ask count lines of code in Python files

🤖 正在请求 AI 生成命令，请稍候...

✨ 建议命令:
   find . -name "*.py" -exec wc -l {} + | tail -1

📖 命令说明:
* `find .`: Search in current directory
* `-name "*.py"`: Match Python files
* `-exec wc -l {} +`: Count lines for each file
* `tail -1`: Show total count

⚠️  警告: 执行前请仔细检查命令，确保其安全无害。
输入 `go` 以执行, 按回车键取消: go

▶️  执行: find . -name "*.py" -exec wc -l {} + | tail -1
# Execute and show results
```

---

## 配置说明 / Configuration Details

支持两种 AI 服务 / Supports two AI services:

### OpenAI API
```bash
ai config --key YOUR_API_KEY --model gpt-4o-mini
```

### Ollama (本地部署 / Local Deployment)
```bash
# 首先启动 Ollama 服务 / First start Ollama service
ollama serve

# 拉取模型 / Pull model
ollama pull llama3

# 配置工具 / Configure tool
ai config --endpoint http://localhost:11434/v1 --model llama3
```

---

## 安全特性 / Security Features

* ⚠️ **命令确认** / **Command Confirmation**: 所有命令执行前都需要用户确认 / All commands require user confirmation before execution
* 🔍 **命令预览** / **Command Preview**: 显示完整命令和参数说明 / Display complete command and parameter explanations
* 📁 **本地配置** / **Local Configuration**: 配置文件存储在用户主目录 / Configuration file stored in user home directory

---

## 开发与贡献 / Development & Contributing

欢迎提交 Issue、Pull Request 或参与讨论，共同完善功能和多语言支持。

We welcome Issues, Pull Requests, and discussions to improve features and multi-language support.

### 开发环境 / Development Environment
```bash
git clone https://github.com/kyuuseiryuu/ai-cmd.git
cd ai-cmd
uv sync
uv run ai --help
```

---

## 协议许可 / License

本项目遵循 MIT 协议，详情见 [LICENSE](LICENSE)。

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**让 AI 驱动你的终端，命令行从此更高效！**  
**Let AI drive your terminal, making command line more efficient!**

> 此 README 也由 AI 自动生成 / This README is also generated by AI