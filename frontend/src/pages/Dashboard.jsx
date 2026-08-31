import { useEffect, useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const defaultHistory = [
  { id: 1, food: 'pizza', calories: 285, quality: 55, protein: 12, timestamp: new Date().toISOString() },
  { id: 2, food: 'salad', calories: 120, quality: 75, protein: 5, timestamp: new Date().toISOString() },
  { id: 3, food: 'burger', calories: 330, quality: 62, protein: 18, timestamp: new Date().toISOString() },
];

export default function Dashboard() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const storedHistory = localStorage.getItem('messfoodlens-history');
    if (storedHistory) {
      try {
        setHistory(JSON.parse(storedHistory));
      } catch {
        setHistory(defaultHistory);
      }
    } else {
      setHistory(defaultHistory);
      localStorage.setItem('messfoodlens-history', JSON.stringify(defaultHistory));
    }
  }, []);

  const weeklyCalories = useMemo(() => {
    const values = history.length ? history : defaultHistory;
    return values.map((entry, index) => ({
      name: `Meal ${index + 1}`,
      calories: Number(entry.calories || 0),
    }));
  }, [history]);

  const qualityTrend = useMemo(() => {
    const values = history.length ? history : defaultHistory;
    return values.map((entry, index) => ({
      name: `M${index + 1}`,
      quality: Number(entry.quality || 0),
    }));
  }, [history]);

  const totalCalories = history.reduce((sum, entry) => sum + Number(entry.calories || 0), 0);
  const averageQuality = history.length ? Math.round(history.reduce((sum, entry) => sum + Number(entry.quality || 0), 0) / history.length) : 0;
  const averageProtein = history.length ? Math.round(history.reduce((sum, entry) => sum + Number(entry.protein || 0), 0) / history.length) : 0;

  return (
    <div className="page dashboard-page">
      <div className="dashboard-header">
        <h2>Meal analytics</h2>
      </div>

      <div className="summary-grid">
        <div className="summary-card">
          <span>Total calories</span>
          <strong>{totalCalories}</strong>
        </div>
        <div className="summary-card">
          <span>Average meal quality</span>
          <strong>{averageQuality}/100</strong>
        </div>
        <div className="summary-card">
          <span>Meals analyzed</span>
          <strong>{history.length}</strong>
        </div>
        <div className="summary-card">
          <span>Average protein</span>
          <strong>{averageProtein} g</strong>
        </div>
      </div>

      <div className="chart-grid">
        <div className="card chart-card">
          <h3>Weekly Calories</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={weeklyCalories}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="calories" fill="#3b82f6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card chart-card">
          <h3>Meal Quality Trend</h3>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={qualityTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="quality" stroke="#22c55e" strokeWidth={3} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
