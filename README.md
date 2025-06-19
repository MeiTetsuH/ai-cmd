# ai — 智能命令行助手 / Intelligent Command Line Assistant

> 让终端更聪明：基于 AI 的交互式命令生成与执行工具  
> Make your terminal smarter: Interactive command generation and execution tool powered by AI

## 项目简介 / Project Overview

**ai** 是一款高度智能化的命令行工具，集成 OpenAI ChatGPT 和本地 Ollama 服务。它能够：[1]

* 自动生成符合需求的 Shell 命令
* 详细解析命令参数，并以友好样式呈现
* 支持即时执行或预览模式，安全可靠
* 支持多种 AI 服务（OpenAI API 和本地 Ollama）
* 灵活切换不同的 AI 服务配置

适用于频繁需要查找和组合常用命令的开发者、运维工程师和终端达人。(才不是)  
适用于一时想不起该用什么指令的健忘的人

---

**ai** is a highly intelligent command-line tool integrated with OpenAI ChatGPT API and local Ollama services. It can:[1]

* Automatically generate Shell commands that meet your requirements
* Provide detailed parameter explanations with user-friendly formatting
* Support instant execution or preview mode, safe and reliable
* Support multiple AI services (OpenAI API and local Ollama)
* Flexibly switch between different AI service configurations

Suitable for developers, DevOps engineers, and terminal enthusiasts who frequently need to look up and combine common commands. (Not really)  
Perfect for forgetful people who can't remember what command to use

---

## 核心功能 / Core Features

1. **config** — 交互式配置 OpenAI 或 Ollama 服务 / Interactive configuration for OpenAI or Ollama services[1]
2. **use** — 快速切换当前使用的 AI 服务 / Quickly switch between AI services[1]
3. **ask** — 为目标提供可运行命令及参数说明，支持确认后执行 / Provide runnable commands with parameter explanations, execute after confirmation[1]

---

## 安装指南 / Installation Guide

### 方法一 / Method 1
```bash
git clone https://github.com/your-username/ai-cmd.git
cd ai-cmd
pip install -e .
```

### 方法二 / Method 2
```bash
pip install git+https://github.com/your-username/ai-cmd.git
```

---

## 快速入门 / Quick Start

### 1. 配置 AI 服务 / Configure AI Services

**交互式配置 / Interactive Configuration:**
```bash
ai config
```

该命令会引导你完成配置：[1]
- 选择服务类型（OpenAI 或 Ollama）
- 输入相应的 API Key 或服务地址
- 选择要使用的模型

This command will guide you through the configuration:[1]
- Choose service type (OpenAI or Ollama)
- Enter corresponding API Key or service address
- Select the model to use

**OpenAI 配置示例 / OpenAI Configuration Example:**
- API Key: `sk-your-openai-api-key`
- 模型选择 / Model Options: `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`

**Ollama 配置示例 / Ollama Configuration Example:**
- 服务地址 / Service URL: `http://localhost:11434/v1`
- 模型名称 / Model Name: `llama3`

配置将被存储在 `~/.ai_cli_tool_config.json`。[1]

The configuration will be stored in `~/.ai_cli_tool_config.json`.[1]

### 2. 服务切换 / Service Switching

```bash
# 切换到 OpenAI 服务 / Switch to OpenAI service
ai use openai

# 切换到 Ollama 服务 / Switch to Ollama service
ai use ollama
```

### 3. 交互模式 (ask) / Interactive Mode (ask)

```bash
ai ask 查找当前目录下所有 Python 文件
# or
ai ask find all Python files in current directory
```

**流程 / Process:**[1]
1. AI 分析需求并生成命令 / AI analyzes requirements and generates commands
2. 显示建议命令及详细参数说明 / Display suggested command with detailed parameter explanations
3. 输入 `go` 确认后执行该命令 / Type `go` to confirm and execute the command

---

## 样例演示 / Example Demo

### 中文示例 / Chinese Example
```bash
$ ai ask 压缩当前目录为 archive.tar.gz

🤖 正在请求 AI 生成命令，请稍候...

✨ 建议命令:
   tar -czvf archive.tar.gz .

📖 命令说明:
【命令】
tar -czvf archive.tar.gz .

【解释】
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
【命令】
find . -name "*.py" -exec wc -l {} + | tail -1

【解释】
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

支持两种 AI 服务 / Supports two AI services:[1]

### OpenAI API
支持的模型 / Supported Models:
- `gpt-4o` - 最新的 GPT-4 Omni 模型
- `gpt-4o-mini` - 轻量版 GPT-4 Omni 模型  
- `gpt-3.5-turbo` - GPT-3.5 Turbo 模型

### Ollama (本地部署 / Local Deployment)
```bash
# 首先启动 Ollama 服务 / First start Ollama service
ollama serve

# 拉取模型 / Pull model
ollama pull llama3

# 使用工具配置 / Configure with tool
ai config
# 选择 ollama，输入服务地址和模型名称
# Select ollama, enter service address and model name
```

### 多服务管理 / Multi-Service Management

```bash
# 查看当前激活的服务 / Check currently active service
ai config

# 快速切换服务 / Quick service switching
ai use openai  # 切换到 OpenAI
ai use ollama  # 切换到 Ollama
```

---

## 安全特性 / Security Features

* ⚠️ **命令确认** / **Command Confirmation**: 所有命令执行前都需要用户确认 / All commands require user confirmation before execution[1]
* 🔍 **命令预览** / **Command Preview**: 显示完整命令和参数说明 / Display complete command and parameter explanations[1]
* 📁 **本地配置** / **Local Configuration**: 配置文件存储在用户主目录 / Configuration file stored in user home directory[1]
* 🛡️ **安全警告** / **Security Warning**: 执行前显示安全提示 / Display security warnings before execution[1]

---

## 高级用法 / Advanced Usage

### 命令行参数 / Command Line Arguments

```bash
# 默认使用 ask 命令 / Default to ask command
ai 查找大文件
ai find large files

# 显式使用 ask 命令 / Explicitly use ask command  
ai ask 创建新的 Git 仓库
ai ask create new Git repository

# 配置管理 / Configuration management
ai config          # 交互式配置 / Interactive configuration
ai use openai      # 切换服务 / Switch service
ai use ollama
```

### 错误处理 / Error Handling

工具具有完善的错误处理机制：[1]
- 配置文件损坏时自动重置
- API 调用失败时显示详细错误信息
- 服务配置不完整时提供修复建议

The tool has comprehensive error handling:[1]
- Automatically reset when configuration file is corrupted
- Display detailed error messages when API calls fail
- Provide repair suggestions when service configuration is incomplete

---

## 开发与贡献 / Development & Contributing

欢迎提交 Issue、Pull Request 或参与讨论，共同完善功能和多语言支持。

We welcome Issues, Pull Requests, and discussions to improve features and multi-language support.

### 开发环境 / Development Environment
```bash
git clone https://github.com/your-username/ai-cmd.git
cd ai-cmd
pip install -e .
python -m ai --help
```

### 项目结构 / Project Structure
- `AIHelper` 类：核心 AI 服务调用逻辑 / Core AI service calling logic[1]
- `load_config_data` / `save_config_data`：配置文件管理 / Configuration file management[1]
- `extract_command_from_response`：智能命令解析 / Intelligent command parsing[1]
- `confirm_and_execute`：安全执行确认 / Safe execution confirmation[1]

---

## 故障排除 / Troubleshooting

### 常见问题 / Common Issues

**Q: 提示未设置当前使用的服务？**  
A: 运行 `ai config` 进行初始配置，或使用 `ai use ` 激活已有配置。[1]

**Q: API 调用失败？**  
A: 检查网络连接、API Key 是否有效，或 Ollama 服务是否正常运行。

**Q: 配置文件损坏？**  
A: 删除 `~/.ai_cli_tool_config.json` 文件，重新运行 `ai config` 配置。

---

## 协议许可 / License

本项目遵循 MIT 协议，详情见 [LICENSE](LICENSE)。

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**让 AI 驱动你的终端，命令行从此更高效！**  
**Let AI drive your terminal, making command line more efficient!**

> 基于现代 AI 技术，让每个人都能轻松驾驭命令行  
> Based on modern AI technology, making command line accessible to everyone
