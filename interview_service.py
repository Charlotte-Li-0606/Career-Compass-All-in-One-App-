from llm_service import call_llm


# =====================================================
# FEATURE 4
# Interview Question Generation
# =====================================================

def generate_interview_questions(data):

    prompt = f"""

ROLE:

You are Career Compass AI.

You are a professional technical interviewer.

You are preparing a personalized mock interview.


==================================================
STUDENT PROFILE
==================================================

Major:
{data.major}

Skills:
{data.skills}

Target Role:
{data.target_role}


==================================================
TASK
==================================================

Generate exactly FIVE interview questions.

The questions must be tailored to:

- student's major
- student's skills
- target role

Question Distribution:

Question 1:
Technical Question

Question 2:
Technical Question

Question 3:
Behavioral Question

Question 4:
Behavioral Question

Question 5:
Problem Solving Question


==================================================
QUESTION QUALITY REQUIREMENTS
==================================================

Technical Questions:

- role-specific
- realistic
- practical

Behavioral Questions:

- teamwork
- communication
- conflict resolution
- project experience

Problem Solving Question:

- scenario-based
- analytical thinking


==================================================
STRICT RULES
==================================================

DO NOT:

- explain reasoning
- provide answers
- provide notes
- provide introductions
- provide conclusions

DO NOT write:

"Here are five interview questions"

DO NOT write:

"I would ask"

DO NOT write anything outside JSON.


==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

{{
    "questions":[
        "question 1",
        "question 2",
        "question 3",
        "question 4",
        "question 5"
    ]
}}

If output is not valid JSON, the response is incorrect.

"""

    return call_llm(prompt)


# =====================================================
# FEATURE 5
# Follow-up Question Generation
# =====================================================

def generate_followup_question(data):

    prompt = f"""

ROLE:

You are a professional interviewer.


==================================================
ORIGINAL QUESTION
==================================================

{data.question}


==================================================
CANDIDATE ANSWER
==================================================

{data.answer}


==================================================
TASK
==================================================

Generate EXACTLY ONE follow-up question.

The purpose is to continue the interview.

The follow-up should:

- explore reasoning
- explore implementation details
- explore decision making
- explore technical depth
- explore tradeoffs


==================================================
EXAMPLES
==================================================

Example 1:

Question:
Why did you choose Random Forest?

Answer:
It performed better.

Follow-up:
What evaluation metrics did you use to determine it performed better?


Example 2:

Question:
Describe your web application project.

Answer:
I used React and FastAPI.

Follow-up:
What challenges did you encounter when integrating React with FastAPI?


==================================================
STRICT RULES
==================================================

DO NOT:

- evaluate the answer
- score the answer
- provide feedback
- explain the answer
- generate multiple questions
- use bullet points

Generate ONLY ONE follow-up question.


==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

{{
    "followup":
    "single follow-up question"
}}

No markdown.

No explanations.

No notes.

No extra text.

If output contains anything outside JSON, the response is incorrect.

"""

    return call_llm(prompt)


# =====================================================
# FEATURE 6
# Interview Evaluation Report
# =====================================================

def generate_interview_report(data):

    prompt = f"""

ROLE:

You are Career Compass AI.

You are a senior interview evaluator.


==================================================
INTERVIEW TRANSCRIPT
==================================================

{data.interview_history}


==================================================
TASK
==================================================

Evaluate the interview performance.

Generate:

1. overall_score
2. technical_knowledge
3. communication
4. problem_solving
5. strengths
6. weaknesses
7. improvement_plan


==================================================
SCORING RULES
==================================================

All scores must be integers.

Range:

0-100

Examples:

80

75

92

NOT:

80%

NOT:

80/100


==================================================
EVALUATION CRITERIA
==================================================

Technical Knowledge:

- correctness
- technical depth
- understanding

Communication:

- clarity
- organization
- confidence

Problem Solving:

- analytical thinking
- reasoning
- decision making


==================================================
STRENGTH REQUIREMENTS
==================================================

Provide at least 3 strengths.

Each strength must:

- be specific
- be evidence-based


==================================================
WEAKNESS REQUIREMENTS
==================================================

Provide at least 3 weaknesses.

Each weakness must:

- be constructive
- be actionable


==================================================
IMPROVEMENT PLAN REQUIREMENTS
==================================================

Provide at least 3 actions.

Actions must:

- be practical
- be measurable
- improve interview performance


==================================================
STRICT RULES
==================================================

Return ONLY JSON.

DO NOT:

- write introductions
- write summaries
- write headings
- write markdown
- write notes
- write explanations

DO NOT output text before JSON.

DO NOT output text after JSON.


==================================================
OUTPUT FORMAT
==================================================

{{
    "overall_score": 85,
    "technical_knowledge": 82,
    "communication": 88,
    "problem_solving": 84,
    "strengths": [
        "...",
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "...",
        "..."
    ],
    "improvement_plan": [
        "...",
        "...",
        "..."
    ]
}}

If output is not valid JSON, the response is incorrect.

"""

    return call_llm(prompt)