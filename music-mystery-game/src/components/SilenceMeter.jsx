import './SilenceMeter.css'

function SilenceMeter({ level, lessonsComplete, totalLessons }) {
  // Color transitions from dark red (silence) to bright cyan (music)
  const silenceColor = `hsl(${(100 - level) * 1.8}, 70%, ${30 + (100 - level) * 0.3}%)`

  return (
    <div className="silence-meter">
      <div className="meter-header">
        <span className="meter-label">The Silence</span>
        <span className="meter-value">{level}%</span>
      </div>

      <div className="meter-bar">
        <div
          className="meter-fill"
          style={{
            width: `${level}%`,
            background: `linear-gradient(90deg, ${silenceColor} 0%, #1a1a2e 100%)`,
          }}
        />
        <div className="meter-markers">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="marker" />
          ))}
        </div>
      </div>

      <div className="meter-footer">
        <span className="lessons-count">
          {lessonsComplete}/{totalLessons} concepts learned
        </span>
        <span className="meter-hint">
          {level > 80 && 'The silence presses heavily...'}
          {level > 60 && level <= 80 && 'Music begins to stir...'}
          {level > 40 && level <= 60 && 'The manor awakens...'}
          {level > 20 && level <= 40 && 'Sound returns to these halls...'}
          {level > 0 && level <= 20 && 'Almost there...'}
          {level === 0 && 'The silence is broken!'}
        </span>
      </div>
    </div>
  )
}

export default SilenceMeter
