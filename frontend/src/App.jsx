import React, { useState, useRef } from 'react';
import { Document, Page } from 'react-pdf';
import './App.css';

const DocumentUpload = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isPdf, setIsPdf] = useState(false);
  const [numPages, setNumPages] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [language, setLanguage] = useState('eng');
  const [activeCategory, setActiveCategory] = useState(null);
  const [showTextRegions, setShowTextRegions] = useState(false);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [textRegions, setTextRegions] = useState([]);
  const [selectedText, setSelectedText] = useState('');
  const fileInputRef = useRef(null);
  const imageContainerRef = useRef(null);

  // Prevent default drag behaviors
  React.useEffect(() => {
    const handleDragOver = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };
    const handleDrop = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };
    
    document.addEventListener('dragover', handleDragOver);
    document.addEventListener('drop', handleDrop);
    
    return () => {
      document.removeEventListener('dragover', handleDragOver);
      document.removeEventListener('drop', handleDrop);
    };
  }, []);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      console.log('File selected:', selectedFile.name);
      setFile(selectedFile);
      setError('');
      setResult(null);
      setTextRegions([]);
      setShowTextRegions(false);
      setSelectedRegion(null);
      setSelectedText('');

      const isPdfFile = selectedFile.type === 'application/pdf' || selectedFile.name.toLowerCase().endsWith('.pdf');
      setIsPdf(isPdfFile);

      if (isPdfFile) {
        const objectUrl = URL.createObjectURL(selectedFile);
        setPreview(objectUrl);
      } else {
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreview(reader.result);
        };
        reader.readAsDataURL(selectedFile);
      }
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.type.startsWith('image/') || droppedFile.type === 'application/pdf')) {
      handleFileChange({ target: { files: [droppedFile] } });
    } else {
      setError('Please drop an image or PDF file');
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setTextRegions([]);
    setShowTextRegions(false);
    setSelectedRegion(null);
    setSelectedText('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/upload?lang=${language}&return_regions=true`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Upload failed with status ${response.status}`);
      }

      const data = await response.json();
      console.log('Full response:', data);
      
      if (data.text_regions && Array.isArray(data.text_regions)) {
        console.log(`Found ${data.text_regions.length} text regions`);
        setTextRegions(data.text_regions);
        setShowTextRegions(true);
      }

      const { text_regions, ...resultData } = data;
      setResult(resultData);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'An error occurred during processing.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    if (preview && isPdf && preview.startsWith('blob:')) {
      URL.revokeObjectURL(preview);
    }
    setFile(null);
    setPreview(null);
    setIsPdf(false);
    setNumPages(null);
    setResult(null);
    setError('');
    setTextRegions([]);
    setShowTextRegions(false);
    setSelectedRegion(null);
    setSelectedText('');
    setActiveCategory(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleRegionClick = (region, index) => {
    setSelectedRegion(index);
    setSelectedText(region.text);
    console.log('Selected text:', region.text);
  };

  const getCategoryColor = (category) => {
    const colors = {
      title: 'purple',
      date: 'blue',
      name: 'green',
      email: 'pink',
      phone: 'orange',
      amount: 'emerald',
      address: 'cyan',
      tax_id: 'red',
      invoice_number: 'teal',
      items: 'indigo',
      other: 'gray',
      document_type: 'amber',
    };
    return colors[category] || 'gray';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      title: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>,
      date: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>,
      name: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>,
      email: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>,
      phone: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>,
      amount: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>,
      address: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>,
      tax_id: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>,
      invoice_number: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>,
      items: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>,
      other: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>,
      document_type: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>,
    };
    return icons[category] || icons.other;
  };

  return (
    <div className="app-container">
      <div className="bg-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>

      <div className="main-card animate-slide-in">
        <header className="header">
          <div className="logo-container">
            <div className="logo-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <polyline points="10 9 9 9 8 9" />
              </svg>
            </div>
          </div>
          <h1 className="title">OCR Document Scanner</h1>
          <p className="subtitle">Upload a document, scan for text, then click on any highlighted text to extract it</p>
        </header>

        <div className="workspace">
          {/* Left Panel - Document Viewer */}
          <div className="document-panel">
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              id="file-upload"
              type="file"
              accept="image/*,.pdf"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />

            <div
              className={`upload-zone ${dragActive ? 'drag-active' : ''} ${preview ? 'has-preview' : ''}`}
              onDragEnter={handleDrag}
              onDragOver={handleDrag}
              onDragLeave={handleDrag}
              onDrop={handleDrop}
              onClick={() => !preview && fileInputRef.current?.click()}
            >
              {preview ? (
                <div className="preview-wrapper">
                  {/* Toggle Text Regions Button */}
                  {result && textRegions.length > 0 && (
                    <button
                      type="button"
                      className={`toggle-regions-btn ${showTextRegions ? 'active' : ''}`}
                      onClick={() => setShowTextRegions(!showTextRegions)}
                      title="Toggle text region selection"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <line x1="9" y1="9" x2="15" y2="9"/>
                        <line x1="9" y1="12" x2="15" y2="12"/>
                        <line x1="9" y1="15" x2="13" y2="15"/>
                      </svg>
                      <span>{showTextRegions ? 'Hide' : 'Show'} Text ({textRegions.length})</span>
                    </button>
                  )}

                  <div
                    ref={imageContainerRef}
                    className="preview-container"
                  >
                    {isPdf ? (
                      <div className="pdf-viewer-wrapper">
                        <Document
                          file={preview}
                          onLoadSuccess={({ numPages }) => setNumPages(numPages)}
                          onLoadError={(error) => setError('Failed to load PDF preview')}
                          loading={
                            <div className="pdf-loading">
                              <div className="spinner"></div>
                              <span>Loading PDF...</span>
                            </div>
                          }
                          className="pdf-document"
                        >
                          <Page
                            pageNumber={1}
                            className="pdf-page"
                            width={600}
                            renderAnnotationLayer={false}
                            renderTextLayer={false}
                          />
                        </Document>
                        {numPages > 1 && (
                          <div className="pdf-page-indicator">Page 1 of {numPages}</div>
                        )}
                      </div>
                    ) : (
                      <div className="image-with-regions">
                        <img 
                          src={preview} 
                          alt="Document" 
                          className="preview-image" 
                        />
                        {/* Text Regions Overlay */}
                        {showTextRegions && textRegions.map((region, index) => (
                          <div
                            key={index}
                            className={`text-region-box ${selectedRegion === index ? 'selected' : ''}`}
                            style={{
                              left: `${region.bbox.x_percent}%`,
                              top: `${region.bbox.y_percent}%`,
                              width: `${region.bbox.width_percent}%`,
                              height: `${region.bbox.height_percent}%`,
                            }}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleRegionClick(region, index);
                            }}
                            title={region.text}
                          >
                            <span className="region-text">{region.text}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Remove button */}
                  <button
                    type="button"
                    className="remove-image-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleClear();
                    }}
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="18" y1="6" x2="6" y2="18" />
                      <line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                  </button>
                </div>
              ) : (
                <div className="upload-content">
                  <div className="upload-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="17 8 12 3 7 8" />
                      <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                  </div>
                  <p className="upload-text">
                    <span className="highlight">Click to upload</span> or drag and drop
                  </p>
                  <p className="upload-hint">PNG, JPG, GIF, or PDF up to 10MB</p>
                </div>
              )}
            </div>

            {/* Controls */}
            {file && (
              <div className="controls-panel">
                <div className="language-selector">
                  <label htmlFor="language" className="language-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="2" y1="12" x2="22" y2="12"/>
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>
                    OCR Language
                  </label>
                  <select
                    id="language"
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="language-select"
                    disabled={loading}
                  >
                    <option value="eng">English</option>
                    <option value="tha">Thai (ไทย)</option>
                    <option value="eng+tha">English + Thai (Mixed)</option>
                  </select>
                </div>

                <div className="form-actions">
                  <button
                    type="button"
                    onClick={handleClear}
                    className="btn btn-secondary"
                    disabled={loading}
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="1 4 1 10 7 10" />
                      <path d="M8.51 16a15.06 15.06 0 0 0 10.36-9.31" />
                    </svg>
                    Clear
                  </button>
                  <button
                    type="button"
                    onClick={handleSubmit}
                    disabled={loading || !file}
                    className={`btn btn-primary ${loading ? 'loading' : ''}`}
                  >
                    {loading ? (
                      <>
                        <span className="spinner"></span>
                        Scanning...
                      </>
                    ) : (
                      <>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <polygon points="5 3 19 12 5 21 5 3" />
                        </svg>
                        {textRegions.length > 0 ? 'Re-scan' : 'Scan for Text'}
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Right Panel - Results */}
          <div className="results-panel">
            {error && (
              <div className="error-message animate-slide-in">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                <span>{error}</span>
                <button onClick={() => setError('')} className="close-error">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
            )}

            {/* Selected Text Output */}
            {selectedText && (
              <div className="selected-text-box animate-slide-in">
                <div className="selected-text-header">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 7V4h16v3M9 20h6M12 4v16"/>
                  </svg>
                  <h3>Selected Text</h3>
                </div>
                <div className="selected-text-content">
                  {selectedText}
                </div>
                <button
                  className="copy-btn"
                  onClick={() => {
                    navigator.clipboard.writeText(selectedText);
                    alert('Copied to clipboard!');
                  }}
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                  </svg>
                  Copy Text
                </button>
              </div>
            )}

            {result ? (
              <div className="results-content animate-slide-in">
                <div className="results-header">
                  <h2 className="results-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                      <polyline points="22 4 12 14.01 9 11.01" />
                    </svg>
                    Scan Complete
                  </h2>
                  <span className="results-badge">Success</span>
                </div>

                <p className="results-instruction">
                  Click on highlighted text in the image to extract it
                </p>

                {/* Document Type Badge */}
                {result.document_type && result.document_type !== 'unknown' && (
                  <div className="document-type-badge">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                    <span>Type: </span>
                    <strong>{result.document_type.replace('_', ' ').toUpperCase()}</strong>
                  </div>
                )}

                {/* Category Tabs */}
                <div className="category-tabs">
                  {Object.entries(result).map(([category, items]) =>
                    category !== 'document_type' && 
                    Array.isArray(items) && 
                    items.length > 0 && (
                      <button
                        key={category}
                        className={`category-tab ${activeCategory === category ? 'active' : ''} ${getCategoryColor(category)}`}
                        onClick={() => setActiveCategory(activeCategory === category ? null : category)}
                      >
                        {getCategoryIcon(category)}
                        <span className="tab-label">{category.charAt(0).toUpperCase() + category.slice(1)}</span>
                        <span className="tab-count">{items.length}</span>
                      </button>
                    )
                  )}
                </div>

                {/* Results Display */}
                <div className="results-display">
                  {activeCategory && result[activeCategory] ? (
                    Array.isArray(result[activeCategory]) && result[activeCategory].length > 0 ? (
                      <div className="category-results animate-fade-in">
                        <div className="category-header">
                          {getCategoryIcon(activeCategory)}
                          <h3>{activeCategory.replace('_', ' ').charAt(0).toUpperCase() + activeCategory.replace('_', ' ').slice(1)}</h3>
                        </div>
                        <ul className="results-list">
                          {result[activeCategory].map((item, index) => (
                            <li key={index} className="result-item">
                              <span className="item-bullet"></span>
                              <span className="item-text">{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : (
                      <div className="no-results">
                        <p>No items found in this category</p>
                      </div>
                    )
                  ) : activeCategory === null ? (
                    <div className="no-selection">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 16v-4M12 8h.01"/>
                      </svg>
                      <p>Click a category above to view results</p>
                    </div>
                  ) : null}
                </div>
              </div>
            ) : (
              <div className="empty-results">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="12" y1="8" x2="12" y2="16"/>
                  <line x1="8" y1="12" x2="16" y2="12"/>
                </svg>
                <h3>No Results Yet</h3>
                <p>Upload a document and click "Scan for Text" to detect all text regions</p>
              </div>
            )}
          </div>
        </div>

        <footer className="footer">
          <p>Powered by AI • Fast & Accurate OCR Processing</p>
        </footer>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <DocumentUpload />
    </div>
  );
}

export default App;
