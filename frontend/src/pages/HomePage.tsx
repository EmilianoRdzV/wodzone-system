import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Clock from '../components/Clock'
import { postCheckin } from '../api/checkin'

const QUOTES = [
  'NO EXCUSES. NO LIMITS.',
  'STRONGER EVERY DAY.',
  'EARN YOUR REST.',
  'PAIN IS TEMPORARY. GLORY IS FOREVER.',
  'SHOW UP. WORK HARD. GET RESULTS.',
  'EL ESFUERZO DE HOY ES EL RESULTADO DE MAÑANA.',
]

export default function HomePage() {
  const navigate = useNavigate()
  const [quote, setQuote] = useState(QUOTES[0])
  const [quoteIdx, setQuoteIdx] = useState(0)
  const [scanning, setScanning] = useState(false)
  const [error, setError] = useState('')
  const [manualQr, setManualQr] = useState('')
  const [showManual, setShowManual] = useState(false)
  const manualInputRef = useRef<HTMLInputElement>(null)
  const qrBuffer = useRef('')
  const qrTimeout = useRef<ReturnType<typeof setTimeout> | null>(null)

  // Rotate motivational quotes
  useEffect(() => {
    const timer = setInterval(() => {
      setQuoteIdx(i => {
        const next = (i + 1) % QUOTES.length
        setQuote(QUOTES[next])
        return next
      })
    }, 5000)
    return () => clearInterval(timer)
  }, [])

  // Focus manual input when shown
  useEffect(() => {
    if (showManual) manualInputRef.current?.focus()
  }, [showManual])

  async function doCheckin(qr: string) {
    const code = qr.trim()
    if (!code) return
    setScanning(true)
    setError('')
    setManualQr('')
    setShowManual(false)
    try {
      const result = await postCheckin(code)
      if (result.success) {
        navigate(`/member/${code}`, { state: result })
      } else {
        setError(result.error || 'Miembro no encontrado')
        setTimeout(() => setError(''), 4000)
      }
    } catch {
      setError('Error de conexión con el servidor')
      setTimeout(() => setError(''), 4000)
    } finally {
      setScanning(false)
    }
  }

  // Listen for barcode scanner input (keyboard wedge) — only when manual input is hidden
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (showManual) return
      if (document.activeElement?.tagName === 'INPUT') return

      if (e.key === 'Enter') {
        const qr = qrBuffer.current.trim()
        qrBuffer.current = ''
        if (qrTimeout.current) clearTimeout(qrTimeout.current)
        if (qr) doCheckin(qr)
      } else if (e.key.length === 1) {
        qrBuffer.current += e.key
        if (qrTimeout.current) clearTimeout(qrTimeout.current)
        qrTimeout.current = setTimeout(() => { qrBuffer.current = '' }, 500)
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [showManual, navigate])

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: '100vh',
      background: 'var(--black)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      overflow: 'hidden',
    }}>

      {/* Background image */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: `url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1920&q=80')`,
        backgroundSize: 'cover', backgroundPosition: 'center', opacity: 0.12,
      }} />

      {/* Top / bottom bars */}
      {['top', 'bottom'].map(pos => (
        <div key={pos} style={{
          position: 'absolute', [pos]: 0, left: 0, right: 0, height: '4px',
          background: 'linear-gradient(90deg, transparent, var(--red), var(--red-bright), var(--red), transparent)',
        }} />
      ))}

      {/* Corner accents */}
      {[
        { top: 20, left: 20, borderTop: '2px solid var(--red)', borderLeft: '2px solid var(--red)' },
        { top: 20, right: 20, borderTop: '2px solid var(--red)', borderRight: '2px solid var(--red)' },
        { bottom: 20, left: 20, borderBottom: '2px solid var(--red)', borderLeft: '2px solid var(--red)' },
        { bottom: 20, right: 20, borderBottom: '2px solid var(--red)', borderRight: '2px solid var(--red)' },
      ].map((s, i) => <div key={i} style={{ position: 'absolute', width: 40, height: 40, ...s }} />)}

      {/* Logo */}
      <div style={{
        fontFamily: 'var(--font-display)', fontSize: 'clamp(14px, 2.5vw, 28px)',
        letterSpacing: '14px', color: 'var(--red)', marginBottom: '8px',
        animation: 'fadeIn 0.8s ease forwards',
      }}>
        ◆ WOD ZONE ◆
      </div>

      {/* Clock */}
      <div style={{ animation: 'fadeIn 0.8s ease 0.2s both' }}>
        <Clock />
      </div>

      {/* Divider */}
      <div style={{
        width: '120px', height: '3px',
        background: 'linear-gradient(90deg, transparent, var(--red), transparent)',
        margin: '30px auto', animation: 'fadeIn 0.8s ease 0.4s both',
      }} />

      {/* Central area: scanner prompt / processing / error / manual input */}
      <div style={{ animation: 'fadeIn 0.8s ease 0.6s both', textAlign: 'center', width: '100%', maxWidth: '520px', padding: '0 24px' }}>

        {scanning ? (
          <div style={{
            fontFamily: 'var(--font-heading)', fontSize: 'clamp(16px, 2.5vw, 28px)',
            letterSpacing: '4px', color: 'var(--red)', animation: 'pulse 0.8s ease infinite',
          }}>
            PROCESANDO...
          </div>

        ) : error ? (
          <div style={{
            fontFamily: 'var(--font-heading)', fontSize: 'clamp(13px, 1.8vw, 20px)',
            letterSpacing: '2px', color: '#ff4444', textAlign: 'center',
          }}>
            ⚠ {error}
          </div>

        ) : showManual ? (
          /* ── Manual input mode ── */
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
            <div style={{
              fontFamily: 'var(--font-heading)', fontSize: 'clamp(13px, 1.8vw, 18px)',
              letterSpacing: '5px', color: 'var(--white-dim)', textTransform: 'uppercase',
            }}>
              Ingresa el código QR
            </div>

            <div style={{ display: 'flex', gap: '10px', width: '100%' }}>
              <input
                ref={manualInputRef}
                type="text"
                value={manualQr}
                onChange={e => setManualQr(e.target.value.toUpperCase())}
                onKeyDown={e => { if (e.key === 'Enter') doCheckin(manualQr) }}
                placeholder="WZ-A1B2C3D4"
                style={{
                  flex: 1,
                  background: '#1a1a1a',
                  color: '#ffffff',
                  border: '2px solid var(--red)',
                  borderRadius: '4px',
                  padding: '14px 18px',
                  fontFamily: 'var(--font-heading)',
                  fontSize: '20px',
                  letterSpacing: '4px',
                  textTransform: 'uppercase',
                  outline: 'none',
                  textAlign: 'center',
                }}
              />
              <button
                onClick={() => doCheckin(manualQr)}
                disabled={!manualQr.trim()}
                style={{
                  background: manualQr.trim() ? 'var(--red)' : '#333',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '14px 22px',
                  fontFamily: 'var(--font-heading)',
                  fontSize: '16px',
                  letterSpacing: '2px',
                  fontWeight: 700,
                  cursor: manualQr.trim() ? 'pointer' : 'not-allowed',
                  textTransform: 'uppercase',
                  transition: 'background 0.2s',
                }}
              >
                ENTRAR
              </button>
            </div>

            <button
              onClick={() => { setShowManual(false); setManualQr(''); setError('') }}
              style={{
                background: 'transparent', color: 'var(--white-faint)',
                border: '1px solid #333', borderRadius: '4px',
                padding: '8px 20px', fontFamily: 'var(--font-body)',
                fontSize: '13px', letterSpacing: '2px', cursor: 'pointer',
                textTransform: 'uppercase',
              }}
            >
              ← Volver al escáner
            </button>
          </div>

        ) : (
          /* ── Scanner idle mode ── */
          <>
            <div style={{
              fontFamily: 'var(--font-heading)', fontSize: 'clamp(14px, 2.2vw, 24px)',
              letterSpacing: '6px', color: 'var(--white-dim)', fontWeight: 400,
              marginBottom: '16px', textTransform: 'uppercase',
            }}>
              Escanea tu código QR para ingresar
            </div>

            {/* Animated scanner box */}
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px' }}>
              <div style={{
                border: '2px solid var(--red)', borderRadius: '8px', padding: '14px 24px',
                animation: 'glowPulse 2s ease-in-out infinite',
                position: 'relative', overflow: 'hidden',
              }}>
                <div style={{
                  fontFamily: 'var(--font-display)', fontSize: '28px',
                  letterSpacing: '8px', color: 'var(--white)',
                }}>
                  ▦ ESCANEAR ▦
                </div>
                <div style={{
                  position: 'absolute', left: 0, right: 0, height: '2px',
                  background: 'linear-gradient(90deg, transparent, var(--red-bright), transparent)',
                  animation: 'scanLine 2s linear infinite',
                }} />
              </div>
            </div>

            {/* Manual entry button */}
            <button
              onClick={() => setShowManual(true)}
              style={{
                background: 'transparent',
                color: 'var(--white-faint)',
                border: '1px solid #333',
                borderRadius: '4px',
                padding: '10px 24px',
                fontFamily: 'var(--font-body)',
                fontSize: '13px',
                letterSpacing: '2px',
                cursor: 'pointer',
                textTransform: 'uppercase',
                transition: 'border-color 0.2s, color 0.2s',
              }}
              onMouseEnter={e => {
                (e.target as HTMLButtonElement).style.borderColor = 'var(--red)'
                ;(e.target as HTMLButtonElement).style.color = 'var(--white)'
              }}
              onMouseLeave={e => {
                (e.target as HTMLButtonElement).style.borderColor = '#333'
                ;(e.target as HTMLButtonElement).style.color = 'var(--white-faint)'
              }}
            >
              ✎ Ingresar código manualmente
            </button>
          </>
        )}
      </div>

      {/* Motivational quote */}
      <div key={quoteIdx} style={{
        position: 'absolute', bottom: '40px',
        fontFamily: 'var(--font-heading)', fontSize: 'clamp(11px, 1.4vw, 16px)',
        letterSpacing: '5px', color: 'var(--white-faint)', textTransform: 'uppercase',
        animation: 'fadeIn 0.8s ease forwards',
      }}>
        {quote}
      </div>
    </div>
  )
}
