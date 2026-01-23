/**
 * LJPW Music Designer Engine - V8.5
 *
 * Helps users design music by goal and generates recipes + AI prompts.
 * Uses the Generative Equation to predict impact and memorability.
 *
 * User-Friendly Terminology:
 * - "Autopoietic" -> "Unforgettable"
 * - "Life Inequality" -> "Memorability Test"
 * - "Semantic Voltage" -> "Emotional Impact"
 * - "Iterations" -> "Listens"
 * - "Distance" -> "Cultural Gap"
 */

import { PHI, PHI_INV, KEYS, MODES, GENRES, INTERVALS, CHORDS } from './ljpwConstants'

// =============================================================================
// MUSIC GOALS - User-friendly presets
// =============================================================================

export const MUSIC_GOALS = {
  earworm: {
    id: 'earworm',
    name: 'Catchy Earworm',
    emoji: '🎵',
    description: 'A song that gets stuck in your head',
    targets: { L: 0.85, J: 0.75, P: 0.70, W: 0.65 },
    tips: ['Focus on a singable hook', 'Clear verse-chorus structure', 'Moderate tempo works best'],
  },
  epic: {
    id: 'epic',
    name: 'Epic Anthem',
    emoji: '🏆',
    description: 'Powerful, uplifting, stadium-ready',
    targets: { L: 0.80, J: 0.85, P: 0.90, W: 0.70 },
    tips: ['Build to big choruses', 'Use power chords', 'Strong rhythmic drive'],
  },
  emotional: {
    id: 'emotional',
    name: 'Emotional Ballad',
    emoji: '💔',
    description: 'Deep feelings, tears and catharsis',
    targets: { L: 0.92, J: 0.70, P: 0.45, W: 0.75 },
    tips: ['Slow tempo', 'Minor mode adds depth', 'Leave space for emotion'],
  },
  chill: {
    id: 'chill',
    name: 'Chill Vibes',
    emoji: '🌊',
    description: 'Relaxing, ambient, background-friendly',
    targets: { L: 0.65, J: 0.70, P: 0.40, W: 0.80 },
    tips: ['Low tempo', 'Subtle textures', 'Avoid strong beats'],
  },
  party: {
    id: 'party',
    name: 'Party Starter',
    emoji: '🎉',
    description: 'Gets people moving and dancing',
    targets: { L: 0.75, J: 0.80, P: 0.92, W: 0.55 },
    tips: ['High tempo (120-130 BPM)', 'Strong four-on-floor beat', 'Catchy drops'],
  },
  focus: {
    id: 'focus',
    name: 'Focus Flow',
    emoji: '🧠',
    description: 'Helps concentration and productivity',
    targets: { L: 0.55, J: 0.85, P: 0.35, W: 0.90 },
    tips: ['No lyrics', 'Steady tempo', 'Minimal dynamic changes'],
  },
  workout: {
    id: 'workout',
    name: 'Workout Fuel',
    emoji: '💪',
    description: 'High energy for exercise',
    targets: { L: 0.70, J: 0.75, P: 0.95, W: 0.50 },
    tips: ['Fast tempo (140+ BPM)', 'Driving beat', 'Motivational feel'],
  },
  cinematic: {
    id: 'cinematic',
    name: 'Cinematic Score',
    emoji: '🎬',
    description: 'Epic, emotional, storytelling',
    targets: { L: 0.85, J: 0.80, P: 0.75, W: 0.90 },
    tips: ['Dynamic contrast', 'Build and release', 'Orchestral elements'],
  },
}

// =============================================================================
// RECIPE GENERATOR - Recommends musical elements based on targets
// =============================================================================

/**
 * Generate a complete music recipe based on target LJPW values
 */
export function generateRecipe(targets) {
  const { L, J, P, W } = targets

  // Find best matching key
  const recommendedKey = findBestMatch(KEYS, targets, 0.3)

  // Find best matching mode
  const recommendedMode = findBestMatch(MODES, targets, 0.25)

  // Find best matching genre
  const recommendedGenre = findBestMatch(GENRES, targets, 0.2)

  // Calculate recommended tempo based on Power
  const recommendedTempo = calculateTempo(P)

  // Find recommended chords
  const recommendedChords = findTopMatches(CHORDS, targets, 4)

  // Find recommended intervals for melody
  const recommendedIntervals = findTopMatches(INTERVALS, targets, 4)

  // Calculate predicted metrics
  const H = calculateHarmonyIndex(L, J, P, W)
  const V = PHI * H * L
  const phase = determinePhase(H, L)

  // Calculate earworm potential
  const earwormPotential = Math.round(calculateEarwormPotential(L, H, P) * 100)

  // Calculate memorability (L^n > phi^d test)
  const memorabilityScore = calculateMemorability(L, 10, 3)

  return {
    key: recommendedKey,
    mode: recommendedMode,
    genre: recommendedGenre,
    tempo: recommendedTempo,
    chords: recommendedChords,
    intervals: recommendedIntervals,
    metrics: {
      L, J, P, W,
      H: Math.round(H * 100) / 100,
      V: Math.round(V * 100) / 100,
      phase,
      earwormPotential,
      memorabilityScore,
    },
    tips: generateTips(targets, phase),
  }
}

/**
 * Find the element that best matches target LJPW values
 */
function findBestMatch(elements, targets, tolerance = 0.2) {
  let bestMatch = null
  let bestScore = -Infinity

  for (const [key, element] of Object.entries(elements)) {
    const score = calculateMatchScore(element, targets)
    if (score > bestScore) {
      bestScore = score
      bestMatch = { key, ...element }
    }
  }

  return bestMatch
}

/**
 * Find top N matching elements
 */
function findTopMatches(elements, targets, n = 3) {
  const scores = Object.entries(elements).map(([key, element]) => ({
    key,
    ...element,
    score: calculateMatchScore(element, targets),
  }))

  return scores
    .sort((a, b) => b.score - a.score)
    .slice(0, n)
}

/**
 * Calculate how well an element matches target values
 */
function calculateMatchScore(element, targets) {
  const { L: tL, J: tJ, P: tP, W: tW } = targets
  const { L = 0.5, J = 0.5, P = 0.5, W = 0.5 } = element

  // Weight Love more heavily (it's the most important for memorability)
  const loveWeight = 2.0
  const justiceWeight = 1.0
  const powerWeight = 1.0
  const wisdomWeight = 1.0

  const lDiff = Math.abs(L - tL) * loveWeight
  const jDiff = Math.abs(J - tJ) * justiceWeight
  const pDiff = Math.abs(P - tP) * powerWeight
  const wDiff = Math.abs(W - tW) * wisdomWeight

  // Score is inverse of total difference
  return 1 / (1 + lDiff + jDiff + pDiff + wDiff)
}

/**
 * Calculate recommended tempo based on Power value
 */
function calculateTempo(power) {
  // Map power to tempo range (40-200 BPM)
  const minTempo = 50
  const maxTempo = 180
  const tempo = Math.round(minTempo + power * (maxTempo - minTempo))

  // Categorize
  let category
  if (tempo < 60) category = 'Largo (very slow)'
  else if (tempo < 80) category = 'Adagio (slow)'
  else if (tempo < 100) category = 'Andante (walking)'
  else if (tempo < 120) category = 'Moderato (moderate)'
  else if (tempo < 140) category = 'Allegro (fast)'
  else if (tempo < 170) category = 'Vivace (lively)'
  else category = 'Presto (very fast)'

  return { bpm: tempo, category }
}

/**
 * Calculate Harmony Index
 */
function calculateHarmonyIndex(L, J, P, W) {
  const distance = Math.sqrt(
    Math.pow(1 - L, 2) +
    Math.pow(1 - J, 2) +
    Math.pow(1 - P, 2) +
    Math.pow(1 - W, 2)
  )
  return 1 / (1 + distance)
}

/**
 * Determine phase classification with user-friendly names
 */
function determinePhase(H, L) {
  if (H >= 0.6 && L >= 0.7) {
    return { name: 'Unforgettable', color: '#2ed573', emoji: '✨' }
  } else if (H >= 0.5) {
    return { name: 'Background Music', color: '#ffa502', emoji: '⚖️' }
  } else {
    return { name: 'Forgettable', color: '#ff4757', emoji: '🌀' }
  }
}

/**
 * Calculate earworm potential
 */
function calculateEarwormPotential(L, H, P) {
  if (L < 0.7 || H < 0.6) return 0.3 * L * H

  // Optimal power is around 0.7
  const powerFactor = 1 - Math.abs(P - 0.7)
  return Math.min(1, L * H * (1 + powerFactor * 0.3))
}

/**
 * Calculate memorability score (simplified Life Inequality)
 */
function calculateMemorability(L, listens, culturalGap) {
  const growth = Math.pow(L, listens)
  const decay = Math.pow(PHI, culturalGap)
  const ratio = growth / decay

  return {
    ratio: Math.round(ratio * 100) / 100,
    verdict: ratio > 1.1 ? 'Highly Memorable' : ratio > 0.9 ? 'Moderately Memorable' : 'May Be Forgotten',
    explanation: ratio > 1.1
      ? 'Emotional connection grows faster than forgetting'
      : ratio > 0.9
        ? 'Connection and forgetting roughly balanced'
        : 'Risk of fading from memory over time',
  }
}

/**
 * Generate helpful tips based on analysis
 */
function generateTips(targets, phase) {
  const tips = []
  const { L, J, P, W } = targets

  if (L < 0.7) {
    tips.push('Boost emotional connection: use major 3rds, singable melodies')
  }
  if (phase.name !== 'Unforgettable') {
    tips.push('To make it unforgettable: aim for Love ≥ 0.7 and Harmony ≥ 0.6')
  }
  if (P > 0.85 && L < 0.75) {
    tips.push('High energy but may lack stickiness - add melodic hooks')
  }
  if (W > 0.85 && L < 0.7) {
    tips.push('Sophisticated but may not be catchy - simplify for wider appeal')
  }
  if (J < 0.6) {
    tips.push('Add more structure: clear verse-chorus, balanced phrases')
  }

  return tips
}

// =============================================================================
// AI PROMPT GENERATOR
// =============================================================================

/**
 * Generate a prompt for AI music generators like Suno
 */
export function generateAIPrompt(recipe, goalId, customInstructions = '') {
  const goal = MUSIC_GOALS[goalId] || MUSIC_GOALS.earworm

  // Build the prompt
  const parts = []

  // Genre and style
  parts.push(`${recipe.genre.name} song`)

  // Key and mode
  parts.push(`in ${recipe.key.name} ${recipe.mode.name.toLowerCase()}`)

  // Tempo and feel
  parts.push(`at ${recipe.tempo.bpm} BPM (${recipe.tempo.category})`)

  // Mood based on goal
  const moodMap = {
    earworm: 'catchy, memorable, hook-driven',
    epic: 'powerful, uplifting, anthemic',
    emotional: 'emotional, heartfelt, moving',
    chill: 'relaxed, atmospheric, smooth',
    party: 'energetic, danceable, fun',
    focus: 'ambient, flowing, non-distracting',
    workout: 'intense, driving, motivating',
    cinematic: 'epic, dramatic, sweeping',
  }
  parts.push(`mood: ${moodMap[goalId] || 'memorable'}`)

  // Chord suggestions
  const chordNames = recipe.chords.slice(0, 3).map(c => c.name).join(', ')
  parts.push(`suggested chords: ${chordNames}`)

  // Additional characteristics
  const characteristics = []
  if (recipe.metrics.L > 0.8) characteristics.push('strong melodic hooks')
  if (recipe.metrics.P > 0.8) characteristics.push('driving rhythm')
  if (recipe.metrics.W > 0.8) characteristics.push('sophisticated harmonies')
  if (recipe.metrics.J > 0.8) characteristics.push('clear structure')

  if (characteristics.length > 0) {
    parts.push(`featuring: ${characteristics.join(', ')}`)
  }

  // Custom instructions
  if (customInstructions) {
    parts.push(customInstructions)
  }

  return parts.join('. ') + '.'
}

/**
 * Generate a detailed prompt with more structure
 */
export function generateDetailedAIPrompt(recipe, goalId, options = {}) {
  const goal = MUSIC_GOALS[goalId] || MUSIC_GOALS.earworm
  const { includeInstruments = true, includeLyricStyle = false, includeStructure = true } = options

  const prompt = {
    style: `${recipe.genre.name}`,
    key: `${recipe.key.name} ${recipe.mode.name}`,
    tempo: `${recipe.tempo.bpm} BPM`,
    mood: getMoodDescription(goalId, recipe.metrics),
    energy: getEnergyLevel(recipe.metrics.P),
  }

  if (includeInstruments) {
    prompt.instruments = getInstrumentSuggestions(recipe.genre.key, recipe.metrics)
  }

  if (includeStructure) {
    prompt.structure = getStructureSuggestion(goalId, recipe.metrics)
  }

  if (includeLyricStyle) {
    prompt.lyricStyle = getLyricStyleSuggestion(goalId, recipe.metrics)
  }

  // Build natural language prompt
  let text = `Create a ${prompt.mood} ${prompt.style} song in ${prompt.key} at ${prompt.tempo}.`
  text += ` Energy level: ${prompt.energy}.`

  if (prompt.instruments) {
    text += ` Instruments: ${prompt.instruments}.`
  }

  if (prompt.structure) {
    text += ` Structure: ${prompt.structure}.`
  }

  if (prompt.lyricStyle) {
    text += ` Lyrics: ${prompt.lyricStyle}.`
  }

  // Add LJPW guidance comment
  text += `\n\n[LJPW Targets: L=${recipe.metrics.L}, J=${recipe.metrics.J}, P=${recipe.metrics.P}, W=${recipe.metrics.W}]`
  text += `\n[Predicted: ${recipe.metrics.phase.name}, Earworm Potential: ${recipe.metrics.earwormPotential}%]`

  return {
    shortPrompt: generateAIPrompt(recipe, goalId),
    detailedPrompt: text,
    metadata: prompt,
  }
}

function getMoodDescription(goalId, metrics) {
  const moods = {
    earworm: 'catchy and memorable with instant hooks',
    epic: 'powerful and triumphant with soaring moments',
    emotional: 'deeply moving and heartfelt',
    chill: 'relaxed and atmospheric',
    party: 'high-energy and danceable',
    focus: 'ambient and flowing',
    workout: 'intense and motivating',
    cinematic: 'epic and dramatic with emotional depth',
  }
  return moods[goalId] || 'memorable and engaging'
}

function getEnergyLevel(power) {
  if (power < 0.3) return 'very low, calm'
  if (power < 0.5) return 'low, relaxed'
  if (power < 0.7) return 'moderate'
  if (power < 0.85) return 'high, energetic'
  return 'very high, intense'
}

function getInstrumentSuggestions(genreKey, metrics) {
  const baseInstruments = {
    pop: 'synths, piano, acoustic guitar, drums',
    rock: 'electric guitar, bass, drums, maybe piano',
    electronic: 'synthesizers, drum machines, bass',
    classical: 'orchestra, strings, piano',
    jazz: 'piano, bass, drums, saxophone',
    gospel: 'piano, organ, choir, bass',
    ambient: 'pads, textures, subtle percussion',
    hiphop: '808s, hi-hats, synths, bass',
    folk: 'acoustic guitar, violin, piano',
  }

  let instruments = baseInstruments[genreKey] || 'piano, guitar, bass, drums'

  // Modify based on metrics
  if (metrics.W > 0.8) instruments += ', strings for depth'
  if (metrics.P > 0.85) instruments += ', heavy drums'
  if (metrics.L > 0.85) instruments += ', warm pads'

  return instruments
}

function getStructureSuggestion(goalId, metrics) {
  if (goalId === 'earworm' || metrics.J > 0.75) {
    return 'Intro - Verse - Chorus - Verse - Chorus - Bridge - Chorus (classic pop structure)'
  }
  if (goalId === 'cinematic') {
    return 'Build from quiet to epic climax, then resolve'
  }
  if (goalId === 'chill' || goalId === 'focus') {
    return 'Flowing, gradual evolution without stark sections'
  }
  if (goalId === 'party') {
    return 'Build - Drop - Build - Drop with clear energy peaks'
  }
  return 'Verse - Chorus - Verse - Chorus - Bridge - Chorus'
}

function getLyricStyleSuggestion(goalId, metrics) {
  const styles = {
    earworm: 'Simple, relatable, with a catchy repeated hook',
    epic: 'Uplifting, universal themes of triumph and perseverance',
    emotional: 'Personal, vulnerable, specific emotional details',
    chill: 'Minimal, evocative imagery, or instrumental',
    party: 'Fun, carefree, celebratory',
    focus: 'Instrumental preferred, or very minimal vocals',
    workout: 'Motivational, empowering, action-oriented',
    cinematic: 'Narrative, epic themes, emotional journey',
  }
  return styles[goalId] || 'Memorable, singable'
}

// =============================================================================
// EXPORTS
// =============================================================================

export default {
  MUSIC_GOALS,
  generateRecipe,
  generateAIPrompt,
  generateDetailedAIPrompt,
}
