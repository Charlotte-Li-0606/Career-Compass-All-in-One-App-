import { useState, useRef, useEffect, type KeyboardEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { ROLE_OPTIONS } from '../data/roles'
import {
  selectInterviewQuestions,
  getSectorForRole as getSectorFromData,
  type InterviewDifficulty,
} from '../data/interviewQuestions'

// ── Types ──
type InterviewState = 'setup' | 'active' | 'report'

interface ChatMessage {
  role: 'ai' | 'user'
  text: string
}

interface PerformanceReport {
  overallScore: number
  dimensions: {
    communication: number
    content: number
    confidence: number
  }
  strengths: string[]
  improvements: string[]
}

// ── Report generation (mock heuristics) ──
function generateReport(answers: string[], role: string): PerformanceReport {
  // Simple heuristic: longer, more detailed answers score higher
  const avgLength = answers.reduce((s, a) => s + a.length, 0) / Math.max(answers.length, 1)
  const hasKeywords = answers.some((a) =>
    /\b(team|project|result|data|learn|challenge|improve|led|developed|analyzed)\b/i.test(a),
  )
  const hasMetrics = answers.some((a) => /\b(\d+%|\d+ [a-z]+|\$\d+|\d+ (people|users|customers|clients))\b/i.test(a))

  const content = clamp(Math.round((avgLength / 300) * 60 + (hasKeywords ? 20 : 0) + (hasMetrics ? 20 : 0)))
  const communication = clamp(Math.round((avgLength / 200) * 50 + (hasKeywords ? 30 : 10) + 20))
  const confidence = clamp(Math.round(60 + (hasMetrics ? 20 : -10) + (avgLength > 150 ? 15 : -5)))

  const overall = Math.round((content + communication + confidence) / 3)

  const strengths: string[] = []
  const improvements: string[] = []

  if (hasMetrics) strengths.push('Uses specific metrics and quantifiable results to back up claims')
  else improvements.push('Include concrete numbers and metrics to strengthen your responses')

  if (hasKeywords) strengths.push('Uses action-oriented language (led, developed, analyzed)')
  else improvements.push('Use more action verbs like "led", "developed", and "implemented"')

  if (avgLength > 200) strengths.push('Provides detailed, well-structured answers')
  else improvements.push('Elaborate more on your answers — aim for 3-4 sentences minimum')

  if (answers.length >= 4) strengths.push('Maintained composure across multiple questions')
  else improvements.push('Practice answering a wider variety of question types')

  strengths.push('Shows genuine interest in the role and industry')

  return { overallScore: overall, dimensions: { communication, content, confidence }, strengths, improvements }
}

function clamp(v: number) {
  return Math.max(10, Math.min(98, v))
}

// ── Component ──
export default function MockInterview() {
  const navigate = useNavigate()

  // State
  const [state, setState] = useState<InterviewState>('setup')
  const [selectedRole, setSelectedRole] = useState('')
  const [difficulty, setDifficulty] = useState<'intern' | 'graduate' | 'experienced'>('graduate')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [questionIndex, setQuestionIndex] = useState(0)
  const [questions, setQuestions] = useState<string[]>([])
  const [answers, setAnswers] = useState<string[]>([])
  const [isRecording, setIsRecording] = useState(false)
  const [aiThinking, setAiThinking] = useState(false)
  const [report, setReport] = useState<PerformanceReport | null>(null)

  const chatEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, aiThinking])

  // Focus input when interview starts
  useEffect(() => {
    if (state === 'active') inputRef.current?.focus()
  }, [state])

  // ── Actions ──
  function getSectorForRole(role: string): string {
    // Prefer the new interview data; fall back to the ROLE_OPTIONS mapping
    return getSectorFromData(role) ?? ROLE_OPTIONS.find((s) => s.roles.includes(role))?.sector ?? 'Technology & IT'
  }

  function startInterview() {
    if (!selectedRole) return

    // Select questions based on role and difficulty
    const selected = selectInterviewQuestions(selectedRole, difficulty as InterviewDifficulty, 4)
    if (selected.length === 0) {
      // Fallback: role not in the new data yet
      const sector = getSectorForRole(selectedRole)
      const fallback = [
        `Tell me about your experience and skills relevant to the ${selectedRole} role.`,
        'Describe a challenging situation you faced and how you resolved it.',
        'What are your strengths and how do they apply to this position?',
        'Where do you see yourself professionally in the next 3-5 years?',
      ]
      selected.push(...fallback)
    }

    setQuestions(selected)
    setQuestionIndex(0)
    setAnswers([])
    setMessages([])
    setReport(null)

    const levelLabel = difficulty.charAt(0).toUpperCase() + difficulty.slice(1)

    // First AI message — includes difficulty context
    const intro = `Hi! I'll be your interviewer for the **${selectedRole}** role at **${levelLabel}** level today. I'll ask you ${selected.length} questions tailored to this experience level to help you practice. Take your time, and remember — this is a safe space to learn.\n\nLet's begin! **Question 1:** ${selected[0]}`
    setMessages([{ role: 'ai', text: intro }])
    setState('active')
  }

  function sendMessage() {
    const trimmed = input.trim()
    if (!trimmed || aiThinking) return

    const userMsg: ChatMessage = { role: 'user', text: trimmed }
    const newMessages = [...messages, userMsg]
    const newAnswers = [...answers, trimmed]
    setMessages(newMessages)
    setAnswers(newAnswers)
    setInput('')

    const nextIdx = questionIndex + 1

    if (nextIdx >= questions.length) {
      // Last question answered — generate report
      setAiThinking(true)
      setTimeout(() => {
        const closingMsg: ChatMessage = {
          role: 'ai',
          text: `Great job! That wraps up our ${difficulty}-level mock interview. I've prepared a performance report based on your responses — tap **View Report** to see how you did.`,
        }
        setMessages([...newMessages, closingMsg])
        setAiThinking(false)
        const rep = generateReport(newAnswers, selectedRole)
        setReport(rep)
      }, 1200)
    } else {
      // Ask next question
      setAiThinking(true)
      setQuestionIndex(nextIdx)
      setTimeout(() => {
        const followUps = difficulty === 'intern'
          ? [
              'Thanks for sharing that. ',
              'Great, I can see you\'ve thought about this. ',
              'Good answer. ',
              'Nice — that\'s a solid example. ',
              'I appreciate hearing your perspective. ',
            ]
          : difficulty === 'graduate'
          ? [
              'Thanks for that detailed response. ',
              'Interesting — I can see how that experience shaped your thinking. ',
              'Good point, well articulated. ',
              'That\'s a strong example. ',
              'I appreciate the depth of that answer. ',
            ]
          : [
              'Excellent — that demonstrates strong experience. ',
              'That\'s a compelling example of leadership. ',
              'Very insightful — I can see the strategic thinking. ',
              'That\'s exactly the kind of experience we look for. ',
              'A nuanced perspective — thank you for sharing. ',
            ]
        const followUp = followUps[Math.floor(Math.random() * followUps.length)]
        const nextQ: ChatMessage = {
          role: 'ai',
          text: `${followUp}**Question ${nextIdx + 1}:** ${questions[nextIdx]}`,
        }
        setMessages([...newMessages, nextQ])
        setAiThinking(false)
      }, 1000 + Math.random() * 800)
    }
  }

  function endInterview() {
    const rep = generateReport(answers, selectedRole)
    setReport(rep)
    setState('report')
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  function toggleMic() {
    // UI only — no actual STT wired yet
    setIsRecording((prev) => !prev)
    if (!isRecording) {
      // Simulate recording for 3 seconds then insert placeholder text
      setTimeout(() => {
        setIsRecording(false)
        if (!input.trim()) {
          setInput('I believe my experience and skills make me a strong fit for this role. I have worked on several projects that demonstrate my ability to deliver results.')
        }
      }, 3000)
    }
  }

  function resetToSetup() {
    setState('setup')
    setSelectedRole('')
    setMessages([])
    setReport(null)
    setAnswers([])
    setQuestions([])
    setQuestionIndex(0)
  }

  // ── Render: Setup ──
  if (state === 'setup') {
    return (
      <main className="page">
        <div className="container">
          <div className="section-header">
            <h1 className="section-title">Mock Interview</h1>
            <p className="section-intro">
              Practice with an AI interviewer that adapts to your target role.
              Choose a position below and start your session.
            </p>
          </div>

          <div className="card" style={{ maxWidth: '640px', margin: '0 auto' }}>
            {/* Role selector */}
            <div className="form-group">
              <label className="form-label">
                Select Target Role <span className="required-star">*</span>
              </label>
              <div className="role-select-container" style={{ maxHeight: '320px' }}>
                {ROLE_OPTIONS.map((sector) => (
                  <div key={sector.sector} className="role-select-sector">
                    <div className="role-select-sector-title">{sector.sector}</div>
                    {sector.roles.map((role) => (
                      <label
                        key={role}
                        className="role-select-item"
                        style={selectedRole === role ? { background: 'rgba(0,245,255,0.08)' } : undefined}
                      >
                        <input
                          type="radio"
                          name="interview-role"
                          checked={selectedRole === role}
                          onChange={() => setSelectedRole(role)}
                          style={{ borderRadius: '50%' }}
                        />
                        <span>{role}</span>
                      </label>
                    ))}
                  </div>
                ))}
              </div>
            </div>

            {/* Difficulty */}
            <div className="form-group">
              <label className="form-label">Experience Level</label>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                {(['intern', 'graduate', 'experienced'] as const).map((level) => (
                  <button
                    key={level}
                    type="button"
                    className={difficulty === level ? 'btn btn-primary' : 'btn btn-secondary'}
                    onClick={() => setDifficulty(level)}
                    style={{ flex: 1, textTransform: 'capitalize', fontSize: '0.8rem', padding: '0.5rem 1rem' }}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            {/* Start button */}
            <button
              className="btn btn-primary btn-full"
              disabled={!selectedRole}
              onClick={startInterview}
              style={{ marginTop: '0.5rem' }}
            >
              🎯 Start Mock Interview
            </button>

            <p style={{
              textAlign: 'center',
              marginTop: '1rem',
              fontSize: '0.75rem',
              color: 'var(--text-muted)',
            }}>
              Your responses are processed locally. No audio or video is recorded.
            </p>
          </div>
        </div>
      </main>
    )
  }

  // ── Render: Report ──
  if (state === 'report' && report) {
    return (
      <main className="page">
        <div className="container" style={{ maxWidth: '680px' }}>
          <div className="section-header">
            <h1 className="section-title">Performance Report</h1>
            <p className="section-intro">
              Here's how you did in your mock interview for <strong>{selectedRole}</strong>.
              Use this feedback to improve before the real thing.
            </p>
          </div>

          {/* Hero score */}
          <div className="report-hero">
            <div className="report-score-ring">
              <svg viewBox="0 0 120 120" width="120" height="120">
                <circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" strokeWidth="6" />
                <circle
                  cx="60" cy="60" r="52"
                  fill="none"
                  stroke="url(#scoreGradient)"
                  strokeWidth="6"
                  strokeLinecap="round"
                  strokeDasharray={`${(report.overallScore / 100) * 327} 327`}
                  strokeDashoffset="0"
                  transform="rotate(-90 60 60)"
                  style={{ transition: 'stroke-dasharray 1s ease' }}
                />
                <defs>
                  <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="var(--accent-cyan)" />
                    <stop offset="100%" stopColor="var(--accent-purple)" />
                  </linearGradient>
                </defs>
              </svg>
              <span className="report-score-number">{report.overallScore}%</span>
            </div>
            <p className="report-score-label">
              {report.overallScore >= 80 ? '🌟 Excellent — Ready for the real thing!'
                : report.overallScore >= 60 ? '👍 Solid — A few areas to polish'
                : '💪 Good start — Keep practicing!'}
            </p>
          </div>

          {/* Dimension bars */}
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h4 style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.7rem',
              letterSpacing: '2px',
              color: 'var(--accent-cyan)',
              marginBottom: '1.25rem',
              textTransform: 'uppercase',
            }}>
              ◆ Performance Dimensions
            </h4>
            {([
              { key: 'communication', label: 'Communication', icon: '💬' },
              { key: 'content', label: 'Content', icon: '📋' },
              { key: 'confidence', label: 'Confidence', icon: '🎯' },
            ] as const).map((dim) => (
              <div key={dim.key} className="report-dimension">
                <div className="report-dimension-header">
                  <span>{dim.icon} {dim.label}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)' }}>
                    {report.dimensions[dim.key]}%
                  </span>
                </div>
                <div className="report-bar-track">
                  <div
                    className="report-bar-fill"
                    style={{ width: `${report.dimensions[dim.key]}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Strengths & Improvements */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="card">
              <h4 style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.7rem',
                letterSpacing: '2px',
                color: 'var(--accent-green)',
                marginBottom: '0.75rem',
                textTransform: 'uppercase',
              }}>
                ✓ Strengths
              </h4>
              <ul className="report-list report-list-good">
                {report.strengths.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
            <div className="card">
              <h4 style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.7rem',
                letterSpacing: '2px',
                color: 'var(--accent-amber)',
                marginBottom: '0.75rem',
                textTransform: 'uppercase',
              }}>
                ⚠ Areas to Improve
              </h4>
              <ul className="report-list report-list-warn">
                {report.improvements.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem', justifyContent: 'center' }}>
            <button className="btn btn-secondary" onClick={() => navigate('/')}>
              ← Back to Career Profile
            </button>
            <button className="btn btn-primary" onClick={resetToSetup}>
              🔄 Practice Again
            </button>
          </div>
        </div>
      </main>
    )
  }

  // ── Render: Active Interview ──
  const totalQuestions = questions.length

  return (
    <main className="page" style={{ paddingBottom: 0 }}>
      <div className="container" style={{ maxWidth: '720px', height: 'calc(100vh - 5rem)', display: 'flex', flexDirection: 'column' }}>
        {/* Top bar */}
        <div className="interview-topbar">
          <div>
            <span style={{ color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)', fontSize: '0.72rem', letterSpacing: '1px' }}>
              {selectedRole}
            </span>
            <span style={{ color: 'var(--text-muted)', margin: '0 0.75rem' }}>·</span>
            <span style={{
              color: 'var(--accent-purple)',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              textTransform: 'uppercase',
              letterSpacing: '1px',
            }}>
              {difficulty}
            </span>
            <span style={{ color: 'var(--text-muted)', margin: '0 0.75rem' }}>·</span>
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
              Q{questionIndex + 1}/{totalQuestions}
            </span>
          </div>
          {report === null && (
            <button className="btn btn-secondary" onClick={endInterview} style={{ padding: '0.4rem 1rem', fontSize: '0.72rem' }}>
              End Interview
            </button>
          )}
        </div>

        {/* Chat area */}
        <div className="interview-chat">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.role}`}>
              <div className="chat-bubble-text">{msg.text}</div>
            </div>
          ))}

          {aiThinking && (
            <div className="chat-message ai">
              <div className="chat-bubble-text">
                <span className="typing-dots">
                  <span>.</span><span>.</span><span>.</span>
                </span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input bar */}
        {report === null ? (
          <div className="interview-input-bar">
            <button
              type="button"
              className={`mic-btn ${isRecording ? 'recording' : ''}`}
              onClick={toggleMic}
              title={isRecording ? 'Recording...' : 'Voice input'}
            >
              🎤
            </button>
            <textarea
              ref={inputRef}
              className="form-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              onInput={(e) => {
                const el = e.currentTarget
                el.style.height = 'auto'
                el.style.height = Math.min(el.scrollHeight, 150) + 'px'
              }}
              placeholder={isRecording ? 'Listening...' : 'Type your answer...'}
              disabled={aiThinking}
              rows={3}
              style={{ flex: 1, margin: 0, resize: 'none', overflow: 'auto' }}
            />
            <button
              className="btn btn-primary"
              onClick={sendMessage}
              disabled={!input.trim() || aiThinking}
              style={{ padding: '0.75rem 1.25rem' }}
            >
              Send
            </button>
          </div>
        ) : (
          <div className="interview-report-bar" style={{
            padding: '1rem 1.25rem',
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
            flexShrink: 0,
          }}>
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              ✅ Interview complete — see how you did
            </span>
            <button
              className="btn btn-primary"
              onClick={() => setState('report')}
              style={{ padding: '0.6rem 1.25rem', fontSize: '0.8rem', whiteSpace: 'nowrap' }}
            >
              View Report →
            </button>
          </div>
        )}
      </div>
    </main>
  )
}
