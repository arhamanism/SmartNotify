import { useMemo, useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import { useApp } from '../context/AppContext'
import { endpoints } from '../api/endpoints'

export default function ObserverPage() {
  const { subscriptions, channels, refreshAll, pushToast } = useApp()
  const [eventType, setEventType] = useState('delivery_update')
  const [channel, setChannel] = useState('sms')
  const [loadingAdd, setLoadingAdd] = useState(false)
  const [loadingRemove, setLoadingRemove] = useState(false)
  const events = useMemo(() => Object.keys(subscriptions || {}), [subscriptions])

  const add = async () => {
    setLoadingAdd(true)
    try {
      await endpoints.addSubscription({ event_type: eventType, channel })
      await refreshAll()
      pushToast({ type: 'success', message: `Subscribed ${channel} to ${eventType}` })
    } catch (e) {
      pushToast({ type: 'error', message: e?.response?.data?.detail || 'Failed to subscribe' })
    } finally {
      setLoadingAdd(false)
    }
  }

  const remove = async () => {
    setLoadingRemove(true)
    try {
      await endpoints.removeSubscription({ event_type: eventType, channel })
      await refreshAll()
      pushToast({ type: 'info', message: `Removed ${channel} from ${eventType}` })
    } catch (e) {
      pushToast({ type: 'error', message: e?.response?.data?.detail || 'Failed to remove subscription' })
    } finally {
      setLoadingRemove(false)
    }
  }

  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Observer Pattern (Event → Subscribers)</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          Services emit events, and observers decide which channels are notified. This decouples
          business logic from delivery logic.
        </p>
      </Card>

      <Card>
        <h3 className='font-semibold'>Manage Subscriptions</h3>
        <div className='mt-3 grid gap-2 md:grid-cols-2'>
          <input
            className='input'
            placeholder='Event type (e.g. delivery_update)'
            value={eventType}
            onChange={(e) => setEventType(e.target.value)}
          />
          <select className='input' value={channel} onChange={(e) => setChannel(e.target.value)}>
            {(channels || []).map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className='mt-3 flex gap-2'>
          <Button onClick={add} loading={loadingAdd}>Add Subscription</Button>
          <Button variant='neutral' onClick={remove} loading={loadingRemove}>Remove Subscription</Button>
        </div>
      </Card>

      <Card>
        <h3 className='mb-2 font-semibold'>Current Event Subscriptions</h3>
        {(events || []).length === 0 && <p className='text-sm text-[#9898a8]'>No subscriptions found.</p>}
        {(events || []).map((event) => (
          <div key={event} className='mb-2 rounded bg-[#22222f] p-3'>
            <p className='text-sm font-medium'>{event}</p>
            <div className='mt-2 flex flex-wrap gap-2'>
              {(subscriptions[event] || []).map((c) => <Badge key={`${event}-${c}`} type={c}>{c}</Badge>)}
            </div>
          </div>
        ))}
      </Card>
    </div>
  )
}
