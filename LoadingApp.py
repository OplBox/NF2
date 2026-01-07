import time
import sys
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import ErrorHandler
import Config

# Включаем перехват ошибок
ErrorHandler.install_handler()
console = Console()

def run_loading():
    console.clear()
    theme = Config.get_theme()
    
    # Логотип (можно заменить на ASCII арт)
    console.print(f"[{theme['primary']}]MF2 Framework v1.0.0[/]", justify="center")
    console.print(f"[{theme['secondary']}]Minecraft Mods For Fabric[/]\n", justify="center")

    with Progress(
        SpinnerColumn(style=theme['primary']),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        
        # Симуляция проверки систем
        task1 = progress.add_task(f"[{theme['warning']}]Init Core...", total=100)
        time.sleep(0.5)
        progress.update(task1, completed=50)
        time.sleep(0.3)
        progress.update(task1, completed=100)

        task2 = progress.add_task(f"[{theme['warning']}]Load Config...", total=100)
        Config.load_config()
        time.sleep(0.4)
        progress.update(task2, completed=100)

        task3 = progress.add_task(f"[{theme['warning']}]Checking Updates...", total=100)
        # Тут могла бы быть проверка обновлений
        time.sleep(0.5)
        progress.update(task3, completed=100)
        
    # Запуск главного меню
    import MainApp
    MainApp.main_menu()

if __name__ == "__main__":
    run_loading()