# -*- coding: utf-8 -*-
"""
Resume Match — Skill Gap Analyzer - Matching Logic Engine
Contains string processing, file reading, skill extraction, and score calculations.
"""

import re
from skills import SKILL_CATEGORIES

def clean_text(text):
    """
    Converts text to lowercase and prepares it for robust matching.
    Removes common formatting symbols but preserves special characters in skills like C++, C#, .NET, CI/CD.
    """
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    
    # Replace newlines and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_skills_from_text(text):
    """
    Extracts pre-defined skills from text using regex matching for whole words or special phrases.
    Uses regex boundaries \b to prevent partial matches (e.g. matching 'go' inside 'google').
    """
    cleaned = clean_text(text)
    found_skills = set()
    
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            # Escape skill for safe regex (handles +, #, . etc.)
            escaped_skill = re.escape(skill)
            
            # For skills containing special characters (like c++, c#, .net, ci/cd), we need custom boundaries.
            # Otherwise, use standard word boundaries.
            if any(char in skill for char in ['+', '#', '.', '/']):
                pattern = rf'(?:^|\s|[,:;\(\)\[\]]){escaped_skill}(?:$|\s|[,:;\(\)\[\]])'
            else:
                pattern = rf'\b{escaped_skill}\b'
                
            if re.search(pattern, cleaned):
                found_skills.add(skill)
                
    return sorted(list(found_skills))

def analyze_resume_vs_job(resume_text, job_text):
    """
    Performs category-wise comparison and calculates percentages.
    Returns a dictionary of metrics, missing skills, and suggestions.
    """
    resume_skills = set(extract_skills_from_text(resume_text))
    job_skills = set(extract_skills_from_text(job_text))
    
    # Matched and missing skills
    matched_skills = sorted(list(resume_skills.intersection(job_skills)))
    missing_skills = sorted(list(job_skills.difference(resume_skills)))
    
    # Calculate match percentage
    if len(job_skills) == 0:
        match_percentage = 0.0
    else:
        match_percentage = round((len(matched_skills) / len(job_skills)) * 100.0, 1)
        
    # Analyze by categories
    category_analysis = []
    for category, skills_list in SKILL_CATEGORIES.items():
        category_set = set(skills_list)
        # Skills required in the job description for this category
        job_cat_skills = job_skills.intersection(category_set)
        # Skills present in resume for this category
        resume_cat_skills = resume_skills.intersection(category_set)
        
        # Calculate matched and missing for this category
        cat_matched = sorted(list(resume_cat_skills.intersection(job_cat_skills)))
        cat_missing = sorted(list(job_cat_skills.difference(resume_cat_skills)))
        
        # Only add to analysis if the job description asked for this category of skill
        if job_cat_skills:
            category_analysis.append({
                "category": category,
                "matched": cat_matched,
                "missing": cat_missing
            })
            
    # Calculate general resume strength score based on total number of unique skills present
    # 0-3 skills: Weak, 4-9 skills: Medium, 10+: Strong
    total_resume_skills_count = len(resume_skills)
    if total_resume_skills_count <= 4:
        strength = "Weak"
        strength_score = min(total_resume_skills_count * 10, 40)
    elif total_resume_skills_count <= 10:
        strength = "Medium"
        strength_score = 40 + min((total_resume_skills_count - 4) * 6.5, 35)
    else:
        strength = "Strong"
        strength_score = 75 + min((total_resume_skills_count - 10) * 2.5, 25)
        
    strength_score = round(strength_score)
    
    # Compile concrete, beginner-friendly recommendations
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider adding these high-priority missing skills required by the employer: {', '.join(missing_skills[:5])}.")
        
        # Categorized tips
        for cat_data in category_analysis:
            if cat_data["missing"]:
                suggestions.append(f"Strengthen your '{cat_data['category']}' section. Add: {', '.join(cat_data['missing'][:3])}.")
    else:
        if job_skills:
            suggestions.append("Outstanding match! Your resume covers all core skills identified in the job description.")
        else:
            suggestions.append("Paste a detailed Job Description to view specific skill suggestions.")
            
    if total_resume_skills_count < 6:
        suggestions.append("Tip: Your overall skill profile looks a bit thin. Expand your resume's Skills Section with specific tools and languages you know.")
        
    return {
        "match_percentage": match_percentage,
        "strength": strength,
        "strength_score": strength_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "category_analysis": category_analysis,
        "suggestions": suggestions,
        "total_resume_skills_count": total_resume_skills_count,
        "total_job_skills_count": len(job_skills)
    }
