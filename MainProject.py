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
    info = {"name": "Unknown", "id": "unknown", "version": "0.0.0"}
    if os.path.exists(f):
        try:
            with open(f, 'r') as file:
                d = json.load(file)
                info["name"] = d.get("name", "Unknown")
                info["id"] = d.get("id", "unknown")
                info["version"] = d.get("version", "0.0.0")
        except: pass
    return info

def run(project_id):
    path = os.path.join(PROJECTS_DIR, project_id)
    while True:
        console.clear()
        theme = Config.get_theme()
        info = get_mod_info(path)
        
        # Шапка Workbench
        head = Table.grid(expand=True)
        head.add_row(Text(f" 🛠️ WORKBENCH: {project_id}", style="bold white"), Text("MC: 1.21.11 ", style="white"))
        console.print(Panel(head, style=f"white on {theme['primary']}", box=box.SQUARE))
        
        # Инфо-панель
        info_table = Table.grid(expand=True)
        info_table.add_row(f"[bold]Name:[/]{info['name']}", f"[bold]ID:[/]{info['id']}")
        info_table.add_row(f"[bold]Version:[/]{info['version']}", f"[bold]Path:[/]{'~/mf2_projects/'}{project_id}")
        console.print(Panel(info_table, border_style=theme['secondary'], title="Project Metadata"))

        # Сетка инструментов
        grid = Table(show_header=False, expand=True, box=box.ROUNDED, border_style=theme['secondary'])
        grid.add_column(); grid.add_column()
        grid.add_row(
            f"[{theme['primary']}]1[/] 🔨 [bold]Build[/]\n[dim]Компиляция JAR[/]",
            f"[{theme['primary']}]2[/] 📝 [bold]Config[/]\n[dim]fabric.mod.json[/]"
        )
        grid.add_row(
            f"[{theme['primary']}]3[/] ☕ [bold]Code[/]\n[dim]Java Исходники[/]",
            f"[{theme['primary']}]4[/] ⚙️  [bold]Gradle[/]\n[dim]Настройки сборки[/]"
        )
        console.print(grid)

        console.print(f" [bold {theme['error']}]0[/] ⬅ Назад | [bold {theme['primary']}]9[/] 🏠 Меню | [bold {theme['error']}]00[/] 🚪 Выход")
        
        choice = Prompt.ask(f"\n[{theme['primary']}]IDE[/] > Action", default="1")
        if choice == "00": sys.exit()
        if choice == "0": return "BACK"
        if choice == "9": return "HOME"
        
        if choice == "1":
            os.system(f"cd {path} && ./gradlew build")
            Prompt.ask("\nНажмите Enter...")
        elif choice in ["2", "4"]:
            f_name = "gradle.properties" if choice == "4" else "src/main/resources/fabric.mod.json"
            os.system(f"nano {os.path.join(path, f_name)}")
