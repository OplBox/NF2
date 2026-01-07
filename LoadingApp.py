import time, sys, os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
import Config

console = Console()

def run_loading():
    console.clear()
    theme = Config.get_theme()
    
    art = f"""
[{theme['primary']}]  __  __ ______ ___  [/]
[{theme['primary']}] |  \/  |  ____|__ \ [/]
[{theme['secondary']}] | \  / | |__     ) |[/]
[{theme['secondary']}] | |\/| |  __|   / / [/]
[{theme['primary']}] | |  | | |     / /_ [/]
[{theme['primary']}] |_|  |_|_|    |____|[/]
    """
    console.print(art, justify="center")
    console.print(f"[{theme['secondary']}]Minecraft Mods For Fabric v1.6.3[/]\n", justify="center")

    with Progress(
        SpinnerColumn(style=theme["primary"]),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None, style=theme["secondary"], complete_style=theme["primary"]),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Initializing Engine...", total=100)
        for step in ["Loading Core...", "Syncing Themes...", "Checking Projects...", "Ready!"]:
            progress.update(task, description=step, advance=25)
            time.sleep(0.4)
            
    import MainApp
    MainApp.main_menu()

if __name__ == "__main__":
    run_loading()