import { useState } from 'react'
import './SongBuilder.css'
import { playNote, playMelody, playChord, buildChord } from '../lib/midiSynth'
import { MODES, CHORDS } from '../lib/musicTheory'

function SongBuilder({ gameState, onComplete, onClose }) {
  const [melody, setMelody] = useState([])
  const [selectedMode, setSelectedMode] = useState('ionian')
  const [isPlaying, setIsPlaying] = useState(false)

  // Available notes based on selected mode
  const mode = MODES[selectedMode]
  const rootNote = 'C'
  const octave = 4

  const scaleNotes = mode.pattern.map(semitone => {
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    const noteIndex = semitone % 12
    const noteOctave = octave + Math.floor(semitone / 12)
    return {
      name: `${noteNames[noteIndex]}${noteOctave}`,
      display: noteNames[noteIndex],
      semitone,
    }
  })

  // Add note to melody
  const addNote = (note) => {
    if (melody.length >= 16) return // Max 16 notes

    playNote(note.name, 0.4, 'piano', 0.4)
    setMelody(prev => [...prev, { note: note.name, duration: 1 }])
  }

  // Remove last note
  const removeLastNote = () => {
    setMelody(prev => prev.slice(0, -1))
  }

  // Clear melody
  const clearMelody = () => {
    setMelody([])
  }

  // Play the melody
  const playCurrentMelody = async () => {
    if (melody.length === 0 || isPlaying) return

    setIsPlaying(true)

    // Play with chord accompaniment
    const chordNotes = buildChord(`${rootNote}${octave}`, 'major')
    if (chordNotes) {
      playChord(chordNotes, melody.length * 0.4, 'pad', 0.1)
    }

    await new Promise(resolve => setTimeout(resolve, 200))
    playMelody(melody, 150, 'piano', 0.5)

    setTimeout(() => setIsPlaying(false), melody.length * 400 + 500)
  }

  // Check if melody is "complete" enough
  const isMelodyComplete = melody.length >= 7 && melody.length <= 16

  // Handle completion
  const handleComplete = () => {
    if (!isMelodyComplete) return

    // Play the final melody with celebration
    playCurrentMelody()

    setTimeout(() => {
      onComplete()
    }, melody.length * 400 + 1000)
  }

  return (
    <div className="song-builder-modal">
      <div className="song-builder-content">
        <button className="close-btn" onClick={onClose}>x</button>

        <h2>The Silence Breaker</h2>
        <p className="builder-intro">
          Compose the final melody. Use what you've learned about intervals,
          modes, and melodic contour to create a phrase that completes
          Edmund Ashworth's masterpiece.
        </p>

        {/* Mode selector */}
        <div className="mode-selector">
          <label>Choose your mode (emotional color):</label>
          <div className="mode-buttons">
            {Object.entries(MODES).slice(0, 4).map(([key, m]) => (
              <button
                key={key}
                className={`mode-btn ${selectedMode === key ? 'selected' : ''}`}
                onClick={() => setSelectedMode(key)}
              >
                <strong>{m.name}</strong>
                <span>{m.feeling.split(',')[0]}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Scale notes to choose from */}
        <div className="note-palette">
          <label>Build your melody (click notes to add):</label>
          <div className="scale-notes">
            {scaleNotes.map((note, i) => (
              <button
                key={i}
                className="scale-note"
                onClick={() => addNote(note)}
                disabled={melody.length >= 16}
              >
                {note.display}
              </button>
            ))}
          </div>
        </div>

        {/* Current melody display */}
        <div className="melody-display">
          <label>Your melody ({melody.length}/16 notes):</label>
          <div className="melody-notes">
            {melody.length === 0 ? (
              <span className="empty-melody">Click notes above to begin composing...</span>
            ) : (
              melody.map((note, i) => (
                <span key={i} className="melody-note">
                  {note.note.replace(/[0-9]/g, '')}
                </span>
              ))
            )}
          </div>
        </div>

        {/* Controls */}
        <div className="builder-controls">
          <button onClick={removeLastNote} disabled={melody.length === 0}>
            Undo
          </button>
          <button onClick={clearMelody} disabled={melody.length === 0}>
            Clear
          </button>
          <button
            onClick={playCurrentMelody}
            disabled={melody.length === 0 || isPlaying}
            className="play-btn"
          >
            {isPlaying ? 'Playing...' : 'Play Melody'}
          </button>
        </div>

        {/* Completion */}
        <div className="completion-section">
          {isMelodyComplete ? (
            <>
              <p className="ready-message">
                Your melody is ready. When you play it, the silence will break forever.
              </p>
              <button
                className="complete-btn"
                onClick={handleComplete}
                disabled={isPlaying}
              >
                Break the Silence
              </button>
            </>
          ) : (
            <p className="progress-message">
              {melody.length < 7
                ? `Add ${7 - melody.length} more notes to complete your melody.`
                : 'Your melody is ready!'}
            </p>
          )}
        </div>

        {/* Tips */}
        <div className="builder-tips">
          <h4>Composition Tips:</h4>
          <ul>
            <li>Start and end on the same note (C) for resolution</li>
            <li>Mix stepwise motion with occasional leaps</li>
            <li>Build to a high point, then descend</li>
            <li>Repetition helps memorability</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default SongBuilder
