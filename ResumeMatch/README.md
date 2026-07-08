# Resume Match — Skill Gap Analyzer 🚀

Analyze resumes against job descriptions to identify skill gaps and improve job readiness. Designed inside a beautiful dark teal dashboard using Python's native GUI toolkit (**Tkinter**).

---

## 🎨 Highlights & Features
- **Offline First**: Runs completely locally. No API keys, no internet connection, and no database configuration needed.
- **Category-wise Skill Analytics**: Matches resume skills against requirements across defined sections like Programming Languages, Web Dev, DevOps, Soft Skills, and databases.
- **Resume Strength Meter**: Evaluates the general robustness of your skill inventory separate from the specific job match.
- **Clean Dark Teal Theme**: Formatted with modern layouts, customized widgets, responsive loading states, and colorful result highlights.
- **Export Reports**: Saves complete, highly-formatted matching feedback directly into a '.txt' file for future reviews.

---

## 📁 File Structure
<pre>
ResumeMatch/
│── main.py            # Main application UI bootstrapper (Tkinter)
│── matcher.py         # Matching algorithms and text sanitization engines
│── skills.py          # Complete structured dictionary of standard industry skills
│── README.md          # Setup instructions and documentation
│── requirements.txt   # Required package dependencies list (clean Python native!)
│── sample_resume.txt  # Quick sample resume file for testing
│── sample_job.txt     # Quick sample job description file for testing
</pre>

---

## 💻 Installation & Quickstart

### Prerequisites
- **Python 3.8+** installed on your operating system.
- Tkinter library support (Usually pre-packaged. On Ubuntu/Debian, install with 'sudo apt-get install python3-tk').

### Running the App
1. Clone or copy the folder files onto your workstation.
2. Navigate into the directory:
   <pre><code>cd ResumeMatch</code></pre>
3. Run the application:
   <pre><code>python main.py</code></pre>

---

## 💡 Python Concepts Used
- **Tkinter GUI**: Modern visual grid alignment, Scrollable Text boxes, custom Styles via 'ttk.Style', Dialog boxes ('filedialog', 'messagebox'), and ProgressBars.
- **Regular Expressions ('re')**: Sanitizing text, whole-word isolation, and processing programming markers like (C++, C#, .NET).
- **Sets & Lists**: Category intersections and difference filters to find matches and missing tags.
- **String Parsing & File I/O**: Open, read, write, and export routines supporting native UTF-8 file interactions.
