import { useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import { useApp } from '../context/AppContext'
import { endpoints } from '../api/endpoints'

export default function FactoryPage() {
  const { channels, refreshAll, pushToast } = useApp()
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)

  const register = async () => {
    if (!name.trim()) {
      pushToast({ type: 'error', message: 'Channel name is required' })
      return
    }
    setLoading(true)
    try {
      await endpoints.registerChannel({ name })
      pushToast({ type: 'success', message: `Channel "${name}" registered` })
      setName('')
      await refreshAll()
    } catch (e) {
      pushToast({ type: 'error', message: e?.response?.data?.detail || 'Failed to register channel' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Factory Pattern (Create Without Coupling)</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          The factory centralizes channel creation, so new channels can be added without editing
          business services. Add a channel below to demonstrate Open/Closed Principle.
        </p>
      </Card>

      <Card>
        <h3 className='font-semibold'>Register New Channel</h3>
        <p className='mt-1 text-sm text-[#9898a8]'>Example names: slack, teams, discord</p>
        <div className='mt-3 flex flex-col gap-2 sm:flex-row'>
          <input
            className='input w-full'
            placeholder='Enter channel name'
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Button onClick={register} loading={loading}>Register Channel</Button>
        </div>
      </Card>

      <Card>
        <h3 className='mb-2 font-semibold'>Available Factory Channels</h3>
        <div className='flex flex-wrap gap-2'>
          {(channels || []).map((c) => <Badge key={c} type={c}>{c}</Badge>)}
        </div>
      </Card>
    </div>
  )
}
