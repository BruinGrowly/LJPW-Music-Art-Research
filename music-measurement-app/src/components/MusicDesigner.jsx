import { useState, useEffect } from 'react'
import './MusicDesigner.css'
import RadarChart from './RadarChart'
import HelpTooltip, { InfoIcon } from './HelpTooltip'
import { MUSIC_GOALS, generateRecipe, generateDetailedAIPrompt } from '../lib/musicDesigner'
import { exportAsJSON } from '../lib/exportUtils'

const STORAGE_KEY = 'ljpw-music-designer'

function MusicDesigner() {
  // State
  const [selectedGoal, setSelectedGoal] = useState(() => {
    const saved = sessionStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved).selectedGoal || 'earworm' : 'earworm'
  })
  const [customTargets, setCustomTargets] = useState(() => {
    const saved = sessionStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved).customTargets || { L: 0.8, J: 0.75, P: 0.7, W: 0.65 } : { L: 0.8, J: 0.75, P: 0.7, W: 0.65 }
  })
  const [useCustom, setUseCustom] = useState(false)
  const [recipe, setRecipe] = useState(null)
  const [aiPrompts, setAiPrompts] = useState(null)
  const [customInstructions, setCustomInstructions] = useState('')
  const [copied, setCopied] = useState(false)

  // Persist state
  useEffect(() => {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ selectedGoal, customTargets }))
  }, [selectedGoal, customTargets])

  // Get current targets
  const currentTargets = useCustom ? customTargets : MUSIC_GOALS[selectedGoal].targets

  // Generate recipe when inputs change
  useEffect(() => {
    const newRecipe = generateRecipe(currentTargets)
    setRecipe(newRecipe)
    setAiPrompts(generateDetailedAIPrompt(newRecipe, selectedGoal, {
      includeInstruments: true,
      includeLyricStyle: true,
      includeStructure: true,
    }))
  }, [currentTargets, selectedGoal])

  const handleGoalSelect = (goalId) => {
    setSelectedGoal(goalId)
    setUseCustom(false)
  }

  const handleCustomTargetChange = (dimension, value) => {
    setCustomTargets(prev => ({ ...prev, [dimension]: parseFloat(value) }))
    setUseCustom(true)
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExport = () => {
    if (recipe && aiPrompts) {
      const data = {
        exportedAt: new Date().toISOString(),
        appVersion: 'LJPW V8.5 Music Designer',
        goal: MUSIC_GOALS[selectedGoal],
        targets: currentTargets,
        recipe: {
          key: recipe.key.name,
          mode: recipe.mode.name,
          genre: recipe.genre.name,
          tempo: recipe.tempo,
          recommendedChords: recipe.chords.map(c => c.name),
          recommendedIntervals: recipe.intervals.map(i => i.name),
        },
        metrics: recipe.metrics,
        aiPrompts: {
          short: aiPrompts.shortPrompt,
          detailed: aiPrompts.detailedPrompt,
        },
      }
      exportAsJSON(data, 'music-design')
    }
  }

  return (
    <div className="music-designer">
      <div className="designer-header">
        <h2>Music Designer</h2>
        <p>Design your perfect song and get AI-ready prompts for Suno, Udio, and more</p>
      </div>

      {/* Goal Selection */}
      <div className="designer-section">
        <h3>
          What do you want to create?
          <HelpTooltip
            title="Music Goals"
            content="Choose a goal and we'll recommend the perfect combination of key, mode, genre, tempo, and chords to achieve it."
            position="right"
          >
            <InfoIcon color="#6c5ce7" size={14} />
          </HelpTooltip>
        </h3>

        <div className="goals-grid">
          {Object.values(MUSIC_GOALS).map((goal) => (
            <button
              key={goal.id}
              className={`goal-card ${selectedGoal === goal.id && !useCustom ? 'selected' : ''}`}
              onClick={() => handleGoalSelect(goal.id)}
            >
              <span className="goal-emoji">{goal.emoji}</span>
              <span className="goal-name">{goal.name}</span>
              <span className="goal-desc">{goal.description}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Targets (Advanced) */}
      <div className="designer-section custom-section">
        <h3>
          Fine-tune your targets
          <span className={`custom-badge ${useCustom ? 'active' : ''}`}>
            {useCustom ? 'Custom Mode' : 'Using Preset'}
          </span>
        </h3>

        <div className="targets-grid">
          <TargetSlider
            label="Emotional Connection"
            sublabel="Love (L)"
            value={currentTargets.L}
            onChange={(v) => handleCustomTargetChange('L', v)}
            color="#ff6b6b"
            description="How deeply it resonates emotionally"
          />
          <TargetSlider
            label="Structure & Balance"
            sublabel="Justice (J)"
            value={currentTargets.J}
            onChange={(v) => handleCustomTargetChange('J', v)}
            color="#4ecdc4"
            description="How organized and coherent it feels"
          />
          <TargetSlider
            label="Energy & Drive"
            sublabel="Power (P)"
            value={currentTargets.P}
            onChange={(v) => handleCustomTargetChange('P', v)}
            color="#ffd93d"
            description="How much it makes you move"
          />
          <TargetSlider
            label="Depth & Complexity"
            sublabel="Wisdom (W)"
            value={currentTargets.W}
            onChange={(v) => handleCustomTargetChange('W', v)}
            color="#6c5ce7"
            description="How sophisticated and layered it is"
          />
        </div>

        {useCustom && (
          <button className="reset-btn" onClick={() => setUseCustom(false)}>
            Reset to {MUSIC_GOALS[selectedGoal].name} preset
          </button>
        )}
      </div>

      {/* Results */}
      {recipe && (
        <div className="designer-results">
          {/* Recipe Card */}
          <div className="result-card recipe-card">
            <div className="card-header">
              <h3>Your Recipe</h3>
              <button className="export-btn" onClick={handleExport}>
                Export
              </button>
            </div>

            <div className="recipe-grid">
              <RecipeItem
                label="Key"
                value={recipe.key.name}
                detail={recipe.key.key === 'C#' ? 'The Love Key - highest emotional resonance' : null}
                color="#ff6b6b"
              />
              <RecipeItem
                label="Mode/Scale"
                value={recipe.mode.name}
                detail={recipe.mode.key === 'ionian' ? 'Major scale - uplifting and memorable' : null}
                color="#4ecdc4"
              />
              <RecipeItem
                label="Genre"
                value={recipe.genre.name}
                color="#ffd93d"
              />
              <RecipeItem
                label="Tempo"
                value={`${recipe.tempo.bpm} BPM`}
                detail={recipe.tempo.category}
                color="#6c5ce7"
              />
            </div>

            {/* Recommended Chords */}
            <div className="recipe-section">
              <h4>Recommended Chords</h4>
              <div className="chord-pills">
                {recipe.chords.map((chord, i) => (
                  <span key={i} className="chord-pill">
                    {chord.name}
                    <span className="chord-score">L:{chord.L?.toFixed(2)}</span>
                  </span>
                ))}
              </div>
            </div>

            {/* Recommended Intervals */}
            <div className="recipe-section">
              <h4>Melody Intervals</h4>
              <div className="interval-pills">
                {recipe.intervals.map((interval, i) => (
                  <span key={i} className="interval-pill">
                    {interval.name}
                  </span>
                ))}
              </div>
            </div>

            {/* Tips */}
            {recipe.tips.length > 0 && (
              <div className="recipe-tips">
                <h4>Tips</h4>
                <ul>
                  {recipe.tips.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Prediction Card */}
          <div className="result-card prediction-card">
            <h3>Predicted Results</h3>

            <div className="prediction-grid">
              <div className="prediction-item main">
                <span className="prediction-label">Status</span>
                <span
                  className="prediction-value phase"
                  style={{ color: recipe.metrics.phase.color }}
                >
                  {recipe.metrics.phase.emoji} {recipe.metrics.phase.name}
                </span>
              </div>

              <div className="prediction-item">
                <span className="prediction-label">Earworm Potential</span>
                <div className="earworm-meter">
                  <div
                    className="earworm-fill"
                    style={{
                      width: `${recipe.metrics.earwormPotential}%`,
                      background: recipe.metrics.earwormPotential > 70
                        ? 'linear-gradient(90deg, #2ed573, #7bed9f)'
                        : recipe.metrics.earwormPotential > 50
                          ? 'linear-gradient(90deg, #ffa502, #ffd93d)'
                          : 'linear-gradient(90deg, #ff4757, #ff6b6b)',
                    }}
                  />
                  <span className="earworm-value">{recipe.metrics.earwormPotential}%</span>
                </div>
              </div>

              <div className="prediction-item">
                <span className="prediction-label">Memorability</span>
                <span className="prediction-value">
                  {recipe.metrics.memorabilityScore.verdict}
                </span>
                <span className="prediction-detail">
                  {recipe.metrics.memorabilityScore.explanation}
                </span>
              </div>

              <div className="prediction-item">
                <span className="prediction-label">Emotional Impact</span>
                <span className="prediction-value">{recipe.metrics.V}</span>
                <span className="prediction-detail">
                  {recipe.metrics.V > 1 ? 'Highly transformative' : recipe.metrics.V > 0.7 ? 'Strong impact' : 'Subtle effect'}
                </span>
              </div>
            </div>

            {/* Radar Chart */}
            <div className="radar-section">
              <h4>Musical DNA</h4>
              <RadarChart
                L={recipe.metrics.L}
                J={recipe.metrics.J}
                P={recipe.metrics.P}
                W={recipe.metrics.W}
                size={180}
              />
              <div className="ljpw-values">
                <span style={{ color: '#ff6b6b' }}>L: {recipe.metrics.L}</span>
                <span style={{ color: '#4ecdc4' }}>J: {recipe.metrics.J}</span>
                <span style={{ color: '#ffd93d' }}>P: {recipe.metrics.P}</span>
                <span style={{ color: '#6c5ce7' }}>W: {recipe.metrics.W}</span>
              </div>
            </div>
          </div>

          {/* AI Prompt Card */}
          {aiPrompts && (
            <div className="result-card ai-prompt-card">
              <h3>
                AI Music Generator Prompts
                <HelpTooltip
                  title="AI Prompts"
                  content="Copy these prompts directly into Suno, Udio, or other AI music generators. The short version is quick, the detailed version gives more control."
                  position="left"
                >
                  <InfoIcon color="#6c5ce7" size={14} />
                </HelpTooltip>
              </h3>

              {/* Custom Instructions */}
              <div className="custom-instructions">
                <label>Add your own instructions (optional):</label>
                <input
                  type="text"
                  placeholder="e.g., 'female vocals, acoustic intro, 80s vibe'"
                  value={customInstructions}
                  onChange={(e) => setCustomInstructions(e.target.value)}
                />
              </div>

              {/* Short Prompt */}
              <div className="prompt-section">
                <div className="prompt-header">
                  <h4>Quick Prompt</h4>
                  <button
                    className="copy-btn"
                    onClick={() => copyToClipboard(aiPrompts.shortPrompt + (customInstructions ? ` ${customInstructions}` : ''))}
                  >
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                </div>
                <div className="prompt-text">
                  {aiPrompts.shortPrompt}
                  {customInstructions && <span className="custom-text"> {customInstructions}</span>}
                </div>
              </div>

              {/* Detailed Prompt */}
              <div className="prompt-section">
                <div className="prompt-header">
                  <h4>Detailed Prompt</h4>
                  <button
                    className="copy-btn"
                    onClick={() => copyToClipboard(aiPrompts.detailedPrompt + (customInstructions ? `\n\nAdditional: ${customInstructions}` : ''))}
                  >
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                </div>
                <pre className="prompt-text detailed">
                  {aiPrompts.detailedPrompt}
                  {customInstructions && <span className="custom-text">{'\n\n'}Additional: {customInstructions}</span>}
                </pre>
              </div>

              {/* Platform Tips */}
              <div className="platform-tips">
                <h4>Platform Tips</h4>
                <div className="platform-grid">
                  <div className="platform-tip">
                    <strong>Suno</strong>
                    <p>Use the quick prompt in the style/genre field. Add custom lyrics separately.</p>
                  </div>
                  <div className="platform-tip">
                    <strong>Udio</strong>
                    <p>Paste the detailed prompt. Udio handles complex instructions well.</p>
                  </div>
                  <div className="platform-tip">
                    <strong>Other AI</strong>
                    <p>Start with the quick prompt, add details as needed for your platform.</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// =============================================================================
// SUB-COMPONENTS
// =============================================================================

function TargetSlider({ label, sublabel, value, onChange, color, description }) {
  return (
    <div className="target-slider">
      <div className="slider-header">
        <span className="slider-label">{label}</span>
        <span className="slider-sublabel" style={{ color }}>{sublabel}</span>
        <span className="slider-value" style={{ color }}>{value.toFixed(2)}</span>
      </div>
      <input
        type="range"
        min="0"
        max="1"
        step="0.05"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ '--slider-color': color }}
      />
      <span className="slider-desc">{description}</span>
    </div>
  )
}

function RecipeItem({ label, value, detail, color }) {
  return (
    <div className="recipe-item">
      <span className="recipe-label">{label}</span>
      <span className="recipe-value" style={{ color }}>{value}</span>
      {detail && <span className="recipe-detail">{detail}</span>}
    </div>
  )
}

export default MusicDesigner
