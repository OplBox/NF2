import os
import sys
import json
import subprocess
import glob
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from rich.text import Text

# Подключаем наши модули настроек
try:
    import Config
    import Resources
except ImportError:
    # Заглушка, если модули еще не созданы
    class Config:
        @staticmethod
        def get_theme(): return {"primary": "green", "secondary": "cyan", "border": "green", "warning": "yellow", "error": "red"}
        @staticmethod
        def get_text(key): return key # Просто возвращаем ключ, если нет перевода
    class Resources: pass

console = Console()
PROJECTS_DIR = os.path.expanduser("~/mf2_projects")

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def get_mod_info(project_path):
    """Читает данные из fabric.mod.json для отображения в меню"""
    json_path = os.path.join(project_path, "src", "main", "resources", "fabric.mod.json")
    info = {
        "name": "Unknown",
        "id": "unknown",
        "version": "0.0.0",
        "desc": "No description"
    }
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                info["name"] = data.get("name", info["name"])
                info["id"] = data.get("id", info["id"])
                info["version"] = data.get("version", info["version"])
                info["desc"] = data.get("description", info["desc"])
        except: pass
    return info

def check_build_status(project_path):
    """Проверяет наличие .jar файла"""
    libs_dir = os.path.join(project_path, "build", "libs")
    if os.path.exists(libs_dir):
        jars = glob.glob(os.path.join(libs_dir, "*.jar"))
        # Ищем релизный файл (без -sources и -dev)
        release_jars = [j for j in jars if "-sources" not in j and "-dev" not in j]
        if release_jars:
            return f"[green]✔ Ready[/] ({os.path.basename(release_jars[0])})"
    return "[dim]Not built yet[/]"

def get_mc_version(project_path):
    """Читает версию MC из gradle.properties"""
    props_path = os.path.join(project_path, "gradle.properties")
    if os.path.exists(props_path):
        with open(props_path, 'r') as f:
            for line in f:
                if "minecraft_version" in line and "=" in line:
                    return line.split("=")[1].strip()
    return "?"

# --- ДЕЙСТВИЯ ---

def build_project(project_path):
    theme = Config.get_theme()
    console.clear()
    console.print(Panel(f"[{theme['warning']}]🔨 Building Project...[/]", border_style=theme['warning']))
    
    # Права на выполнение
    gradlew = os.path.join(project_path, "gradlew")
    if os.path.exists(gradlew):
        os.chmod(gradlew, 0o755)
    
    # Запуск сборки
    cmd = f"cd {project_path} && ./gradlew build"
    try:
        # os.system выводит лог прямо в консоль
        res = os.system(cmd)
        
        if res == 0:
            console.print("\n[bold green]✅ BUILD SUCCESSFUL![/]")
        else:
            console.print("\n[bold red]❌ BUILD FAILED[/]")
            console.print(f"[{theme['warning']}]Подсказка: Для 1.21+ убедись, что loader_version >= 0.18.4[/]")
    except Exception as e:
        console.print(f"[{theme['error']}]Error: {e}[/]")
    
    Prompt.ask("\n[dim]Press Enter...[/]")

def edit_config_menu(project_path):
    """Меню выбора конфига для редактирования"""
    while True:
        console.clear()
        theme = Config.get_theme()
        console.print(Panel(f"[bold {theme['secondary']}]📝 Configuration Editor[/]", border_style=theme['secondary']))
        console.print("[1] Edit fabric.mod.json (Info)")
        console.print("[2] Edit gradle.properties (Versions)")
        console.print("[0] Back")
        
        choice = Prompt.ask("Select", choices=["0", "1", "2"])
        if choice == "0": break
        
        editor = "nano" # Можно заменить на 'vim' или 'micro' если есть
        
        if choice == "1":
            f = os.path.join(project_path, "src", "main", "resources", "fabric.mod.json")
            if os.path.exists(f):
                os.system(f"{editor} {f}")
            else:
                console.print(f"[{theme['error']}]File not found: {f}[/]")
                time.sleep(1)
            
        elif choice == "2":
            f = os.path.join(project_path, "gradle.properties")
            if os.path.exists(f):
                os.system(f"{editor} {f}")
            else:
                console.print(f"[{theme['error']}]File not found: {f}[/]")
                time.sleep(1)

# --- ГЛАВНЫЙ ЦИКЛ ПРОЕКТА ---

def run(project_id):
    project_path = os.path.join(PROJECTS_DIR, project_id)
    theme = Config.get_theme()
    
    while True:
        console.clear()
        
        # 1. Данные
        mod_info = get_mod_info(project_path)
        mc_ver = get_mc_version(project_path)
        status = check_build_status(project_path)
        
        # 2. Шапка (Header)
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column(justify="right")
        
        left = Text()
        left.append(f"{mod_info['name']}", style=f"bold {theme['primary']}")
        left.append(f" v{mod_info['version']}", style="dim white")
        left.append(f"\nID: {mod_info['id']}", style="dim white")
        
        right = Text()
        right.append(f"MC: {mc_ver}\n", style=theme['warning'])
        right.append(f"Status: {status}", style="white")
        
        grid.add_row(left, right)
        
        console.print(Panel(
            grid, 
            title=f"[bold]WORKBENCH: {project_id}[/]",
            subtitle="MF2 Framework",
            border_style=theme['border']
        ))
        
        # 3. Таблица действий
        menu = Table(show_header=False, box=box.ROUNDED, expand=True, border_style=theme['secondary'])
        menu.add_column("Key", style=f"bold {theme['primary']}", width=4)
        menu.add_column("Action", style="bold white")
        menu.add_column("Desc", style="dim white")
        
        menu.add_row("1", "🔨 Build Mod", "Собрать проект")
        menu.add_row("2", "📝 Edit Configs", "Изменить настройки")
        menu.add_row("3", "📦 Dependencies", "Управление зависимостями (WIP)")
        menu.add_section()
        menu.add_row("0", "⬅ Back", "В список проектов")
        menu.add_row("00", "🚪 Exit", "Выход из программы")
        
        console.print(menu)
        
        # 4. Выбор
        choice = Prompt.ask("\nAction", default="1")
        
        if choice == "1":
            build_project(project_path)
        elif choice == "2":
            edit_config_menu(project_path)
        elif choice == "0":
            return "BACK"
        elif choice == "00":
            console.print(f"[{theme['error']}]Bye![/]")
            sys.exit()
        else:
            console.print(f"[{theme['error']}]Invalid choice[/]")
            time.sleep(1)
