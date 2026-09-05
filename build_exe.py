#!/usr/bin/env python3
import subprocess
import sys
import os

def build_exe():
    print('Building Random Joke Generator EXE...')
    
    try:
        import PyInstaller
    except ImportError:
        print('Installing PyInstaller...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    build_cmd = ['pyinstaller', '--onefile', '--windowed', '--name=Random-Joke-Generator', '--distpath=./dist', '--buildpath=./build', 'main.py']
    
    print(f'Running: {" ".join(build_cmd)}')
    result = subprocess.run(build_cmd)
    
    if result.returncode == 0:
        print('Build successful!')
        exe_path = os.path.join('dist', 'Random-Joke-Generator.exe')
        print(f'Executable created at: {exe_path}')
    else:
        print('Build failed!')
        sys.exit(1)

if __name__ == '__main__':
    build_exe()