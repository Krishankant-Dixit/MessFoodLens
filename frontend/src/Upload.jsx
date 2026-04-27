import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const onDrop = useCallback((accepted) => {
    if (!accepted.length) return
    const f = accepted[0]
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    multiple: false,
    maxSize: 10 * 1024 * 1024,
  })

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const form = new FormData()
      form.append('file', file)
      const { data } = await axios.post(`${API_BASE}/analyze`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      })
      // Persist result + image preview in sessionStorage so Result page can read them
      sessionStorage.setItem('mfl_result', JSON.stringify(data))
      sessionStorage.setItem('mfl_preview', preview)
      navigate('/result')
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'Analysis failed. Please try again.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFile(null)
    setPreview(null)
    setError(null)
  }

  return (
    <main className="page">
      {loading && (
        <div className="loading-overlay">
          <div className="spinner" />
          <p>🔍 Analyzing your food…</p>
        </div>
      )}

      <h2 className="upload-title">Analyze Food</h2>
      <p className="upload-subtitle">
        Upload a food photo to detect the dish and see detailed nutrition information.
      </p>

      {!file ? (
        <div
          {...getRootProps()}
          className={`dropzone${isDragActive ? ' drag-over' : ''}`}
        >
          <input {...getInputProps()} />
          <div className="dz-icon">📷</div>
          <strong>Drag &amp; drop your food image here</strong>
          <p>or click to browse — JPEG, PNG, WEBP supported (max 10 MB)</p>
        </div>
      ) : (
        <div className="preview-box">
          <img src={preview} alt="Food preview" />
          <div className="preview-actions">
            <button className="btn-secondary" onClick={handleReset}>
              ✕ Choose different image
            </button>
            <button className="btn-primary" onClick={handleAnalyze} disabled={loading}>
              🔬 Analyze Nutrition
            </button>
          </div>
        </div>
      )}

      {error && (
        <p style={{ marginTop: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>
          ⚠️ {error}
        </p>
      )}
    </main>
  )
}
