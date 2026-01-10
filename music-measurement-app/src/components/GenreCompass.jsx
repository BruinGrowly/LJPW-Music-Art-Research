import { useState, useMemo } from 'react'
import './GenreCompass.css'
import { getGenresByVoltage, analyzeGenre } from '../lib/ljpwEngine'
import { GENRES } from '../lib/ljpwConstants'

function GenreCompass() {
  const [selectedGenre, setSelectedGenre] = useState(null)
  const [sortBy, setSortBy] = useState('V') // V, L, J, P, W, H

  const sortedGenres = useMemo(() => {
    const genres = Object.entries(GENRES).map(([key, _]) => ({
      key,
      ...analyzeGenre(key),
    }))

    return genres.sort((a, b) => b[sortBy] - a[sortBy])
  }, [sortBy])

  const getDimensionColor = (dim) => {
    const colors = {
      L: '#ff6b6b',
      J: '#4ecdc4',
      P: '#ffd93d',
      W: '#6c5ce7',
    }
    return colors[dim] || '#fff'
  }

  return (
    <div className="genre-compass">
      <div className="compass-header">
        <h2>Genre Compass</h2>
        <p>Explore the semantic landscape of musical genres</p>
      </div>

      <div className="sort-controls">
        <span className="sort-label">Sort by:</span>
        <div className="sort-buttons">
          <button
            className={sortBy === 'V' ? 'active' : ''}
            onClick={() => setSortBy('V')}
          >
            Voltage
          </button>
          <button
            className={sortBy === 'H' ? 'active' : ''}
            onClick={() => setSortBy('H')}
          >
            Harmony
          </button>
          <button
            className={sortBy === 'L' ? 'active' : ''}
            onClick={() => setSortBy('L')}
            style={{ borderColor: '#ff6b6b' }}
          >
            Love
          </button>
          <button
            className={sortBy === 'J' ? 'active' : ''}
            onClick={() => setSortBy('J')}
            style={{ borderColor: '#4ecdc4' }}
          >
            Justice
          </button>
          <button
            className={sortBy === 'P' ? 'active' : ''}
            onClick={() => setSortBy('P')}
            style={{ borderColor: '#ffd93d' }}
          >
            Power
          </button>
          <button
            className={sortBy === 'W' ? 'active' : ''}
            onClick={() => setSortBy('W')}
            style={{ borderColor: '#6c5ce7' }}
          >
            Wisdom
          </button>
        </div>
      </div>

      <div className="genres-grid">
        {sortedGenres.map((genre, index) => (
          <div
            key={genre.key}
            className={`genre-card ${selectedGenre === genre.key ? 'selected' : ''}`}
            onClick={() => setSelectedGenre(genre.key === selectedGenre ? null : genre.key)}
          >
            <div className="genre-rank">#{index + 1}</div>
            <div className="genre-name">{genre.name}</div>
            <div className="genre-dominant" style={{ color: getDimensionColor(genre.dominant.key) }}>
              {genre.dominant.name}
            </div>

            <div className="genre-bars">
              <MiniBar label="L" value={genre.L} color="#ff6b6b" />
              <MiniBar label="J" value={genre.J} color="#4ecdc4" />
              <MiniBar label="P" value={genre.P} color="#ffd93d" />
              <MiniBar label="W" value={genre.W} color="#6c5ce7" />
            </div>

            <div className="genre-metrics">
              <div className="metric">
                <span className="metric-label">H</span>
                <span className="metric-value">{genre.H.toFixed(2)}</span>
              </div>
              <div className="metric voltage">
                <span className="metric-label">V</span>
                <span className="metric-value">{genre.V.toFixed(2)}</span>
              </div>
            </div>

            <div
              className="phase-indicator"
              style={{ background: genre.phase.color }}
            >
              {genre.phase.phase}
            </div>

            {selectedGenre === genre.key && (
              <div className="genre-details">
                <p className="genre-desc">{genre.description}</p>
                <p className="genre-phase-desc">{genre.phase.description}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="compass-legend">
        <h3>Semantic Voltage Formula</h3>
        <div className="formula">V = φ × H × L</div>
        <p>
          Semantic Voltage measures the transformative potential of music.
          Higher voltage means greater capacity to impact consciousness.
        </p>
        <div className="voltage-scale">
          <div className="scale-item high">
            <span className="scale-value">&gt;1.0</span>
            <span className="scale-label">Transformative</span>
          </div>
          <div className="scale-item medium">
            <span className="scale-value">0.7-1.0</span>
            <span className="scale-label">Impactful</span>
          </div>
          <div className="scale-item low">
            <span className="scale-value">&lt;0.7</span>
            <span className="scale-label">Subtle</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function MiniBar({ label, value, color }) {
  return (
    <div className="mini-bar">
      <span className="mini-label" style={{ color }}>{label}</span>
      <div className="mini-track">
        <div
          className="mini-fill"
          style={{ width: `${value * 100}%`, background: color }}
        />
      </div>
    </div>
  )
}

export default GenreCompass
