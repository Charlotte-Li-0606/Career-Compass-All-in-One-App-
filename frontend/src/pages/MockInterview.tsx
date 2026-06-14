export default function MockInterview() {
  return (
    <main className="page">
      <div className="container">
        <div className="section-header">
          <span className="section-tag">// INTERVIEW_COACH</span>
          <h1 className="section-title">Mock Interview</h1>
          <p className="section-intro">
            Practice with an AI interviewer that adapts to your target role.
            Real-time voice interaction with personalized feedback after each session.
          </p>
        </div>

        {/* Coming soon stub */}
        <div className="interview-mockup">
          <div className="mic-icon">🎙️</div>
          <h3 style={{
            fontFamily: 'var(--font-display)',
            fontSize: '1.1rem',
            letterSpacing: '1px',
            marginBottom: '0.75rem',
          }}>
            Voice Interview Engine
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: '400px', marginBottom: '0.5rem' }}>
            Real-time speech-to-text and text-to-speech powered by Azure AI Speech Services.
            Role-specific question banks and adaptive follow-up questions.
          </p>
          <div className="coming-soon-badge">COMING SOON</div>

          {/* Placeholder chat UI to illustrate the vision */}
          <div className="interview-placeholder-ui">
            <div className="chat-bubble ai">
              Hi! I'm your interview coach. I see you're targeting a <strong>Data Analyst</strong> role.
              Let's start with a common question: <em>"Tell me about a time you used data to solve a problem."</em>
            </div>
            <div className="chat-bubble user">
              In my internship, I analyzed 50K+ transaction records to find cost-saving opportunities...
            </div>
            <div className="chat-bubble ai">
              Great answer! You gave a specific metric. Let's dig deeper — what tools did you use,
              and how did you present your findings to the team?
            </div>
          </div>

          {/* Planned features */}
          <div style={{
            marginTop: '2rem',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '0.75rem',
            maxWidth: '500px',
            width: '100%',
          }}>
            {[
              { icon: '🎤', label: 'Voice Input (STT)' },
              { icon: '🔊', label: 'Voice Output (TTS)' },
              { icon: '📋', label: 'Role-Based Questions' },
              { icon: '📊', label: 'Performance Report' },
            ].map((f, i) => (
              <div key={i} style={{
                padding: '0.75rem',
                background: 'rgba(0, 245, 255, 0.03)',
                border: '1px solid var(--border)',
                borderRadius: '10px',
                textAlign: 'center',
                fontSize: '0.78rem',
                color: 'var(--text-secondary)',
              }}>
                <div style={{ fontSize: '1.2rem', marginBottom: '0.25rem' }}>{f.icon}</div>
                {f.label}
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}
