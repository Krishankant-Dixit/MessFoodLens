export default function Loading({ message = 'Loading...' }) {
  return (
    <div className="loading-state">
      <div className="spinner" aria-label="Loading indicator" />
      <p>{message}</p>
    </div>
  );
}
