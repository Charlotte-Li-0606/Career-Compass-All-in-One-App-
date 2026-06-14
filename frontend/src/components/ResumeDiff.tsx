import type { ResumeChange } from '../types'

interface Props {
  original: string
  refined: string
  changes: ResumeChange[]
}

const ICONS: Record<string, string> = {
  added: '+',
  modified: '~',
  removed: '−',
}

export default function ResumeDiff({ original, refined, changes }: Props) {
  return (
    <div>
      {/* Side-by-side diff */}
      <div className="diff-container">
        <div className="diff-panel">
          <div className="diff-panel-header original">Original Resume</div>
          <div className="diff-panel-content">{original}</div>
        </div>
        <div className="diff-panel">
          <div className="diff-panel-header refined">Refined Resume</div>
          <div className="diff-panel-content">{refined}</div>
        </div>
      </div>

      {/* Changes summary */}
      {changes.length > 0 && (
        <div className="changes-list">
          <h4>WHAT CHANGED</h4>
          {changes.map((c, i) => (
            <div key={i} className="change-item">
              <span className={`icon-${c.type}`}>{ICONS[c.type] ?? '·'}</span>
              <span>
                {c.description}
                {c.section && (
                  <span style={{ color: 'var(--text-muted)', marginLeft: '0.4rem', fontSize: '0.72rem' }}>
                    [{c.section}]
                  </span>
                )}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
