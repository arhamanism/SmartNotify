import { useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { endpoints } from '../api/endpoints'
import { useApp } from '../context/AppContext'

export default function FireEvents() {
  const { pushToast, refreshAll } = useApp()
  const [eventType, setEventType] = useState('order_placed')
  const [recipient, setRecipient] = useState('hassan@example.com')
  const [message, setMessage] = useState('Demo message')
  const [channels, setChannels] = useState([])
  const [lines, setLines] = useState([])
  const [loading, setLoading] = useState(false)

  const toggle = (c) => setChannels((p) => p.includes(c) ? p.filter((x) => x !== c) : [...p, c])

  const fire = async () => {
    setLoading(true)
    try {
      const res = await endpoints.fireEvent({ event_type: eventType, recipient, message, channels })
      const sent = res.data.notifications_sent || 0
      setLines((p) => [...p, `[${new Date().toLocaleTimeString()}] Event "${eventType}" fired`, ...((res.data.logs || []).map((l) => `${l.status} ${l.channel} -> ${l.recipient}`))])
      pushToast({ type: 'success', message: `Event fired — ${sent} notifications sent` })
      refreshAll()
    } catch (e) {
      pushToast({ type: 'error', message: e?.response?.data?.detail || 'Failed to fire event' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='grid gap-4 lg:grid-cols-2'>
      <Card>
        <h3 className='mb-1 font-semibold'>Event Builder</h3>
        <p className='mb-2 text-sm text-[#9898a8]'>Fill fields, choose optional channels, then click Fire Event.</p>
        <select className='input mb-2 w-full' value={eventType} onChange={(e) => setEventType(e.target.value)}>
          {['order_placed', 'security_alert', 'promotional', 'password_reset', 'refund_processed'].map((e) => <option key={e}>{e}</option>)}
        </select>
        <input className='input mb-2 w-full' value={recipient} onChange={(e) => setRecipient(e.target.value)} />
        <textarea className='input mb-2 w-full' rows='3' value={message} onChange={(e) => setMessage(e.target.value)} />
        <div className='mb-2 flex flex-wrap gap-2'>{['email', 'sms', 'push', 'whatsapp'].map((c) => <button key={c} className={`rounded px-2 py-1 text-xs ${channels.includes(c) ? 'bg-[#6c63ff]' : 'bg-[#22222f]'}`} onClick={() => toggle(c)}>{c}</button>)}</div>
        <p className='mb-2 text-xs text-[#9898a8]'>No channel selected = use saved Observer subscriptions for this event.</p>
        <Button className='w-full' loading={loading} onClick={fire}>Fire Event</Button>
      </Card>
      <Card>
        <div className='mb-2 flex justify-between'>
          <h3 className='font-semibold'>Dispatch Log</h3>
          <Button variant='neutral' onClick={() => setLines([])}>Clear</Button>
        </div>
        <div className='h-[420px] overflow-auto rounded bg-[#0d1117] p-3 font-mono text-xs'>
          {lines.length ? lines.map((l, i) => <div key={i}>{l}</div>) : <div className='text-[#5a5a6e]'>Waiting for events...</div>}
        </div>
      </Card>
    </div>
  )
}
