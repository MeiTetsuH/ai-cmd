#!/usr/bin/env python3
import os
import json
import subprocess
import click
from click import UNPROCESSED
from openai import OpenAI
import re
from typing import Tuple, Optional, Dict, Any

# 将配置文件路径定义为常量
CONFIG_PATH = os.path.expanduser("~/.ai_cli_tool_config.json")

# --- Helper Functions ---

def load_config_data() -> Dict[str, Any]:
    """安全地加载整个配置文件，如果不存在则返回空字典。"""
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # 如果文件损坏或无法读取，当作空配置处理
        return {}

def save_config_data(config_data: Dict[str, Any]) -> None:
    """将配置数据写入文件。"""
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        click.echo(click.style(f"✅ 配置已保存至 {CONFIG_PATH}", fg='green'))
    except IOError as e:
        raise click.ClickException(f'保存配置失败: {e}')

# --- Core Logic Class ---

class AIHelper:
    """AI助手类，封装API调用和配置管理"""
    
    def __init__(self):
        """初始化AIHelper，加载并验证当前激活服务的配置，然后创建OpenAI客户端。"""
        self.config = self._load_active_config()
        self.model = self.config.get('model')
        
        try:
            self.client = OpenAI(
                api_key=self.config.get('api_key'),
                base_url=self.config.get('base_url')
            )
        except Exception as e:
            raise click.ClickException(f"创建 OpenAI 客户端失败: {e}")
    
    def _load_active_config(self) -> Dict[str, Any]:
        """加载当前激活服务的配置。"""
        config_data = load_config_data()
        active_service = config_data.get('active_service')
        
        if not active_service:
            raise click.ClickException(
                '未设置当前使用的服务。请先运行 `ai config` 进行设置，或运行 `ai use <service>` 来激活一个已有的配置。'
            )
        
        service_config = config_data.get(active_service)
        if not service_config or not service_config.get('model'):
            raise click.ClickException(
                f'当前激活的服务 `{active_service}` 配置不完整。请运行 `ai config` 来完成配置。'
            )

        return service_config

    def get_command(self, user_input: str, explain: bool = False) -> str:
        """调用AI获取命令。"""
        system_msg = (
            "你是一个命令行大师。请严格按照以下格式提供回答，不要添加任何额外内容或Markdown标记：\n"
            "【命令】\n"
            "[这里只写命令本身]\n\n"
            "【解释】\n"
            "[这里对命令和参数进行解释]"
        ) if explain else (
            "你是一个命令行大师。请只返回用户所需功能的shell命令，不要包含任何解释、描述或Markdown标记。"
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_msg},
                    {'role': 'user', 'content': user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise click.ClickException(f'调用 AI API 失败: {e}')

# --- Command Execution & Parsing ---

def execute_command(cmd: str) -> None:
    """执行系统命令并流式输出。"""
    click.echo(click.style(f"\n▶️  执行: {cmd}", fg='cyan'))
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                click.echo(line, nl=False)
        process.wait()
        if process.stderr:
            stderr_output = process.stderr.read()
            if stderr_output:
                click.echo(click.style(stderr_output, fg='red'), err=True)
    except Exception as e:
        raise click.ClickException(f'执行命令失败: {e}')

def extract_command_from_response(output: str) -> Tuple[str, str]:
    """从AI响应中提取命令和说明。"""
    # 优先匹配【命令】和【解释】标签
    cmd_match = re.search(r'【命令】\s*(.*?)\s*【解释】', output, re.DOTALL)
    exp_match = re.search(r'【解释】\s*(.*)', output, re.DOTALL)
    
    if cmd_match and exp_match:
        cmd = cmd_match.group(1).strip()
        explanation = exp_match.group(1).strip()
        return cmd, explanation

    # 回退到旧的解析逻辑
    code_block_match = re.search(r'```(?:bash|sh)?\n(.*?)\n```', output, re.DOTALL)
    if code_block_match:
        cmd = code_block_match.group(1).strip()
        explanation = output.replace(code_block_match.group(0), '', 1).strip()
        return cmd, explanation
    
    lines = output.splitlines()
    cmd = lines[0].strip() if lines else ""
    return cmd, "\n".join(lines[1:]).strip() if len(lines) > 1 else ""


def confirm_and_execute(cmd: str, explanation: Optional[str] = None):
    """显示命令并请求确认后执行。"""
    if not cmd:
        click.echo(click.style("AI 未能生成有效命令。", fg='yellow'))
        return

    click.echo('\n' + click.style('✨ 建议命令:', bold=True))
    click.echo(click.style(f"   {cmd}", fg='green') + '\n')
    if explanation:
        click.echo(click.style('📖 命令说明:', bold=True))
        click.echo(explanation + '\n')
    
    click.echo(click.style("⚠️  警告: 执行前请仔细检查命令，确保其安全无害。", fg='yellow', bold=True))
    confirm = click.prompt('输入 `go` 以执行, 按回车键取消', default='', show_default=False, err=True)
    if confirm.strip().lower() == 'go':
        execute_command(cmd)
    else:
        click.echo('已取消执行。')

# --- Click CLI Commands ---

@click.group(help="""
AI 命令行助手。

一个可以通过AI自然语言生成并执行Shell命令的工具。
支持 OpenAI API 和本地 Ollama 服务。
""")
def cli():
    pass

@cli.command(help="通过交互式会话配置服务 (OpenAI 或 Ollama)。")
def config():
    config_data = load_config_data()
    
    # 第一步：选择服务类型
    active_service = config_data.get('active_service')
    service_type = click.prompt(
        "请选择要配置的服务类型",
        type=click.Choice(['openai', 'ollama'], case_sensitive=False),
        default=active_service
    )
    
    # 获取该服务之前的配置作为默认值
    current_service_config = config_data.get(service_type, {})

    if service_type == 'openai':
        click.echo(click.style("\n--- 正在配置 OpenAI ---", bold=True))
        api_key = click.prompt("请输入你的 OpenAI API Key", default=current_service_config.get('api_key'), hide_input=True)
        model = click.prompt(
            "请选择要使用的模型",
            type=click.Choice(['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo']),
            default=current_service_config.get('model', 'gpt-4o-mini')
        )
        config_data['openai'] = {'api_key': api_key, 'model': model, 'base_url': None}
    
    elif service_type == 'ollama':
        click.echo(click.style("\n--- 正在配置 Ollama ---", bold=True))
        base_url = click.prompt(
            "请输入 Ollama 服务的完整地址",
            default=current_service_config.get('base_url', 'http://localhost:11434/v1')
        )
        model = click.prompt(
            "请输入要使用的 Ollama 模型名称 (例如: llama3)",
            default=current_service_config.get('model')
        )
        # OpenAI SDK for Ollama still requires an api_key field, even if it's not used.
        config_data['ollama'] = {'base_url': base_url, 'model': model, 'api_key': 'ollama'}

    # 将当前配置的服务设为激活状态
    config_data['active_service'] = service_type
    
    save_config_data(config_data)
    click.echo(f"\n当前激活的服务: {click.style(service_type, fg='green', bold=True)}")

@cli.command(help="快速切换当前使用的服务。用法: ai use [openai|ollama]")
@click.argument('service', type=click.Choice(['openai', 'ollama']))
def use(service: str):
    config_data = load_config_data()
    
    if service not in config_data:
        raise click.ClickException(
            f"未找到 `{service}` 的配置。请先运行 `ai config` 来进行配置。"
        )
    
    config_data['active_service'] = service
    save_config_data(config_data)
    click.echo(f"已切换服务，当前激活: {click.style(service, fg='green', bold=True)}")


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('prompt', nargs=-1, type=UNPROCESSED)
@click.pass_context
def ask(ctx, prompt):
    """(默认命令) 询问AI生成命令，解释并确认后执行。"""
    user_input = ' '.join(list(prompt) + ctx.args)
    if not user_input:
        raise click.ClickException("请输入你的目标描述。例如: ai ask 查找当前目录下所有大于1MB的json文件")

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
