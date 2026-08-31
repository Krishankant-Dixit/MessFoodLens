import { Link } from 'react-router-dom';

const features = [
  { title: 'AI Food Detection', text: 'ImageNet-based prediction with explicit low-confidence handling.' },
  { title: 'Nutrition Analysis', text: 'Estimated calories, protein, carbs, fats, and fiber.' },
  { title: 'Meal Quality Score', text: 'A transparent score based on nutrition balance and moderation.' },
  { title: 'Analytics', text: 'Track calories and quality trends over time locally in your browser.' },
];

export default function Home() {
  return (
    <div className="page home-page">
      <section className="hero">
        <div>
          <p className="eyebrow">AI-powered food nutrition analyzer</p>
          <h1>Understand what you eat, one meal at a time.</h1>
          <p className="hero-copy">
            Upload a meal photo and get a quick estimate of the likely food, nutrition values,
            and a meal quality score.
          </p>
          <div className="hero-actions">
            <Link to="/upload" className="primary-btn">
              Analyze Your Meal
            </Link>
          </div>
        </div>
      </section>

      <section className="feature-grid">
        {features.map((feature) => (
          <div className="feature-card" key={feature.title}>
            <h3>{feature.title}</h3>
            <p>{feature.text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
