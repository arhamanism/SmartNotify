import { Bell } from 'lucide-react'
import Button from '../ui/Button'
export default function Header({ currentLabel, runDemo, runningDemo, demoProgress }) {
  return <header className='fixed inset-x-0 top-0 z-40 h-14 border-b border-[rgba(255,255,255,0.08)] bg-[#13131a] px-4'><div className='mx-auto flex h-full max-w-[1600px] items-center justify-between'><div className='flex items-center gap-2'><Bell size={18} /><span className='font-medium'>Smart Notification System</span></div><div className='text-sm text-[#9898a8]'>{currentLabel}</div><div className='flex items-center gap-3'><span className='hidden text-xs text-[#9898a8] md:block'>SE Project · Group 23K</span><Button onClick={runDemo} loading={runningDemo}>{runningDemo ? 'Running Demo...' : 'Run Guided Demo'}</Button></div></div>{runningDemo && <div className='h-1 bg-[#22222f]'><div className='h-1 bg-[#6c63ff] transition-all' style={{ width: `${demoProgress}%` }} /></div>}</header>
}
