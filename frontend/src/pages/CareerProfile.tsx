import { useState, type FormEvent } from 'react'
import type { UserProfile, CareerSummary, SkillsTable as SkillsTableType } from '../types'
import { getCareerSummary, getSkillsTable } from '../services/api'
import { mockCareerSummary, mockSkillsTable } from '../services/mockData'
import PersonalSummary from '../components/PersonalSummary'
import SkillsTable from '../components/SkillsTable'
import ChipInput from '../components/ChipInput'

const EMPTY_PROFILE: UserProfile = {
  major: '',
  year: 1,
  university: '',
  interests: [],
  targetRoles: [],
  pastInternships: [],
  extracurriculars: [],
}

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || !import.meta.env.VITE_API_BASE

export default function CareerProfile() {
  // ── State ──
  const [profile, setProfile] = useState<UserProfile>(EMPTY_PROFILE)
  const [careerSummary, setCareerSummary] = useState<CareerSummary | null>(null)
  const [skillsTable, setSkillsTable] = useState<SkillsTableType | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // ── Generate ──
  async function handleGenerate(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      if (USE_MOCK) {
        // Simulate network delay
        await new Promise((r) => setTimeout(r, 1200))
        setCareerSummary(mockCareerSummary)
        setSkillsTable(mockSkillsTable)
      } else {
        const summary = await getCareerSummary(profile)
        setCareerSummary(summary)

        const skills = await getSkillsTable(profile, summary)
        setSkillsTable(skills)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
      setCareerSummary(null)
      setSkillsTable(null)
    } finally {
      setLoading(false)
    }
  }

  // ── Render ──
  return (
    <main className="page">
      <div className="container">
        {/* Header */}
        <div className="section-header">
          <span className="section-tag">// CAREER_PROFILE</span>
          <h1 className="section-title">Your Career Compass</h1>
          <p className="section-intro">
            Tell me about yourself and I'll map your path — identifying promising roles, industry insights,
            and the exact skills you need to get there.
          </p>
        </div>

        {/* Error */}
        {error && <div className="error-banner">{error}</div>}

        {/* Profile Form */}
        <div className="card" style={{ marginBottom: careerSummary ? '2rem' : 0 }}>
          <form onSubmit={handleGenerate}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Major / Field of Study</label>
                <input
                  className="form-input"
                  value={profile.major}
                  onChange={(e) => setProfile({ ...profile, major: e.target.value })}
                  placeholder="e.g. Computer Science, Business Analytics"
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Year of Study</label>
                <select
                  className="form-input"
                  value={profile.year}
                  onChange={(e) => setProfile({ ...profile, year: Number(e.target.value) })}
                >
                  <option value={1}>Year 1</option>
                  <option value={2}>Year 2</option>
                  <option value={3}>Year 3</option>
                  <option value={4}>Year 4</option>
                  <option value={5}>Postgraduate</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">University</label>
              <input
                className="form-input"
                value={profile.university}
                onChange={(e) => setProfile({ ...profile, university: e.target.value })}
                placeholder="e.g. University of Hong Kong, CUHK"
                required
              />
            </div>

            <ChipInput
              label="Target Roles"
              values={profile.targetRoles}
              onChange={(targetRoles) => setProfile({ ...profile, targetRoles })}
              placeholder="e.g. Data Analyst, Software Engineer..."
            />

            <ChipInput
              label="Interests"
              values={profile.interests}
              onChange={(interests) => setProfile({ ...profile, interests })}
              placeholder="e.g. Machine Learning, Fintech..."
            />

            <ChipInput
              label="Past Internships"
              values={profile.pastInternships}
              onChange={(pastInternships) => setProfile({ ...profile, pastInternships })}
              placeholder="e.g. Google Summer 2025..."
            />

            <ChipInput
              label="Extracurriculars"
              values={profile.extracurriculars}
              onChange={(extracurriculars) => setProfile({ ...profile, extracurriculars })}
              placeholder="e.g. Debate Club, Hackathon..."
            />

            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Career Compass'}
            </button>
          </form>
        </div>

        {/* Loading */}
        {loading && (
          <div className="loading-spinner">
            <span className="spinner" />
            Analyzing your profile & mapping your career path...
          </div>
        )}

        {/* Results */}
        {careerSummary && !loading && (
          <PersonalSummary summary={careerSummary} />
        )}

        {skillsTable && !loading && (
          <div className="card" style={{ marginTop: '1.5rem' }}>
            <SkillsTable skillsTable={skillsTable} />
          </div>
        )}
      </div>
    </main>
  )
}
