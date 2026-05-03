import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import { useApp } from '../context/AppContext'

const meanings = {
  email: 'Best for detailed updates and transactional confirmations.',
  sms: 'Best for urgent, short alerts with high visibility.',
  push: 'Best for app engagement and quick reminders.',
  whatsapp: 'Best for conversational updates and broad reach.',
}

export default function ChannelsPage() {
  const { channels } = useApp()
  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Notification Channels</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          Channels are concrete strategy implementations. New channels can be registered at runtime
          from the Factory page without changing service classes.
        </p>
      </Card>
      <Card>
        <h3 className='mb-2 font-semibold'>Active Channels in System</h3>
        <div className='flex flex-wrap gap-2'>
          {(channels || []).map((c) => <Badge key={c} type={c}>{c}</Badge>)}
        </div>
      </Card>
      <Card>
        <h3 className='mb-2 font-semibold'>When to use which channel</h3>
        <div className='space-y-2'>
          {(channels || []).map((c) => (
            <div key={c} className='rounded bg-[#22222f] p-3'>
              <div className='mb-1'><Badge type={c}>{c}</Badge></div>
              <p className='text-sm text-[#cbd5e1]'>{meanings[c] || 'Custom dynamic channel created from factory.'}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
