import './HarmonyGauge.css'

function HarmonyGauge({ value, label = 'Harmony Index', showVoltage = false, voltage = 0 }) {
  const percentage = Math.min(Math.max(value * 100, 0), 100)

  // Determine color based on value
  const getColor = () => {
    if (value < 0.5) return '#ff4757'    // Entropic - red
    if (value < 0.6) return '#ffa502'    // Homeostatic - orange
    return '#2ed573'                       // Autopoietic - green
  }

  const getPhase = () => {
    if (value < 0.5) return 'ENTROPIC'
    if (value < 0.6) return 'HOMEOSTATIC'
    return 'AUTOPOIETIC'
  }

  return (
    <div className="harmony-gauge">
      <div className="gauge-label">{label}</div>
      <div className="gauge-container">
        <div className="gauge-track">
          <div
            className="gauge-fill"
            style={{
              width: `${percentage}%`,
              background: getColor(),
            }}
          />
          <div className="gauge-markers">
            <div className="marker marker-entropic" style={{ left: '50%' }} />
            <div className="marker marker-autopoietic" style={{ left: '60%' }} />
          </div>
        </div>
        <div className="gauge-value" style={{ color: getColor() }}>
          {value.toFixed(3)}
        </div>
      </div>
      <div className="gauge-phase" style={{ color: getColor() }}>
        {getPhase()}
      </div>
      {showVoltage && (
        <div className="voltage-display">
          <span className="voltage-label">Semantic Voltage:</span>
          <span className="voltage-value">{voltage.toFixed(3)} V</span>
        </div>
      )}
    </div>
  )
}

export default HarmonyGauge
