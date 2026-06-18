import { NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <NavLink to="/" className="nav-logo">
        <span className="hex">⬡</span>
        <span>CAREER<span className="highlight">COMPASS</span></span>
      </NavLink>
      <ul className="nav-links">
        <li>
          <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>
            Career Profile
          </NavLink>
        </li>
        <li>
          <NavLink to="/resume-studio" className={({ isActive }) => isActive ? 'active' : ''}>
            Resume Studio
          </NavLink>
        </li>
        <li>
          <NavLink to="/mock-interview" className={({ isActive }) => isActive ? 'active' : ''}>
            Mock Interview
          </NavLink>
        </li>
      </ul>
    </nav>
  )
}
