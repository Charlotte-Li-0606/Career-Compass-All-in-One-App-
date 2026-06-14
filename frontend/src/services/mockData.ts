import type { CareerSummary, SkillsTable, ResumeRefinementResponse } from '../types';

// ── Mock Career Summary ──
export const mockCareerSummary: CareerSummary = {
  overview:
    "You're on an exciting path! With a background in Computer Science and a keen interest in data and analytics, you're well-positioned for the fast-growing data career ecosystem. Your Python skills and internship experience give you a strong foundation — now it's about layering on the specific tools and domain knowledge that employers in Hong Kong's finance and tech sectors are actively seeking.",
  recommendedRoles: [
    {
      title: 'Data Analyst',
      fit: 'Strong fit — your SQL and Python foundation plus business-facing internship experience align well with analyst roles at banks and consultancies in Hong Kong.',
      growthOutlook: 'Demand in HK fintech sector growing ~15% YoY. Entry roles typically HKD 22k–30k/month.',
    },
    {
      title: 'Business Intelligence Developer',
      fit: 'Good fit — your interest in visualization and data storytelling maps to BI roles that bridge technical and business teams.',
      growthOutlook: 'Steady demand across MNCs with APAC hubs in Hong Kong. Power BI and Tableau are key.',
    },
    {
      title: 'AI/ML Engineer (future target)',
      fit: 'Longer-term path — after building analytics experience and deepening your math/stats, this becomes reachable within 2–3 years.',
      growthOutlook: 'Highest growth segment in HK tech. Requires strong Python, ML frameworks, and cloud deployment skills.',
    },
  ],
  industryInsights:
    "Hong Kong's push toward smart city and fintech innovation means data-skilled graduates are in high demand. Employers like HSBC, AIA, and the HKMA are expanding data teams. Your multilingual background is a unique advantage — many firms need analysts who can work across Cantonese, Mandarin, and English datasets.",
  nextSteps: [
    'Build a portfolio project using real Hong Kong open data (e.g., Transport Department, Census data)',
    'Complete a Power BI or Tableau certification before graduation',
    'Join HK Data Science Meetup or similar community to network with hiring managers',
    'Consider a part-time data internship or freelance project this semester',
  ],
};

// ── Mock Skills Table ──
export const mockSkillsTable: SkillsTable = {
  summary:
    'Based on your target role of Data Analyst, here is your current skills landscape. You have a solid technical core — investing in visualization tools and cloud basics will make you highly competitive.',
  skills: [
    { name: 'Python', category: 'Programming', proficiency: 'mastered', description: 'Strong foundation — you can write scripts, use pandas, and automate tasks.', importance: 'critical' },
    { name: 'SQL', category: 'Data', proficiency: 'mastered', description: 'Comfortable with queries, joins, and basic aggregation from your coursework.', importance: 'critical' },
    { name: 'Excel / Sheets', category: 'Business Tools', proficiency: 'mastered', description: 'Pivot tables, VLOOKUP, and basic macros.', importance: 'recommended' },
    { name: 'Data Visualization (Tableau/Power BI)', category: 'BI Tools', proficiency: 'learning', description: 'You have exposure through one class project. Build more dashboards to reach proficiency.', importance: 'critical' },
    { name: 'Statistics & A/B Testing', category: 'Analytics', proficiency: 'learning', description: 'You understand basic concepts. Deepening this helps with data analyst interviews.', importance: 'critical' },
    { name: 'R', category: 'Programming', proficiency: 'learning', description: 'Some exposure. Many HK universities still teach R — useful for academic research roles.', importance: 'recommended' },
    { name: 'Cloud (Azure / AWS)', category: 'Infrastructure', proficiency: 'missing', description: 'No experience yet. Cloud basics are increasingly expected even for analyst roles. Start with Azure Fundamentals (AZ-900).', importance: 'recommended' },
    { name: 'Machine Learning (scikit-learn)', category: 'AI/ML', proficiency: 'missing', description: 'Not required for entry analyst roles, but important if you want to move toward AI/ML engineering later.', importance: 'nice-to-have' },
    { name: 'Git & GitHub', category: 'Dev Tools', proficiency: 'learning', description: 'You can clone and commit. Practice branching and PR workflows for team environments.', importance: 'recommended' },
    { name: 'Cantonese Business Communication', category: 'Language', proficiency: 'mastered', description: 'Fluent — a strong asset for HK-based roles requiring stakeholder interaction.', importance: 'critical' },
  ],
};

// ── Mock Resume Refinement ──
export const mockResumeRefinement: ResumeRefinementResponse = {
  refinedText: `# JOHN DOE
**Data Analyst | Python • SQL • Tableau**
📧 jdoe@link.cuhk.edu.hk | 📱 +852 1234 5678 | 🔗 linkedin.com/in/johndoe

## SUMMARY
Detail-oriented Computer Science student at CUHK with hands-on data analysis experience from a fintech internship. Proficient in Python, SQL, and data visualization. Seeking a Data Analyst role where I can apply analytical skills to drive business insights.

## EDUCATION
**The Chinese University of Hong Kong** — B.Sc. Computer Science
*Expected June 2027* | GPA: 3.4/4.0
Relevant Coursework: Data Structures, Database Systems, Statistics for Computing, Machine Learning

## EXPERIENCE
**FinTech Innovations Ltd, Hong Kong** — Data Analyst Intern
*Jun 2025 – Aug 2025*
- Analyzed 50,000+ transaction records using Python (pandas), identifying 3 cost-saving opportunities adopted by the operations team
- Built an automated reporting dashboard in Power BI, reducing weekly manual reporting time by 40%
- Collaborated with the risk team to develop SQL queries for fraud pattern detection

**CUHK Student IT Helpdesk** — Part-Time Support
*Sep 2024 – Present*
- Assist 30+ students weekly with technical issues, developing strong communication and problem-solving skills

## PROJECTS
**Hong Kong Public Transport Analysis** | Python, Tableau
- Scraped and analyzed MTR and bus route data to visualize peak-hour congestion patterns
- Created an interactive Tableau dashboard viewed by 200+ students for commute planning

## SKILLS
- **Languages:** Python, SQL, JavaScript, R (basic)
- **Tools:** Power BI, Tableau, Git, Excel, Jupyter
- **Languages:** English (Fluent), Cantonese (Native), Mandarin (Conversational)`,
  changes: [
    { type: 'added', description: 'Quantified achievements with specific metrics (50K+ records, 40% time reduction)', section: 'Experience' },
    { type: 'modified', description: 'Strengthened summary section to target Data Analyst roles specifically', section: 'Summary' },
    { type: 'added', description: 'Added LinkedIn link for professional visibility', section: 'Header' },
    { type: 'modified', description: 'Reformatted skills into categorized groups for readability', section: 'Skills' },
    { type: 'removed', description: 'Removed generic "References available upon request" line', section: 'Footer' },
  ],
};
