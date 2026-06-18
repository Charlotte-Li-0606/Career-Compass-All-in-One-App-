import type {
  UserProfile,
  CareerSummary,
  SkillsTable,
  ResumeRefinementRequest,
  ResumeRefinementResponse,
} from '../types';

// Swap this to your deployed Azure Functions base URL
const API_BASE = import.meta.env.VITE_API_BASE ?? 'https://hub-career-compass-ai.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview';

async function request<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(err.error ?? `HTTP ${res.status}`);
  }

  return res.json();
}

// ── Career Profile ──
export async function getCareerSummary(profile: UserProfile): Promise<CareerSummary> {
  return request<CareerSummary>('/get_career_summary', profile);
}

export async function getSkillsTable(
  profile: UserProfile,
  careerSummary: CareerSummary,
): Promise<SkillsTable> {
  return request<SkillsTable>('/get_skills_table', { profile, careerSummary });
}

// ── Resume Refinement ──
export async function optimizeResume(
  req: ResumeRefinementRequest,
): Promise<ResumeRefinementResponse> {
  return request<ResumeRefinementResponse>('/optimize_resume', req);
}

// ── Profile persistence (if you wire Cosmos DB later) ──
export async function saveProfile(userId: string, profile: UserProfile): Promise<void> {
  await fetch(`${API_BASE}/profile/${encodeURIComponent(userId)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  });
}
