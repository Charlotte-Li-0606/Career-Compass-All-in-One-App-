import { useRef } from 'react'
import type { ResumeChange } from '../types'

interface Props {
  original: string
  refined: string
  changes: ResumeChange[]
  pdfFile?: File | null
}

const ICONS: Record<string, string> = {
  added: '+',
  modified: '~',
  removed: '−',
}

export default function ResumeDiff({ original, refined, changes, pdfFile }: Props) {
  // Create an object URL from the PDF file so the browser can render it inline.
  // We manage the URL imperatively in a ref to avoid React Strict Mode tearing:
  // a useMemo + useEffect cleanup pattern would let Strict Mode revoke the blob
  // URL mid-lifecycle (cleanup fires but useMemo does not re-run), breaking the
  // <embed> tag. Instead we only create / revoke when pdfFile actually changes,
  // and we skip cleanup on unmount — the browser reclaims blob URLs on page
  // unload anyway, and the single-URL memory cost is negligible.
  const pdfUrlRef = useRef<string | null>(null)
  const prevFileRef = useRef<File | null | undefined>(undefined)

  if (pdfFile !== prevFileRef.current) {
    // Revoke the previous blob URL so we don't leak
    if (pdfUrlRef.current) {
      URL.revokeObjectURL(pdfUrlRef.current)
    }
    pdfUrlRef.current = pdfFile ? URL.createObjectURL(pdfFile) : null
    prevFileRef.current = pdfFile
  }

  const pdfUrl = pdfUrlRef.current
  return (
    <div>
      {/* Side-by-side diff */}
      <div className="diff-container">
        <div className="diff-panel">
          <div className="diff-panel-header original">Original Resume</div>
          {pdfUrl ? (
            <embed
              src={pdfUrl}
              type="application/pdf"
              style={{ width: '100%', height: '520px', border: 'none' }}
            />
          ) : (
            <div className="diff-panel-content">{original}</div>
          )}
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
