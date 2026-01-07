import os, sys, json, glob, time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import box
import Config

console = Console()
PROJECTS_DIR = os.path.expanduser("~/mf2_projects")

def get_mod_info(path):
    f = os.path.join(path, "src", "main", "resources", "fabric.mod.json")
    info = {"name": "Unknown", "version": "0.0.0"}
    if os.path.exists(f):
        try:
            with open(f, 'r') as file:
                d = json.load(file); info["name"] = d.get("name", "Unknown"); info["version"] = d.get("version", "0.0.0")
        except: pass
    return info

def run(project_id):
    path = os.path.join(PROJECTS_DIR, project_id)
    while True:
        console.clear()
        theme = Config.get_theme()
        info = get_mod_info(path)
        
        # Компактная шапка IDE
        head_grid = Table.grid(expand=True)
        head_grid.add_row(
            Text(f" WORKBENCH: {project_id}", style="bold white"),
            Text(f"MC: 1.21.11 ", style="white")
        )
        console.print(Panel(head_grid, style=f"white on {theme['primary']}", box=box.SQUARE))
        
        # Инфо-панель проекта
        info_text = Text.from_markup(f"Name: [bold]{info['name']}[/] | Version: [bold]{info['version']}[/]")
        console.print(Panel(info_text, border_style=theme['secondary']))

        # Сетка инструментов (2x2)
        grid = Table(show_header=False, expand=True, box=box.ROUNDED, border_style=theme['secondary'])
        grid.add_column(); grid.add_column()
        grid.add_row(
            f"[{theme['primary']}]1[/] 🔨 [bold]Build[/]\n[dim]Сборка JAR[/]",
            f"[{theme['primary']}]2[/] 📝 [bold]Config[/]\n[dim]Настройка JSON[/]"
        )
        grid.add_row(
            f"[{theme['primary']}]3[/] ☕ [bold]Code[/]\n[dim]Java файлы[/]",
            f"[{theme['primary']}]4[/] ⚙️  [bold]Gradle[/]\n[dim]gradle.props[/]"
        )
        console.print(grid)

        # Футер
        console.print(f" [{theme['error']}]0[/] ⬅ Back | [{theme['error']}]00[/] 🚪 Exit")
        
        choice = Prompt.ask(f"\n[{theme['primary']}]IDE[/] > Action", default="1")
        if choice == "00": sys.exit()
        if choice == "0": return "BACK"
        elif choice == "1":
            console.print("[yellow]🔨 Сборка...[/]")
            os.system(f"cd {path} && ./gradlew build")
            Prompt.ask("Enter...")
        elif choice in ["2", "4"]:
            file = "gradle.properties" if choice == "4" else "src/main/resources/fabric.mod.json"
            os.system(f"nano {os.path.join(path, file)}")