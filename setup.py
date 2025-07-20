#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import zipfile
import shutil

class ReaperBuilder:
    def __init__(self):
        self.plugins_installed = False
        self.lang = "en"
        
    def language_menu(self):
        """Display language selection menu"""
        while True:
            print()
            print("----------")
            print("(1) German")
            print("----------")
            try:
                choice = input("Choose Language: ").strip()
                if choice == "1":
                    self.lang = "en"
                    break
                elif choice == "2":
                    self.lang = "de"
                    break
                else:
                    continue
            except KeyboardInterrupt:
                sys.exit(0)
    
    def main_menu(self):
        """Display main menu"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print()
            print("(1) Build")
            print("(2) Language Menu")
            print()
            try:
                choice = input("Input: ").strip()
                if choice == "1":
                    self.build()
                elif choice == "2":
                    self.language_menu()
                else:
                    continue
            except KeyboardInterrupt:
                sys.exit(0)
    
    def build(self):
        """Build confirmation and process"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Do you want to build your Reaper? (Y/N)")
        try:
            confirm = input().strip().upper()
            if confirm in ["J", "Y"]:
                self.extract()
            else:
                return
        except KeyboardInterrupt:
            sys.exit(0)
    
    def extract(self):
        """Extract packages and install plugins"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Extracting...")
        
        # Extract packages.zip using Python's zipfile module
        try:
            if os.path.exists("packages.zip"):
                with zipfile.ZipFile("packages.zip", 'r') as zip_ref:
                    zip_ref.extractall(".")
                os.remove("packages.zip")
                print("Packages extracted successfully.")
            else:
                print("packages.zip not found!")
        except Exception as e:
            print(f"Error extracting packages: {e}")
        
        print("Installing plugins...")
        time.sleep(2)
        
        # Check if plugins folder exists and install packages
        if os.path.exists("plugins"):
            print("Installing Python packages...")
            # Install packages using pip with the tar.gz files from plugins folder
            packages = [
                "plugins/colored-2.3.0.tar.gz",
                "plugins/discord_webhook-1.4.1.tar.gz", 
                "plugins/numpy-2.2.4.tar.gz",
                "plugins/requests-2.32.3.tar.gz"
            ]
            
            # Check which packages are already installed
            installed_check = subprocess.run([
                sys.executable, "-c", 
                "import subprocess; subprocess.run(['pip', 'show', 'requests', 'discord_webhook', 'colored', 'numpy'])"
            ], capture_output=True)
            
            # If not all packages are installed, install from tar.gz files
            if installed_check.returncode != 0:
                for package in packages:
                    if os.path.exists(package):
                        try:
                            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                         check=True, capture_output=True)
                            print(f"Installed: {os.path.basename(package)}")
                        except subprocess.CalledProcessError as e:
                            print(f"Failed to install {package}: {e}")
            
            print("Plugins installed successfully.")
            
            # Remove plugins directory
            try:
                shutil.rmtree("plugins")
                print("Cleaned up plugins directory.")
            except Exception as e:
                print(f"Could not remove plugins directory: {e}")
        else:
            print("No plugins to install. Skipping plugin installation...")
        
        print("Building Reaper...")
        time.sleep(5)
        
        # Start the start.bat file
        try:
            if os.path.exists("start.bat"):
                if os.name == 'nt':  # Windows
                    subprocess.Popen(["start.bat"], shell=True)
                else:  # Unix-like systems
                    subprocess.Popen(["./start.bat"])
                print("Started start.bat")
            else:
                print("start.bat not found!")
        except Exception as e:
            print(f"Error starting start.bat: {e}")
        
        # Exit the program
        sys.exit(0)

def main():
    """Main function"""
    # Set console title (Windows only)
    if os.name == 'nt':
        os.system("title Reaper Builder")
    
    # Create ReaperBuilder instance and start
    builder = ReaperBuilder()
    builder.language_menu()
    builder.main_menu()

if __name__ == "__main__":
    main()