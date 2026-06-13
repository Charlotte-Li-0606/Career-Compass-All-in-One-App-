import type { CareerSummary } from '../types'

interface Props {
  summary: CareerSummary
}

export default function PersonalSummary({ summary }: Props) {
  return (
    <div className="summary-card">
      {/* Overview */}
      <p className="overview">{summary.overview}</p>

      {/* Recommended Roles */}
      <h4 style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.7rem',
        letterSpacing: '2px',
        color: 'var(--accent-cyan)',
        marginBottom: '1rem',
        textTransform: 'uppercase',
      }}>
        ◆ Recommended Roles
      </h4>

      {summary.recommendedRoles.map((role, i) => (
        <div key={i} className="role-card">
          <h4>{role.title}</h4>
          <p className="fit">{role.fit}</p>
          <p className="outlook">{role.growthOutlook}</p>
        </div>
      ))}

      {/* Industry Insights */}
      <div className="insights-block">
        <h4>MARKET INSIGHTS</h4>
        <p>{summary.industryInsights}</p>
      </div>

      {/* Next Steps */}
      {summary.nextSteps.length > 0 && (
        <>
          <h4 style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.7rem',
            letterSpacing: '2px',
            color: 'var(--accent-cyan)',
            marginTop: '1.25rem',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
          }}>
            ◆ Your Next Steps
          </h4>
          <ol className="next-steps-list">
            {summary.nextSteps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </>
      )}
    </div>
  )
}
