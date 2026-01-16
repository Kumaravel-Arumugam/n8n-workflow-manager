import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
import re
from datetime import datetime
from collections import Counter
from itertools import combinations
import json

# ============================================
# DATA EXTRACTION
# ============================================
jobs = _items
if not jobs:
    return [{'error': 'No job data received', 'has_data': False, 'report_text': 'No data available', 'chart1_base64': '', 'chart2_base64': '', 'chart3_base64': '', 'chart1_caption': '', 'chart2_caption': '', 'chart3_caption': '', 'raw_analysis': '{}'}]

records = [item.get('json', item) if isinstance(item, dict) else item for item in jobs]
df = pd.DataFrame(records)

# Deduplicate by job_id
if 'job_id' in df.columns:
    original_count = len(df)
    df = df.drop_duplicates(subset=['job_id'])
    duplicates_removed = original_count - len(df)
else:
    duplicates_removed = 0

total_jobs = len(df)
role_name = df['role'].iloc[0] if 'role' in df.columns and len(df) > 0 else 'Unknown Role'

# ============================================
# SKILL NORMALIZATION DICTIONARY
# ============================================
SKILL_NORMALIZATION = {
    # Power BI variants
    'powerbi': 'Power BI', 'power bi': 'Power BI', 'power-bi': 'Power BI', 'pbi': 'Power BI',
    # PostgreSQL variants
    'postgres': 'PostgreSQL', 'postgresql': 'PostgreSQL', 'pg': 'PostgreSQL',
    # GCP variants
    'gcp': 'GCP', 'google cloud platform': 'GCP', 'google cloud': 'GCP',
    # AWS variants
    'aws': 'AWS', 'amazon web services': 'AWS',
    # Azure variants
    'azure': 'Azure', 'microsoft azure': 'Azure',
    # SQL variants
    'sql': 'SQL', 'mysql': 'MySQL', 'mssql': 'SQL Server', 'sql server': 'SQL Server',
    # Python
    'python': 'Python', 'python3': 'Python', 'py': 'Python',
    # JavaScript
    'javascript': 'JavaScript', 'js': 'JavaScript', 'node.js': 'Node.js', 'nodejs': 'Node.js',
    # Java
    'java': 'Java',
    # Excel
    'excel': 'Excel', 'ms excel': 'Excel', 'microsoft excel': 'Excel',
    # Tableau
    'tableau': 'Tableau',
    # Machine Learning
    'machine learning': 'Machine Learning', 'ml': 'Machine Learning',
    # AI / Artificial Intelligence
    'ai': 'AI', 'artificial intelligence': 'AI',
    # Data Science
    'data science': 'Data Science', 'datascience': 'Data Science',
    # Data Analysis
    'data analysis': 'Data Analysis', 'data analytics': 'Data Analytics',
    # ETL
    'etl': 'ETL',
    # Agile / Scrum
    'agile': 'Agile', 'scrum': 'Scrum',
    # Jira / Confluence
    'jira': 'Jira', 'confluence': 'Confluence',
    # Docker / Kubernetes
    'docker': 'Docker', 'kubernetes': 'Kubernetes', 'k8s': 'Kubernetes',
    # Git
    'git': 'Git', 'github': 'GitHub', 'gitlab': 'GitLab',
    # Spark / Hadoop
    'spark': 'Spark', 'apache spark': 'Spark', 'hadoop': 'Hadoop',
    # BigQuery / Snowflake
    'bigquery': 'BigQuery', 'snowflake': 'Snowflake', 'databricks': 'Databricks',
    # CRM / ERP
    'salesforce': 'Salesforce', 'crm': 'CRM', 'erp': 'ERP', 'sap': 'SAP', 'oracle': 'Oracle',
    # Communication / Soft
    'communication': 'Communication', 'collaboration': 'Collaboration',
    # Project Management
    'project management': 'Project Management', 'pm': 'Project Management',
    # Business Analysis
    'business analyst': 'Business Analysis', 'business analysis': 'Business Analysis',
    # Process
    'process mapping': 'Process Mapping', 'business processes': 'Business Processes',
    # Others
    'api': 'API', 'linux': 'Linux', 'ci/cd': 'CI/CD', 'mongodb': 'MongoDB', 'nosql': 'NoSQL',
    'kafka': 'Kafka', 'data warehousing': 'Data Warehousing', 'data engineering': 'Data Engineering',
    'data quality': 'Data Quality', 'advanced analytics': 'Advanced Analytics', 'analytics': 'Analytics',
    'analytical': 'Analytical', 'finance': 'Finance', 'operations': 'Operations', 
    'management': 'Management', 'compliance': 'Compliance', 'design': 'Design'
}

# ============================================
# SKILL CATEGORIZATION
# ============================================
SKILL_CATEGORIES = {
    'Technical / Programming': ['Python', 'Java', 'JavaScript', 'Node.js', 'SQL', 'MySQL', 'PostgreSQL', 'SQL Server', 'MongoDB', 'NoSQL', 'API', 'Linux', 'CI/CD', 'Git', 'GitHub', 'GitLab'],
    'Data & Analytics': ['Data Analysis', 'Data Analytics', 'Data Science', 'Machine Learning', 'AI', 'ETL', 'Data Warehousing', 'Data Engineering', 'Data Quality', 'Advanced Analytics', 'Analytics', 'Analytical', 'Business Analysis'],
    'Cloud & Infrastructure': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Spark', 'Hadoop', 'Kafka', 'BigQuery', 'Snowflake', 'Databricks'],
    'Business / Process': ['Business Processes', 'Process Mapping', 'Project Management', 'Finance', 'Operations', 'Management', 'Compliance'],
    'Tools & Platforms': ['Excel', 'Tableau', 'Power BI', 'Jira', 'Confluence', 'Salesforce', 'CRM', 'ERP', 'SAP', 'Oracle'],
    'Soft / Collaboration': ['Communication', 'Collaboration', 'Agile', 'Scrum', 'Design']
}

def get_skill_category(skill):
    """Return the category for a normalized skill"""
    for category, skills in SKILL_CATEGORIES.items():
        if skill in skills:
            return category
    return 'Other'

# ============================================
# SKILL PARSING WITH NORMALIZATION
# ============================================
known_skills = list(set(SKILL_NORMALIZATION.keys()))

def parse_skills(skill_string):
    """Parse concatenated skills and return normalized skill names"""
    if pd.isna(skill_string) or not str(skill_string).strip():
        return []
    s = str(skill_string).lower().strip()
    found_skills = []
    remaining = s
    
    # Sort by length descending to match longer phrases first
    for skill in sorted(known_skills, key=len, reverse=True):
        if skill in remaining:
            normalized = SKILL_NORMALIZATION.get(skill, skill.title())
            if normalized not in found_skills:
                found_skills.append(normalized)
            remaining = remaining.replace(skill, ' ')
    
    # Capture leftover words as potential skills
    leftover = [w.strip() for w in remaining.split() if len(w.strip()) > 3 and w.strip() not in ['yrs', 'years', 'the', 'and', 'for', 'with']]
    for word in leftover[:3]:
        if word.title() not in found_skills:
            found_skills.append(word.title())
    
    return found_skills

def parse_experience(exp_string):
    if pd.isna(exp_string) or not str(exp_string).strip():
        return None
    s = str(exp_string).lower().strip()
    match = re.search(r'(\d+)\s*[-–]\s*(\d+)', s)
    if match:
        return (int(match.group(1)) + int(match.group(2))) / 2
    match = re.search(r'(\d+)', s)
    return int(match.group(1)) if match else None

# ============================================
# DATA QUALITY ASSESSMENT
# ============================================
data_quality = {
    'total_raw': len(records),
    'total_unique': total_jobs,
    'duplicates_removed': duplicates_removed,
    'has_description': int(df['description'].notna().sum()),
    'has_skills': int(df['skills'].notna().sum()),
    'has_experience': int(df['experience'].notna().sum()),
    'has_salary': int((df['salary'].notna() & (df['salary'] != '')).sum()) if 'salary' in df.columns else 0,
    'companies_count': int(df['company'].nunique()) if 'company' in df.columns else 0,
    'locations_count': int(df['location'].nunique()) if 'location' in df.columns else 0
}
data_quality['completeness'] = round((
    data_quality['has_description'] + 
    data_quality['has_skills'] + 
    data_quality['has_experience']
) / (total_jobs * 3) * 100, 1) if total_jobs > 0 else 0

if total_jobs >= 20 and data_quality['completeness'] >= 80:
    quality_grade = "HIGH"
    quality_desc = "Robust dataset suitable for comprehensive analysis"
elif total_jobs >= 10 and data_quality['completeness'] >= 60:
    quality_grade = "MEDIUM"
    quality_desc = "Adequate data for directional insights"
else:
    quality_grade = "LOW"
    quality_desc = "Limited data; findings are indicative only"

# ============================================
# SKILL ANALYSIS (EXTENDED)
# ============================================
all_skills = []
skills_per_job = []  # For co-occurrence analysis

for skills_str in df['skills'].dropna():
    parsed = parse_skills(skills_str)
    all_skills.extend(parsed)
    skills_per_job.append(parsed)

skill_counts = Counter(all_skills)
top_skills = skill_counts.most_common(15)
total_skill_mentions = sum(skill_counts.values())

# Core and secondary skills (normalized)
core_skills = [s for s, c in top_skills[:5]]
secondary_skills = [s for s, c in top_skills[5:10]]

# ============================================
# SKILL DOMINANCE METRICS
# ============================================
skill_dominance = {}
if total_skill_mentions > 0:
    top1_count = top_skills[0][1] if len(top_skills) >= 1 else 0
    top3_count = sum(c for s, c in top_skills[:3])
    top5_count = sum(c for s, c in top_skills[:5])
    long_tail_count = sum(c for s, c in top_skills[5:])
    
    skill_dominance = {
        'top1_skill': top_skills[0][0] if len(top_skills) >= 1 else None,
        'top1_share': round(top1_count / total_skill_mentions * 100, 1),
        'top3_share': round(top3_count / total_skill_mentions * 100, 1),
        'top5_share': round(top5_count / total_skill_mentions * 100, 1),
        'long_tail_share': round(long_tail_count / total_skill_mentions * 100, 1),
        'dominance_ratio': round(top5_count / max(long_tail_count, 1), 2),
        'total_unique_skills': len(skill_counts),
        'total_skill_mentions': total_skill_mentions
    }

# ============================================
# SKILL CATEGORIZATION
# ============================================
category_counts = Counter()
for skill, count in skill_counts.items():
    cat = get_skill_category(skill)
    category_counts[cat] += count

category_distribution = {}
if total_skill_mentions > 0:
    category_distribution = {
        cat: {
            'count': count,
            'percentage': round(count / total_skill_mentions * 100, 1)
        }
        for cat, count in category_counts.most_common()
    }

# ============================================
# SKILL CO-OCCURRENCE
# ============================================
pair_counts = Counter()
for job_skills in skills_per_job:
    if len(job_skills) >= 2:
        # Get all unique pairs from this job
        for pair in combinations(sorted(set(job_skills)), 2):
            pair_counts[pair] += 1

top_pairs = pair_counts.most_common(10)
skill_cooccurrence = [
    {
        'pair': f"{p[0]} + {p[1]}",
        'count': count,
        'percentage': round(count / max(len(skills_per_job), 1) * 100, 1)
    }
    for p, count in top_pairs if count >= 2
]

# ============================================
# EXPERIENCE ANALYSIS
# ============================================
exp_values = [parse_experience(e) for e in df['experience'].dropna()]
exp_values = [e for e in exp_values if e is not None]

exp_dist = {}
dominant_level = "3-5 yrs"
if exp_values:
    exp_series = pd.Series(exp_values)
    bins = [0, 2, 5, 8, 12, 25]
    labels = ['0-2 yrs', '3-5 yrs', '6-8 yrs', '9-12 yrs', '12+ yrs']
    exp_binned = pd.cut(exp_series, bins=bins, labels=labels, right=True)
    exp_dist = exp_binned.value_counts().to_dict()
    exp_dist = {str(k): int(v) for k, v in exp_dist.items() if v > 0}
    if exp_dist:
        dominant_level = max(exp_dist, key=exp_dist.get)

# ============================================
# ROLE CLARITY ANALYSIS
# ============================================
titles = df['title'].dropna().unique().tolist()[:10]
companies = df['company'].dropna().unique().tolist()[:8]
locations = df['location'].dropna().unique().tolist()[:5]

title_variance = len(titles)
if title_variance > 5:
    title_clarity = "LOW"
elif title_variance > 2:
    title_clarity = "MEDIUM"
else:
    title_clarity = "HIGH"

# ============================================
# MARKET CONSISTENCY
# ============================================
skill_sets = [set(skills) for skills in skills_per_job if len(skills) > 0]
avg_similarity = 0
if len(skill_sets) > 1:
    sims = []
    for i in range(len(skill_sets)-1):
        intersection = len(skill_sets[i] & skill_sets[i+1])
        union = len(skill_sets[i] | skill_sets[i+1])
        if union > 0:
            sims.append(intersection / union)
    avg_similarity = float(np.mean(sims)) if sims else 0

if avg_similarity > 0.4:
    consistency = "HIGH"
elif avg_similarity > 0.2:
    consistency = "MEDIUM"
else:
    consistency = "LOW"

# ============================================
# DATA LIMITATION FLAGS
# ============================================
limitations = []
if total_jobs < 10:
    limitations.append("Small sample size - findings are directional only")
if data_quality['completeness'] < 60:
    limitations.append("Low data completeness - some fields missing")
if len(skill_counts) < 5:
    limitations.append("Limited skill variety detected")
if len(exp_values) < 3:
    limitations.append("Insufficient experience data for patterns")

# ============================================
# GENERATE CHARTS
# ============================================
chart1_base64 = ""
chart2_base64 = ""
chart3_base64 = ""
can_generate_charts = total_jobs >= 3

plt.style.use("dark_background")
bg_color, text_color = "#0a0e1a", "#f0f0f0"

# CHART 1: Skill Frequency (existing)
if can_generate_charts and len(top_skills) >= 3:
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    chart_skills = top_skills[:12]
    skills_labels = [s[0] for s in chart_skills]
    skills_values = [s[1] for s in chart_skills]
    
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(skills_labels)))
    bars = ax.barh(skills_labels[::-1], skills_values[::-1], color=colors[::-1], edgecolor='white', linewidth=0.5)
    
    ax.set_xlabel('Frequency', color=text_color, fontsize=12, fontweight='600')
    ax.set_title(f'Skill Demand - {role_name}', color=text_color, fontsize=16, fontweight='bold', pad=20)
    ax.tick_params(colors=text_color, labelsize=10)
    ax.grid(axis='x', color='#1a1f2e', linestyle='-', linewidth=0.6, alpha=0.6)
    
    for bar, val in zip(bars, skills_values[::-1]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, str(val), va='center', color=text_color, fontsize=10)
    
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", facecolor=bg_color, dpi=150)
    buffer.seek(0)
    chart1_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close(fig)

# CHART 2: Experience Distribution (existing)
if can_generate_charts and len(exp_dist) >= 2:
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    exp_labels = list(exp_dist.keys())
    exp_vals = list(exp_dist.values())
    colors = ['#00d4ff', '#00ff88', '#ffc107', '#ff6b6b', '#b388ff'][:len(exp_labels)]
    bars = ax.bar(exp_labels, exp_vals, color=colors, edgecolor='white', linewidth=0.5)
    
    ax.set_xlabel('Experience Level', color=text_color, fontsize=12, fontweight='600')
    ax.set_ylabel('Postings', color=text_color, fontsize=12, fontweight='600')
    ax.set_title(f'Experience Distribution - {role_name}', color=text_color, fontsize=16, fontweight='bold', pad=20)
    ax.tick_params(colors=text_color, labelsize=10)
    ax.grid(axis='y', color='#1a1f2e', linestyle='-', linewidth=0.6, alpha=0.6)
    
    for bar, val in zip(bars, exp_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, str(val), ha='center', color=text_color, fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", facecolor=bg_color, dpi=150)
    buffer.seek(0)
    chart2_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close(fig)

# CHART 3: Skill Category Distribution (NEW)
if can_generate_charts and len(category_distribution) >= 3:
    fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    cat_labels = list(category_distribution.keys())[:6]
    cat_values = [category_distribution[c]['count'] for c in cat_labels]
    cat_colors = ['#00d4ff', '#00ff88', '#ffc107', '#ff6b6b', '#b388ff', '#ff9966'][:len(cat_labels)]
    
    wedges, texts, autotexts = ax.pie(
        cat_values, 
        labels=cat_labels, 
        autopct='%1.0f%%',
        colors=cat_colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'color': text_color, 'fontsize': 10},
        pctdistance=0.75
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(f'Skill Categories - {role_name}', color=text_color, fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", facecolor=bg_color, dpi=150)
    buffer.seek(0)
    chart3_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close(fig)

# ============================================
# PREPARE RAW ANALYSIS DATA FOR AI (EXTENDED)
# ============================================
raw_analysis = {
    # Existing fields (preserved)
    'role_name': role_name,
    'total_jobs': total_jobs,
    'data_quality': data_quality,
    'quality_grade': quality_grade,
    'quality_desc': quality_desc,
    'core_skills': core_skills,
    'secondary_skills': secondary_skills,
    'skill_counts': dict(top_skills[:10]),
    'experience_distribution': exp_dist,
    'dominant_experience': dominant_level,
    'titles': titles[:5],
    'title_clarity': title_clarity,
    'companies': companies[:5],
    'locations': locations[:3],
    'market_consistency': consistency,
    'similarity_score': round(avg_similarity * 100, 1),
    
    # NEW: Skill normalization applied
    'skills_normalized': True,
    
    # NEW: Skill dominance metrics
    'skill_dominance': skill_dominance,
    
    # NEW: Skill category distribution
    'skill_categories': category_distribution,
    
    # NEW: Skill co-occurrence pairs
    'skill_cooccurrence': skill_cooccurrence[:5],
    
    # NEW: Data limitation flags
    'limitations': limitations,
    'has_limitations': len(limitations) > 0
}

# ============================================
# CHART CAPTIONS (Markdown)
# ============================================
chart1_caption = f"*📊 Skill Demand - {role_name}*\n\n_Top skills from {total_jobs} postings (normalized)._\n\n*Core:* {', '.join(core_skills[:3])}" if chart1_base64 else ""
chart2_caption = f"*📈 Experience Distribution - {role_name}*\n\n_Most demand: {dominant_level}_" if chart2_base64 else ""
chart3_caption = f"*🏷️ Skill Categories - {role_name}*\n\n_Distribution across {len(category_distribution)} categories._" if chart3_base64 else ""

return [{
    'raw_analysis': json.dumps(raw_analysis),
    'role_name': role_name,
    'total_jobs': total_jobs,
    'chart1_base64': chart1_base64,
    'chart1_caption': chart1_caption,
    'chart2_base64': chart2_base64,
    'chart2_caption': chart2_caption,
    'chart3_base64': chart3_base64,
    'chart3_caption': chart3_caption,
    'has_data': True
}]
