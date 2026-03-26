import { useEffect } from 'react'

interface StreakModalProps {
  streakName: string
  streakCount: number
  onClose: () => void
}

export default function StreakModal({ streakName, streakCount, onClose }: StreakModalProps) {
  useEffect(() => {
    const timer = setTimeout(onClose, 8000)
    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0,0,0,0.85)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        backdropFilter: 'blur(8px)',
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          background: 'linear-gradient(135deg, #1a0000 0%, #0a0a0a 50%, #1a0000 100%)',
          border: '2px solid var(--red)',
          borderRadius: '16px',
          padding: '60px 70px',
          textAlign: 'center',
          maxWidth: '600px',
          width: '90%',
          animation: 'scaleIn 0.4s ease forwards',
          boxShadow: '0 0 60px rgba(204,0,0,0.5), 0 0 120px rgba(204,0,0,0.2)',
        }}
      >
        <div style={{
          fontSize: 'clamp(60px, 10vw, 100px)',
          lineHeight: 1,
          animation: 'fireFlicker 0.8s ease-in-out infinite',
          marginBottom: '20px',
        }}>
          🔥
        </div>

        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(16px, 3vw, 22px)',
          letterSpacing: '8px',
          color: 'var(--red)',
          marginBottom: '16px',
          textTransform: 'uppercase',
        }}>
          ¡LOGRO DESBLOQUEADO!
        </div>

        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(50px, 9vw, 90px)',
          lineHeight: 1,
          color: 'var(--white)',
          letterSpacing: '4px',
          animation: 'streakNumber 0.6s ease forwards',
          marginBottom: '8px',
        }}>
          {streakCount} DÍAS
        </div>

        <div style={{
          fontFamily: 'var(--font-heading)',
          fontSize: 'clamp(20px, 3.5vw, 32px)',
          color: 'var(--red-bright)',
          fontWeight: 700,
          letterSpacing: '3px',
          marginBottom: '30px',
          textTransform: 'uppercase',
        }}>
          {streakName}
        </div>

        <div
          style={{
            width: '80px',
            height: '3px',
            background: 'var(--red)',
            margin: '0 auto 30px',
          }}
        />

        <p style={{
          fontFamily: 'var(--font-body)',
          fontSize: 'clamp(14px, 2vw, 18px)',
          color: 'var(--white-dim)',
          lineHeight: 1.6,
          letterSpacing: '1px',
        }}>
          Habla con tu <strong style={{ color: 'var(--white)' }}>Head Coach</strong> para<br />
          recibir tu reconocimiento
        </p>

        {/* Progress bar countdown */}
        <div style={{
          marginTop: '40px',
          height: '3px',
          background: 'var(--black-border)',
          borderRadius: '2px',
          overflow: 'hidden',
        }}>
          <div style={{
            height: '100%',
            background: 'var(--red)',
            animation: 'timerCountdown 8s linear forwards',
          }} />
        </div>
      </div>
    </div>
  )
}
