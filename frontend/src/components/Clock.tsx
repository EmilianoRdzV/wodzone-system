import { useState, useEffect } from 'react'

const DAYS = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
const MONTHS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

export default function Clock() {
  const [now, setNow] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  const seconds = now.getSeconds().toString().padStart(2, '0')
  const dayName = DAYS[now.getDay()]
  const day = now.getDate()
  const month = MONTHS[now.getMonth()]
  const year = now.getFullYear()

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '8px',
    }}>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: 'clamp(80px, 14vw, 180px)',
        lineHeight: 1,
        letterSpacing: '6px',
        color: 'var(--white)',
        textShadow: '0 0 40px rgba(255,255,255,0.1)',
      }}>
        {hours}<span style={{ color: 'var(--red)', animation: 'pulse 1s step-start infinite' }}>:</span>{minutes}
        <span style={{ fontSize: '0.45em', color: 'var(--white-faint)', marginLeft: '12px' }}>{seconds}</span>
      </div>
      <div style={{
        fontFamily: 'var(--font-heading)',
        fontSize: 'clamp(14px, 2vw, 22px)',
        letterSpacing: '6px',
        color: 'var(--white-dim)',
        textTransform: 'uppercase',
        fontWeight: 400,
      }}>
        {dayName} {day} {month} {year}
      </div>
    </div>
  )
}
