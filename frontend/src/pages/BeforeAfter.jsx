import Card from '../components/ui/Card'

const rows = [
  ['Add new channel', 'Edit multiple service classes', 'Register one strategy in factory'],
  ['Business services', 'Contain notification sending code', 'Only emit events'],
  ['Logging', 'Scattered per service', 'Centralized in singleton manager'],
  ['Maintainability', 'High coupling, repeated logic', 'Modular, easier to extend'],
  ['Pattern clarity', 'No clear architecture boundaries', 'Strategy + Factory + Observer + Singleton'],
]

export default function BeforeAfter() {
  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Before vs After Architecture</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          This project demonstrates why design patterns matter: less coupling, cleaner services,
          and easier channel/event extension.
        </p>
      </Card>
      <Card>
        <div className='overflow-auto rounded border border-[rgba(255,255,255,0.08)]'>
          <table className='w-full text-sm'>
            <thead className='bg-[#22222f] text-left'>
              <tr>
                <th className='px-3 py-2'>Concern</th>
                <th className='px-3 py-2'>Traditional / Bad Design</th>
                <th className='px-3 py-2'>Pattern-based Design (This Project)</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(([a, b, c]) => (
                <tr key={a} className='border-t border-[rgba(255,255,255,0.08)]'>
                  <td className='px-3 py-2 font-medium'>{a}</td>
                  <td className='px-3 py-2 text-[#fca5a5]'>{b}</td>
                  <td className='px-3 py-2 text-[#86efac]'>{c}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
