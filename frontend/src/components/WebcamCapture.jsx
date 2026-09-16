import { useEffect, useRef, useState } from 'react'

const CAPTURE_INTERVAL_MS = 1500 // how often a frame is sent for mood analysis

export default function WebcamCapture({ onFrame, active }) {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)
  const [error, setError] = useState(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    let cancelled = false

    async function start() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 480, height: 480, facingMode: 'user' },
          audio: false,
        })
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop())
          return
        }
        streamRef.current = stream
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          await videoRef.current.play()
        }
        setReady(true)
      } catch (err) {
        setError('Camera access was denied or is unavailable. Allow camera access and reload.')
      }
    }

    start()
    return () => {
      cancelled = true
      streamRef.current?.getTracks().forEach((t) => t.stop())
    }
  }, [])

  useEffect(() => {
    if (!ready || !active) return
    const canvas = canvasRef.current
    const video = videoRef.current

    const id = setInterval(() => {
      if (!video || !canvas || video.readyState < 2) return
      const ctx = canvas.getContext('2d')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      ctx.drawImage(video, 0, 0)
      const dataUrl = canvas.toDataURL('image/jpeg', 0.8)
      onFrame(dataUrl)
    }, CAPTURE_INTERVAL_MS)

    return () => clearInterval(id)
  }, [ready, active, onFrame])

  return (
    <div className="webcam-wrap">
      {error ? (
        <div className="webcam-error">{error}</div>
      ) : (
        <video ref={videoRef} className="webcam-video" muted playsInline />
      )}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  )
}
