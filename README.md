# AI Career Advisor for Indian Students

An intelligent career guidance platform powered by AI that provides personalized career recommendations, skills gap analysis, and learning roadmaps specifically designed for Indian students and the local job market.

## Features

### Core Functionality
- **Comprehensive Profile Builder**: Multi-tab interface for capturing academic background, skills, interests, and career preferences
- **AI-Powered Career Recommendations**: Personalized career matches with detailed scoring and rationale
- **Skills Gap Analysis**: Visual analysis of current vs required skills with learning recommendations
- **Learning Roadmap Generator**: Structured learning paths with phases, milestones, and resources
- **Job Market Insights**: Real-time trends, emerging roles, and salary data for the Indian market

### Key Capabilities
- **Indian Market Focus**: Salary ranges in LPA, location preferences, and sector-specific insights
- **Multi-dimensional Assessment**: Beyond skills - includes personality traits, work environment, and cultural factors
- **Visual Analytics**: Interactive charts and progress tracking using Altair
- **Resource Integration**: Curated learning resources from Indian and international platforms
- **Progress Tracking**: Session-based profile completion and learning phase monitoring

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas for data manipulation
- **Visualizations**: Altair for interactive charts
- **AI Integration**: Google Gemini API (with fallback mechanisms)
- **State Management**: Streamlit session state
- **Data Models**: Python dataclasses for structured profile management

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-career-advisor.git
cd ai-career-advisor
```

2. **Create virtual environment**
```bash
python -m venv career_advisor_env
source career_advisor_env/bin/activate  # On Windows: career_advisor_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install streamlit pandas altair python-dotenv
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your-actual-gemini-api-key-here
```

Alternatively, configure in Streamlit secrets:
```toml
# .streamlit/secrets.toml
[api_keys]
GEMINI_API_KEY = "your-actual-gemini-api-key-here"
```

## Usage

1. **Start the application**
```bash
streamlit run main.py
```

2. **Navigate to the application**
Open your browser and go to `http://localhost:8501`

3. **Build your profile**
   - Complete the comprehensive profile across 4 tabs
   - Provide information about academics, skills, interests, and career preferences
   - Profile completion percentage is tracked in the sidebar

4. **Get career recommendations**
   - AI analyzes your profile and generates personalized career matches
   - Each recommendation includes match score, description, and requirements
   - Filter by category, salary range, or match score

5. **Analyze skills gaps**
   - Select a target career for detailed analysis
   - View visual comparison of current vs required skills
   - Get prioritized learning recommendations

6. **Create learning roadmap**
   - Generate structured learning paths based on your goals
   - Customize timeframe and intensity
   - Track progress through different phases

## Project Structure

```
ai-career-advisor/
│
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── .streamlit/
│   └── secrets.toml       # Streamlit secrets (alternative config)
│
└── README.md              # This file
```

## Configuration

### Gemini API Setup
1. Get your Gemini API key from Google AI Studio
2. Add it to either `.env` file or Streamlit secrets
3. The application includes fallback mechanisms if API is unavailable

### Customization Options
- **Career Database**: Modify `get_sample_careers()` function to add more career options
- **Market Insights**: Update `get_sample_market_insights()` for current data
- **Skills Framework**: Extend skill categories in profile builder
- **Regional Adaptation**: Modify location options and salary ranges

## Key Components

### StudentProfile Class
Dataclass-based model capturing:
- Basic information (name, age, location, languages)
- Academic background (education level, stream, performance)
- Skills and interests (current skills, technical skills, personality traits)
- Career preferences (work environment, salary expectations, job type)

### GeminiClient Class
AI integration layer providing:
- Profile analysis and insights
- Career recommendation generation
- Skills gap analysis
- Learning resource suggestions
- Market trend analysis

### Page Functions
- `render_dashboard()`: Main overview with metrics and quick actions
- `render_profile_builder()`: Multi-tab profile creation interface
- `render_career_recommendations()`: AI-generated career matches with filtering
- `render_skills_analysis()`: Visual skills gap analysis
- `render_job_market_insights()`: Market trends and employer data
- `render_learning_roadmap()`: Structured learning path generation

## Data Models

The application uses structured data models for:
- **Career Recommendations**: Title, category, match score, description, required skills
- **Market Insights**: Growing sectors, in-demand skills, salary trends
- **Learning Roadmaps**: Phases, objectives, activities, milestones, resources

## Deployment

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy with automatic updates

### Local Deployment
```bash
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## API Integration Notes

The application is designed to work with Google's Gemini API but includes comprehensive fallback mechanisms:
- Sample career data when API is unavailable
- Basic skills analysis without AI
- Template learning roadmaps
- Static market insights

## Limitations and Future Enhancements

### Current Limitations
- Requires manual profile completion
- Limited to predefined career options in fallback mode
- Static market data when API is unavailable

### Planned Enhancements
- Integration with job portals for real-time data
- Advanced personality assessment tools
- Mentor matching functionality
- Progress tracking with notifications
- Multi-language support for Indian regional languages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions:
- Create an issue in the GitHub repository
- Contact: 8897977896

## Acknowledgments

- Built for Indian students with local market context
- Utilizes Google Gemini API for AI capabilities
- Streamlit for rapid web application development
- Altair for interactive data visualizations

---

**Note**: This application is designed specifically for the Indian job market and includes culturally relevant features such as LPA salary ranges, Indian cities, and local education systems.
