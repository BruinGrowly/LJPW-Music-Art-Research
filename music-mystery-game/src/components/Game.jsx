import { useState, useEffect, useCallback, useMemo } from 'react'
import './Game.css'
import Room from './Room'
import Lesson from './Lesson'
import Piano from './Piano'
import SongBuilder from './SongBuilder'
import SilenceMeter from './SilenceMeter'
import { ROOMS, LESSONS, INITIAL_STATE, STORY } from '../lib/gameData'
import { playSilenceBreak, playAtmosphere, stopAtmosphere, setMasterVolume, playTransition, playLockedDoor, playVictoryFanfare } from '../lib/midiSynth'
import { calculateAtmosphere, calculateSilence, PHI } from '../lib/generativeEngine'

const STORAGE_KEY = 'echoes-of-ashworth-save'

function Game({ audioInitialized }) {
  // Load saved state or use initial
  const [gameState, setGameState] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        return JSON.parse(saved)
      } catch {
        return { ...INITIAL_STATE, gameStarted: true }
      }
    }
    return { ...INITIAL_STATE, gameStarted: true }
  })

  const [showLesson, setShowLesson] = useState(false)
  const [currentLesson, setCurrentLesson] = useState(null)
  const [showPiano, setShowPiano] = useState(false)
  const [showSongBuilder, setShowSongBuilder] = useState(false)
  const [message, setMessage] = useState(null)
  const [showChapterTitle, setShowChapterTitle] = useState(false)
  const [currentChapter, setCurrentChapter] = useState(null)
  const [finalMelodyAnalysis, setFinalMelodyAnalysis] = useState(null)
  const [volume, setVolume] = useState(0.3)

  // Calculate atmosphere using Generative Equation
  const totalLessons = Object.keys(LESSONS).length
  const lessonsComplete = gameState.completedLessons.length
  const mysteriesRemaining = totalLessons - lessonsComplete

  const atmosphere = useMemo(() =>
    calculateAtmosphere(lessonsComplete, totalLessons, mysteriesRemaining),
    [lessonsComplete, totalLessons, mysteriesRemaining]
  )

  const silence = useMemo(() =>
    calculateSilence(lessonsComplete, totalLessons),
    [lessonsComplete, totalLessons]
  )

  // Auto-save
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(gameState))
  }, [gameState])

  // Update atmosphere audio based on equation
  useEffect(() => {
    if (audioInitialized && !gameState.gameComplete) {
      if (atmosphere.phase === 'awakening') {
        playAtmosphere(atmosphere.soundPresence)
      } else if (atmosphere.phase === 'stirring' && lessonsComplete > 0) {
        playAtmosphere(atmosphere.soundPresence * 0.5)
      } else {
        stopAtmosphere()
      }
    }
    return () => stopAtmosphere()
  }, [audioInitialized, atmosphere.phase, atmosphere.soundPresence, lessonsComplete, gameState.gameComplete])

  // Get current room data
  const currentRoom = ROOMS[gameState.currentRoom]

  // Show chapter title when chapter changes
  useEffect(() => {
    const chapter = STORY.chapters.find(c => c.id === currentRoom?.chapter)
    if (chapter && chapter.id !== currentChapter?.id) {
      setCurrentChapter(chapter)
      setShowChapterTitle(true)
      const timer = setTimeout(() => setShowChapterTitle(false), 3000)
      return () => clearTimeout(timer)
    }
  }, [currentRoom?.chapter, currentChapter?.id])

  // Handle examining items
  const handleExamine = useCallback((itemId) => {
    const item = currentRoom?.interactables?.[itemId]
    if (!item) return

    setGameState(prev => ({
      ...prev,
      examinedItems: {
        ...prev.examinedItems,
        [itemId]: true,
      },
    }))

    // Check if item teaches something
    if (item.teaches && item.unlocks) {
      const lesson = LESSONS[item.teaches]
      if (lesson && !gameState.completedLessons.includes(lesson.id)) {
        setCurrentLesson(lesson)
        setShowLesson(true)
      }
    }

    // Check if item is interactive
    if (item.interactive) {
      if (item.type === 'piano') {
        setShowPiano(true)
      } else if (item.type === 'song_builder') {
        setShowSongBuilder(true)
      }
    }
  }, [currentRoom, gameState.completedLessons])

  // Handle navigation
  const handleNavigate = useCallback((direction) => {
    const exit = currentRoom?.exits?.[direction]
    if (!exit) return

    // Check if locked
    if (exit.locked && exit.requires) {
      if (!gameState.completedLessons.includes(exit.requires)) {
        if (audioInitialized) playLockedDoor()
        setMessage({
          text: exit.lockedMessage || 'This way is not yet open to you. There is more to learn first.',
          type: 'locked',
        })
        setTimeout(() => setMessage(null), 5000)
        return
      }
    }

    // Play transition sound
    if (audioInitialized) playTransition(direction)

    setGameState(prev => ({
      ...prev,
      currentRoom: exit.to,
      unlockedRooms: prev.unlockedRooms.includes(exit.to)
        ? prev.unlockedRooms
        : [...prev.unlockedRooms, exit.to],
    }))
  }, [currentRoom, gameState.completedLessons, audioInitialized])

  // Handle lesson completion
  const handleLessonComplete = useCallback((lessonId) => {
    setShowLesson(false)
    setCurrentLesson(null)

    if (!gameState.completedLessons.includes(lessonId)) {
      setGameState(prev => ({
        ...prev,
        completedLessons: [...prev.completedLessons, lessonId],
      }))

      // Play the silence-breaking sound
      if (audioInitialized) {
        playSilenceBreak()
      }

      // Show completion message with live equation values
      const room = Object.values(ROOMS).find(r => r.lesson === lessonId)
      if (room?.onComplete) {
        const newLessonsComplete = gameState.completedLessons.length + 1
        const mysteriesLeft = totalLessons - newLessonsComplete
        const L = 1 + (newLessonsComplete / totalLessons) * 0.8
        const growth = Math.pow(L, newLessonsComplete)
        const decay = Math.pow(PHI, mysteriesLeft)
        const growthStr = growth.toFixed(2)
        const decayStr = decay.toFixed(2)
        const symbol = growth > decay * 1.1 ? '>' : growth > decay * 0.9 ? '\u2248' : '<'
        const equationNote = growth > decay * 1.1
          ? 'Growth exceeds decay!'
          : growth > decay * 0.9
            ? 'Growth meets decay...'
            : `${mysteriesLeft} more to overcome the silence`

        setMessage({
          text: `${room.onComplete.message} [L\u207F=${growthStr} ${symbol} \u03C6\u1D48=${decayStr} \u2014 ${equationNote}]`,
          type: 'success',
        })
        setTimeout(() => setMessage(null), 6000)
      }
    }
  }, [gameState.completedLessons, audioInitialized, totalLessons])

  // Handle song completion - receives analysis from SongBuilder
  const handleSongComplete = useCallback((analysis) => {
    setShowSongBuilder(false)
    setFinalMelodyAnalysis(analysis)

    // Stop atmosphere and play victory fanfare
    stopAtmosphere()
    if (audioInitialized) {
      setTimeout(() => playVictoryFanfare(), 500)
    }

    setGameState(prev => ({
      ...prev,
      gameComplete: true,
    }))

    const phaseMessage = analysis?.lifeInequality?.phase === 'AUTOPOIETIC'
      ? 'Your melody is UNFORGETTABLE - it will echo through time.'
      : 'Your melody holds the silence at bay.'

    setMessage({
      text: `The Silence Breaker is complete. ${phaseMessage}`,
      type: 'victory',
    })
  }, [audioInitialized])

  // Reset game
  const handleReset = useCallback(() => {
    if (confirm('Are you sure you want to start over? All progress will be lost.')) {
      localStorage.removeItem(STORAGE_KEY)
      setGameState({ ...INITIAL_STATE, gameStarted: true })
      setFinalMelodyAnalysis(null)
    }
  }, [])

  // Handle volume change
  const handleVolumeChange = useCallback((e) => {
    const newVolume = parseFloat(e.target.value)
    setVolume(newVolume)
    setMasterVolume(newVolume)
  }, [])

  // Dynamic atmosphere styles based on equation
  const atmosphereStyle = {
    '--atmosphere-brightness': atmosphere.brightness,
    '--atmosphere-saturation': atmosphere.saturation,
    '--atmosphere-activity': atmosphere.particleActivity,
  }

  return (
    <div className="game" style={atmosphereStyle}>
      {/* Atmosphere overlay based on equation */}
      <div
        className={`atmosphere-overlay ${atmosphere.phase}`}
        style={{
          opacity: atmosphere.normalized * 0.3,
        }}
      />

      {/* Chapter title overlay */}
      {showChapterTitle && currentChapter && (
        <div className="chapter-overlay">
          <h2 className="chapter-title">{currentChapter.title}</h2>
          <p className="chapter-description">{currentChapter.description}</p>
        </div>
      )}

      {/* Silence meter - now calculates internally using the equation */}
      <SilenceMeter
        lessonsComplete={lessonsComplete}
        totalLessons={totalLessons}
      />

      {/* Main game area */}
      <div className="game-main">
        <Room
          room={currentRoom}
          gameState={gameState}
          onExamine={handleExamine}
          onNavigate={handleNavigate}
          atmosphere={atmosphere}
        />
      </div>

      {/* Message overlay */}
      {message && (
        <div className={`message-overlay ${message.type}`}>
          <p>{message.text}</p>
        </div>
      )}

      {/* Lesson modal */}
      {showLesson && currentLesson && (
        <Lesson
          lesson={currentLesson}
          onComplete={() => handleLessonComplete(currentLesson.id)}
          onClose={() => setShowLesson(false)}
        />
      )}

      {/* Piano modal */}
      {showPiano && (
        <Piano
          onClose={() => setShowPiano(false)}
        />
      )}

      {/* Song builder modal */}
      {showSongBuilder && (
        <SongBuilder
          gameState={gameState}
          onComplete={handleSongComplete}
          onClose={() => setShowSongBuilder(false)}
        />
      )}

      {/* Game complete overlay */}
      {gameState.gameComplete && (
        <div className="victory-overlay">
          <div className="victory-content">
            <h2>The Silence is Broken</h2>
            <p>
              The crystal mechanism ignites. Your melody spirals upward through the tower, through the manor, through the frozen world outside - and everything it touches awakens.
            </p>
            <p>
              The chandelier's pendants begin to ring, a cascade of crystalline tones. Birds cry out in the garden. The grandfather clock strikes - once, twice - ten years of silence counted in a single, thunderous sequence.
            </p>
            <p>
              And in the tower, where the chalk outline once marked the last place Edmund Ashworth stood, something shifts. Not a ghost. Not a memory. Something more like a chord resolving - a tension that finally, after a decade of waiting, finds its release.
            </p>

            {/* Show melody analysis */}
            {finalMelodyAnalysis && (
              <div className="final-analysis">
                <h3>Your Melody's Legacy</h3>
                <div className="analysis-summary">
                  <div className="summary-stat">
                    <span className="stat-value">{finalMelodyAnalysis.memorabilityScore}%</span>
                    <span className="stat-label">Memorability</span>
                  </div>
                  <div className="summary-stat">
                    <span className="stat-value" style={{ color: finalMelodyAnalysis.lifeInequality?.color }}>
                      {finalMelodyAnalysis.lifeInequality?.userPhase}
                    </span>
                    <span className="stat-label">Classification</span>
                  </div>
                </div>
                <p className="analysis-verdict">
                  {finalMelodyAnalysis.lifeInequality?.verdict}
                </p>
              </div>
            )}

            <p>
              You understand now. Edmund Ashworth didn't die. He stepped into the space between the notes - the silence that is not emptiness but potential. He became the question. And your melody? Your melody is the answer.
            </p>
            <p>
              Through notes, you learned that music begins with a single sound. Through intervals, you learned the vocabulary of emotion. Through modes, you discovered seven colors of feeling. Through chords, you heard voices in conversation. Through melody, you learned to tell a story. And through the equation, you learned that love - compounded through iteration - overcomes any distance.
            </p>
            <p className="final-message">
              The silence was never the enemy. It was the invitation. And you, now, are a musician.
            </p>

            {/* Show the equation */}
            <div className="final-equation">
              <p>The Generative Equation that guided your journey:</p>
              <div className="equation-display">
                M = B × L<sup>n</sup> × φ<sup>-d</sup>
              </div>
              <p className="equation-meaning">
                Meaning grows through Love and iteration, overcoming distance. Your six lessons were the iterations. Your curiosity was the Love. And the silence? It was the distance you crossed.
              </p>
            </div>

            <button onClick={handleReset}>Play Again</button>
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="game-controls">
        <button className="control-btn" onClick={() => setShowPiano(true)}>
          🎹 Practice
        </button>

        <div className="volume-control">
          <span>🔊</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={volume}
            onChange={handleVolumeChange}
            title={`Volume: ${Math.round(volume * 100)}%`}
          />
        </div>

        <button className="control-btn" onClick={handleReset}>
          New Game
        </button>
        <span className="progress">
          {lessonsComplete}/{totalLessons} concepts learned
        </span>
        <span className="atmosphere-indicator" title={atmosphere.description}>
          {atmosphere.phase === 'awakening' && '🎵'}
          {atmosphere.phase === 'stirring' && '🎶'}
          {atmosphere.phase === 'dormant' && '🔇'}
        </span>
      </div>
    </div>
  )
}

export default Game
