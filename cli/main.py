#!/usr/bin/env python3
import os
import json
import subprocess
import click
from click import UNPROCESSED
from openai import OpenAI
import re
from typing import Tuple, Optional, Dict, Any
import threading
import queue

# 将配置文件路径定义为常量
CONFIG_PATH = os.path.expanduser("~/.ai_cli_tool_config.json")

class AIHelper:
    """AI助手类，封装API调用和配置管理"""
    
    def __init__(self):
        """
        初始化AIHelper，加载配置并根据配置创建OpenAI客户端。
        """
        self.config = self._load_config()
        self.model = self.config.get('model')
        
        # 关键改动：使用配置中的 base_url 初始化客户端
        # 如果 base_url 为 None，则会使用默认的 OpenAI API 地址
        try:
            self.client = OpenAI(
                api_key=self.config.get('api_key'),
                base_url=self.config.get('base_url')
            )
        except Exception as e:
            raise click.ClickException(f"创建 OpenAI 客户端失败: {e}")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件。如果文件或关键配置不存在，则会抛出异常。
        """
        if not os.path.exists(CONFIG_PATH):
            raise click.ClickException(f'未找到配置文件 ({CONFIG_PATH})，请先运行 `ai config` 进行设置。')
        
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise click.ClickException(f'读取配置文件失败: {e}')

        # 检查关键配置是否存在
        if not config_data.get('model'):
             raise click.ClickException('配置文件中缺少模型名称 (model)，请运行 `ai config --model <your-model-name>` 设置。')
        
        # 对于非Ollama的默认API，API Key是必需的
        if not config_data.get('base_url') and not config_data.get('api_key'):
            raise click.ClickException('未配置 API endpoint 时，必须提供 API Key。请运行 `ai config --key <your-key>`。')

        return config_data

    def get_command(self, user_input: str, explain: bool = False) -> str:
        """
        调用AI获取命令。
        """
        if not self.model:
            raise click.ClickException("模型名称未配置，无法调用 API。")

        system_msg = (
            "你是一个命令行大师，接受用户的功能目标描述，返回实现该功能的命令。"
            + ("并对每个参数做详细解释，输出格式要对控制台友好。" if explain else "只返回命令，不要包含任何额外的解释或markdown标记。")
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_msg},
                    {'role': 'user', 'content': user_input}
                ]
            )
            # 修复：添加缺失的索引访问
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise click.ClickException(f'调用 AI API 失败: {e}')

def execute_command(cmd: str) -> None:
    """
    以安全的方式执行系统命令，支持实时输出。
    """
    click.echo(click.style(f"\n▶️  执行: {cmd}", fg='cyan'))
    try:
        # 使用 subprocess.run 替代 Popen 避免死锁问题
        result = subprocess.run(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # 打印标准输出
        if result.stdout:
            click.echo(result.stdout)
        
        # 打印标准错误
        if result.stderr:
            click.echo(click.style(result.stderr, fg='red'), err=True)
            
        # 显示退出码（如果非零）
        if result.returncode != 0:
            click.echo(click.style(f"命令退出码: {result.returncode}", fg='yellow'))

    except Exception as e:
        raise click.ClickException(f'执行命令失败: {e}')

def parse_user_input(ctx, prompt) -> str:
    """解析用户输入"""
    args = list(prompt) + ctx.args
    if not args:
        raise click.ClickException('请提供功能目标描述。')
    return ' '.join(args)

def extract_command_from_response(output: str) -> Tuple[str, str]:
    """
    从AI响应中提取命令和说明。
    此函数现在更加健壮，能正确处理代码块。
    """
    # 修复：改进代码块匹配的正则表达式
    code_block_match = re.search(r'``````', output, re.DOTALL)
    if code_block_match:
        cmd = code_block_match.group(1).strip()
        explanation = output.replace(code_block_match.group(0), '', 1).strip()
        return cmd, explanation
    
    # 匹配行内代码 `ls -l`
    inline_match = re.search(r'`([^`]+)`', output)
    if inline_match:
        cmd = inline_match.group(1).strip()
        explanation = output.replace(inline_match.group(0), '', 1).strip()
        return cmd, explanation
    
    # 回退到第一行作为命令，其余作为解释
    lines = output.splitlines()
    cmd = lines[0].strip() if lines else ""
    explanation = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
    return cmd, explanation

def confirm_and_execute(cmd: str, explanation: Optional[str] = None):
    """
    向用户显示命令和说明，并请求确认后执行。
    """
    if not cmd:
        click.echo(click.style("AI 未能生成有效命令。", fg='yellow'))
        return

    # 显示建议命令
    click.echo('\n' + click.style('✨ 建议命令:', bold=True))
    click.echo(click.style(f"   {cmd}", fg='green') + '\n')
    
    if explanation:
        click.echo(click.style('📖 命令说明:', bold=True))
        click.echo(explanation + '\n')
    
    # 强警告
    click.echo(click.style("⚠️  警告: 执行前请仔细检查命令，确保其安全无害。", fg='yellow', bold=True))
    
    # 确认执行
    confirm = click.prompt('输入 `go` 以执行, 按回车键取消', default='', show_default=False, err=True)
    if confirm.strip().lower() == 'go':
        execute_command(cmd)
    else:
        click.echo('已取消执行。')

@click.group()
def cli():
    """
    AI 命令行助手。
    
    可以通过 `ai config` 配置使用 OpenAI API 或本地 Ollama 服务。
    """
    pass

@cli.command()
@click.option('--key', help='你的 OpenAI API Key。对于 Ollama，可以忽略此项或设为任意值。')
@click.option('--endpoint', help='API 的 Endpoint URL。例如，Ollama 的地址: http://localhost:11434/v1')
@click.option('--model', help='要使用的模型名称, 例如: gpt-4o-mini 或 llama3。')
def config(key: Optional[str], endpoint: Optional[str], model: Optional[str]):
    """
    配置 API Key, Endpoint 和模型。
    
    示例:
    
    - 配置 OpenAI:
      ai config --key sk-your-key --model gpt-4o-mini
      
    - 配置 Ollama (本地):
      ai config --endpoint http://localhost:11434/v1 --model llama3
    """
    config_data = {}
    # 如果配置文件已存在，先读取现有配置
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass # 如果文件损坏，则忽略旧配置

    # 更新传入的配置项
    if key is not None:
        config_data['api_key'] = key
    if endpoint is not None:
        config_data['base_url'] = endpoint
    if model is not None:
        config_data['model'] = model

    # 保存更新后的配置
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        click.echo(click.style(f"✅ 配置已更新并保存至 {CONFIG_PATH}", fg='green'))
        click.echo(json.dumps(config_data, indent=2))
    except IOError as e:
        raise click.ClickException(f'保存配置失败: {e}')

# 安全性修复：移除了不需要确认的 `run` 命令，所有执行都需要经过 `ask`
@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('prompt', nargs=-1, type=UNPROCESSED)
@click.pass_context
def ask(ctx, prompt):
    """
    询问AI生成命令，解释并确认后执行。这是推荐的主要用法。
    """
    user_input = parse_user_input(ctx, prompt)
    try:
        click.echo("🤖 正在请求 AI 生成命令，请稍候...")
        ai_helper = AIHelper()
        output = ai_helper.get_command(user_input, explain=True)
        cmd, explanation = extract_command_from_response(output)
        
        confirm_and_execute(cmd, explanation)

    except click.ClickException as e:
        click.echo(click.style(f"错误: {e}", fg='red'), err=True)
    except Exception as e:
        click.echo(click.style(f"发生未知错误: {e}", fg='red'), err=True)

if __name__ == '__main__':
    cli()
