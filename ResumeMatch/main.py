# -*- coding: utf-8 -*-
"""
Resume Match — Skill Gap Analyzer - Main GUI Application
A professional dark teal theme application constructed in pure Tkinter.
No AI models or ML libraries needed; runs entirely locally using Python standard libraries.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matcher import analyze_resume_vs_job

# Define Theme Colors
COLOR_BG_DARK = "#0B1F24"      # Deep Dark Teal background
COLOR_BG_CARD = "#142F35"      # Medium Dark Teal for sections
COLOR_ACCENT = "#14B8A6"       # Teal Accent / Primary Highlight
COLOR_ACCENT_HOVER = "#0D9488" # Teal Accent Hover state
COLOR_TEXT_LIGHT = "#F0FDFA"   # Off-white / light cyan
COLOR_TEXT_MUTED = "#99F6E4"   # Secondary muted teal text
COLOR_WHITE = "#FFFFFF"
COLOR_RED = "#F43F5E"          # Rose Red for missing elements
COLOR_GREEN = "#10B981"        # Emerald Green for matched elements

class ResumeMatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Match — Skill Gap Analyzer - Desktop Resume Analyzer")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        
        # Set background color of root window
        self.root.configure(bg=COLOR_BG_DARK)
        
        # Setup modern styles
        self.setup_styles()
        
        # Build UI layout
        self.build_ui()
        
        # Load internal sample data initially
        self.load_samples()
        
    def setup_styles(self):
        """Configure ttk Styles to support dark teal theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main Frame Background
        style.configure("TFrame", background=COLOR_BG_DARK)
        
        # Label Styles
        style.configure("TLabel", background=COLOR_BG_DARK, foreground=COLOR_TEXT_LIGHT, font=("Helvetica", 10))
        style.configure("Header.TLabel", background=COLOR_BG_DARK, foreground=COLOR_WHITE, font=("Helvetica", 18, "bold"))
        style.configure("Subheader.TLabel", background=COLOR_BG_DARK, foreground=COLOR_ACCENT, font=("Helvetica", 10, "italic"))
        
        # Card Frames (Containers)
        style.configure("Card.TFrame", background=COLOR_BG_CARD, relief="flat")
        style.configure("CardLabel.TLabel", background=COLOR_BG_CARD, foreground=COLOR_WHITE, font=("Helvetica", 11, "bold"))
        style.configure("MutedCardLabel.TLabel", background=COLOR_BG_CARD, foreground=COLOR_TEXT_MUTED, font=("Helvetica", 9))
        
        # Button Styles
        style.configure("TButton", 
                        background=COLOR_BG_CARD, 
                        foreground=COLOR_TEXT_LIGHT, 
                        bordercolor=COLOR_BG_CARD,
                        lightcolor=COLOR_BG_CARD, 
                        darkcolor=COLOR_BG_CARD, 
                        font=("Helvetica", 10, "bold"),
                        padding=(10, 5))
        style.map("TButton",
                  background=[("active", COLOR_BG_DARK)],
                  foreground=[("active", COLOR_ACCENT)])
                  
        # Accent Analyze Button
        style.configure("Accent.TButton", 
                        background=COLOR_ACCENT, 
                        foreground=COLOR_BG_DARK,
                        bordercolor=COLOR_ACCENT,
                        lightcolor=COLOR_ACCENT, 
                        darkcolor=COLOR_ACCENT, 
                        font=("Helvetica", 11, "bold"),
                        padding=(15, 8))
        style.map("Accent.TButton",
                  background=[("active", COLOR_ACCENT_HOVER)],
                  foreground=[("active", COLOR_WHITE)])
                  
        # Progress Bar style
        style.configure("Custom.Horizontal.TProgressbar", 
                        troughcolor=COLOR_BG_DARK, 
                        background=COLOR_ACCENT, 
                        bordercolor=COLOR_BG_DARK, 
                        lightcolor=COLOR_ACCENT, 
                        darkcolor=COLOR_ACCENT,
                        thickness=15)
        
    def build_ui(self):
        """Construct the modern dashboard layout"""
        
        # ==================== HEADER SECTION ====================
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        title_label = ttk.Label(header_frame, text="Resume Match — Skill Gap Analyzer", style="Header.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Analyze resumes against job descriptions to identify skill gaps and improve job readiness", style="Subheader.TLabel")
        subtitle_label.pack(anchor="w", pady=(2, 0))
        
        # Quick Load Samples Buttons on Header
        top_btn_frame = ttk.Frame(header_frame)
        top_btn_frame.place(relx=1.0, rely=0.5, anchor="e")
        
        sample_btn = ttk.Button(top_btn_frame, text="Load Samples", command=self.load_samples)
        sample_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(top_btn_frame, text="Clear Fields", command=self.clear_fields)
        clear_btn.pack(side="left", padx=5)

        # ==================== MAIN COMPONENT PANELS ====================
        main_pane = ttk.Frame(self.root)
        main_pane.pack(fill="both", expand=True, padx=25, pady=5)
        
        # Configure columns: Left column (inputs), Right column (metrics and results)
        main_pane.columnconfigure(0, weight=4, uniform="group1")
        main_pane.columnconfigure(1, weight=5, uniform="group1")
        main_pane.rowconfigure(0, weight=1)
        
        # -------------------- LEFT FRAME (INPUTS) --------------------
        left_frame = ttk.Frame(main_pane)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        # Resume input card
        resume_card = ttk.Frame(left_frame, style="Card.TFrame")
        resume_card.pack(fill="both", expand=True, pady=(0, 10))
        
        resume_header = ttk.Frame(resume_card, style="Card.TFrame")
        resume_header.pack(fill="x", padx=15, pady=(10, 5))
        ttk.Label(resume_header, text="Resume / CV", style="CardLabel.TLabel").pack(side="left")
        ttk.Button(resume_header, text="Browse TXT", command=self.browse_resume).pack(side="right")
        
        # Scrollable Text Area for Resume
        resume_txt_frame = ttk.Frame(resume_card)
        resume_txt_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.resume_scroll = tk.Scrollbar(resume_txt_frame)
        self.resume_scroll.pack(side="right", fill="y")
        self.resume_text_widget = tk.Text(resume_txt_frame, 
                                          bg="#10252A", 
                                          fg=COLOR_TEXT_LIGHT, 
                                          insertbackground=COLOR_WHITE,
                                          selectbackground=COLOR_ACCENT,
                                          selectforeground=COLOR_BG_DARK,
                                          font=("Consolas", 10), 
                                          bd=0, 
                                          yscrollcommand=self.resume_scroll.set)
        self.resume_text_widget.pack(fill="both", expand=True)
        self.resume_scroll.config(command=self.resume_text_widget.yview)

        # Job Description input card
        job_card = ttk.Frame(left_frame, style="Card.TFrame")
        job_card.pack(fill="both", expand=True, pady=(5, 0))
        
        job_header = ttk.Frame(job_card, style="Card.TFrame")
        job_header.pack(fill="x", padx=15, pady=(10, 5))
        ttk.Label(job_header, text="Job Description", style="CardLabel.TLabel").pack(side="left")
        ttk.Button(job_header, text="Browse TXT", command=self.browse_job).pack(side="right")
        
        # Scrollable Text Area for Job Description
        job_txt_frame = ttk.Frame(job_card)
        job_txt_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.job_scroll = tk.Scrollbar(job_txt_frame)
        self.job_scroll.pack(side="right", fill="y")
        self.job_text_widget = tk.Text(job_txt_frame, 
                                        bg="#10252A", 
                                        fg=COLOR_TEXT_LIGHT, 
                                        insertbackground=COLOR_WHITE,
                                        selectbackground=COLOR_ACCENT,
                                        selectforeground=COLOR_BG_DARK,
                                        font=("Consolas", 10), 
                                        bd=0, 
                                        yscrollcommand=self.job_scroll.set)
        self.job_text_widget.pack(fill="both", expand=True)
        self.job_scroll.config(command=self.job_text_widget.yview)
        
        # -------------------- RIGHT FRAME (METRICS & RESULTS) --------------------
        right_frame = ttk.Frame(main_pane)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        
        # Dashboard Score Summary Card
        score_card = ttk.Frame(right_frame, style="Card.TFrame")
        score_card.pack(fill="x", pady=(0, 10))
        
        # Multi-column grid within Score Card
        score_card.columnconfigure(0, weight=1)
        score_card.columnconfigure(1, weight=1)
        
        # Left Panel - Match score
        score_left = ttk.Frame(score_card, style="Card.TFrame")
        score_left.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        ttk.Label(score_left, text="MATCH PERCENTAGE", style="MutedCardLabel.TLabel").pack(anchor="w")
        self.score_lbl = tk.Label(score_left, text="0.0%", bg=COLOR_BG_CARD, fg=COLOR_ACCENT, font=("Helvetica", 32, "bold"))
        self.score_lbl.pack(anchor="w", pady=(2, 5))
        
        self.progress = ttk.Progressbar(score_left, style="Custom.Horizontal.TProgressbar", mode="determinate")
        self.progress.pack(fill="x", pady=2)
        
        # Right Panel - Resume Strength
        score_right = ttk.Frame(score_card, style="Card.TFrame")
        score_right.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        ttk.Label(score_right, text="RESUME STRENGTH", style="MutedCardLabel.TLabel").pack(anchor="w")
        
        self.strength_lbl = tk.Label(score_right, text="Empty", bg=COLOR_BG_CARD, fg=COLOR_WHITE, font=("Helvetica", 20, "bold"))
        self.strength_lbl.pack(anchor="w", pady=(2, 2))
        
        self.strength_desc = ttk.Label(score_right, text="Please load inputs and analyze", style="MutedCardLabel.TLabel")
        self.strength_desc.pack(anchor="w")

        # Results analysis panel (Scrollable Category-wise details)
        analysis_card = ttk.Frame(right_frame, style="Card.TFrame")
        analysis_card.pack(fill="both", expand=True, pady=(5, 0))
        
        ttk.Label(analysis_card, text="Skill-wise Match Analysis", style="CardLabel.TLabel").pack(anchor="w", padx=15, pady=(10, 5))
        
        # Styled Text view with Tags for colored text highlights
        text_pane_frame = ttk.Frame(analysis_card)
        text_pane_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.results_scroll = tk.Scrollbar(text_pane_frame)
        self.results_scroll.pack(side="right", fill="y")
        self.results_widget = tk.Text(text_pane_frame, 
                                      bg="#0F2428", 
                                      fg=COLOR_WHITE, 
                                      font=("Helvetica", 10), 
                                      bd=0, 
                                      yscrollcommand=self.results_scroll.set)
        self.results_widget.pack(fill="both", expand=True)
        self.results_scroll.config(command=self.results_widget.yview)
        
        # Configure text color highlights
        self.results_widget.tag_config("title", font=("Helvetica", 11, "bold"), foreground=COLOR_WHITE)
        self.results_widget.tag_config("category", font=("Helvetica", 10, "bold"), foreground=COLOR_TEXT_MUTED)
        self.results_widget.tag_config("matched", font=("Helvetica", 9), foreground=COLOR_GREEN)
        self.results_widget.tag_config("missing", font=("Helvetica", 9), foreground=COLOR_RED)
        self.results_widget.tag_config("normal", font=("Helvetica", 9), foreground=COLOR_TEXT_LIGHT)
        self.results_widget.tag_config("divider", font=("Helvetica", 8), foreground="#2D5A64")
        self.results_widget.config(state="disabled") # Disabled by default until calculated

        # ==================== BOTTOM BUTTON PANEL & STATUS BAR ====================
        action_bar = ttk.Frame(self.root)
        action_bar.pack(fill="x", padx=25, pady=(10, 15))
        
        # Central Action Buttons
        btn_container = ttk.Frame(action_bar)
        btn_container.pack(side="left")
        
        self.analyze_btn = ttk.Button(btn_container, text="Analyze Match Percentage", style="Accent.TButton", command=self.perform_analysis)
        self.analyze_btn.pack(side="left")
        
        self.export_btn = ttk.Button(btn_container, text="Export Match Report", command=self.export_report)
        self.export_btn.pack(side="left", padx=10)
        
        # Status Bar right-aligned
        self.status_lbl = ttk.Label(action_bar, text="Ready to analyze.", font=("Helvetica", 9, "italic"), foreground=COLOR_TEXT_MUTED)
        self.status_lbl.pack(side="right", pady=10)
        
    def browse_resume(self):
        """Browse disk to load text resume"""
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.resume_text_widget.delete("1.0", "end")
                self.resume_text_widget.insert("1.0", content)
                self.status_lbl.config(text=f"Loaded Resume: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def browse_job(self):
        """Browse disk to load text job description"""
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.job_text_widget.delete("1.0", "end")
                self.job_text_widget.insert("1.0", content)
                self.status_lbl.config(text=f"Loaded Job Description: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def load_samples(self):
        """Populates the input widgets with high-quality sample texts"""
        sample_resume_txt = """JOHN DOE
john.doe@email.com | (123) 456-7890 | Seattle, WA | github.com/johndoe

TECHNICAL SKILLS
- Programming Languages: Python, JavaScript, TypeScript, HTML, CSS, SQL
- Web Development: React, Django, NodeJS, Tailwind
- Databases: PostgreSQL, SQLite
- DevOps & Cloud: Git, GitHub, Docker, AWS (S3, EC2)
- Tools: Jira, Figma, Slack, Postman
- Soft Skills: Teamwork, Problem Solving, Communication, Adaptability"""

        sample_job_txt = """POSITION: Full Stack Software Engineer
We are looking for a skilled Software Engineer to design and implement web applications.
The ideal candidate has strong hands-on experience with Python and TypeScript.

REQUIREMENTS:
- Build modular web applications using React and NodeJS.
- Develop scalable backend APIs using Python (Django) and PostgreSQL databases.
- Containerize application workloads using Docker and deploy to AWS.
- Participate in agile practices like Scrum, and reviews in GitHub.
- Possess strong problem solving, teamwork, and communication skills."""

        self.resume_text_widget.delete("1.0", "end")
        self.resume_text_widget.insert("1.0", sample_resume_txt)
        
        self.job_text_widget.delete("1.0", "end")
        self.job_text_widget.insert("1.0", sample_job_txt)
        
        self.status_lbl.config(text="Loaded sample resume and job description.")
        
    def clear_fields(self):
        """Clears text boxes, metrics, progress, and results displays"""
        self.resume_text_widget.delete("1.0", "end")
        self.job_text_widget.delete("1.0", "end")
        
        self.score_lbl.config(text="0.0%")
        self.progress.config(value=0)
        self.strength_lbl.config(text="Empty", fg=COLOR_WHITE)
        self.strength_desc.config(text="Please load inputs and analyze")
        
        self.results_widget.config(state="normal")
        self.results_widget.delete("1.0", "end")
        self.results_widget.insert("1.0", "No active analysis. Load inputs and click 'Analyze'.", "normal")
        self.results_widget.config(state="disabled")
        
        self.status_lbl.config(text="Cleared inputs and results.")
        
    def perform_analysis(self):
        """Triggers matching algorithm and updates dashboard UI"""
        resume_text = self.resume_text_widget.get("1.0", "end-1c").strip()
        job_text = self.job_text_widget.get("1.0", "end-1c").strip()
        
        if not resume_text:
            messagebox.showwarning("Incomplete Inputs", "Please paste or browse a Resume before analyzing.")
            return
        if not job_text:
            messagebox.showwarning("Incomplete Inputs", "Please paste or browse a Job Description before analyzing.")
            return
            
        # Call core matcher library (zero external dependencies!)
        self.analysis_results = analyze_resume_vs_job(resume_text, job_text)
        
        # Update progress bar and percentage display
        pct = self.analysis_results["match_percentage"]
        self.score_lbl.config(text=f"{pct}%")
        self.progress.config(value=pct)
        
        # Update Strength Panel colors & ratings
        strength = self.analysis_results["strength"]
        score = self.analysis_results["strength_score"]
        self.strength_lbl.config(text=f"{strength} ({score}/100)")
        
        if strength == "Strong":
            self.strength_lbl.config(fg=COLOR_GREEN)
            self.strength_desc.config(text="Highly robust technical skills profile")
        elif strength == "Medium":
            self.strength_lbl.config(fg=COLOR_ACCENT)
            self.strength_desc.config(text="Solid set of core skills present")
        else:
            self.strength_lbl.config(fg=COLOR_RED)
            self.strength_desc.config(text="Requires additional technical skills")
            
        # Update Rich Analysis panel contents
        self.results_widget.config(state="normal")
        self.results_widget.delete("1.0", "end")
        
        self.results_widget.insert("end", "📊 CORE SKILL BREAKDOWN\n", "title")
        self.results_widget.insert("end", "="*50 + "\n", "divider")
        
        # Category breakdown
        cat_data = self.analysis_results["category_analysis"]
        if cat_data:
            for cat_item in cat_data:
                category_name = cat_item["category"]
                matched_set = cat_item["matched"]
                missing_set = cat_item["missing"]
                
                self.results_widget.insert("end", f"\n📁 {category_name.upper()}\n", "category")
                
                if matched_set:
                    self.results_widget.insert("end", "  ✓ Matched: ", "normal")
                    self.results_widget.insert("end", f"{', '.join(matched_set)}\n", "matched")
                if missing_set:
                    self.results_widget.insert("end", "  ✗ Missing: ", "normal")
                    self.results_widget.insert("end", f"{', '.join(missing_set)}\n", "missing")
        else:
            self.results_widget.insert("end", "\nNo categorized skill requests matched the job description.\n", "normal")
            
        self.results_widget.insert("end", "\n\n💡 ACTIONABLE SUGGESTIONS\n", "title")
        self.results_widget.insert("end", "="*50 + "\n", "divider")
        
        for idx, suggestion in enumerate(self.analysis_results["suggestions"], 1):
            self.results_widget.insert("end", f"\n{idx}. {suggestion}\n", "normal")
            
        self.results_widget.config(state="disabled")
        self.status_lbl.config(text="Analysis successfully completed!")
        
    def export_report(self):
        """Save analysis metrics and suggestions to disk as a text report"""
        if not hasattr(self, 'analysis_results'):
            messagebox.showwarning("No Data", "Please analyze a match before trying to export.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="ResumeMatch_SkillGap_Report.txt"
        )
        
        if filepath:
            try:
                results = self.analysis_results
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("             RESUME MATCH — SKILL GAP ANALYZER - ANALYSIS REPORT\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Match Percentage:      {results['match_percentage']}%\n")
                    f.write(f"Resume Strength Score: {results['strength']} ({results['strength_score']}/100)\n")
                    f.write(f"Skills Found in CV:    {results['total_resume_skills_count']}\n")
                    f.write(f"Required Skills Found: {results['total_job_skills_count']}\n\n")
                    
                    f.write("------------------------------------------------------------\n")
                    f.write("MATCHED SKILLS\n")
                    f.write("------------------------------------------------------------\n")
                    if results['matched_skills']:
                        f.write(", ".join(results['matched_skills']) + "\n\n")
                    else:
                        f.write("None\n\n")
                        
                    f.write("------------------------------------------------------------\n")
                    f.write("MISSING SKILLS\n")
                    f.write("------------------------------------------------------------\n")
                    if results['missing_skills']:
                        f.write(", ".join(results['missing_skills']) + "\n\n")
                    else:
                        f.write("None\n\n")
                        
                    f.write("------------------------------------------------------------\n")
                    f.write("CATEGORY BREAKDOWN\n")
                    f.write("------------------------------------------------------------\n")
                    for cat in results['category_analysis']:
                        f.write(f"\n[{cat['category']}]\n")
                        f.write(f"  ✓ Matched: {', '.join(cat['matched']) if cat['matched'] else 'None'}\n")
                        f.write(f"  ✗ Missing: {', '.join(cat['missing']) if cat['missing'] else 'None'}\n")
                        
                    f.write("\n------------------------------------------------------------\n")
                    f.write("SUGGESTIONS & FEEDBACK\n")
                    f.write("------------------------------------------------------------\n")
                    for idx, sug in enumerate(results['suggestions'], 1):
                        f.write(f"{idx}. {sug}\n")
                        
                    f.write("\nGenerated by Resume Match — Skill Gap Analyzer.\n")
                
                messagebox.showinfo("Success", f"Report successfully exported to:\n{filepath}")
                self.status_lbl.config(text=f"Exported Report: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"An error occurred during file export: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeMatchApp(root)
    root.mainloop()
