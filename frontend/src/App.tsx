import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import CareerProfile from './pages/CareerProfile'
import ResumeStudio from './pages/ResumeStudio'
import MockInterview from './pages/MockInterview'

export default function App() {
  return (
    <>
      <div className="bg-grid" />
      <Navbar />
      <Routes>
        <Route path="/" element={<CareerProfile />} />
        <Route path="/career-profile" element={<Navigate to="/" replace />} />
        <Route path="/resume-studio" element={<ResumeStudio />} />
        <Route path="/mock-interview" element={<MockInterview />} />
      </Routes>
      <footer className="footer">
        Microsoft HK × Student Ambassador Program · Agent Impact Lab 2026
      </footer>
    </>
  )
}
