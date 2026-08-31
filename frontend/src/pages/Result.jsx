import { Link, useLocation } from 'react-router-dom';
import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';

const COLORS = ['#22c55e', '#f59e0b', '#ef4444'];

export default function Result() {
  const location = useLocation();
  const result = location.state?.result;
  const image = location.state?.image;

  if (!result) {
    return (
      <div className="page">
        <div className="card empty-state-card">
          <h2>No analysis found</h2>
          <p>Please upload an image before viewing results.</p>
          <Link to="/upload" className="primary-btn">Go to Upload</Link>
        </div>
      </div>
    );
  }

  const chartData = [
    { name: 'Protein', value: Number(result.protein || 0) },
    { name: 'Carbohydrates', value: Number(result.carbs || 0) },
    { name: 'Fats', value: Number(result.fats || 0) },
  ];

  return (
    <div className="page result-page">
      <div className="card result-layout">
        <div className="result-image-panel">
          {image ? <img src={image} alt="Uploaded meal" className="result-image" /> : null}
        </div>

        <div className="result-meta">
          <p className="eyebrow">Detection result</p>
          <h2>{result.food ? result.food : 'Food not identified'}</h2>

          {result.success === false ? (
            <div className="warning-box">
              <strong>Food identification has low confidence.</strong>
              <p>Nutrition values may be inaccurate.</p>
            </div>
          ) : null}

          <div className="stats-grid">
            <div className="stat-box">
              <span>AI Confidence</span>
              <strong>{result.confidence ? `${result.confidence}%` : 'N/A'}</strong>
            </div>
            <div className="stat-box">
              <span>Calories</span>
              <strong>{result.calories} kcal</strong>
            </div>
            <div className="stat-box">
              <span>Protein</span>
              <strong>{result.protein} g</strong>
            </div>
            <div className="stat-box">
              <span>Carbs</span>
              <strong>{result.carbs} g</strong>
            </div>
            <div className="stat-box">
              <span>Fats</span>
              <strong>{result.fats} g</strong>
            </div>
            <div className="stat-box">
              <span>Fiber</span>
              <strong>{result.fiber} g</strong>
            </div>
            <div className="stat-box full-width">
              <span>Serving Size</span>
              <strong>{result.serving}</strong>
            </div>
            <div className="stat-box full-width">
              <span>Meal Quality Score</span>
              <strong>{result.meal_quality_score}/100</strong>
            </div>
          </div>

          <div className="chart-panel">
            <h3>Macro Breakdown</h3>
            <div className="chart-wrapper">
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie data={chartData} dataKey="value" nameKey="name" innerRadius={45} outerRadius={80} paddingAngle={2}>
                    {chartData.map((entry, index) => (
                      <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value} g`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="result-actions">
            <Link to="/upload" className="primary-btn">
              Analyze Another Meal
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
