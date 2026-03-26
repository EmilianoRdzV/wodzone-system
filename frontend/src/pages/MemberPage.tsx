import { useEffect, useState, useCallback } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import { getMemberInfo } from '../api/checkin'
import type { CheckInResponse } from '../types'
import StreakModal from '../components/StreakModal'

const AUTO_REDIRECT_SECONDS = 12

export default function MemberPage() {
  const { qr } = useParams<{ qr: string }>()
  const location = useLocation()
  const navigate = useNavigate()

  const [member, setMember] = useState<CheckInResponse | null>(
    location.state as CheckInResponse | null
  )
  const [loading, setLoading] = useState(!location.state)
  const [showStreak, setShowStreak] = useState(false)
  const [countdown, setCountdown] = useState(AUTO_REDIRECT_SECONDS)
  const [visible, setVisible] = useState(false)

  const goHome = useCallback(() => {
    navigate('/', { replace: true })
  }, [navigate])

  // Fetch member info if not passed via router state
  useEffect(() => {
    if (!location.state && qr) {
      getMemberInfo(qr)
        .then(data => { setMember(data); setLoading(false) })
        .catch(() => { setLoading(false) })
    }
  }, [qr, location.state])

  // Show streak modal after brief delay
  useEffect(() => {
    if (member?.streakName && member.streakName !== 'No cumple con ninguna racha') {
      const t = setTimeout(() => setShowStreak(true), 1500)
      return () => clearTimeout(t)
    }
  }, [member])

  // Fade in
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 50)
    return () => clearTimeout(t)
  }, [])

  // Auto-redirect countdown
  useEffect(() => {
    const interval = setInterval(() => {
      setCountdown(c => {
        if (c <= 1) { goHome(); return 0 }
        return c - 1
      })
    }, 1000)
    return () => clearInterval(interval)
  }, [goHome])

  if (loading) {
    return (
      <div style={{
        width: '100vw', height: '100vh',
        background: 'var(--black)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: '48px',
          letterSpacing: '8px',
          color: 'var(--red)',
          animation: 'pulse 0.8s ease infinite',
        }}>
          CARGANDO...
        </div>
      </div>
    )
  }

  if (!member) {
    return (
      <div style={{
        width: '100vw', height: '100vh',
        background: 'var(--black)',
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: '24px',
      }}>
        <div style={{ fontFamily: 'var(--font-display)', fontSize: '60px', color: '#ff4444', letterSpacing: '4px' }}>
          MIEMBRO NO ENCONTRADO
        </div>
        <button
          onClick={goHome}
          style={{
            fontFamily: 'var(--font-heading)', fontSize: '20px', letterSpacing: '4px',
            background: 'var(--red)', color: 'var(--white)', border: 'none',
            padding: '14px 40px', borderRadius: '4px', cursor: 'pointer',
          }}
        >
          VOLVER
        </button>
      </div>
    )
  }

  const streakHasName = member.streakName && member.streakName !== 'No cumple con ninguna racha'
  const progressPct = (countdown / AUTO_REDIRECT_SECONDS) * 100

  return (
    <>
      <div
        style={{
          position: 'relative',
          width: '100vw',
          height: '100vh',
          background: 'var(--black)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: visible ? 1 : 0,
          transition: 'opacity 0.5s ease',
        }}
      >
        {/* Background crossfit image */}
        <div style={{
          position: 'absolute', inset: 0,
          backgroundImage: `url('https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=1920&q=80')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center top',
          opacity: 0.07,
        }} />

        {/* Left red accent bar */}
        <div style={{
          position: 'absolute',
          top: 0, bottom: 0, left: 0,
          width: '6px',
          background: 'linear-gradient(180deg, transparent, var(--red) 20%, var(--red-bright) 50%, var(--red) 80%, transparent)',
        }} />
        {/* Right red accent bar */}
        <div style={{
          position: 'absolute',
          top: 0, bottom: 0, right: 0,
          width: '6px',
          background: 'linear-gradient(180deg, transparent, var(--red) 20%, var(--red-bright) 50%, var(--red) 80%, transparent)',
        }} />

        {/* Top label */}
        <div style={{
          position: 'absolute', top: '40px',
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(12px, 2vw, 20px)',
          letterSpacing: '12px',
          color: 'var(--red)',
          animation: 'fadeIn 0.6s ease forwards',
        }}>
          ◆ WOD ZONE ◆
        </div>

        {/* Main content */}
        <div style={{
          textAlign: 'center',
          padding: '0 40px',
          zIndex: 1,
        }}>

          {/* BIENVENIDO */}
          <div style={{
            fontFamily: 'var(--font-heading)',
            fontSize: 'clamp(16px, 3vw, 32px)',
            letterSpacing: '10px',
            color: 'var(--white-faint)',
            fontWeight: 400,
            textTransform: 'uppercase',
            animation: 'slideIn 0.6s ease forwards',
            marginBottom: '8px',
          }}>
            BIENVENIDO
          </div>

          {/* Member Name */}
          <div style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(52px, 10vw, 130px)',
            lineHeight: 0.95,
            letterSpacing: '4px',
            color: 'var(--white)',
            textTransform: 'uppercase',
            animation: 'slideIn 0.6s ease 0.1s both',
            marginBottom: '24px',
            textShadow: '0 0 60px rgba(255,255,255,0.1)',
          }}>
            {member.name}
          </div>

          {/* Red divider */}
          <div style={{
            width: '100px',
            height: '4px',
            background: 'linear-gradient(90deg, transparent, var(--red), var(--red-bright), var(--red), transparent)',
            margin: '0 auto 28px',
            animation: 'fadeIn 0.6s ease 0.2s both',
          }} />

          {/* Streak section */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 'clamp(24px, 5vw, 60px)',
            animation: 'fadeIn 0.6s ease 0.3s both',
            flexWrap: 'wrap',
          }}>
            {/* Streak count */}
            <div style={{ textAlign: 'center' }}>
              <div style={{
                fontFamily: 'var(--font-display)',
                fontSize: 'clamp(60px, 11vw, 140px)',
                lineHeight: 1,
                color: 'var(--red)',
                textShadow: '0 0 40px rgba(204,0,0,0.4)',
              }}>
                {member.streakCurrent}
              </div>
              <div style={{
                fontFamily: 'var(--font-heading)',
                fontSize: 'clamp(12px, 1.8vw, 20px)',
                letterSpacing: '6px',
                color: 'var(--white-faint)',
                fontWeight: 400,
                textTransform: 'uppercase',
              }}>
                DÍAS DE RACHA
              </div>
            </div>

            {/* Vertical separator */}
            <div style={{
              width: '2px',
              height: 'clamp(60px, 10vw, 120px)',
              background: 'linear-gradient(180deg, transparent, var(--red-dark), transparent)',
            }} />

            {/* Expiry info */}
            <div style={{ textAlign: 'center' }}>
              <div style={{
                fontFamily: 'var(--font-heading)',
                fontSize: 'clamp(11px, 1.6vw, 18px)',
                letterSpacing: '4px',
                color: 'var(--white-faint)',
                fontWeight: 400,
                textTransform: 'uppercase',
                marginBottom: '8px',
              }}>
                MENSUALIDAD VENCE
              </div>
              <div style={{
                fontFamily: 'var(--font-display)',
                fontSize: 'clamp(26px, 4.5vw, 58px)',
                color: 'var(--white)',
                letterSpacing: '2px',
              }}>
                {member.expiryDate}
              </div>
            </div>
          </div>

          {/* Streak badge if has named streak */}
          {streakHasName && (
            <div style={{
              marginTop: '24px',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '12px',
              background: 'rgba(204,0,0,0.15)',
              border: '1px solid var(--red)',
              borderRadius: '6px',
              padding: '12px 28px',
              animation: 'fadeIn 0.6s ease 0.5s both',
            }}>
              <span style={{ fontSize: '28px', animation: 'fireFlicker 0.8s ease-in-out infinite' }}>🔥</span>
              <span style={{
                fontFamily: 'var(--font-heading)',
                fontSize: 'clamp(14px, 2vw, 22px)',
                letterSpacing: '4px',
                color: 'var(--red-bright)',
                fontWeight: 700,
                textTransform: 'uppercase',
              }}>
                {member.streakName}
              </span>
              <span style={{ fontSize: '28px', animation: 'fireFlicker 0.8s ease-in-out 0.4s infinite' }}>🔥</span>
            </div>
          )}
        </div>

        {/* Bottom tagline */}
        <div style={{
          position: 'absolute', bottom: '60px',
          fontFamily: 'var(--font-heading)',
          fontSize: 'clamp(10px, 1.5vw, 16px)',
          letterSpacing: '6px',
          color: 'var(--white-faint)',
          textTransform: 'uppercase',
          fontWeight: 400,
          animation: 'fadeIn 0.6s ease 0.6s both',
        }}>
          Stronger Every Day • No Excuses
        </div>

        {/* Countdown progress bar */}
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          height: '4px',
          background: 'var(--black-border)',
        }}>
          <div style={{
            height: '100%',
            width: `${progressPct}%`,
            background: 'linear-gradient(90deg, var(--red-dark), var(--red))',
            transition: 'width 1s linear',
          }} />
        </div>

        {/* Countdown indicator */}
        <div
          onClick={goHome}
          style={{
            position: 'absolute', top: '36px', right: '50px',
            fontFamily: 'var(--font-body)',
            fontSize: '13px',
            color: 'var(--white-faint)',
            cursor: 'pointer',
            letterSpacing: '2px',
          }}
        >
          {countdown}s ✕
        </div>
      </div>

      {/* Streak milestone modal */}
      {showStreak && streakHasName && (
        <StreakModal
          streakName={member.streakName}
          streakCount={member.streakCurrent}
          onClose={() => setShowStreak(false)}
        />
      )}
    </>
  )
}
