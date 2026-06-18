import { useState, useRef, type KeyboardEvent } from 'react'

interface Props {
  label: string
  values: string[]
  onChange: (values: string[]) => void
  placeholder?: string
}

export default function ChipInput({ label, values, onChange, placeholder }: Props) {
  const [input, setInput] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  function add() {
    const trimmed = input.trim()
    if (trimmed && !values.includes(trimmed)) {
      onChange([...values, trimmed])
    }
    setInput('')
  }

  function remove(index: number) {
    onChange(values.filter((_, i) => i !== index))
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault()
      add()
    }
  }

  return (
    <div className="form-group">
      <label className="form-label">{label}</label>
      <div className="chip-input-wrap" onClick={() => inputRef.current?.focus()}>
        {values.map((v, i) => (
          <span key={i} className="chip">
            {v}
            <button type="button" onClick={() => remove(i)}>&times;</button>
          </span>
        ))}
        <input
          ref={inputRef}
          className="chip-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => input.trim() && add()}
          placeholder={values.length === 0 ? (placeholder ?? 'Type and press Enter...') : ''}
        />
      </div>
    </div>
  )
}
