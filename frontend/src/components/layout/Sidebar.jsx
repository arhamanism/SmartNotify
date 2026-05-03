import { LayoutDashboard, Zap, ScrollText, Lock, Boxes, Eye, GitBranch, ArrowLeftRight, Radio, CheckSquare } from 'lucide-react'

const items = [
  ['1. Overview', 'overview', LayoutDashboard],
  ['2. Fire Events', 'fire-events', Zap],
  ['3. Live Logs', 'live-logs', ScrollText],
  ['Singleton', 'singleton', Lock],
  ['Factory', 'factory', Boxes],
  ['Observer', 'observer', Eye],
  ['Strategy', 'strategy', GitBranch],
  ['Before vs After', 'before-after', ArrowLeftRight],
  ['Channels', 'channels', Radio],
  ['Test Results', 'test-results', CheckSquare],
]

export default function Sidebar({ currentPage, setCurrentPage }) {
  return (
    <aside className='fixed left-0 top-14 z-30 hidden h-[calc(100vh-56px)] w-[260px] border-r border-[rgba(255,255,255,0.08)] bg-[#13131a] p-4 md:block'>
      <p className='mb-2 px-2 text-xs uppercase tracking-wide text-[#5a5a6e]'>Recommended Demo Flow</p>
      {items.map(([label, key, Icon]) => {
        const a = currentPage === key
        return (
          <button
            key={key}
            onClick={() => setCurrentPage(key)}
            className={`mb-1 flex w-full items-center gap-2 rounded-lg border-l-2 px-3 py-2 text-sm ${a ? 'border-l-[#6c63ff] bg-[#22222f] text-[#6c63ff]' : 'border-l-transparent text-[#9898a8] hover:bg-[#1a1a24]'}`}
          >
            <Icon size={16} />
            {label}
          </button>
        )
      })}
    </aside>
  )
}
