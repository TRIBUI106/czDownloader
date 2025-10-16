#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CZ Video Downloader v2.0 - Launcher
Smart launcher with dependency management
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import importlib.util

class DependencyInstaller:
    """Smart dependency installer with progress UI"""
    
    def __init__(self):
        self.root = None
        self.progress_window = None
        self.progress_var = None
        self.status_var = None
        
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        required_modules = {
            'yt_dlp': 'yt-dlp',
            'requests': 'requests', 
            'PIL': 'Pillow'
        }
        
        missing = []
        for module_name, package_name in required_modules.items():
            if not self.is_module_available(module_name):
                missing.append(package_name)
                
        return missing
        
    def is_module_available(self, module_name):
        """Check if a module is available for import"""
        try:
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except (ImportError, AttributeError, ValueError):
            return False
            
    def install_dependencies(self, packages):
        """Install missing dependencies with GUI"""
        if not packages:
            return True
            
        try:
            # Create root window if needed
            if self.root is None:
                self.root = tk.Tk()
                self.root.withdraw()
                
            # Create progress window
            self.create_progress_window(packages)
            
            # Install in background thread
            install_thread = threading.Thread(target=self.install_worker, args=(packages,))
            install_thread.daemon = True
            install_thread.start()
            
            # Show progress window
            self.progress_window.mainloop()
            
            # Clean up
            if self.root:
                self.root.destroy()
                self.root = None
            
            return hasattr(self, 'install_success') and self.install_success
            
        except Exception as e:
            print(f"Warning: GUI installation failed: {e}")
            print("Falling back to command line installation...")
            return self.install_packages_cli(packages)
        
    def create_progress_window(self, packages):
        """Create installation progress window"""
        try:
            # Create root if not exists
            if self.root is None:
                self.root = tk.Tk()
                self.root.withdraw()
                
            self.progress_window = tk.Toplevel(self.root)
            self.progress_window.title("Installing Dependencies")
            self.progress_window.geometry("500x200")
            self.progress_window.resizable(False, False)
            self.progress_window.grab_set()
            
            # Center window
            self.progress_window.update_idletasks()
            x = (self.progress_window.winfo_screenwidth() // 2) - 250
            y = (self.progress_window.winfo_screenheight() // 2) - 100
            self.progress_window.geometry(f"500x200+{x}+{y}")
            
        except Exception as e:
            print(f"Warning: Could not create progress window: {e}")
            # Create a simple root window instead
            self.progress_window = tk.Tk()
            self.progress_window.title("Installing Dependencies")
            self.progress_window.geometry("500x200")
            
        # Main frame
        main_frame = ttk.Frame(self.progress_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔧 Installing Required Dependencies", 
                               font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Package list
        packages_text = "Installing: " + ", ".join(packages)
        packages_label = ttk.Label(main_frame, text=packages_text, 
                                  font=("Segoe UI", 10))
        packages_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                     maximum=100, length=400)
        progress_bar.pack(pady=(0, 10))
        
        # Status
        self.status_var = tk.StringVar(value="Preparing installation...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Segoe UI", 9))
        status_label.pack()
        
    def install_worker(self, packages):
        """Worker thread for installing packages"""
        try:
            total_packages = len(packages)
            
            for i, package in enumerate(packages):
                # Update progress
                progress = (i / total_packages) * 90  # Reserve 10% for completion
                self.progress_var.set(progress)
                self.status_var.set(f"Installing {package}...")
                
                # Install package
                cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    self.status_var.set(f"Failed to install {package}")
                    self.install_success = False
                    self.progress_window.after(2000, self.progress_window.destroy)
                    return
                    
            # Completion
            self.progress_var.set(100)
            self.status_var.set("✅ All dependencies installed successfully!")
            self.install_success = True
            
            # Close window after delay
            self.progress_window.after(1500, self.progress_window.destroy)
            
        except subprocess.TimeoutExpired:
            self.status_var.set("❌ Installation timeout")
            self.install_success = False
            self.progress_window.after(2000, self.progress_window.destroy)
        except Exception as e:
            self.status_var.set(f"❌ Installation error: {str(e)}")
            self.install_success = False
            self.progress_window.after(2000, self.progress_window.destroy)
            
    def install_packages_cli(self, packages):
        """Fallback: install packages via command line"""
        try:
            print("Installing packages via command line...")
            for package in packages:
                print(f"Installing {package}...")
                cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    print(f"Failed to install {package}: {result.stderr}")
                    return False
                else:
                    print(f"✅ {package} installed successfully")
                    
            return True
            
        except Exception as e:
            print(f"CLI installation failed: {e}")
            return False

def show_welcome_dialog():
    """Show welcome dialog"""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        welcome_text = """🎬 Welcome to CZ Video Downloader v2.0!

This is the modern version with enhanced features:
• Beautiful modern interface
• Multi-URL queue system  
• Individual progress tracking for each video
• Dark/Light theme support
• Batch downloads
• Support for YouTube, Facebook, TikTok, Instagram

The application will now check and install any missing dependencies."""
        
        messagebox.showinfo("CZ Video Downloader v2.0", welcome_text)
        root.destroy()
    except Exception as e:
        print(f"Warning: Could not show welcome dialog: {e}")
        # Continue without dialog

def main():
    """Main launcher function"""
    print("🎬 CZ Video Downloader v2.0 - Starting...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        if tk:
            messagebox.showerror("Python Version Error", 
                               "Python 3.7 or higher is required!\n" +
                               "Please upgrade your Python installation.")
        return False
        
    # Show welcome dialog
    show_welcome_dialog()
    
    # Initialize dependency installer
    installer = DependencyInstaller()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing_packages = installer.check_dependencies()
    
    if missing_packages:
        print(f"📦 Missing packages: {missing_packages}")
        
        # Ask user for permission to install
        root = tk.Tk()
        root.withdraw()
        
        install_msg = f"""Missing required dependencies:
{', '.join(missing_packages)}

Would you like to install them automatically?
This may take a few minutes depending on your internet connection.

Click 'Yes' to install automatically
Click 'No' to exit and install manually"""
        
        try:
            root = tk.Tk()
            root.withdraw()
            result = messagebox.askyesno("Install Dependencies", install_msg)
            root.destroy()
        except Exception as e:
            print(f"Warning: Could not show dialog: {e}")
            print("Please install dependencies manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        if not result:
            print("❌ Installation cancelled by user")
            return False
            
        # Install dependencies
        print("📦 Installing dependencies...")
        success = installer.install_dependencies(missing_packages)
        
        if not success:
            print("❌ Failed to install dependencies")
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Installation Failed", 
                                   "Failed to install required dependencies.\n\n" +
                                   "Please install them manually using:\n" +
                                   f"pip install {' '.join(missing_packages)}")
                root.destroy()
            except:
                print("Could not show error dialog")
                print(f"Please install manually: pip install {' '.join(missing_packages)}")
            return False
            
        print("✅ Dependencies installed successfully!")
        
    else:
        print("✅ All dependencies available")
        
    # Launch main application
    print("🚀 Launching CZ Video Downloader v2.0...")
    
    try:
        # Import and run the main application
        import main
        main.main()
            
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Launch Error", 
                               f"Failed to start the application:\n{e}\n\n" +
                               "Please check the installation and try again.")
            root.destroy()
        except:
            print("Could not show error dialog")
        return False
        
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPress Enter to exit...")
        sys.exit(1)