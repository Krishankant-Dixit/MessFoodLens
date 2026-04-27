import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'

const COLORS = ['#4f46e5', '#f59e0b', '#10b981', '#ef4444']

function qualityColor(score) {
  if (score >= 80) return 'var(--success)'
  if (score >= 50) return 'var(--accent)'
  return 'var(--danger)'
}

function parseGrams(val) {
  if (typeof val === 'number') return val
  return parseFloat(val) || 0
}

export default function Result() {
  const navigate = useNavigate()
  const [result, setResult] = useState(null)
  const [preview, setPreview] = useState(null)

  useEffect(() => {
    const r = sessionStorage.getItem('mfl_result')
    const p = sessionStorage.getItem('mfl_preview')
    if (!r) { navigate('/upload'); return }
    setResult(JSON.parse(r))
    setPreview(p)
  }, [navigate])

  if (!result) return null

  const macroData = [
    { name: 'Protein', value: parseGrams(result.protein) },
    { name: 'Carbs',   value: parseGrams(result.carbs) },
    { name: 'Fats',    value: parseGrams(result.fats) },
    { name: 'Fiber',   value: parseGrams(result.fiber) },
  ].filter(d => d.value > 0)

  const score = result.meal_quality_score || 0
  const scoreColor = qualityColor(score)

  // Save to session history for dashboard
  const history = JSON.parse(sessionStorage.getItem('mfl_history') || '[]')
  const alreadySaved = history.find(
    h => h.food === result.food && h.ts === result.ts
  )
  if (!alreadySaved) {
    history.unshift({ ...result, ts: Date.now() })
    sessionStorage.setItem('mfl_history', JSON.stringify(history.slice(0, 30)))
  }

  return (
    <main className="page result-page">
      {/* Header */}
      <div className="result-header">
        <h2>Analysis Result</h2>
        {result.confidence > 0 && (
          <span className="badge-confidence">
            {result.confidence}% confidence
          </span>
        )}
      </div>

      {/* Detected food */}
      <div className="detected-food">
        <div>
          <h3>Detected Food</h3>
          <div className="food-name">{result.food}</div>
          {result.serving && result.serving !== 'N/A' && (
            <div className="serving">Serving: {result.serving}</div>
          )}
        </div>
        <div className="quality-ring-wrap">
          <div className="qs-label">Meal Quality</div>
          <div
            className="quality-circle"
            style={{ borderColor: scoreColor, color: scoreColor }}
          >
            {score}
            <span className="qs-unit">/100</span>
          </div>
        </div>
      </div>

      {/* Macro cards */}
      <div className="macro-grid">
        {[
          { label: 'Calories', value: result.calories, unit: 'kcal', color: 'var(--accent)' },
          { label: 'Protein',  value: result.protein,  unit: '',     color: '#4f46e5' },
          { label: 'Carbs',    value: result.carbs,    unit: '',     color: '#10b981' },
          { label: 'Fats',     value: result.fats,     unit: '',     color: '#ef4444' },
          { label: 'Fiber',    value: result.fiber,    unit: '',     color: '#8b5cf6' },
        ].map(m => (
          <div key={m.label} className="macro-card">
            <span className="mc-label">{m.label}</span>
            <span className="mc-value" style={{ color: m.color }}>
              {m.value ?? 'N/A'}
            </span>
            {m.unit && <span className="mc-unit">{m.unit}</span>}
          </div>
        ))}
      </div>

      {/* Macro pie chart */}
      {macroData.length > 0 && (
        <div className="chart-section">
          <h4>📊 Macro Breakdown</h4>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={macroData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={90}
                label={({ name, percent }) =>
                  `${name} ${(percent * 100).toFixed(0)}%`
                }
              >
                {macroData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `${v}g`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Uploaded image preview */}
      {preview && (
        <div className="chart-section">
          <h4>🖼️ Uploaded Image</h4>
          <img src={preview} alt="Analyzed food" className="img-preview-small" />
        </div>
      )}

      {/* Raw model predictions */}
      {result.raw_labels && result.raw_labels.length > 0 && (
        <div className="raw-labels">
          <h4>Model Top Predictions</h4>
          {result.raw_labels.slice(0, 5).map((rl, i) => (
            <div key={i} className="raw-label-row">
              <span style={{ minWidth: 160, textTransform: 'capitalize' }}>
                {rl.label}
              </span>
              <div className="bar-bg">
                <div
                  className="bar-fill"
                  style={{ width: `${Math.min(rl.confidence, 100)}%` }}
                />
              </div>
              <span style={{ minWidth: 55, textAlign: 'right' }}>
                {rl.confidence.toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="result-actions">
        <button className="btn-primary" onClick={() => navigate('/upload')}>
          📷 Analyze Another
        </button>
        <button className="btn-secondary" onClick={() => navigate('/dashboard')}>
          📊 View Dashboard
        </button>
      </div>
    </main>
  )
}
