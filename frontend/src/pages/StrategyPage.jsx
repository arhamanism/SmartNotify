import { useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import { endpoints } from '../api/endpoints'
import { useApp } from '../context/AppContext'

export default function StrategyPage() {
  const { channels, pushToast, refreshAll } = useApp()
  const [eventType, setEventType] = useState('strategy_demo')
  const [recipient, setRecipient] = useState('student@example.com')
  const [message, setMessage] = useState('This event will use selected strategies/channels.')
  const [selected, setSelected] = useState(['email', 'sms'])
  const [loading, setLoading] = useState(false)

  const toggle = (c) => setSelected((prev) => (
    prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]
  ))

  const fire = async () => {
    if (!selected.length) {
      pushToast({ type: 'error', message: 'Select at least one channel strategy' })
      return
    }
    setLoading(true)
    try {
      const res = await endpoints.fireEvent({
        event_type: eventType,
        recipient,
        message,
        channels: selected,
      })
      pushToast({ type: 'success', message: `Strategy demo sent via ${res.data.notifications_sent} channel(s)` })
      await refreshAll()
    } catch (e) {
      pushToast({ type: 'error', message: e?.response?.data?.detail || 'Strategy demo failed' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Strategy Pattern (Runtime Channel Selection)</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          Strategy means the same notification flow can switch delivery behavior at runtime.
          Select channels below and fire one event to compare outcomes.
        </p>
      </Card>

      <Card>
        <h3 className='font-semibold'>Run Strategy Demo</h3>
        <div className='mt-3 grid gap-2 md:grid-cols-2'>
          <input className='input' value={eventType} onChange={(e) => setEventType(e.target.value)} />
          <input className='input' value={recipient} onChange={(e) => setRecipient(e.target.value)} />
        </div>
        <textarea className='input mt-2 w-full' rows='3' value={message} onChange={(e) => setMessage(e.target.value)} />
        <p className='mt-2 text-xs text-[#9898a8]'>Click channels to include/exclude strategies:</p>
        <div className='mt-2 flex flex-wrap gap-2'>
          {(channels || []).map((c) => (
            <button
              key={c}
              className={`rounded px-3 py-1 text-sm ${selected.includes(c) ? 'bg-[#6c63ff] text-white' : 'bg-[#22222f] text-[#9898a8]'}`}
              onClick={() => toggle(c)}
            >
              {c}
            </button>
          ))}
        </div>
        <Button className='mt-3' onClick={fire} loading={loading}>Fire Strategy Event</Button>
      </Card>

      <Card>
        <h3 className='mb-2 font-semibold'>Selected Strategies</h3>
        <div className='flex flex-wrap gap-2'>
          {selected.map((c) => <Badge key={c} type={c}>{c}</Badge>)}
        </div>
      </Card>
    </div>
  )
}
