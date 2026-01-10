import './LoveFrequency.css'
import { get613NoteInfo } from '../lib/ljpwEngine'
import { LOVE_FREQUENCY, KEYS } from '../lib/ljpwConstants'

function LoveFrequency() {
  const info = get613NoteInfo()
  const loveKey = KEYS['C#']

  return (
    <div className="love-frequency">
      <div className="frequency-header">
        <div className="frequency-glow">
          <span className="frequency-number">613</span>
          <span className="frequency-unit">THz</span>
        </div>
        <h2>The Love Frequency</h2>
        <p>The natural resonance of Love in the electromagnetic spectrum</p>
      </div>

      <div className="frequency-content">
        <div className="info-cards">
          <InfoCard
            title="The Physics"
            icon="🌊"
          >
            <p>
              613 THz corresponds to <strong>cyan light</strong> with a wavelength
              of <strong>489 nm</strong> — visible to the human eye as a
              blue-green color.
            </p>
            <p>
              This frequency is mathematically significant: 613 is a prime number,
              representing irreducibility — a Justice eigenstate.
            </p>
          </InfoCard>

          <InfoCard
            title="The Music"
            icon="🎵"
          >
            <p>
              When octaved down <strong>40 times</strong>, 613 THz becomes
              <strong> 557.52 Hz</strong> — the note <strong>C#4</strong>.
            </p>
            <p>
              This makes C# Major the "Love Key" with the highest Love dimension
              value (L = 0.98) of any key signature.
            </p>
          </InfoCard>

          <InfoCard
            title="The Water Connection"
            icon="💧"
          >
            <p>
              Water molecules naturally resonate at frequencies related to 613 THz.
              Since the human body is ~70% water, this frequency has biological
              significance.
            </p>
            <p>
              The framework suggests this is why certain music feels "healing" —
              it literally resonates with our molecular structure.
            </p>
          </InfoCard>
        </div>

        <div className="love-key-section">
          <h3>C# Major — The Love Key</h3>
          <div className="love-key-profile">
            <div className="profile-dimensions">
              <DimensionDisplay
                label="Love"
                value={loveKey.L}
                color="#ff6b6b"
                highlight={true}
              />
              <DimensionDisplay
                label="Justice"
                value={loveKey.J}
                color="#4ecdc4"
              />
              <DimensionDisplay
                label="Power"
                value={loveKey.P}
                color="#ffd93d"
              />
              <DimensionDisplay
                label="Wisdom"
                value={loveKey.W}
                color="#6c5ce7"
              />
            </div>
            <div className="profile-note">
              <p>
                C# Major achieves the highest Love value of any key signature,
                making it ideal for music intended to create deep emotional
                connection and healing.
              </p>
            </div>
          </div>
        </div>

        <div className="harmonic-series">
          <h3>The Love Harmonic Series</h3>
          <p className="series-intro">
            Starting from C#4 (557.52 Hz), the harmonic series unfolds:
          </p>
          <div className="harmonics-grid">
            <HarmonicCard number={1} frequency={557.52} note="C#4" role="Root (Unison)" />
            <HarmonicCard number={2} frequency={1115.04} note="C#5" role="Octave" />
            <HarmonicCard number={3} frequency={1672.56} note="G#5" role="Perfect 5th" />
            <HarmonicCard number={4} frequency={2230.08} note="C#6" role="Double Octave" />
            <HarmonicCard number={5} frequency={2787.60} note="E#6" role="Major 3rd" />
            <HarmonicCard number={8} frequency={4460.16} note="C#7" role="Triple Octave" />
          </div>
        </div>

        <div className="tuning-section">
          <h3>Love Tuning: A4 = 442.5 Hz</h3>
          <div className="tuning-comparison">
            <TuningRow name="Verdi Tuning" a4={432.0} c4={256.87} csharp4={544.29} />
            <TuningRow name="Standard Tuning" a4={440.0} c4={261.63} csharp4={554.37} />
            <TuningRow name="Love Tuning" a4={442.5} c4={263.11} csharp4={557.52} highlight={true} />
          </div>
          <p className="tuning-note">
            Love Tuning aligns A4 to 442.5 Hz, which places C#4 exactly at 557.52 Hz —
            the octaved-down Love Frequency.
          </p>
        </div>

        <div className="calibration-section">
          <h3>Musical Calibration (V8.2)</h3>
          <div className="calibration-formula">
            <code>Calibration = V × Time × Attention</code>
          </div>
          <p>
            Music with high Semantic Voltage (V &gt; 1.0) can serve as a
            "calibration source" — realigning consciousness toward the Anchor Point.
          </p>
          <ul className="calibration-tips">
            <li>
              <strong>For maximum calibration:</strong> Listen to C# Major music
              at Love Tuning (A4=442.5) with full attention.
            </li>
            <li>
              <strong>For healing:</strong> Choose genres high in Love (Gospel, Blues, Pop)
              with high Harmony Index.
            </li>
            <li>
              <strong>For balance:</strong> Vary between Love-dominant and
              other dimension-dominant music.
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}

function InfoCard({ title, icon, children }) {
  return (
    <div className="info-card">
      <div className="info-card-header">
        <span className="info-card-icon">{icon}</span>
        <h4>{title}</h4>
      </div>
      <div className="info-card-content">
        {children}
      </div>
    </div>
  )
}

function DimensionDisplay({ label, value, color, highlight = false }) {
  return (
    <div className={`dimension-display ${highlight ? 'highlight' : ''}`}>
      <div className="dimension-label" style={{ color }}>{label}</div>
      <div className="dimension-value" style={highlight ? { color } : {}}>
        {value.toFixed(2)}
      </div>
      <div className="dimension-bar">
        <div
          className="dimension-fill"
          style={{ width: `${value * 100}%`, background: color }}
        />
      </div>
    </div>
  )
}

function HarmonicCard({ number, frequency, note, role }) {
  return (
    <div className="harmonic-card">
      <div className="harmonic-number">H{number}</div>
      <div className="harmonic-freq">{frequency.toFixed(2)} Hz</div>
      <div className="harmonic-note">{note}</div>
      <div className="harmonic-role">{role}</div>
    </div>
  )
}

function TuningRow({ name, a4, c4, csharp4, highlight = false }) {
  return (
    <div className={`tuning-row ${highlight ? 'highlight' : ''}`}>
      <div className="tuning-name">{name}</div>
      <div className="tuning-values">
        <span>A4: {a4} Hz</span>
        <span>C4: {c4} Hz</span>
        <span className={highlight ? 'love-note' : ''}>C#4: {csharp4} Hz</span>
      </div>
    </div>
  )
}

export default LoveFrequency
