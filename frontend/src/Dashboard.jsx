import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, Legend,
} from 'recharts'

function qualityColor(score) {
  if (score >= 80) return '#10b981'
  if (score >= 50) return '#f59e0b'
  return '#ef4444'
}

// Build demo weekly data; if session history exists use it, else use mock
function buildWeeklyData(history) {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  if (history.length === 0) {
    return days.map((day, i) => ({
      day,
      calories: [350, 480, 220, 600, 410, 530, 290][i],
      score: [72, 55, 90, 40, 68, 50, 85][i],
    }))
  }
  return days.map((day, i) => {
    const entry = history[i] || {}
    return {
      day,
      calories: entry.calories || 0,
      score: entry.meal_quality_score || 0,
    }
  })
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [history, setHistory] = useState([])
  const [weekly, setWeekly] = useState([])

  useEffect(() => {
    const h = JSON.parse(sessionStorage.getItem('mfl_history') || '[]')
    setHistory(h)
    setWeekly(buildWeeklyData(h))
  }, [])

  const totalMeals = history.length
  const avgCalories = totalMeals
    ? Math.round(history.reduce((s, m) => s + (m.calories || 0), 0) / totalMeals)
    : '--'
  const avgScore = totalMeals
    ? Math.round(history.reduce((s, m) => s + (m.meal_quality_score || 0), 0) / totalMeals)
    : '--'
  const totalProtein = totalMeals
    ? history.reduce((s, m) => s + (parseFloat(m.protein) || 0), 0).toFixed(0) + 'g'
    : '--'

  return (
    <main className="page">
      <h2 className="dashboard-title">📊 Analytics Dashboard</h2>
      <p className="dashboard-subtitle">
        {totalMeals > 0
          ? `Showing data from your last ${totalMeals} analyzed meal${totalMeals > 1 ? 's' : ''}.`
          : 'No meals analyzed yet. Sample data shown below.'}
      </p>

      {/* Stats row */}
      <div className="stats-row">
        {[
          { label: 'Meals Analyzed', value: totalMeals || 0 },
          { label: 'Avg Calories', value: avgCalories, unit: 'kcal' },
          { label: 'Avg Quality Score', value: avgScore, unit: '/100' },
          { label: 'Total Protein', value: totalProtein },
        ].map(s => (
          <div key={s.label} className="stat-card">
            <div className="sc-label">{s.label}</div>
            <div className="sc-value">
              {s.value}
              {s.unit && (
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginLeft: 4 }}>
                  {s.unit}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="dash-grid">
        {/* Weekly calories bar chart */}
        <div className="dash-card">
          <h4>📅 Weekly Calories</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={weekly} margin={{ top: 0, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="day" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155' }}
              />
              <Bar dataKey="calories" fill="#4f46e5" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Meal quality trend */}
        <div className="dash-card">
          <h4>⭐ Meal Quality Trend</h4>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={weekly} margin={{ top: 0, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="day" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155' }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="score"
                stroke="#f59e0b"
                strokeWidth={2}
                dot={{ fill: '#f59e0b' }}
                name="Quality Score"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent meals */}
      {totalMeals > 0 && (
        <div className="dash-card" style={{ marginTop: '1.5rem' }}>
          <h4>🍽️ Recent Meals</h4>
          <div className="recent-meals">
            {history.slice(0, 8).map((m, i) => (
              <div key={i} className="meal-row">
                <span className="meal-name">{m.food}</span>
                <span className="meal-kcal">{m.calories} kcal</span>
                <span
                  className="meal-score"
                  style={{
                    background: `${qualityColor(m.meal_quality_score)}22`,
                    color: qualityColor(m.meal_quality_score),
                  }}
                >
                  {m.meal_quality_score}/100
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ marginTop: '2rem' }}>
        <button className="btn-primary" onClick={() => navigate('/upload')}>
          📷 Analyze a new meal
        </button>
      </div>
    </main>
  )
}
