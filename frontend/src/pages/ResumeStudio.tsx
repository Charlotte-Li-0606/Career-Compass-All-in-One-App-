import { useState } from 'react'
import type { ResumeRefinementResponse } from '../types'
import { optimizeResume } from '../services/api'
import { mockResumeRefinement } from '../services/mockData'
import ResumeUploader from '../components/ResumeUploader'
import ResumeDiff from '../components/ResumeDiff'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || !import.meta.env.VITE_API_BASE

export default function ResumeStudio() {
  const [originalText, setOriginalText] = useState('')
  const [instructions, setInstructions] = useState('')
  const [refined, setRefined] = useState<ResumeRefinementResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleRefine() {
    if (!originalText.trim() || !instructions.trim()) return
    setError(null)
    setLoading(true)

    try {
      if (USE_MOCK) {
        await new Promise((r) => setTimeout(r, 1500))
        setRefined(mockResumeRefinement)
      } else {
        const result = await optimizeResume({
          originalText: originalText.trim(),
          instructions: instructions.trim(),
        })
        setRefined(result)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
      setRefined(null)
    } finally {
      setLoading(false)
    }
  }

  function handleDownload() {
    if (!refined) return
    const blob = new Blob([refined.refinedText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'resume-refined.md'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <main className="page">
      <div className="container">
        <div className="section-header">
          <span className="section-tag">// RESUME_STUDIO</span>
          <h1 className="section-title">Resume Refinement</h1>
          <p className="section-intro">
            Upload your resume, tell me what to optimize for, and I'll refine it —
            tailoring language, highlighting strengths, and making every bullet count.
          </p>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {/* Step 1: Upload */}
        <ResumeUploader onUpload={setOriginalText} disabled={loading} />

        {/* Step 2: Instructions */}
        {originalText && (
          <div className="card" style={{ marginBottom: '1.5rem', animation: 'fadeSlideIn 0.4s ease' }}>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Refinement Instructions</label>
              <textarea
                className="form-input"
                rows={3}
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                placeholder='e.g. "Tailor this for a Data Analyst role at a fintech company", "Make it more concise", "Highlight my technical projects more"'
                disabled={loading}
              />
            </div>
          </div>
        )}

        {/* Generate button */}
        {originalText && instructions.trim() && (
          <button
            className="btn btn-primary btn-full"
            onClick={handleRefine}
            disabled={loading}
            style={{ marginBottom: '2rem' }}
          >
            {loading ? 'Refining...' : 'Refine My Resume'}
          </button>
        )}

        {loading && (
          <div className="loading-spinner">
            <span className="spinner" />
            Polishing your resume...
          </div>
        )}

        {/* Results */}
        {refined && !loading && (
          <>
            <ResumeDiff
              original={originalText}
              refined={refined.refinedText}
              changes={refined.changes}
            />

            <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
              <button className="btn btn-secondary" onClick={handleDownload}>
                ⬇ Download Refined Resume
              </button>
            </div>
          </>
        )}

        {/* Empty state */}
        {!originalText && (
          <div className="empty-state">
            <div className="icon">📄</div>
            <p>Upload or paste your resume above to get started</p>
          </div>
        )}
      </div>
    </main>
  )
}
