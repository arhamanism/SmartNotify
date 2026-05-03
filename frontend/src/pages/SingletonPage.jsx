import { useEffect, useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import { endpoints } from '../api/endpoints'
import { useApp } from '../context/AppContext'

export default function SingletonPage() {
  const { stats } = useApp()
  const [proof, setProof] = useState(null)
  const [loading, setLoading] = useState(false)

  const loadProof = async () => {
    setLoading(true)
    try {
      const res = await endpoints.singletonProof()
      setProof(res.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProof().catch(() => {})
  }, [])

  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Singleton Pattern (One Shared Manager)</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          This page proves that every service uses the same <code>NotificationManager</code> instance.
          If both instance IDs are identical, singleton behavior is correct.
        </p>
        <div className='mt-3 flex flex-wrap items-center gap-2'>
          <Button onClick={loadProof} loading={loading}>Re-check Singleton Proof</Button>
          <Badge type={proof?.are_same ? 'success' : 'failed'}>
            {proof?.are_same ? 'PASS: Same instance' : 'Not verified yet'}
          </Badge>
        </div>
      </Card>

      <Card>
        <h3 className='font-semibold'>Runtime Evidence</h3>
        <div className='mt-3 grid gap-3 md:grid-cols-2'>
          <div className='rounded bg-[#22222f] p-3'>
            <p className='text-xs text-[#9898a8]'>Instance ID 1</p>
            <p className='font-mono text-sm'>{proof?.instance_id_1 || '—'}</p>
          </div>
          <div className='rounded bg-[#22222f] p-3'>
            <p className='text-xs text-[#9898a8]'>Instance ID 2</p>
            <p className='font-mono text-sm'>{proof?.instance_id_2 || '—'}</p>
          </div>
          <div className='rounded bg-[#22222f] p-3'>
            <p className='text-xs text-[#9898a8]'>App Initialized At</p>
            <p className='text-sm'>{proof?.initialized_at || '—'}</p>
          </div>
          <div className='rounded bg-[#22222f] p-3'>
            <p className='text-xs text-[#9898a8]'>Total Notifications Logged</p>
            <p className='text-sm'>{proof?.total_logs ?? stats?.total_notifications ?? 0}</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
