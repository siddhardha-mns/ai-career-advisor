import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json
import hashlib
import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Configure page
st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini API Client
class GeminiClient:
    def __init__(self):
        # Get API key from Streamlit secrets or environment variable
        try:
            self.api_key = st.secrets["api_keys"]["GEMINI_API_KEY"]
        except (KeyError, FileNotFoundError):
            self.api_key = os.environ.get("GEMINI_API_KEY")
            
        if not self.api_key or self.api_key == "your-actual-gemini-api-key-here":
            st.warning("⚠️ Gemini API key not configured. Using fallback data.")
            self.api_key = None
    
    def analyze_student_profile(self, profile: 'StudentProfile') -> str:
        """Analyze student profile and provide insights"""
        try:
            # This is a placeholder - you would implement actual Gemini API calls here
            # For now, returning a structured analysis based on the profile
            
            strengths = []
            if profile.technical_skills:
                strengths.append(f"Strong technical foundation with skills in {', '.join(profile.technical_skills[:3])}")
            if profile.academic_performance and float(profile.academic_performance or 0) > 75:
                strengths.append("Excellent academic performance")
            if profile.interests:
                strengths.append(f"Clear interests in {', '.join(profile.interests[:2])}")
            
            recommendations = []
            if not profile.technical_skills:
                recommendations.append("Consider developing technical skills relevant to your field")
            if not profile.career_goals:
                recommendations.append("Define clearer career goals and aspirations")
            
            completion_percentage = profile.get_completion_percentage()
            
            analysis = f"""
            **Profile Analysis for {profile.name or 'Student'}**
            
            **Strengths:**
            {chr(10).join('• ' + s for s in strengths) if strengths else '• Complete your profile to see personalized strengths'}
            
            **Career Readiness:** {'High' if completion_percentage > 70 else 'Developing'}
            
            **Key Recommendations:**
            {chr(10).join('• ' + r for r in recommendations) if recommendations else '• Continue building your skills and exploring career options'}
            
            **Next Steps:**
            • Explore career recommendations based on your profile
            • Analyze skills gaps for target careers
            • Create a learning roadmap for skill development
            """
            
            return analysis.strip()
            
        except Exception as e:
            return f"Profile analysis is currently unavailable. Error: {str(e)}"
    
    def get_career_recommendations(self, profile: 'StudentProfile') -> list:
        """Generate career recommendations using Gemini API"""
        try:
            # Placeholder for actual Gemini API call
            # You would construct a prompt and send it to Gemini API here
            
            prompt = f"""
            Based on this student profile, provide career recommendations:
            - Education: {profile.education_level} in {profile.stream}
            - Skills: {', '.join(profile.current_skills or [])}
            - Interests: {', '.join(profile.interests or [])}
            - Location: {profile.location}
            - Salary Expectations: {profile.salary_expectations}
            
            Provide 5-6 career recommendations with match scores, descriptions, and required skills.
            """
            
            # For now, fall back to the sample data function
            return get_sample_careers(profile)
            
        except Exception as e:
            st.error(f"Error generating recommendations with Gemini: {str(e)}")
            return get_sample_careers(profile)
    
    def analyze_skills_gap(self, profile: 'StudentProfile', career_data: dict) -> dict:
        """Analyze skills gap for a specific career using Gemini API"""
        try:
            # Placeholder for Gemini API call
            prompt = f"""
            Analyze the skills gap for this student pursuing {career_data.get('title')}:
            Current Skills: {', '.join(profile.current_skills or [])}
            Required Skills: {', '.join(career_data.get('required_skills', []))}
            
            Provide detailed gap analysis and learning recommendations.
            """
            
            # For now, return fallback analysis
            return generate_fallback_skills_analysis(profile, career_data)
            
        except Exception as e:
            st.error(f"Error analyzing skills gap with Gemini: {str(e)}")
            return generate_fallback_skills_analysis(profile, career_data)
    
    def get_skill_learning_resources(self, skill: str, profile: 'StudentProfile') -> str:
        """Get learning resources for a specific skill using Gemini API"""
        try:
            # Placeholder for Gemini API call
            resources = f"""
            **Learning Resources for {skill}:**
            
            **Online Courses:**
            • Coursera - Search for "{skill}" courses
            • Udemy - Practical {skill} tutorials
            • edX - University-level {skill} courses
            
            **Free Resources:**
            • YouTube tutorials on {skill}
            • GitHub repositories and projects
            • Official documentation and guides
            
            **Practice Platforms:**
            • HackerRank, LeetCode (for programming skills)
            • Kaggle (for data science skills)
            • Behance, Dribbble (for design skills)
            
            **Estimated Timeline:** 3-6 months with consistent practice
            """
            
            return resources
            
        except Exception as e:
            return f"Unable to fetch learning resources for {skill}. Please search for online courses and tutorials."
    
    def get_market_insights(self) -> dict:
        """Get job market insights using Gemini API"""
        try:
            # Placeholder for Gemini API call
            # For now, return sample data
            return get_sample_market_insights()
            
        except Exception as e:
            st.error(f"Error fetching market insights with Gemini: {str(e)}")
            return get_sample_market_insights()
    
    def generate_learning_roadmap(self, profile: 'StudentProfile', career_data: dict, 
                                 timeframe: str, intensity: str) -> dict:
        """Generate a learning roadmap using Gemini API"""
        try:
            # Placeholder for Gemini API call
            prompt = f"""
            Create a learning roadmap for:
            Student: {profile.name} targeting {career_data.get('title')}
            Timeframe: {timeframe}
            Intensity: {intensity}
            Current Skills: {', '.join(profile.current_skills or [])}
            Required Skills: {', '.join(career_data.get('required_skills', []))}
            """
            
            # For now, return fallback roadmap
            return generate_fallback_roadmap(profile, career_data, timeframe)
            
        except Exception as e:
            st.error(f"Error generating roadmap with Gemini: {str(e)}")
            return generate_fallback_roadmap(profile, career_data, timeframe)

# Data Models
@dataclass
class StudentProfile:
    # Basic Information
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    languages: List[str] = field(default_factory=list)
    
    # Academic Background
    education_level: Optional[str] = None
    stream: Optional[str] = None
    institution: Optional[str] = None
    academic_performance: Optional[str] = None
    subjects: List[str] = field(default_factory=list)
    
    # Skills and Interests
    current_skills: List[str] = field(default_factory=list)
    technical_skills: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    personality_traits: List[str] = field(default_factory=list)
    
    # Career Preferences
    work_environment: List[str] = field(default_factory=list)
    salary_expectations: Optional[str] = None
    job_type_preference: List[str] = field(default_factory=list)
    location_preference: List[str] = field(default_factory=list)
    career_goals: Optional[str] = None
    
    def get_completion_percentage(self) -> float:
        """Calculate profile completion percentage"""
        total_fields = 18
        completed_fields = 0
        
        if self.name and self.name.strip():
            completed_fields += 1
        if self.age and self.age > 0:
            completed_fields += 1
        if self.email and self.email.strip():
            completed_fields += 1
        if self.location and self.location != "Select State":
            completed_fields += 1
        if self.languages:
            completed_fields += 1
        if self.education_level:
            completed_fields += 1
        if self.stream:
            completed_fields += 1
        if self.institution and self.institution.strip():
            completed_fields += 1
        if self.academic_performance and float(self.academic_performance or 0) > 0:
            completed_fields += 1
        if self.subjects:
            completed_fields += 1
        if self.current_skills:
            completed_fields += 1
        if self.technical_skills:
            completed_fields += 1
        if self.interests:
            completed_fields += 1
        if self.personality_traits:
            completed_fields += 1
        if self.work_environment:
            completed_fields += 1
        if self.salary_expectations:
            completed_fields += 1
        if self.job_type_preference:
            completed_fields += 1
        if self.career_goals and self.career_goals.strip():
            completed_fields += 1
        
        return (completed_fields / total_fields) * 100

# Sample data functions
def get_sample_careers(profile: StudentProfile) -> List[Dict]:
    """Generate sample career recommendations based on profile"""
    all_careers = [
        {
            "title": "Software Engineer",
            "category": "Technology",
            "match_score": 85,
            "description": "Design, develop, and maintain software applications and systems",
            "why_suitable": "Strong technical aptitude and problem-solving skills align well",
            "required_skills": ["Programming", "Data Structures", "Problem Solving", "Software Design"],
            "education_required": "Bachelor's in Computer Science or related field",
            "salary_range": "6-25 LPA",
            "job_outlook": "Excellent growth prospects",
            "career_path": "Junior Developer → Senior Developer → Tech Lead → Engineering Manager"
        },
        {
            "title": "Data Scientist",
            "category": "Technology",
            "match_score": 80,
            "description": "Analyze complex data to derive insights and build predictive models",
            "why_suitable": "Analytical mindset and mathematical background are valuable",
            "required_skills": ["Python", "Statistics", "Machine Learning", "Data Visualization"],
            "education_required": "Bachelor's in Engineering, Mathematics, or related field",
            "salary_range": "8-30 LPA",
            "job_outlook": "High demand across industries",
            "career_path": "Data Analyst → Data Scientist → Senior Data Scientist → Data Science Manager"
        },
        {
            "title": "Digital Marketing Specialist",
            "category": "Sales & Marketing",
            "match_score": 75,
            "description": "Plan and execute digital marketing campaigns across various platforms",
            "why_suitable": "Creative thinking and communication skills are advantageous",
            "required_skills": ["Digital Marketing", "SEO/SEM", "Content Creation", "Analytics"],
            "education_required": "Bachelor's in Marketing, Business, or any field with relevant skills",
            "salary_range": "4-15 LPA",
            "job_outlook": "Growing rapidly with digital transformation",
            "career_path": "Marketing Executive → Digital Marketing Specialist → Marketing Manager → CMO"
        },
        {
            "title": "Business Analyst",
            "category": "Business & Management",
            "match_score": 70,
            "description": "Analyze business processes and recommend improvements",
            "why_suitable": "Strong analytical and communication skills are essential",
            "required_skills": ["Business Analysis", "Process Improvement", "Data Analysis", "Communication"],
            "education_required": "Bachelor's in Business, Engineering, or related field",
            "salary_range": "5-20 LPA",
            "job_outlook": "Steady demand across industries",
            "career_path": "Junior Analyst → Business Analyst → Senior Analyst → Consultant"
        },
        {
            "title": "UI/UX Designer",
            "category": "Creative & Media",
            "match_score": 78,
            "description": "Design user interfaces and experiences for digital products",
            "why_suitable": "Creative abilities and attention to detail are valuable",
            "required_skills": ["Design Tools", "User Research", "Prototyping", "Visual Design"],
            "education_required": "Bachelor's in Design, Computer Science, or relevant portfolio",
            "salary_range": "5-18 LPA",
            "job_outlook": "High demand with growing tech industry",
            "career_path": "Junior Designer → UI/UX Designer → Senior Designer → Design Lead"
        }
    ]
    
    # Adjust scores based on profile
    for career in all_careers:
        match_score = career["match_score"]
        
        # Check technical skills alignment
        if profile.technical_skills:
            career_skills = [skill.lower() for skill in career["required_skills"]]
            student_skills = [skill.lower() for skill in profile.technical_skills]
            skill_overlap = len(set(career_skills) & set(student_skills))
            if skill_overlap > 0:
                match_score += (skill_overlap * 5)
        
        # Check interest alignment
        if profile.interests:
            if career["category"].lower() in [interest.lower() for interest in profile.interests]:
                match_score += 10
        
        career["match_score"] = min(match_score, 100)
    
    all_careers.sort(key=lambda x: x["match_score"], reverse=True)
    return all_careers[:6]

def get_sample_market_insights():
    """Fallback market insights data"""
    return {
        'trends_summary': """
        The Indian job market is experiencing rapid transformation driven by digital adoption, 
        startup ecosystem growth, and emerging technologies. Key trends include:
        
        • **Digital Transformation**: 70% of companies are investing heavily in digital capabilities
        • **Remote Work**: Hybrid work models have become the new normal
        • **Skill-based Hiring**: Emphasis on skills over traditional qualifications
        • **Green Jobs**: Growing demand for sustainability-focused roles
        • **AI Integration**: Automation is creating new job categories while transforming existing ones
        """,
        'growing_sectors': [
            {'sector': 'Technology', 'growth_rate': 25, 'description': 'Continued digital transformation'},
            {'sector': 'Healthcare', 'growth_rate': 18, 'description': 'Post-pandemic growth and telemedicine'},
            {'sector': 'E-commerce', 'growth_rate': 22, 'description': 'Online retail expansion'},
            {'sector': 'Fintech', 'growth_rate': 20, 'description': 'Digital payments and banking'},
            {'sector': 'Education Technology', 'growth_rate': 16, 'description': 'Online learning platforms'},
            {'sector': 'Renewable Energy', 'growth_rate': 15, 'description': 'Green energy initiatives'}
        ],
        'in_demand_skills': [
            {'skill': 'Python Programming', 'demand_level': 'Very High'},
            {'skill': 'Data Analysis', 'demand_level': 'Very High'},
            {'skill': 'Digital Marketing', 'demand_level': 'High'},
            {'skill': 'Cloud Computing', 'demand_level': 'Very High'},
            {'skill': 'Machine Learning', 'demand_level': 'High'},
            {'skill': 'Cybersecurity', 'demand_level': 'High'},
            {'skill': 'UI/UX Design', 'demand_level': 'High'},
            {'skill': 'Project Management', 'demand_level': 'High'}
        ]
    }

def generate_fallback_roadmap(profile, career_data, timeframe):
    """Generate a basic roadmap when AI is not available"""
    required_skills = career_data.get('required_skills', [])
    current_skills = set(profile.current_skills or [])
    skills_to_learn = [skill for skill in required_skills if skill not in current_skills]
    
    if timeframe == "6 months":
        num_phases = 3
        phase_duration = "2 months"
    elif timeframe == "1 year":
        num_phases = 4
        phase_duration = "3 months"
    elif timeframe == "2 years":
        num_phases = 6
        phase_duration = "4 months"
    else:
        num_phases = 8
        phase_duration = "4-5 months"
    
    phases = []
    skills_per_phase = max(1, len(skills_to_learn) // num_phases) if skills_to_learn else 1
    
    for i in range(num_phases):
        start_idx = i * skills_per_phase
        end_idx = min((i + 1) * skills_per_phase, len(skills_to_learn))
        phase_skills = skills_to_learn[start_idx:end_idx] if skills_to_learn else []
        
        if i == 0:
            title = "Foundation Building"
            objective = "Build fundamental skills and knowledge base"
        elif i == num_phases - 1:
            title = "Advanced Skills & Specialization"
            objective = "Master advanced concepts and specialize in your chosen area"
        else:
            title = f"Skill Development Phase {i}"
            objective = f"Develop intermediate skills and practical experience"
        
        phases.append({
            'title': title,
            'duration': phase_duration,
            'objective': objective,
            'skills_to_learn': phase_skills,
            'activities': [
                "Online courses and tutorials",
                "Hands-on projects",
                "Practice and application",
                "Community participation"
            ],
            'milestones': [
                f"Complete {len(phase_skills)} skill modules",
                "Build 1-2 practical projects",
                "Join relevant communities",
                "Update portfolio/resume"
            ]
        })
    
    return {
        'overview': f"""
        This {timeframe} roadmap is designed to help you transition into {career_data.get('title', 'your target career')}.
        The plan is divided into {num_phases} phases, each focusing on specific skills and milestones.
        
        **Key Focus Areas:**
        • Skill development through practical learning
        • Building a strong portfolio
        • Networking and community engagement
        • Continuous practice and improvement
        """,
        'phases': phases,
        'resources': {
            'Online Platforms': [
                'Coursera - University courses and specializations',
                'Udemy - Practical skill-based courses',
                'YouTube - Free tutorials and walkthroughs',
                'freeCodeCamp - Programming and web development'
            ],
            'Practice Platforms': [
                'GitHub - Code repositories and projects',
                'Kaggle - Data science competitions',
                'HackerRank - Coding challenges',
                'LeetCode - Programming practice'
            ],
            'Communities': [
                'Reddit - Subject-specific communities',
                'Discord - Learning groups and study sessions',
                'LinkedIn - Professional networking',
                'Stack Overflow - Technical Q&A'
            ]
        }
    }

# Session state initialization
def initialize_session():
    if 'student_profile' not in st.session_state:
        st.session_state.student_profile = StudentProfile()
    if 'career_recommendations' not in st.session_state:
        st.session_state.career_recommendations = []
    if 'skills_analysis' not in st.session_state:
        st.session_state.skills_analysis = {}
    if 'learning_roadmap' not in st.session_state:
        st.session_state.learning_roadmap = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'

# Page functions
def render_dashboard():
    st.title("🎯 AI Career Advisor for Indian Students")
    st.markdown("### Personalized career guidance powered by AI")
    
    profile = st.session_state.student_profile
    completion_percentage = profile.get_completion_percentage()
    
    # Profile completion status
    st.sidebar.metric("Profile Completion", f"{completion_percentage:.0f}%")
    st.sidebar.progress(completion_percentage / 100)
    
    if completion_percentage < 50:
        st.sidebar.warning("Complete your profile to get better recommendations!")
    
    # Main dashboard content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Career Matches Found",
            value=len(st.session_state.career_recommendations),
            delta=f"+{len(st.session_state.career_recommendations)} new" if st.session_state.career_recommendations else None
        )
    
    with col2:
        skills_count = len(profile.current_skills) if profile.current_skills else 0
        st.metric(
            label="Current Skills",
            value=skills_count,
            delta=f"+{skills_count} mapped" if skills_count > 0 else None
        )
    
    with col3:
        market_trends = 15
        st.metric(
            label="Trending Opportunities",
            value=market_trends,
            delta="+3 this week"
        )
    
    st.markdown("---")
    
    # Quick start guide or summary
    if completion_percentage == 0:
        st.info("👋 Welcome! Let's get started with building your profile.")
        
        st.markdown("""
        ### How it works:
        1. **Build Your Profile** - Tell us about your interests, skills, and academic background
        2. **Get Recommendations** - Receive AI-powered career path suggestions
        3. **Analyze Skills Gap** - Understand what skills you need to develop
        4. **Explore Market Insights** - Stay updated with job market trends
        5. **Create Learning Path** - Get a personalized roadmap for skill development
        """)
        
        if st.button("Start Building Profile", type="primary"):
            st.session_state.current_page = 'Profile Builder'
            st.rerun()
    
    else:
        st.subheader("Your Career Journey Overview")
        
        # Career recommendations summary
        if st.session_state.career_recommendations:
            st.markdown("#### 🎯 Top Career Matches")
            
            for i, rec in enumerate(st.session_state.career_recommendations[:3]):
                with st.expander(f"{i+1}. {rec.get('title', 'Career Option')} - {rec.get('match_score', 0):.0f}% match"):
                    st.write(rec.get('description', 'No description available'))
                    if 'required_skills' in rec:
                        st.write("**Key Skills Required:**")
                        st.write(", ".join(rec['required_skills'][:5]))
        
        # Skills visualization
        if profile.current_skills:
            st.markdown("#### 📊 Your Skills Profile")
            
            skills_data = pd.DataFrame({
                'Skill': profile.current_skills,
                'Level': ['Intermediate'] * len(profile.current_skills)
            })
            
            chart = alt.Chart(skills_data).mark_bar().encode(
                x='Skill:N',
                y=alt.value(50),  # Fixed height for all bars
                color=alt.value('steelblue')
            ).properties(
                title="Current Skills Overview",
                width=600,
                height=300
            )
            st.altair_chart(chart, use_container_width=True)
        
        # Quick actions
        st.markdown("#### 🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Update Profile", type="secondary"):
                st.session_state.current_page = 'Profile Builder'
                st.rerun()
        
        with col2:
            if st.button("View Recommendations", type="secondary"):
                st.session_state.current_page = 'Career Recommendations'
                st.rerun()
        
        with col3:
            if st.button("Skills Analysis", type="secondary"):
                st.session_state.current_page = 'Skills Analysis'
                st.rerun()

def render_profile_builder():
    st.title("👤 Build Your Student Profile")
    st.markdown("Tell us about yourself to get personalized career recommendations")
    
    profile = st.session_state.student_profile
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Basic Info", "Academic Background", "Skills & Interests", "Career Preferences"])
    
    with tab1:
        st.subheader("Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            profile.name = st.text_input("Full Name", value=profile.name or "")
            profile.age = st.number_input("Age", min_value=16, max_value=30, value=profile.age or 18)
            profile.location = st.selectbox(
                "Location (State/City)",
                ["Select State", "Andhra Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "Telangana", 
                 "West Bengal", "Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"],
                index=0 if not profile.location else (
                    ["Select State", "Andhra Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "Telangana", 
                     "West Bengal", "Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"].index(profile.location) 
                    if profile.location in ["Select State", "Andhra Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "Telangana", 
                     "West Bengal", "Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"] else 0
                )
            )
        
        with col2:
            profile.email = st.text_input("Email Address", value=profile.email or "")
            profile.phone = st.text_input("Phone Number", value=profile.phone or "")
            
            languages = st.multiselect(
                "Languages Known",
                ["Hindi", "English", "Tamil", "Telugu", "Marathi", "Bengali", "Gujarati", "Kannada", 
                 "Malayalam", "Punjabi", "Other"],
                default=profile.languages or []
            )
            profile.languages = languages
    
    with tab2:
        st.subheader("Academic Background")
        
        col1, col2 = st.columns(2)
        
        with col1:
            profile.education_level = st.selectbox(
                "Current Education Level",
                ["High School (Class 10)", "Senior Secondary (Class 12)", "Undergraduate", 
                 "Graduate", "Post Graduate", "PhD"],
                index=0 if not profile.education_level else (
                    ["High School (Class 10)", "Senior Secondary (Class 12)", "Undergraduate", 
                     "Graduate", "Post Graduate", "PhD"].index(profile.education_level) 
                    if profile.education_level in ["High School (Class 10)", "Senior Secondary (Class 12)", "Undergraduate", 
                     "Graduate", "Post Graduate", "PhD"] else 0
                )
            )
            
            if profile.education_level in ["Senior Secondary (Class 12)", "Undergraduate", "Graduate", "Post Graduate"]:
                profile.stream = st.selectbox(
                    "Academic Stream/Field",
                    ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", 
                     "Engineering", "Medicine", "Law", "Management", "Computer Science", 
                     "Other"],
                    index=0 if not profile.stream else (
                        ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", 
                         "Engineering", "Medicine", "Law", "Management", "Computer Science", 
                         "Other"].index(profile.stream) 
                        if profile.stream in ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", 
                         "Engineering", "Medicine", "Law", "Management", "Computer Science", 
                         "Other"] else 0
                    )
                )
        
        with col2:
            profile.institution = st.text_input("Institution/College Name", value=profile.institution or "")
            
            percentage = st.number_input(
                "Academic Performance (%)", 
                min_value=0.0, max_value=100.0, 
                value=float(profile.academic_performance) if profile.academic_performance else 0.0,
                step=0.1
            )
            profile.academic_performance = str(percentage)
        
        # Subjects and specializations
        st.markdown("#### Subjects/Specializations")
        subjects = st.text_area(
            "List your main subjects or specializations (one per line)",
            value="\n".join(profile.subjects) if profile.subjects else "",
            help="e.g., Mathematics, Physics, Computer Science, Economics"
        )
        if subjects:
            profile.subjects = [s.strip() for s in subjects.split('\n') if s.strip()]
    
    with tab3:
        st.subheader("Skills & Interests")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current Skills")
            current_skills = st.text_area(
                "What skills do you currently have?",
                value="\n".join(profile.current_skills) if profile.current_skills else "",
                help="e.g., Programming, Communication, Leadership, Data Analysis",
                key="current_skills"
            )
            if current_skills:
                profile.current_skills = [s.strip() for s in current_skills.split('\n') if s.strip()]
            
            st.markdown("#### Technical Skills")
            tech_skills = st.multiselect(
                "Select your technical skills",
                ["Programming (Python)", "Programming (Java)", "Programming (C++)", "Web Development", 
                 "Data Analysis", "Machine Learning", "Database Management", "Cloud Computing", 
                 "Mobile App Development", "UI/UX Design", "Digital Marketing", "Content Writing"],
                default=profile.technical_skills or []
            )
            profile.technical_skills = tech_skills
        
        with col2:
            st.markdown("#### Areas of Interest")
            interests = st.multiselect(
                "What are you passionate about?",
                ["Technology", "Healthcare", "Education", "Finance", "Arts & Culture", "Sports", 
                 "Environment", "Social Work", "Business", "Research", "Government", "Media", 
                 "Entertainment", "Travel", "Fashion", "Food"],
                default=profile.interests or []
            )
            profile.interests = interests
            
            st.markdown("#### Personality Traits")
            personality = st.multiselect(
                "How would you describe yourself?",
                ["Analytical", "Creative", "Leadership", "Team Player", "Independent", "Detail-Oriented", 
                 "Problem Solver", "Communicative", "Adaptable", "Ambitious"],
                default=profile.personality_traits or []
            )
            profile.personality_traits = personality
    
    with tab4:
        st.subheader("Career Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            work_environment = st.multiselect(
                "Preferred Work Environment",
                ["Office-based", "Remote/Work from home", "Hybrid", "Field work", "Laboratory", 
                 "Hospital/Clinic", "Outdoor", "Creative studio", "Startup environment", "Corporate"],
                default=profile.work_environment or []
            )
            profile.work_environment = work_environment
            
            salary_expectations = st.selectbox(
                "Salary Expectations (Annual)",
                ["Below 3 LPA", "3-6 LPA", "6-10 LPA", "10-15 LPA", "15-25 LPA", "Above 25 LPA"],
                index=0 if not profile.salary_expectations else (
                    ["Below 3 LPA", "3-6 LPA", "6-10 LPA", "10-15 LPA", "15-25 LPA", "Above 25 LPA"].index(profile.salary_expectations) 
                    if profile.salary_expectations in ["Below 3 LPA", "3-6 LPA", "6-10 LPA", "10-15 LPA", "15-25 LPA", "Above 25 LPA"] else 0
                )
            )
            profile.salary_expectations = salary_expectations
        
        with col2:
            job_type = st.multiselect(
                "Job Type Preference",
                ["Full-time", "Part-time", "Freelance/Contract", "Internship", "Entrepreneurship"],
                default=profile.job_type_preference or []
            )
            profile.job_type_preference = job_type
            
            location_preference = st.multiselect(
                "Location Preference",
                ["Same city", "Same state", "Anywhere in India", "International", "Metro cities only"],
                default=profile.location_preference or []
            )
            profile.location_preference = location_preference
        
        # Career goals
        st.markdown("#### Career Goals")
        career_goals = st.text_area(
            "Describe your career goals and aspirations",
            value=profile.career_goals or "",
            help="What do you want to achieve in your career? Where do you see yourself in 5-10 years?"
        )
        profile.career_goals = career_goals
    
    # Save and analyze profile
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        completion = profile.get_completion_percentage()
        st.progress(completion / 100)
        st.caption(f"Profile Completion: {completion:.0f}%")
        
        if st.button("Save Profile & Generate Recommendations", type="primary", use_container_width=True):
            st.session_state.student_profile = profile
            
            with st.spinner("Analyzing your profile and generating recommendations..."):
                try:
                    # Initialize Gemini client and get AI analysis
                    client = GeminiClient()
                    analysis = client.analyze_student_profile(profile)
                    
                    # Generate career recommendations using Gemini
                    recommendations = client.get_career_recommendations(profile)
                    st.session_state.career_recommendations = recommendations
                    
                    st.success("Profile saved and recommendations generated!")
                    
                    # Display AI analysis
                    st.markdown("### 🤖 AI Profile Analysis")
                    st.write(analysis)
                    
                    st.markdown("### 🎯 Career Recommendations Generated")
                    st.write(f"Found {len(recommendations)} career matches based on your profile!")
                    
                    # Show top recommendation
                    if recommendations:
                        top_rec = recommendations[0]
                        st.markdown(f"**Top Match:** {top_rec['title']} ({top_rec['match_score']:.0f}% match)")
                        st.write(top_rec['description'])
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    # Fallback to basic recommendations
                    recommendations = get_sample_careers(profile)
                    st.session_state.career_recommendations = recommendations
                    st.info("Using basic recommendations due to API limitations.")
                
                st.markdown("### What's Next?")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("View All Recommendations", type="secondary"):
                        st.session_state.current_page = 'Career Recommendations'
                        st.rerun()
                
                with col2:
                    if st.button("Analyze Skills Gap", type="secondary"):
                        st.session_state.current_page = 'Skills Analysis'
                        st.rerun()

def render_career_recommendations():
    st.title("🎯 AI-Powered Career Recommendations")
    
    profile = st.session_state.student_profile
    
    # Check if profile is complete enough
    if profile.get_completion_percentage() < 30:
        st.warning("⚠️ Please complete more of your profile to get better recommendations.")
        if st.button("Complete Profile"):
            st.session_state.current_page = 'Profile Builder'
            st.rerun()
        return
    
    # Generate recommendations if not already available
    if not st.session_state.career_recommendations:
        with st.spinner("🤖 Generating personalized career recommendations..."):
            try:
                client = GeminiClient()
                recommendations = client.get_career_recommendations(profile)
                st.session_state.career_recommendations = recommendations
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
                st.info("Using sample recommendations...")
                # Fallback to basic recommendations
                st.session_state.career_recommendations = get_sample_careers(profile)
    
    recommendations = st.session_state.career_recommendations
    
    if not recommendations:
        st.error("Unable to generate recommendations. Please try again later.")
        return
    
    # Sidebar filters
    st.sidebar.header("Filter Recommendations")
    
    all_categories = list(set([rec.get('category', 'Other') for rec in recommendations]))
    selected_categories = st.sidebar.multiselect(
        "Career Categories",
        all_categories,
        default=all_categories
    )
    
    min_match_score = st.sidebar.slider(
        "Minimum Match Score",
        min_value=0,
        max_value=100,
        value=50,
        help="Filter careers by compatibility score"
    )
    
    # Filter recommendations
    filtered_recs = [
        rec for rec in recommendations 
        if rec.get('category', 'Other') in selected_categories 
        and rec.get('match_score', 0) >= min_match_score
    ]
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📊 Found {len(filtered_recs)} Career Matches")
    
    with col2:
        if st.button("🔄 Regenerate Recommendations", type="secondary"):
            st.session_state.career_recommendations = []
            st.rerun()
    
    if not filtered_recs:
        st.info("No careers match your current filters. Try adjusting the criteria.")
        return
    
    # Display recommendations
    for i, rec in enumerate(filtered_recs):
        with st.expander(
            f"🎯 {rec.get('title', f'Career Option {i+1}')} - {rec.get('match_score', 0):.0f}% Match",
            expanded=(i == 0)  # Expand first recommendation
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Category:** {rec.get('category', 'Not specified')}")
                st.markdown(f"**Description:**")
                st.write(rec.get('description', 'No description available'))
                
                if 'why_suitable' in rec:
                    st.markdown("**Why this career suits you:**")
                    st.write(rec['why_suitable'])
                
                if 'career_path' in rec:
                    st.markdown("**Typical Career Path:**")
                    st.write(rec['career_path'])
            
            with col2:
                # Match score display
                match_score = rec.get('match_score', 0)
                st.metric(
                    label="Match Score", 
                    value=f"{match_score:.0f}%",
                    delta=f"{'High' if match_score >= 80 else 'Good' if match_score >= 60 else 'Fair'} match"
                )
                
                # Progress bar for match score
                st.progress(match_score / 100)
                
                # Color-coded indicator
                if match_score >= 80:
                    st.success("Excellent Match!")
                elif match_score >= 60:
                    st.info("Good Match")
                else:
                    st.warning("Fair Match")
            
            # Skills and requirements
            col1, col2 = st.columns(2)
            
            with col1:
                if 'required_skills' in rec:
                    st.markdown("**Required Skills:**")
                    for skill in rec['required_skills']:
                        st.markdown(f"• {skill}")
            
            with col2:
                if 'salary_range' in rec:
                    st.markdown(f"**Salary Range:** {rec['salary_range']}")
                if 'job_outlook' in rec:
                    st.markdown(f"**Job Outlook:** {rec['job_outlook']}")
                if 'education_required' in rec:
                    st.markdown(f"**Education Required:** {rec['education_required']}")
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📋 Skills Analysis", key=f"skills_{i}"):
                    st.session_state.selected_career_for_analysis = rec
                    st.session_state.current_page = 'Skills Analysis'
                    st.rerun()
            
            with col2:
                if st.button(f"📚 Learning Path", key=f"learning_{i}"):
                    st.session_state.selected_career_for_roadmap = rec
                    st.session_state.current_page = 'Learning Roadmap'
                    st.rerun()
            
            with col3:
                if st.button(f"💼 Market Insights", key=f"market_{i}"):
                    st.session_state.current_page = 'Job Market Insights'
                    st.rerun()
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📈 Recommendations Summary")
    
    if filtered_recs:
        summary_df = pd.DataFrame(filtered_recs)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'category' in summary_df.columns and 'match_score' in summary_df.columns:
                avg_scores = summary_df.groupby('category')['match_score'].mean().reset_index()
                
                chart = alt.Chart(avg_scores).mark_bar().encode(
                    x=alt.X('match_score:Q', title='Average Match Score'),
                    y=alt.Y('category:N', title='Career Category', sort='-x'),
                    color=alt.value('steelblue')
                ).properties(
                    title="Average Match Score by Category",
                    width=400,
                    height=300
                )
                st.altair_chart(chart, use_container_width=True)
        
        with col2:
            if 'match_score' in summary_df.columns:
                chart = alt.Chart(summary_df).mark_bar().encode(
                    x=alt.X('match_score:Q', bin=alt.Bin(maxbins=10), title='Match Score'),
                    y=alt.Y('count():Q', title='Number of Careers'),
                    color=alt.value('lightblue')
                ).properties(
                    title="Distribution of Match Scores",
                    width=400,
                    height=300
                )
                st.altair_chart(chart, use_container_width=True)

def render_skills_analysis():
    st.title("📊 Skills Gap Analysis")
    st.markdown("Understand what skills you need to develop for your target careers")
    
    profile = st.session_state.student_profile
    
    # Check if we have a selected career from recommendations
    selected_career = st.session_state.get('selected_career_for_analysis', None)
    
    # Career selection
    st.subheader("🎯 Select Career for Analysis")
    
    if st.session_state.career_recommendations:
        career_options = [f"{rec.get('title', 'Unknown')} ({rec.get('match_score', 0):.0f}% match)" 
                         for rec in st.session_state.career_recommendations]
        
        if selected_career:
            try:
                selected_title = f"{selected_career.get('title', 'Unknown')} ({selected_career.get('match_score', 0):.0f}% match)"
                default_index = career_options.index(selected_title)
            except ValueError:
                default_index = 0
        else:
            default_index = 0
        
        selected_option = st.selectbox(
            "Choose a career to analyze",
            career_options,
            index=default_index
        )
        
        selected_index = career_options.index(selected_option)
        career_data = st.session_state.career_recommendations[selected_index]
        
    else:
        st.warning("No career recommendations found. Please generate recommendations first.")
        if st.button("Get Career Recommendations"):
            st.session_state.current_page = 'Career Recommendations'
            st.rerun()
        return
    
    # Generate skills analysis
    if st.button("🔍 Analyze Skills Gap", type="primary"):
        with st.spinner("Analyzing your skills gap..."):
            try:
                client = GeminiClient()
                analysis = client.analyze_skills_gap(profile, career_data)
                st.session_state.skills_analysis = analysis
            except Exception as e:
                st.error(f"Error analyzing skills: {str(e)}")
                # Fallback analysis
                analysis = generate_fallback_skills_analysis(profile, career_data)
                st.session_state.skills_analysis = analysis
    
    # Display analysis if available
    if 'skills_analysis' in st.session_state and st.session_state.skills_analysis:
        analysis = st.session_state.skills_analysis
        
        st.markdown("---")
        st.subheader(f"📈 Skills Analysis for {career_data.get('title', 'Selected Career')}")
        
        # Current skills vs Required skills
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Your Current Skills")
            current_skills = profile.current_skills or []
            if current_skills:
                for skill in current_skills:
                    st.markdown(f"• {skill}")
            else:
                st.info("No current skills listed in your profile")
        
        with col2:
            st.markdown("#### 🎯 Required Skills")
            required_skills = career_data.get('required_skills', [])
            if required_skills:
                for skill in required_skills:
                    st.markdown(f"• {skill}")
            else:
                st.info("No specific skills listed for this career")
        
        # Skills gap visualization
        if current_skills and required_skills:
            st.markdown("---")
            st.subheader("📊 Skills Gap Visualization")
            
            current_set = set(current_skills)
            required_set = set(required_skills)
            
            matching_skills = list(current_set.intersection(required_set))
            missing_skills = list(required_set - current_set)
            extra_skills = list(current_set - required_set)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Skills Match", len(matching_skills))
            
            with col2:
                st.metric("Skills to Learn", len(missing_skills))
            
            with col3:
                st.metric("Extra Skills", len(extra_skills))
            
            with col4:
                match_percentage = (len(matching_skills) / len(required_skills) * 100) if required_skills else 0
                st.metric("Match Percentage", f"{match_percentage:.0f}%")
            
            # Skills comparison chart
            skills_data = []
            
            for skill in matching_skills:
                skills_data.append({"Skill": skill, "Status": "You Have", "Category": "Matching"})
            
            for skill in missing_skills:
                skills_data.append({"Skill": skill, "Status": "Need to Learn", "Category": "Missing"})
            
            for skill in extra_skills:
                skills_data.append({"Skill": skill, "Status": "Additional", "Category": "Extra"})
            
            if skills_data:
                df = pd.DataFrame(skills_data)
                
                # Create color mapping
                color_scale = alt.Scale(
                    domain=["You Have", "Need to Learn", "Additional"],
                    range=["green", "red", "blue"]
                )
                
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('Skill:N', title='Skills'),
                    y=alt.value(30),  # Fixed height
                    color=alt.Color('Status:N', scale=color_scale),
                    tooltip=['Skill:N', 'Status:N', 'Category:N']
                ).properties(
                    title="Skills Analysis Overview",
                    width=600,
                    height=400
                )
                st.altair_chart(chart, use_container_width=True)
        
        # Detailed gap analysis
        if 'gap_analysis' in analysis:
            st.markdown("---")
            st.subheader("🤖 Skills Gap Analysis")
            st.write(analysis['gap_analysis'])
        
        # Priority skills to develop with learning resources
        if current_skills and required_skills:
            missing_skills = list(set(required_skills) - set(current_skills))
            
            if missing_skills:
                st.markdown("---")
                st.subheader("🎯 Priority Skills to Develop")
                
                priority_skills = st.multiselect(
                    "Select skills you want to focus on first:",
                    missing_skills,
                    default=missing_skills[:3] if len(missing_skills) >= 3 else missing_skills
                )
                
                if priority_skills:
                    st.markdown("#### 📚 Learning Resources for Priority Skills")
                    
                    for skill in priority_skills:
                        with st.expander(f"📖 Learn {skill}"):
                            # Generate learning resources for each skill using Gemini
                            try:
                                client = GeminiClient()
                                resources = client.get_skill_learning_resources(skill, profile)
                                st.write(resources)
                            except:
                                # Fallback resources
                                st.write(f"""
                                **Recommended learning paths for {skill}:**
                                
                                • Online courses (Coursera, edX, Udemy)
                                • YouTube tutorials and channels
                                • Practice projects and portfolios
                                • Professional certifications
                                • Books and documentation
                                • Industry workshops and webinars
                                """)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Create Learning Roadmap", type="primary"):
                st.session_state.selected_career_for_roadmap = career_data
                st.session_state.current_page = 'Learning Roadmap'
                st.rerun()
        
        with col2:
            if st.button("💼 View Market Insights", type="secondary"):
                st.session_state.current_page = 'Job Market Insights'
                st.rerun()
        
        with col3:
            if st.button("🎯 Back to Recommendations", type="secondary"):
                st.session_state.current_page = 'Career Recommendations'
                st.rerun()

def generate_fallback_skills_analysis(profile, career_data):
    """Generate a basic skills analysis"""
    current_skills = set(profile.current_skills or [])
    required_skills = set(career_data.get('required_skills', []))
    
    matching = current_skills.intersection(required_skills)
    missing = required_skills - current_skills
    
    return {
        'gap_analysis': f"""
        Based on your profile and the selected career path, here's your skills analysis:
        
        **Strengths:**
        You already have {len(matching)} out of {len(required_skills)} required skills.
        
        **Areas for Development:**
        You need to develop {len(missing)} additional skills to be fully prepared for this career.
        
        **Recommendation:**
        Focus on building the missing skills through online courses, practical projects, and hands-on experience.
        """,
        'recommendations': """
        **Immediate Actions:**
        1. Enroll in online courses for your top 2-3 missing skills
        2. Start working on practical projects to build your portfolio
        3. Connect with professionals in this field for mentorship
        4. Join relevant communities and forums
        5. Consider internships or entry-level positions to gain experience
        """
    }

def render_job_market_insights():
    st.title("💼 Indian Job Market Insights")
    st.markdown("Stay updated with the latest trends and opportunities in the Indian job market")
    
    # Market insights tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Trends", "🚀 Emerging Roles", "💰 Salary Insights", "🏢 Top Employers"])
    
    with tab1:
        st.subheader("📈 Current Market Trends")
        
        # Generate market insights
        if st.button("🔄 Get Latest Market Insights", type="primary"):
            with st.spinner("Fetching latest job market data..."):
                try:
                    client = GeminiClient()
                    market_insights = client.get_market_insights()
                    st.session_state.market_insights = market_insights
                except Exception as e:
                    st.error(f"Error fetching insights: {str(e)}")
                    # Fallback to sample data
                    st.session_state.market_insights = get_sample_market_insights()
        
        insights = st.session_state.get('market_insights', get_sample_market_insights())
        
        if insights:
            st.markdown("#### 🎯 Key Market Trends")
            st.write(insights.get('trends_summary', 'Market insights not available'))
            
            st.markdown("#### 📊 Top Growing Sectors")
            
            growing_sectors = insights.get('growing_sectors', [])
            if growing_sectors:
                sectors_df = pd.DataFrame(growing_sectors)
                
                if 'growth_rate' in sectors_df.columns:
                    chart = alt.Chart(sectors_df).mark_bar().encode(
                        x=alt.X('growth_rate:Q', title='Growth Rate (%)'),
                        y=alt.Y('sector:N', title='Sector', sort='-x'),
                        color=alt.value('lightgreen'),
                        tooltip=['sector:N', 'growth_rate:Q', 'description:N']
                    ).properties(
                        title="Fastest Growing Sectors in India",
                        width=600,
                        height=400
                    )
                    st.altair_chart(chart, use_container_width=True)
            
            st.markdown("#### 🔥 Most In-Demand Skills")
            
            demand_skills = insights.get('in_demand_skills', [])
            if demand_skills:
                col1, col2 = st.columns(2)
                
                mid_point = len(demand_skills) // 2
                
                with col1:
                    for skill in demand_skills[:mid_point]:
                        demand_level = skill.get('demand_level', 'High')
                        color = "🔴" if demand_level == "Very High" else "🟡" if demand_level == "High" else "🟢"
                        st.markdown(f"{color} **{skill.get('skill', 'Unknown')}** - {demand_level} demand")
                
                with col2:
                    for skill in demand_skills[mid_point:]:
                        demand_level = skill.get('demand_level', 'High')
                        color = "🔴" if demand_level == "Very High" else "🟡" if demand_level == "High" else "🟢"
                        st.markdown(f"{color} **{skill.get('skill', 'Unknown')}** - {demand_level} demand")
    
    with tab2:
        st.subheader("🚀 Emerging Roles & Future Careers")
        
        emerging_roles = [
            {
                'title': 'AI Ethics Specialist',
                'growth_potential': 'Very High',
                'description': 'Ensures responsible development and deployment of AI systems',
                'why_emerging': 'Growing concerns about AI bias, privacy, and ethical implications',
                'key_skills': ['Machine Learning', 'Ethics', 'Policy Development', 'Risk Assessment'],
                'salary_range': '15-30 LPA',
                'experience_level': 'Mid to Senior',
                'remote_friendly': True
            },
            {
                'title': 'Sustainability Manager',
                'growth_potential': 'High',
                'description': 'Develops and implements environmental sustainability strategies',
                'why_emerging': 'Increased focus on ESG goals and climate change',
                'key_skills': ['Environmental Science', 'Project Management', 'Data Analysis', 'Policy'],
                'salary_range': '12-25 LPA',
                'experience_level': 'Mid-level',
                'remote_friendly': False
            }
        ]
        
        for role in emerging_roles:
            with st.expander(f"🆕 {role['title']} - {role['growth_potential']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {role['description']}")
                    st.markdown(f"**Why it's emerging:** {role['why_emerging']}")
                    
                    if 'key_skills' in role:
                        st.markdown("**Key Skills Required:**")
                        for skill in role['key_skills']:
                            st.markdown(f"• {skill}")
                
                with col2:
                    st.markdown(f"**Salary Range:** {role.get('salary_range', 'Varies')}")
                    st.markdown(f"**Experience Level:** {role.get('experience_level', 'Entry to Mid')}")
                    st.markdown(f"**Remote Friendly:** {'✅' if role.get('remote_friendly', False) else '❌'}")
    
    with tab3:
        st.subheader("💰 Salary Insights & Compensation Trends")
        
        # Sample salary data
        salary_data = []
        roles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'Digital Marketer']
        base_salaries = [8, 12, 15, 6]
        
        for role, base in zip(roles, base_salaries):
            for i in range(10):
                salary_data.append({
                    'role': role,
                    'salary_lpa': base + (i * 2) + (i % 3)
                })
        
        salary_df = pd.DataFrame(salary_data)
        
        # Create a simpler bar chart showing average salaries
        avg_salary = salary_df.groupby('role')['salary_lpa'].mean().reset_index()
        
        chart = alt.Chart(avg_salary).mark_bar().encode(
            x=alt.X('role:N', title='Job Role'),
            y=alt.Y('salary_lpa:Q', title='Average Salary (LPA)'),
            color=alt.value('lightcoral'),
            tooltip=['role:N', 'salary_lpa:Q']
        ).properties(
            title="Average Salary by Role",
            width=600,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)
    
    with tab4:
        st.subheader("🏢 Top Employers & Company Insights")
        
        employers_data = {
            '🚀 Technology Companies': [
                {
                    'name': 'Tata Consultancy Services',
                    'size': '500,000+',
                    'known_for': 'IT Services, Consulting',
                    'hiring_trend': 'Actively hiring for cloud and AI roles'
                },
                {
                    'name': 'Infosys',
                    'size': '300,000+',
                    'known_for': 'Digital transformation, Consulting',
                    'hiring_trend': 'Focus on digital skills and automation'
                }
            ]
        }
        
        for category, companies in employers_data.items():
            st.markdown(f"#### {category}")
            
            for company in companies:
                with st.container():
                    st.markdown(f"**{company['name']}**")
                    st.markdown(f"• Employees: {company['size']}")
                    st.markdown(f"• Known for: {company['known_for']}")
                    st.markdown(f"• Hiring trends: {company['hiring_trend']}")
                    st.markdown("---")

def render_learning_roadmap():
    st.title("📚 Personalized Learning Roadmap")
    st.markdown("Create a structured path to achieve your career goals")
    
    profile = st.session_state.student_profile
    
    # Career selection for roadmap
    st.subheader("🎯 Select Career Goal")
    
    selected_career = st.session_state.get('selected_career_for_roadmap', None)
    
    if st.session_state.career_recommendations:
        career_options = [f"{rec.get('title', 'Unknown')} ({rec.get('match_score', 0):.0f}% match)" 
                         for rec in st.session_state.career_recommendations]
        
        if selected_career:
            try:
                selected_title = f"{selected_career.get('title', 'Unknown')} ({selected_career.get('match_score', 0):.0f}% match)"
                default_index = career_options.index(selected_title)
            except ValueError:
                default_index = 0
        else:
            default_index = 0
        
        selected_option = st.selectbox(
            "Choose your target career",
            career_options,
            index=default_index
        )
        
        selected_index = career_options.index(selected_option)
        career_data = st.session_state.career_recommendations[selected_index]
        
    else:
        st.warning("No career recommendations found. Please generate recommendations first.")
        if st.button("Get Career Recommendations"):
            st.session_state.current_page = 'Career Recommendations'
            st.rerun()
        return
    
    # Roadmap customization
    col1, col2 = st.columns(2)
    
    with col1:
        target_timeframe = st.selectbox(
            "Target Timeframe",
            ["6 months", "1 year", "2 years", "3 years"],
            index=1
        )
    
    with col2:
        learning_intensity = st.selectbox(
            "Learning Intensity",
            ["Light (5-10 hrs/week)", "Moderate (10-20 hrs/week)", "Intensive (20+ hrs/week)"],
            index=1
        )
    
    # Generate roadmap
    if st.button("🛣️ Generate Learning Roadmap", type="primary"):
        with st.spinner("Creating your personalized learning roadmap..."):
            try:
                client = GeminiClient()
                roadmap = client.generate_learning_roadmap(profile, career_data, target_timeframe, learning_intensity)
                st.session_state.learning_roadmap = roadmap
            except Exception as e:
                st.error(f"Error generating roadmap: {str(e)}")
                # Fallback roadmap
                roadmap = generate_fallback_roadmap(profile, career_data, target_timeframe)
                st.session_state.learning_roadmap = roadmap
    
    # Display roadmap
    if 'learning_roadmap' in st.session_state and st.session_state.learning_roadmap:
        roadmap = st.session_state.learning_roadmap
        
        st.markdown("---")
        st.subheader(f"🎯 Learning Roadmap for {career_data.get('title', 'Your Career Goal')}")
        
        # Overview
        if 'overview' in roadmap:
            st.markdown("#### 📋 Roadmap Overview")
            st.write(roadmap['overview'])
        
        # Learning phases
        if 'phases' in roadmap:
            st.markdown("#### 📅 Learning Phases")
            
            for i, phase in enumerate(roadmap['phases']):
                with st.expander(f"Phase {i+1}: {phase.get('title', f'Phase {i+1}')} ({phase.get('duration', 'TBD')})", expanded=(i==0)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Objective:** {phase.get('objective', 'Not specified')}")
                        
                        if 'skills_to_learn' in phase:
                            st.markdown("**Skills to Learn:**")
                            for skill in phase['skills_to_learn']:
                                st.markdown(f"• {skill}")
                        
                        if 'activities' in phase:
                            st.markdown("**Learning Activities:**")
                            for activity in phase['activities']:
                                st.markdown(f"• {activity}")
                    
                    with col2:
                        if 'milestones' in phase:
                            st.markdown("**Milestones:**")
                            for milestone in phase['milestones']:
                                st.markdown(f"✅ {milestone}")
                        
                        # Progress tracking
                        st.markdown("**Track Progress:**")
                        progress = st.slider(
                            f"Phase {i+1} Progress",
                            0, 100, 0,
                            key=f"phase_{i}_progress"
                        )
                        
                        if progress > 0:
                            st.success(f"{progress}% Complete")
        
        # Resource recommendations
        if 'resources' in roadmap:
            st.markdown("#### 📖 Recommended Learning Resources")
            
            resource_categories = roadmap['resources']
            
            for category, resources in resource_categories.items():
                st.markdown(f"**{category}:**")
                for resource in resources:
                    st.markdown(f"• {resource}")

# Navigation
def render_navigation():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    pages = {
        'Dashboard': '🏠',
        'Profile Builder': '👤',
        'Career Recommendations': '🎯',
        'Skills Analysis': '📊',
        'Job Market Insights': '💼',
        'Learning Roadmap': '📚'
    }
    
    for page, icon in pages.items():
        if st.sidebar.button(f"{icon} {page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Profile completion status
    if hasattr(st.session_state, 'student_profile'):
        profile = st.session_state.student_profile
        completion = profile.get_completion_percentage()
        st.sidebar.metric("Profile Completion", f"{completion:.0f}%")
        st.sidebar.progress(completion / 100)

# Main application
def main():
    initialize_session()
    render_navigation()
    
    # Route to appropriate page
    current_page = st.session_state.get('current_page', 'Dashboard')
    
    if current_page == 'Dashboard':
        render_dashboard()
    elif current_page == 'Profile Builder':
        render_profile_builder()
    elif current_page == 'Career Recommendations':
        render_career_recommendations()
    elif current_page == 'Skills Analysis':
        render_skills_analysis()
    elif current_page == 'Job Market Insights':
        render_job_market_insights()
    elif current_page == 'Learning Roadmap':
        render_learning_roadmap()

if __name__ == "__main__":
    main()
