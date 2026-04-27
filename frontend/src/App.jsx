import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import './App.css'
import Home from './Home'
import Upload from './Upload'
import Result from './Result'
import Dashboard from './Dashboard'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-wrapper">
        <nav className="navbar">
          <span className="nav-brand">🍽️ MessFoodLens</span>
          <div className="nav-links">
            <NavLink to="/" end>Home</NavLink>
            <NavLink to="/upload">Analyze</NavLink>
            <NavLink to="/dashboard">Dashboard</NavLink>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/result" element={<Result />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
