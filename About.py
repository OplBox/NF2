import sys, os, subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import Config

console = Console()

def get_java_version():
    try:
        res = subprocess.check_output("java -version", shell=True, stderr=subprocess.STDOUT).decode()
        return res.splitlines()[0]
    except: return "Not Found"

def show_about():
    theme = Config.get_theme()
    console.clear()
    
    # 1. Лицензия и Автор
    license_text = """
[bold green]MF2 Framework v1.6.3[/]
Copyright (c) 2026 NIVILON (или твоё имя)

Лицензия: [bold cyan]MIT License[/]
Данное ПО предоставляется "как есть", без каких-либо гарантий.
Разрешено использование, копирование и модификация.
    """
    console.print(Panel(license_text, title="📜 LICENSE & IDENTITY", border_style=theme['primary']))

    # 2. Стек технологий (то что ты просил)
    table = Table(title="🛠️ SYSTEM STACK", expand=True, border_style=theme['secondary'])
    table.add_column("Компонент", style="bold")
    table.add_column("Версия / Статус")

    table.add_row("Python Engine", sys.version.split()[0])
    table.add_row("Java Development Kit", get_java_version())
    table.add_row("Fabric Loader (Target)", "0.18.4")
    table.add_row("Gradle Wrapper", "8.14")
    table.add_row("Loom Plugin", "1.11-SNAPSHOT")
    table.add_row("Environment", "Termux (Android)")

    console.print(table)
    input("\nНажмите Enter, чтобы выйти...")
