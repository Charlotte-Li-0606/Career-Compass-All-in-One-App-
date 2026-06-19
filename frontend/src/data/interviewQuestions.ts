/**
 * Interview Questions Data Module
 *
 * Provides role-specific, difficulty-leveled interview questions for the Mock Interview page.
 * Questions are organized by role, difficulty (intern/graduate/experienced), and category
 * (behavioral/technical/situational).
 *
 * Canonical data source: data/interviews/interview_questions.json
 * Frontend copy: frontend/src/data/interview_questions.json
 */

import rawData from './interview_questions.json'

export type InterviewDifficulty = 'intern' | 'graduate' | 'experienced'

export type QuestionCategory = 'behavioral' | 'technical' | 'situational'

export interface RoleQuestions {
  sector: string
  intern: Record<QuestionCategory, string[]>
  graduate: Record<QuestionCategory, string[]>
  experienced: Record<QuestionCategory, string[]>
}

export interface InterviewQuestionData {
  lastUpdated: string
  source: string
  description: string
  roles: Record<string, RoleQuestions>
}

const data = rawData as unknown as InterviewQuestionData

/**
 * Get all available roles that have interview questions.
 */
export function getAllRoles(): string[] {
  return Object.keys(data.roles)
}

/**
 * Get the sector for a given role.
 */
export function getSectorForRole(role: string): string | undefined {
  return data.roles[role]?.sector
}

/**
 * Get all sectors that have interview questions.
 */
export function getAllSectors(): string[] {
  const sectors = new Set<string>()
  for (const role of Object.values(data.roles)) {
    sectors.add(role.sector)
  }
  return Array.from(sectors)
}

/**
 * Get interview questions for a specific role and difficulty level.
 * Returns all questions across all categories, shuffled.
 */
export function getQuestionsForRole(
  role: string,
  difficulty: InterviewDifficulty
): string[] {
  const roleData = data.roles[role]
  if (!roleData) return []

  const questions = roleData[difficulty]
  const allQuestions = [
    ...questions.behavioral,
    ...questions.technical,
    ...questions.situational,
  ]
  return allQuestions
}

/**
 * Get interview questions organized by category for a specific role and difficulty.
 */
export function getQuestionsByCategory(
  role: string,
  difficulty: InterviewDifficulty
): Record<QuestionCategory, string[]> {
  const roleData = data.roles[role]
  if (!roleData) {
    return { behavioral: [], technical: [], situational: [] }
  }
  return { ...roleData[difficulty] }
}

/**
 * Shuffle an array in place (Fisher-Yates) and return it.
 */
export function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

/**
 * Select a balanced set of questions for an interview session.
 * Picks questions proportionally from each category.
 *
 * @param role - The role title
 * @param difficulty - The experience level
 * @param count - Total number of questions to select (default: 4)
 * @returns Shuffled array of questions
 */
export function selectInterviewQuestions(
  role: string,
  difficulty: InterviewDifficulty,
  count: number = 4
): string[] {
  const categories = getQuestionsByCategory(role, difficulty)

  // Determine how many to pick from each category
  const behavioral = Math.ceil((count / 3))
  const technical = Math.ceil((count / 3))
  const situational = count - behavioral - technical

  const selected: string[] = []

  const addShuffled = (pool: string[], n: number) => {
    const picked = shuffleArray(pool).slice(0, n)
    selected.push(...picked)
  }

  addShuffled(categories.behavioral, behavioral)
  addShuffled(categories.technical, technical)
  addShuffled(categories.situational, situational)

  return shuffleArray(selected)
}

/**
 * Get the total question count for a role/difficulty combination.
 */
export function getQuestionCount(
  role: string,
  difficulty: InterviewDifficulty
): number {
  return getQuestionsForRole(role, difficulty).length
}

export default data
