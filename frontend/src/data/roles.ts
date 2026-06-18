export interface RoleSector {
  sector: string
  roles: string[]
}

export const ROLE_OPTIONS: RoleSector[] = [
  {
    sector: 'Technology & IT',
    roles: [
      'Data Analyst',
      'Software Engineer',
      'AI / Machine Learning Engineer',
      'IT Project Manager',
      'Business Intelligence Developer',
    ],
  },
  {
    sector: 'Banking & Finance',
    roles: [
      'Investment Banking Analyst',
      'Risk Analyst',
      'Wealth Management Trainee',
      'Fintech Associate',
      'Compliance Officer',
    ],
  },
  {
    sector: 'Professional Services',
    roles: [
      'Audit Associate',
      'Management Consultant',
      'HR Specialist',
      'ESG Analyst',
    ],
  },
  {
    sector: 'Marketing & E-commerce',
    roles: [
      'Digital Marketing Specialist',
      'E-commerce Operations Specialist',
      'Product Manager',
    ],
  },
  {
    sector: 'Engineering & Construction',
    roles: [
      'Civil Engineer',
      'Supply Chain Analyst',
      'Building Services Engineer',
    ],
  },
]

/** Flat list of all role names — useful for dropdowns / validation */
export const ALL_ROLES: string[] = ROLE_OPTIONS.flatMap((s) => s.roles)
