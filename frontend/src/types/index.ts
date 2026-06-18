// ── User Profile ──
export interface UserProfile {
  major: string;
  year: number;
  university: string;
  interests: string[];
  targetRoles: string[];
  pastInternships: string[];
  extracurriculars: string[];
}

// ── Career Summary (structured output from GPT-4o) ──
export interface CareerSummary {
  overview: string;
  recommendedRoles: CareerRole[];
  industryInsights: string;
  nextSteps: string[];
  generatedAt?: string;
}

export interface CareerRole {
  title: string;
  fit: string;
  growthOutlook: string;
}

// ── Skills Table (derived from Career Summary) ──
export type Proficiency = 'mastered' | 'learning' | 'missing';

export interface SkillEntry {
  name: string;
  category: string;
  proficiency: Proficiency;
  description: string;
  importance: 'critical' | 'recommended' | 'nice-to-have';
}

export interface SkillsTable {
  skills: SkillEntry[];
  summary: string;
  generatedAt?: string;
}

// ── Resume Refinement ──
export interface ResumeRefinementRequest {
  originalText: string;
  instructions: string;
  careerContext?: string; // optional: feed in career summary for targeted refinement
}

export interface ResumeChange {
  type: 'added' | 'removed' | 'modified';
  description: string;
  section?: string;
}

export interface ResumeRefinementResponse {
  refinedText: string;
  changes: ResumeChange[];
}

// ── API response wrappers ──
export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}
