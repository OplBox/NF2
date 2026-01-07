#!/bin/bash

# Этот скрипт предназначен для первоначальной настройки окружения Termux
# для работы с генератором модов Fabric.
# Запускать его должен пользователь вручную.

echo "Настройка окружения Termux для MF2..."

# 1. Установка Python и необходимых утилит
echo "Установка базовых пакетов..."
pkg update && pkg upgrade -y
pkg install python -y
pkg install openjdk-17 -y # Java Development Kit для Gradle

# 2. Установка Python-библиотек
echo "Установка Python-библиотек (rich, requests)..."
pip install rich requests

# 3. Создание символической ссылки для команды mf2
echo "Создание команды 'mf2'..."
# Убедимся, что директория ~/mmff существует
mkdir -p ~/mmff
# Создаем обертку для запуска MainApp.py
cat << 'EOF' > ~/bin/mf2
#!/bin/bash
python ~/mmff/MainApp.py "$@"
EOF
chmod +x ~/bin/mf2

# Убедимся, что ~/bin находится в PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
  echo "Добавление $HOME/bin в PATH. Возможно, потребуется перезапустить Termux."
  echo "export PATH=\$PATH:\$HOME/bin" >> ~/.bashrc
fi

echo "Настройка завершена! Теперь вы можете запустить генератор командой 'mf2'."
echo "Возможно, потребуется перезапустить Termux, чтобы команда 'mf2' стала доступна."
