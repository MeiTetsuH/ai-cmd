# ai — 智能命令行助手

> 让终端更聪明：基于 ChatGPT 的交互式命令生成与执行工具

## 项目简介

**ai** 是一款高度智能化的命令行工具，集成 OpenAI ChatGPT 接口。它能够：

* 自动生成符合需求的 Shell 命令。
* 详细解析命令参数，并以友好样式呈现。
* 支持即时执行或预览模式，安全可靠。

<del>适用于频繁需要查找和组合常用命令的开发者、运维工程师和终端达人。</del>(才不是)
适用于一时想不起该用什么指令的健忘的人

---

## 核心功能

1. **config**  — 配置并安全存储 ChatGPT API Key。
2. **run**     — 根据功能描述自动生成并立即执行命令。
3. **ask**     — 为目标提供可运行命令及参数说明，支持确认后执行。

---

## 安装指南

```bash
# 克隆仓库
git clone https://github.com/kyuuseiryuu/ai-cmd.git
cd ai-cmd

# 安装依赖
# pip install -r requirements.txt
uv sync

# 添加可执行权限
chmod +x ai.py
# 或安装到系统命令路径
mv ai.py /usr/local/bin/ai
```

---

## 快速入门

### 1. 配置 API Key

首次使用前，执行：

```bash
ai config
```

输入并确认你的 OpenAI API Key，它将被<del>加密(个屁)</del>存储在 `~/.ai_config.json`。

### 2. 直接执行命令 (run)

```bash
ai run 查找当前目录下所有 Python 文件
```

自动调用 ChatGPT 生成 `find . -name "*.py"` 并执行，立即返回结果。

### 3. 交互模式 (ask)

```bash
ai ask 统计日志文件中错误行数
```

1. 显示建议命令及详细参数说明；
2. 输入 `go` 确认后执行该命令。

---

## 样例演示

````bash
$ ai ask 压缩当前目录为 archive.tar.gz

建议命令:
```bash
 tar -czvf archive.tar.gz .
```

命令说明:

* `-c`：创建档案。
* `-z`：通过 gzip 压缩。
* `-v`：显示详细过程。
* `-f`：指定输出文件。

输入 go 以执行上述命令: go

# 执行并完成压缩

````

---

## 开发与贡献

欢迎提交 Issue、Pull Request 或参与讨论，共同完善功能和多语言支持。

---

## 协议许可

本项目遵循 MIT 协议，详情见 [LICENSE](LICENSE)。

---

**让 AI 驱动你的终端，命令行从此更高效！**

> 此 README 也由 AI 自动生成

