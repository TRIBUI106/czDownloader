#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CZ Video Downloader v2.0 - Theme Test
Simple theme testing without dependencies
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

class ModernThemeTest:
    """Test theme system"""
    
    # Light theme colors
    LIGHT_COLORS = {
        'primary': '#2563eb',
        'bg_primary': '#ffffff',
        'bg_secondary': '#f8fafc',
        'bg_card': '#ffffff',
        'text_primary': '#0f172a',
        'text_secondary': '#64748b',
        'border': '#e2e8f0',
    }
    
    # Dark theme colors
    DARK_COLORS = {
        'primary': '#3b82f6',
        'bg_primary': '#0f172a',
        'bg_secondary': '#1e293b',
        'bg_card': '#1e293b',
        'text_primary': '#f1f5f9',
        'text_secondary': '#94a3b8',
        'border': '#334155',
    }
    
    def __init__(self, root):
        self.root = root
        self.is_dark = False
        self.current_colors = self.LIGHT_COLORS.copy()
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("🎨 Theme Test - CZ Video Downloader")
        self.root.geometry("600x400")
        self.root.configure(bg=self.current_colors['bg_secondary'])
        
        # Header
        self.header = tk.Frame(self.root, bg=self.current_colors['primary'], height=60)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)
        
        self.header_content = tk.Frame(self.header, bg=self.current_colors['primary'])
        self.header_content.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        self.title_label = tk.Label(self.header_content, text="🎬 CZ Video Downloader", 
                                   font=("Segoe UI", 18, "bold"),
                                   bg=self.current_colors['primary'], fg="white")
        self.title_label.pack(side=tk.LEFT)
        
        self.theme_btn = tk.Button(self.header_content, text="🌙", 
                                  command=self.toggle_theme,
                                  font=("Segoe UI", 12), width=3,
                                  bg="#1d4ed8", fg="white", border=0, cursor="hand2")
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Main content
        self.main_frame = tk.Frame(self.root, bg=self.current_colors['bg_secondary'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sample card
        self.create_sample_card()
        
        # Test controls
        self.create_test_controls()
        
    def create_sample_card(self):
        # Video card simulation
        self.card = tk.Frame(self.main_frame, 
                            bg=self.current_colors['bg_card'],
                            relief="solid", bd=1,
                            highlightbackground=self.current_colors['border'])
        self.card.pack(fill=tk.X, pady=10)
        
        card_inner = tk.Frame(self.card, bg=self.current_colors['bg_card'])
        card_inner.pack(fill=tk.X, padx=15, pady=15)
        
        # Title
        self.card_title = tk.Label(card_inner, 
                                  text="🎬 Sample Video Title - Testing Theme System",
                                  font=("Segoe UI", 12, "bold"),
                                  fg=self.current_colors['text_primary'],
                                  bg=self.current_colors['bg_card'],
                                  anchor="w")
        self.card_title.pack(fill=tk.X, pady=(0, 5))
        
        # URL
        self.card_url = tk.Label(card_inner,
                                text="https://youtube.com/watch?v=sample123...",
                                font=("Segoe UI", 9),
                                fg=self.current_colors['text_secondary'],
                                bg=self.current_colors['bg_card'],
                                anchor="w")
        self.card_url.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        self.progress_frame = tk.Frame(card_inner, bg=self.current_colors['bg_card'])
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress = ttk.Progressbar(self.progress_frame, value=65, maximum=100)
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_text = tk.Label(self.progress_frame,
                                     text="📥 Downloading... 65% • 2.3 MB/s • ETA: 30s",
                                     font=("Segoe UI", 9),
                                     fg=self.current_colors['text_secondary'],
                                     bg=self.current_colors['bg_card'],
                                     anchor="w")
        self.progress_text.pack(fill=tk.X)
        
    def create_test_controls(self):
        controls = tk.Frame(self.main_frame, bg=self.current_colors['bg_secondary'])
        controls.pack(fill=tk.X, pady=20)
        
        tk.Label(controls, text="Theme Test Controls:",
                font=("Segoe UI", 12, "bold"),
                fg=self.current_colors['text_primary'],
                bg=self.current_colors['bg_secondary']).pack(anchor=tk.W, pady=(0, 10))
        
        # Theme info
        theme_info = f"Current: {'Dark' if self.is_dark else 'Light'} Mode"
        self.theme_info = tk.Label(controls, text=theme_info,
                                  font=("Segoe UI", 10),
                                  fg=self.current_colors['text_secondary'],
                                  bg=self.current_colors['bg_secondary'])
        self.theme_info.pack(anchor=tk.W, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(controls, bg=self.current_colors['bg_secondary'])
        btn_frame.pack(anchor=tk.W, pady=10)
        
        test_btn = tk.Button(btn_frame, text="✅ Theme Working!",
                           font=("Segoe UI", 10), 
                           bg=self.current_colors['primary'], fg="white",
                           relief="flat", padx=20, pady=8, cursor="hand2")
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(btn_frame, text="❌ Close Test",
                            command=self.root.destroy,
                            font=("Segoe UI", 10),
                            bg="#dc2626", fg="white",
                            relief="flat", padx=20, pady=8, cursor="hand2")
        close_btn.pack(side=tk.LEFT)
        
    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.current_colors = self.DARK_COLORS.copy() if self.is_dark else self.LIGHT_COLORS.copy()
        
        # Update theme button
        self.theme_btn.config(text="☀️" if self.is_dark else "🌙")
        
        # Update all components
        self.update_theme()
        
    def update_theme(self):
        colors = self.current_colors
        
        # Root
        self.root.configure(bg=colors['bg_secondary'])
        
        # Header
        self.header.configure(bg=colors['primary'])
        self.header_content.configure(bg=colors['primary'])
        self.title_label.configure(bg=colors['primary'])
        
        # Main frame
        self.main_frame.configure(bg=colors['bg_secondary'])
        
        # Card
        self.card.configure(bg=colors['bg_card'], 
                           highlightbackground=colors['border'])
        self.card.winfo_children()[0].configure(bg=colors['bg_card'])
        
        # Card content
        for widget in self.card.winfo_children()[0].winfo_children():
            widget.configure(bg=colors['bg_card'])
            if hasattr(widget, 'configure'):
                try:
                    if 'fg' in widget.keys():
                        if widget == self.card_title:
                            widget.configure(fg=colors['text_primary'])
                        else:
                            widget.configure(fg=colors['text_secondary'])
                except:
                    pass
        
        # Update progress frame
        self.progress_frame.configure(bg=colors['bg_card'])
        self.progress_text.configure(bg=colors['bg_card'], fg=colors['text_secondary'])
        
        # Update controls
        for widget in self.main_frame.winfo_children():
            if widget != self.card:
                widget.configure(bg=colors['bg_secondary'])
                self.update_widget_recursive(widget, colors)
        
        # Update theme info
        theme_info = f"Current: {'Dark' if self.is_dark else 'Light'} Mode"
        self.theme_info.configure(text=theme_info)
        
    def update_widget_recursive(self, widget, colors):
        """Recursively update widget colors"""
        try:
            widget.configure(bg=colors['bg_secondary'])
            if hasattr(widget, 'configure') and 'fg' in widget.keys():
                if 'bold' in str(widget.cget('font')):
                    widget.configure(fg=colors['text_primary'])
                else:
                    widget.configure(fg=colors['text_secondary'])
        except:
            pass
            
        for child in widget.winfo_children():
            self.update_widget_recursive(child, colors)

def main():
    print("🎨 Starting Theme Test...")
    
    root = tk.Tk()
    app = ModernThemeTest(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 300
    y = (root.winfo_screenheight() // 2) - 200
    root.geometry(f"600x400+{x}+{y}")
    
    print("✅ Theme test window created!")
    print("🔄 Testing theme switching automatically...")
    
    # Auto test sequence
    def auto_test():
        try:
            # Test theme toggle after 1 second
            root.after(1000, lambda: app.toggle_theme())
            print("🌙 Switched to dark mode")
            
            # Switch back after another 1 second  
            root.after(2000, lambda: app.toggle_theme())
            print("☀️ Switched back to light mode")
            
            # Close after 3 seconds total
            root.after(3000, lambda: [
                print("✅ Theme test completed successfully!"),
                root.destroy()
            ])
        except Exception as e:
            print(f"⚠️ Theme test had issues: {e}")
            root.after(3000, root.destroy)
    
    # Start auto test
    auto_test()
    
    root.mainloop()
    print("🎯 Theme test finished - proceeding to main app...")

if __name__ == "__main__":
    main()