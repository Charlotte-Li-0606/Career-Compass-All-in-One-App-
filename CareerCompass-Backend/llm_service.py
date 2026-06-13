from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import hashlib
import time
from openai import RateLimitError

load_dotenv()


MODEL_NAME = os.getenv("MODEL_NAME")

print("MODEL NAME =", MODEL_NAME)
print("ENDPOINT =", os.getenv("AZURE_ENDPOINT"))

client = OpenAI(
    base_url=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY")
)



# =====================================================
# Global Career Compass Identity Prompt
# =====================================================


SYSTEM_PROMPT = """

You are Career Compass AI.

You are NOT a general chatbot.

You are a professional AI career advisor designed for university students.

Your mission:

Help students make better career decisions by analyzing:

- academic background
- interests
- technical skills
- experiences
- career goals
- job requirements


Your expertise includes:

1. Career planning
2. Technical skill gap analysis
3. Resume optimization
4. Learning roadmap design
5. Internship and job preparation



=====================================================
GENERAL BEHAVIOR RULES
=====================================================


RULE 1:
Always act as a professional career advisor.

Do NOT:
- chat casually
- use greetings
- say "That's great"
- say "I'd be happy to help"
- provide generic motivational answers


RULE 2:
Always provide practical and actionable recommendations.

Avoid:
"This field is promising."

Prefer:
"Learn Python fundamentals first, then complete two machine learning projects using scikit-learn."


RULE 3:
When information is missing:

Do NOT invent facts.

Clearly state assumptions.

Example:

"Based on the provided information, I assume the student has beginner-level programming experience."


RULE 4:
Never fabricate:

- internships
- projects
- achievements
- certifications
- technical skills

Especially during resume optimization.



=====================================================
OUTPUT QUALITY REQUIREMENTS
=====================================================


Every response must:

- Be structured
- Be specific
- Include actionable next steps
- Focus on career development


Avoid:

- vague advice
- generic explanations
- unnecessary introductions


"""
# =====================================================
# Simple LLM Cache Layer
# =====================================================


CACHE_FILE = "cache.json"



def get_cache_key(prompt):

    combined = SYSTEM_PROMPT + prompt

    return hashlib.md5(
        combined.encode("utf-8")
    ).hexdigest()



def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_cache(cache):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cache,
            f,
            ensure_ascii=False,
            indent=4
        )


# =====================================================
# LLM Wrapper
# =====================================================


def call_llm(prompt: str):

    prompt = prompt.strip()

    cache = load_cache()

    cache_key = get_cache_key(prompt)



    # ================================
    # 1. Check cache
    # ================================

    if cache_key in cache:

        print("====== CACHE HIT ======")

        return cache[cache_key]



    print("====== CALLING AZURE LLM ======")



    # ================================
    # 2. Call Azure with retry
    # ================================

    max_retry = 3


    for attempt in range(max_retry):

        try:


            response = client.chat.completions.create(

                model=MODEL_NAME,


                messages=[

                    {
                        "role":"system",
                        "content":SYSTEM_PROMPT
                    },

                    {
                        "role":"user",
                        "content":prompt
                    }

                ],


                temperature=0.15,

                max_tokens=250

            )


            result = response.choices[0].message.content.strip()



            break



        except RateLimitError:


            wait = 10 * (attempt + 1)


            print(
                f"Rate limit reached. Waiting {wait}s..."
            )


            time.sleep(wait)



    else:

        return (
            "AI service temporarily unavailable. "
            "Please try again later."
        )



    # ================================
    # 3. Save cache
    # ================================


    cache[cache_key] = result

    save_cache(cache)



    print("==============================")
    print(result)
    print("==============================")


    return result




# =====================================================
# FEATURE 1
# Student Profile & Career Summary
# =====================================================


def analyze_profile(data):


    prompt=f"""


TASK:

Analyze a university student's profile and generate a personalized career summary.


Student Information:


Major:
{data.major}


Academic Year:
{data.year}


GPA:
{data.gpa}


Interests:
{data.interests}


Previous Experiences:
{data.experiences}




You MUST provide the following sections:


## Career Snapshot

Summarize the student's current career position.


## Recommended Career Paths

Provide 2-3 suitable career directions.

For each path explain:

- Why it matches
- Required skills


## Current Strengths

Identify existing advantages.


## Skill Gaps

Identify missing skills required for recommended careers.


## Learning Roadmap

Create a realistic roadmap:

Short term (0-3 months)

Medium term (3-6 months)

Long term (6-12 months)



IMPORTANT:

Make recommendations personalized.

Do not give generic computer science advice.


"""


    return call_llm(prompt)




# =====================================================
# FEATURE 2
# Technical Skill Analysis
# =====================================================


def analyze_skills(data):


    prompt=f"""


TASK:

Perform a technical skill gap analysis for a student targeting a specific career role.


Target Role:

{data.target_role}



Current Skills:

{data.current_skills}




Generate a professional technical assessment.



Required Output:



## Skill Requirement Table


For each important skill include:


Skill:

Importance:

Current Status:

Gap Level:

Recommendation:




Example categories:


Programming

Machine Learning

Cloud

Database

Software Engineering

Tools




## Priority Ranking


Classify missing skills:


High Priority:

Medium Priority:

Low Priority:



## Learning Plan


Provide:

First 30 days:

First 90 days:

Long-term improvement:




IMPORTANT:

Do not list unnecessary technologies.

Focus on skills relevant to the target role.

"""


    return call_llm(prompt)





# =====================================================
# FEATURE 3
# Resume Tailoring
# =====================================================


def optimize_resume(data):


    prompt=f"""


TASK:

You are an expert technical resume reviewer.


Your job:

Optimize a student's resume for a target job description.



Resume:


{data.resume_text}




Target Job Description:


{data.job_description}





Perform the following analysis:



## 1. Resume Match Score

Estimate compatibility percentage.

Explain why.



## 2. Missing Keywords

Identify important skills or keywords from the job description that are missing.



## 3. Weak Resume Sections

Identify unclear or weak descriptions.



## 4. Rewrite Suggestions


For each weak bullet point:


Original:

Improved Version:

Reason:



IMPORTANT RULES:


NEVER:

- invent projects
- invent achievements
- invent technologies
- add fake numbers


ONLY improve:

- wording
- structure
- clarity
- alignment with job description



The goal is optimization, NOT fabrication.


"""


    return call_llm(prompt)


def generate_response(user_message):
    return call_llm(user_message)