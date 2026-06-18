import type { SkillsTable as SkillsTableType } from '../types'

const TAG_LABELS: Record<string, string> = {
  mastered: 'Mastered',
  learning: 'Learning',
  missing: 'Missing',
}

const IMPORTANCE_LABELS: Record<string, string> = {
  critical: 'CRITICAL',
  recommended: 'RECOMMENDED',
  'nice-to-have': 'NICE',
}

interface Props {
  skillsTable: SkillsTableType
}

export default function SkillsTable({ skillsTable }: Props) {
  return (
    <div>
      {/* Summary */}
      <p style={{
        fontSize: '0.9rem',
        color: 'var(--text-secondary)',
        marginBottom: '1.5rem',
        lineHeight: 1.6,
      }}>
        {skillsTable.summary}
      </p>

      {/* Table header */}
      <div className="skills-table-header">
        <span>Skill</span>
        <span>Importance</span>
        <span>Proficiency</span>
      </div>

      {/* Skills rows */}
      <div className="skills-grid">
        {skillsTable.skills.map((skill, i) => (
          <div key={i} className="skill-row">
            <div>
              <span className="skill-name">{skill.name}</span>
              <span className="skill-category">{skill.category}</span>
            </div>
            <span className={`skill-importance ${skill.importance}`}>
              {IMPORTANCE_LABELS[skill.importance] ?? skill.importance}
            </span>
            <span className={`tag tag-${skill.proficiency}`}>
              {TAG_LABELS[skill.proficiency] ?? skill.proficiency}
            </span>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="skills-legend">
        <span><span className="legend-dot mastered" /> Mastered</span>
        <span><span className="legend-dot learning" /> Learning</span>
        <span><span className="legend-dot missing" /> Missing</span>
      </div>
    </div>
  )
}
