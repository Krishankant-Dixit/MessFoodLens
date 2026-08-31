import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage';
import Loading from '../components/Loading';
import { analyzeImage } from '../services/api';

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export default function Upload() {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const validateFile = (selectedFile) => {
    if (!selectedFile) {
      return 'Please select an image to analyze.';
    }

    if (!ACCEPTED_TYPES.includes(selectedFile.type) && !['.jpg', '.jpeg', '.png', '.webp'].includes(selectedFile.name.slice(selectedFile.name.lastIndexOf('.')).toLowerCase())) {
      return 'Unsupported file type. Please upload a JPEG, PNG, or WEBP image.';
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      return 'File is larger than 10 MB. Please choose a smaller image.';
    }

    return '';
  };

  const handleFileSelection = (selectedFile) => {
    const validationMessage = validateFile(selectedFile);

    if (validationMessage) {
      setError(validationMessage);
      setFile(null);
      setPreview('');
      return;
    }

    setError('');
    setFile(selectedFile);

    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result);
    reader.readAsDataURL(selectedFile);
  };

  const onPickFile = (event) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) handleFileSelection(selectedFile);
  };

  const onDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const selectedFile = event.dataTransfer.files?.[0];
    if (selectedFile) handleFileSelection(selectedFile);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please choose an image before analyzing.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await analyzeImage(file);
      if (!response.success) {
        setError(response.message || 'Food could not be identified confidently.');
        setIsLoading(false);
        return;
      }

      const history = JSON.parse(localStorage.getItem('messfoodlens-history') || '[]');
      const entry = {
        id: Date.now(),
        food: response.food,
        calories: response.calories,
        quality: response.meal_quality_score,
        protein: response.protein,
        timestamp: new Date().toISOString(),
      };
      localStorage.setItem('messfoodlens-history', JSON.stringify([entry, ...history].slice(0, 30)));

      navigate('/result', { state: { result: response, image: preview } });
    } catch (err) {
      const status = err?.response?.status;
      const responseData = err?.response?.data || {};
      const message = responseData?.detail || responseData?.message || err?.message || 'The server is unavailable right now.';

      if (status === 422 || status === 415 || status === 413 || status === 400) {
        setError(message);
      } else {
        setError(message || 'The server is unavailable right now.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page upload-page">
      <div className="card upload-card">
        <h2>Upload a food image</h2>
        <p className="helper-text">JPEG, PNG, or WEBP up to 10 MB.</p>

        <div
          className={`dropzone ${isDragging ? 'dragging' : ''}`}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={onDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {preview ? (
            <img src={preview} alt="Food preview" className="image-preview" />
          ) : (
            <div className="dropzone-content">
              <span className="upload-icon">📷</span>
              <p>Drag & drop an image here</p>
              <button type="button" className="secondary-btn">Choose file</button>
            </div>
          )}
          <input ref={fileInputRef} type="file" accept="image/jpeg,image/png,image/webp" hidden onChange={onPickFile} />
        </div>

        {file && (
          <div className="file-info">
            <span>{file.name}</span>
            <span>{formatFileSize(file.size)}</span>
          </div>
        )}

        <ErrorMessage message={error} />

        {isLoading ? (
          <Loading message="Analyzing your food..." />
        ) : (
          <button type="button" className="primary-btn large" onClick={handleAnalyze} disabled={!file}>
            Analyze Food
          </button>
        )}
      </div>
    </div>
  );
}
