import { useState } from 'react'
import './ElementAnalyzer.css'
import RadarChart from './RadarChart'
import HarmonyGauge from './HarmonyGauge'
import {
  analyzeInterval,
  analyzeChord,
  analyzeMode,
} from '../lib/ljpwEngine'
import { INTERVALS, CHORDS, MODES } from '../lib/ljpwConstants'

function ElementAnalyzer() {
  const [elementType, setElementType] = useState('interval')
  const [selectedElement, setSelectedElement] = useState('major_3rd')
  const [analysis, setAnalysis] = useState(null)

  const handleAnalyze = () => {
    let result
    switch (elementType) {
      case 'interval':
        result = analyzeInterval(selectedElement)
        break
      case 'chord':
        result = analyzeChord(selectedElement)
        break
      case 'mode':
        result = analyzeMode(selectedElement)
        break
      default:
        result = null
    }
    setAnalysis(result)
  }

  const getOptions = () => {
    switch (elementType) {
      case 'interval':
        return Object.entries(INTERVALS).map(([key, val]) => ({
          key,
          label: `${val.name} (${val.semitones} semitones)`,
        }))
      case 'chord':
        return Object.entries(CHORDS).map(([key, val]) => ({
          key,
          label: val.name,
        }))
      case 'mode':
        return Object.entries(MODES).map(([key, val]) => ({
          key,
          label: `${val.name}`,
        }))
      default:
        return []
    }
  }

  // Set default selection when type changes
  const handleTypeChange = (type) => {
    setElementType(type)
    setAnalysis(null)
    switch (type) {
      case 'interval':
        setSelectedElement('major_3rd')
        break
      case 'chord':
        setSelectedElement('major')
        break
      case 'mode':
        setSelectedElement('ionian')
        break
    }
  }

  return (
    <div className="element-analyzer">
      <div className="analyzer-header">
        <h2>Musical Element Analyzer</h2>
        <p>Select a musical element to see its semantic profile</p>
      </div>

      <div className="analyzer-controls">
        <div className="control-group">
          <label>Element Type</label>
          <div className="type-buttons">
            <button
              className={elementType === 'interval' ? 'active' : ''}
              onClick={() => handleTypeChange('interval')}
            >
              Intervals
            </button>
            <button
              className={elementType === 'chord' ? 'active' : ''}
              onClick={() => handleTypeChange('chord')}
            >
              Chords
            </button>
            <button
              className={elementType === 'mode' ? 'active' : ''}
              onClick={() => handleTypeChange('mode')}
            >
              Modes
            </button>
          </div>
        </div>

        <div className="control-group">
          <label>Select {elementType}</label>
          <select
            value={selectedElement}
            onChange={(e) => setSelectedElement(e.target.value)}
          >
            {getOptions().map((opt) => (
              <option key={opt.key} value={opt.key}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <button className="analyze-button" onClick={handleAnalyze}>
          Analyze
        </button>
      </div>

      {analysis && (
        <div className="analysis-results">
          <div className="result-header">
            <h3>{analysis.name}</h3>
            <span
              className="phase-badge"
              style={{ background: analysis.phase.color }}
            >
              {analysis.phase.emoji} {analysis.phase.phase}
            </span>
          </div>

          <div className="result-grid">
            <div className="chart-section">
              <RadarChart
                L={analysis.L}
                J={analysis.J}
                P={analysis.P}
                W={analysis.W}
                size={220}
              />
            </div>

            <div className="metrics-section">
              <div className="dimension-bars">
                <DimensionBar label="Love" value={analysis.L} color="#ff6b6b" />
                <DimensionBar label="Justice" value={analysis.J} color="#4ecdc4" />
                <DimensionBar label="Power" value={analysis.P} color="#ffd93d" />
                <DimensionBar label="Wisdom" value={analysis.W} color="#6c5ce7" />
              </div>

              <HarmonyGauge
                value={analysis.H}
                showVoltage={true}
                voltage={analysis.V}
              />

              <div className="dominant-section">
                <span className="dominant-label">Dominant Dimension:</span>
                <span
                  className="dominant-value"
                  style={{ color: analysis.dominant.color }}
                >
                  {analysis.dominant.name}
                </span>
              </div>
            </div>
          </div>

          <div className="phase-description">
            {analysis.phase.description}
          </div>
        </div>
      )}
    </div>
  )
}

function DimensionBar({ label, value, color }) {
  return (
    <div className="dimension-bar">
      <div className="bar-label">
        <span>{label}</span>
        <span style={{ color }}>{value.toFixed(2)}</span>
      </div>
      <div className="bar-track">
        <div
          className="bar-fill"
          style={{
            width: `${value * 100}%`,
            background: color,
          }}
        />
      </div>
    </div>
  )
}

export default ElementAnalyzer
