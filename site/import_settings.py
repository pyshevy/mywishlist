import os
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Добавляем путь к корневой директории в системный путь
sys.path.append(main_dir)
sys.path.append(main_dir+r'\bot')
