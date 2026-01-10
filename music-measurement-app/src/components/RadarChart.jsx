import { useRef, useEffect } from 'react'
import './RadarChart.css'

function RadarChart({ L, J, P, W, size = 200 }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const center = size / 2
    const radius = size * 0.4

    // Clear canvas
    ctx.clearRect(0, 0, size, size)

    // Draw background circles
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
    ctx.lineWidth = 1
    for (let i = 1; i <= 4; i++) {
      ctx.beginPath()
      ctx.arc(center, center, radius * (i / 4), 0, Math.PI * 2)
      ctx.stroke()
    }

    // Draw axes
    const angles = [
      { angle: -Math.PI / 2, label: 'L', color: '#ff6b6b' },      // Top (Love)
      { angle: 0, label: 'J', color: '#4ecdc4' },                  // Right (Justice)
      { angle: Math.PI / 2, label: 'P', color: '#ffd93d' },       // Bottom (Power)
      { angle: Math.PI, label: 'W', color: '#6c5ce7' },           // Left (Wisdom)
    ]

    angles.forEach(({ angle, label, color }) => {
      const x = center + Math.cos(angle) * radius
      const y = center + Math.sin(angle) * radius

      // Draw axis line
      ctx.beginPath()
      ctx.moveTo(center, center)
      ctx.lineTo(x, y)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)'
      ctx.stroke()

      // Draw label
      const labelX = center + Math.cos(angle) * (radius + 15)
      const labelY = center + Math.sin(angle) * (radius + 15)
      ctx.fillStyle = color
      ctx.font = 'bold 14px system-ui'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(label, labelX, labelY)
    })

    // Calculate points for the data polygon
    const values = [L, J, P, W]
    const points = angles.map(({ angle }, i) => ({
      x: center + Math.cos(angle) * radius * values[i],
      y: center + Math.sin(angle) * radius * values[i],
    }))

    // Draw filled polygon
    ctx.beginPath()
    ctx.moveTo(points[0].x, points[0].y)
    points.forEach((point) => ctx.lineTo(point.x, point.y))
    ctx.closePath()

    // Create gradient fill
    const gradient = ctx.createRadialGradient(center, center, 0, center, center, radius)
    gradient.addColorStop(0, 'rgba(255, 107, 107, 0.3)')
    gradient.addColorStop(0.5, 'rgba(108, 92, 231, 0.3)')
    gradient.addColorStop(1, 'rgba(78, 205, 196, 0.3)')
    ctx.fillStyle = gradient
    ctx.fill()

    // Draw polygon outline
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)'
    ctx.lineWidth = 2
    ctx.stroke()

    // Draw data points
    points.forEach((point, i) => {
      ctx.beginPath()
      ctx.arc(point.x, point.y, 5, 0, Math.PI * 2)
      ctx.fillStyle = angles[i].color
      ctx.fill()
      ctx.strokeStyle = 'white'
      ctx.lineWidth = 2
      ctx.stroke()
    })

  }, [L, J, P, W, size])

  return (
    <div className="radar-chart">
      <canvas ref={canvasRef} width={size} height={size} />
    </div>
  )
}

export default RadarChart
