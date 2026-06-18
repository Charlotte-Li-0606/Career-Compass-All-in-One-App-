import { useState, useRef } from 'react'

interface Props {
  onUpload: (text: string, file?: File) => void
  disabled?: boolean
}

async function extractPdfText(file: File): Promise<string> {
  const pdfjsLib = await import('pdfjs-dist')
  // pdfjs-dist 6.x requires the web worker to be explicitly configured.
  // Worker file is served from public/ to keep it same-origin (no CORS issues).
  pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs'
  const arrayBuffer = await file.arrayBuffer()
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise
  const pages: string[] = []

  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i)
    const content = await page.getTextContent()
    const pageText = content.items
      .map((item) => ('str' in item ? item.str : ''))
      .join(' ')
    pages.push(pageText)
  }

  return pages.join('\n\n')
}

export default function ResumeUploader({ onUpload, disabled }: Props) {
  const [pastedText, setPastedText] = useState('')
  const [fileName, setFileName] = useState<string | null>(null)
  const [extracting, setExtracting] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setFileName(file.name)

    if (file.name.toLowerCase().endsWith('.pdf')) {
      setExtracting(true)
      try {
        const text = await extractPdfText(file)
        onUpload(text, file)
      } catch (err) {
        console.error('PDF extraction failed', err)
        onUpload('[PDF extraction failed — please paste your resume text instead]')
      } finally {
        setExtracting(false)
      }
    } else {
      const reader = new FileReader()
      reader.onload = () => {
        const text = reader.result as string
        onUpload(text)
      }
      reader.readAsText(file)
    }
  }

  function handlePasteSubmit() {
    if (pastedText.trim()) {
      onUpload(pastedText.trim())
    }
  }

  return (
    <div className="card" style={{ marginBottom: '1.5rem' }}>
      <h3 style={{
        fontFamily: 'var(--font-display)',
        fontSize: '0.95rem',
        letterSpacing: '1px',
        marginBottom: '1.25rem',
      }}>
        Upload Your Resume
      </h3>

      {/* Custom styled file upload */}
      <div className="form-group">
        <label className="form-label">Upload File (PDF, TXT, DOCX, MD)</label>

        {/* Hidden native input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt,.pdf,.docx,.md"
          onChange={handleFile}
          disabled={disabled || extracting}
          style={{ display: 'none' }}
        />

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.4rem' }}>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled || extracting}
          >
            {extracting ? 'Extracting...' : 'Choose File'}
          </button>
          <span style={{
            fontSize: '0.82rem',
            color: fileName ? 'var(--accent-green)' : 'var(--text-muted)',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}>
            {extracting ? 'Reading PDF...' : (fileName ?? 'No file selected')}
          </span>
        </div>
      </div>

      {/* Divider */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        margin: '1.25rem 0',
        color: 'var(--text-muted)',
        fontSize: '0.75rem',
      }}>
        <span style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
        OR PASTE TEXT
        <span style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
      </div>

      {/* Paste text */}
      <div className="form-group">
        <label className="form-label">Paste Resume Text</label>
        <textarea
          className="form-input"
          rows={8}
          value={pastedText}
          onChange={(e) => setPastedText(e.target.value)}
          placeholder="Paste your resume content here..."
          disabled={disabled}
          style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem' }}
        />
      </div>

      <button
        type="button"
        className="btn btn-secondary btn-full"
        onClick={handlePasteSubmit}
        disabled={disabled || !pastedText.trim()}
      >
        Use Pasted Text
      </button>
    </div>
  )
}
