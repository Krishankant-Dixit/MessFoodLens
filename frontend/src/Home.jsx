import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <main className="page">
      <div className="home-hero">
        <h1>AI Food Nutrition Analyzer</h1>
        <p>
          Upload any food photo and instantly get detailed nutrition information
          powered by a pre-trained MobileNetV2 model.
        </p>
        <Link to="/upload" className="btn-primary">
          📷 Analyze Food →
        </Link>
      </div>

      <div className="features-grid">
        {[
          { icon: '🤖', title: 'AI Detection', desc: 'MobileNetV2 pre-trained on ImageNet identifies the food in your photo.' },
          { icon: '🥗', title: 'Nutrition Info', desc: 'Get calories, protein, carbs, fats and fiber per standard serving.' },
          { icon: '⭐', title: 'Meal Quality Score', desc: 'A 0–100 score tells you at a glance how nutritious the meal is.' },
          { icon: '📊', title: 'Analytics Dashboard', desc: 'Track your weekly meals, calorie trends and macro breakdown.' },
        ].map(f => (
          <div key={f.title} className="feature-card">
            <div className="icon">{f.icon}</div>
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </div>
        ))}
      </div>
    </main>
  )
}
