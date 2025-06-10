#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import click
from click import UNPROCESSED
from openai import OpenAI
import re

CONFIG_PATH = os.path.expanduser("~/.ai_config.json")

@click.group()
def cli():
    pass

@cli.command()
@click.option('--key', prompt='请输入 ChatGPT API Key', hide_input=True, confirmation_prompt=True, help='你的 ChatGPT API Key')
def config(key):
    data = {'api_key': key}
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        click.echo(f'API Key 已保存至 {CONFIG_PATH}')
    except Exception as e:
        click.echo(f'保存 API Key 时发生错误: {e}', err=True)
        sys.exit(1)

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('prompt', nargs=-1, type=UNPROCESSED)
@click.pass_context
def run(ctx, prompt):
    args = list(prompt) + ctx.args
    if not args:
        click.echo('请提供要执行的功能目标描述', err=True)
        sys.exit(1)
    user_input = ' '.join(args)

    if not os.path.exists(CONFIG_PATH):
        click.echo('未找到配置文件，请先运行 `ai config` 保存 API Key', err=True)
        sys.exit(1)
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            api_key = json.load(f).get('api_key')
    except Exception as e:
        click.echo(f'读取 API Key 时发生错误: {e}', err=True)
        sys.exit(1)
    if not api_key:
        click.echo('未在配置文件中找到 API Key，请重新运行 `ai config`', err=True)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    system_msg = (
        "你是一个命令行大师，"
        "你将接受用户的输入作为功能目标，返回实现该功能的命令，"
        "除了指令之外不要输出任何内容。"
    )
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'system', 'content': system_msg}, {'role': 'user', 'content': user_input}]
        )
        cmd = response.choices[0].message.content.strip()
    except Exception as e:
        click.echo(f'调用 ChatGPT API 时发生错误: {e}', err=True)
        sys.exit(1)

    click.echo(f'执行命令: {cmd}')
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)
    except Exception as e:
        click.echo(f'执行命令时发生错误: {e}', err=True)
        sys.exit(1)

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('prompt', nargs=-1, type=UNPROCESSED)
@click.pass_context
def ask(ctx, prompt):
    args = list(prompt) + ctx.args
    if not args:
        click.echo('请提供要完成的目标描述', err=True)
        sys.exit(1)
    user_input = ' '.join(args)

    if not os.path.exists(CONFIG_PATH):
        click.echo('未找到配置文件，请先运行 `ai config` 保存 API Key', err=True)
        sys.exit(1)
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            api_key = json.load(f).get('api_key')
    except Exception as e:
        click.echo(f'读取 API Key 时发生错误: {e}', err=True)
        sys.exit(1)
    if not api_key:
        click.echo('未在配置文件中找到 API Key，请重新运行 `ai config`', err=True)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    system_msg = (
        "你是一个命令行大师，"
        "你将接受用户的输入作为功能目标，返回实现该功能的命令，并对每个参数做详细解释，"
        "输出格式要对控制台友好。"
    )
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'system', 'content': system_msg}, {'role': 'user', 'content': user_input}]
        )
        output = response.choices[0].message.content.strip()
    except Exception as e:
        click.echo(f'调用 ChatGPT API 时发生错误: {e}', err=True)
        sys.exit(1)

    # 从 markdown 中提取命令
    # 优先匹配代码块
    m_block = re.search(r'```(?:bash)?\s*([\s\S]*?)\s*```', output)
    if m_block:
        cmd_to_run = m_block.group(1).strip()
        explanation_text = re.sub(r'```(?:bash)?[\s\S]*?```', '', output).strip()
    else:
        # 匹配行内代码
        m_inline = re.search(r'`([^`]+)`', output)
        if m_inline:
            cmd_to_run = m_inline.group(1).strip()
            explanation_text = re.sub(r'`[^`]+`', '', output).strip()
        else:
            # 回退到第一行
            parts = output.splitlines()
            cmd_to_run = parts[0].strip()
            explanation_text = "\n".join(parts[1:]).strip()

    click.echo('\n' + click.style('建议命令:', bold=True))
    click.echo(cmd_to_run + '\n')
    if explanation_text:
        click.echo(click.style('命令说明:', bold=True))
        click.echo(explanation_text + '\n')

    confirm = click.prompt('输入 go 以执行上述命令', default='', show_default=False)
    if confirm.strip().lower() == 'go' and cmd_to_run:
        click.echo(click.style(f'执行命令: {cmd_to_run}', fg='green'))
        try:
            result = subprocess.run(cmd_to_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                click.echo(result.stdout)
            if result.stderr:
                click.echo(result.stderr, err=True)
        except Exception as e:
            click.echo(f'执行命令时发生错误: {e}', err=True)
            sys.exit(1)
    else:
        click.echo('已取消执行。')

if __name__ == '__main__':
    cli()


