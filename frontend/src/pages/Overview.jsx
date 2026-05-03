import { useEffect } from 'react'
import { CheckCircle, Eye, XCircle, Zap } from 'lucide-react'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import StatCard from '../components/ui/StatCard'
import { useApp } from '../context/AppContext'
import { endpoints } from '../api/endpoints'
import usePolling from '../hooks/usePolling'

export default function Overview() {
  const { stats, logs, subscriptions, setStats, setLogs, setSubscriptions } = useApp()

  const refresh = async () => {
    const [s, l, sub] = await Promise.all([endpoints.stats(), endpoints.logs(), endpoints.subscriptions()])
    setStats(s.data)
    setLogs(l.data)
    setSubscriptions(sub.data)
  }

  useEffect(() => {
    refresh().catch(() => {})
  }, [])

  usePolling(refresh, 3000, true)

  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>How to Use This Dashboard</h2>
        <ol className='mt-2 list-decimal space-y-1 pl-5 text-sm text-[#cbd5e1]'>
          <li>Click <strong>Run Demo</strong> in the top-right to trigger all major event scenarios.</li>
          <li>Watch counters update in real time (fired, success, failed, active observers).</li>
          <li>Open <strong>Fire Events</strong> to send custom events manually.</li>
          <li>Open <strong>Live Logs</strong> to inspect each dispatch record and status.</li>
          <li>Use pattern pages to validate Singleton, Factory, Observer, and Strategy behavior.</li>
        </ol>
      </Card>

      <div className='grid gap-3 md:grid-cols-2 xl:grid-cols-4'>
        <StatCard title='Total Fired' value={stats?.total_notifications || 0} icon={Zap} />
        <StatCard title='Successful' value={stats?.successful || 0} icon={CheckCircle} />
        <StatCard title='Failed' value={stats?.failed || 0} icon={XCircle} />
        <StatCard title='Active Observers' value={stats?.active_observers || 0} icon={Eye} />
      </div>

      <div className='grid gap-4 lg:grid-cols-2'>
        <Card>
          <h3 className='mb-2 font-semibold'>Singleton Proof</h3>
          <pre className='rounded bg-[#0d1117] p-3 text-sm text-[#cbd5e1]'>manager1 = NotificationManager()</pre>
        </Card>
        <Card>
          <h3 className='mb-2 font-semibold'>Live Activity Feed</h3>
          <div className='space-y-2'>
            {[...(logs || [])].slice(-8).reverse().map((entry, i) => (
              <div key={`${entry.timestamp}-${i}`} className='rounded bg-[#22222f] p-2'>
                <div className='flex items-center justify-between'>
                  <Badge type={(entry.channel || '').toLowerCase()}>{entry.channel}</Badge>
                  <Badge type={entry.status === 'SUCCESS' ? 'success' : 'failed'}>{entry.status}</Badge>
                </div>
                <div className='mt-1 text-sm'>{entry.event_type} · {entry.recipient}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <h3 className='mb-2 font-semibold'>Observer Subscriptions</h3>
        {Object.entries(subscriptions || {}).map(([event, channels]) => (
          <div key={event} className='mb-1 flex items-center justify-between rounded bg-[#22222f] p-2'>
            <span>{event}</span>
            <div className='flex gap-1'>{channels.map((c) => <Badge key={c} type={c}>{c}</Badge>)}</div>
          </div>
        ))}
      </Card>
    </div>
  )
}
