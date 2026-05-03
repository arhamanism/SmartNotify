import { useMemo, useState } from 'react'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Button from '../components/ui/Button'
import Modal from '../components/ui/Modal'
import { endpoints } from '../api/endpoints'
import { useApp } from '../context/AppContext'
import usePolling from '../hooks/usePolling'

export default function LiveLogs() {
  const { logs, setLogs, pushToast } = useApp()
  const [search, setSearch] = useState('')
  const [confirm, setConfirm] = useState(false)
  const [auto, setAuto] = useState(true)

  usePolling(async () => {
    if (!auto) return
    const res = await endpoints.logs()
    setLogs(res.data)
  }, 2000, auto)

  const filtered = useMemo(() => (logs || []).filter((l) => [l.recipient, l.message, l.event_type].join(' ').toLowerCase().includes(search.toLowerCase())), [logs, search])
  const success = filtered.filter((x) => x.status === 'SUCCESS').length
  const failed = filtered.filter((x) => x.status === 'FAILED').length

  const clear = async () => {
    await endpoints.clearLogs()
    setLogs([])
    setConfirm(false)
    pushToast({ type: 'info', message: 'Logs cleared' })
  }

  return (
    <Card>
      <div className='mb-3 flex items-center justify-between'>
        <h2 className='text-xl font-semibold'>Notification Logs</h2>
        <div className='flex gap-2'>
          <button className={`rounded-full px-3 py-1 text-xs ${auto ? 'bg-[#22c55e22] text-[#22c55e]' : 'bg-[#22222f] text-[#9898a8]'}`} onClick={() => setAuto((v) => !v)}>Auto-refresh</button>
          <Button variant='danger' onClick={() => setConfirm(true)}>Clear All</Button>
        </div>
      </div>
      <input className='input mb-3 w-full' placeholder='Search recipient, message, event_type' value={search} onChange={(e) => setSearch(e.target.value)} />
      <div className='max-h-[460px] overflow-auto rounded border border-[rgba(255,255,255,0.08)]'>
        <table className='w-full text-sm'>
          <thead className='sticky top-0 bg-[#22222f]'><tr><th className='px-2 py-2'>#</th><th>Timestamp</th><th>Event</th><th>Channel</th><th>Recipient</th><th>Message</th><th>Status</th></tr></thead>
          <tbody>{filtered.map((l, i) => <tr key={`${l.timestamp}-${i}`} className='border-t border-[rgba(255,255,255,0.06)]'><td className='px-2 py-2'>{i + 1}</td><td>{l.timestamp}</td><td>{l.event_type}</td><td><Badge type={(l.channel || '').toLowerCase()}>{l.channel}</Badge></td><td>{l.recipient}</td><td className='max-w-[240px] truncate'>{l.message}</td><td><Badge type={l.status === 'SUCCESS' ? 'success' : 'failed'}>{l.status}</Badge></td></tr>)}</tbody>
        </table>
      </div>
      <p className='mt-3 text-sm text-[#9898a8]'>Showing {filtered.length} of {(logs || []).length} entries · {success} successful · {failed} failed</p>
      <Modal open={confirm} title='Clear all logs?' onConfirm={clear} onClose={() => setConfirm(false)}>This will reset in-memory logs and counters.</Modal>
    </Card>
  )
}
