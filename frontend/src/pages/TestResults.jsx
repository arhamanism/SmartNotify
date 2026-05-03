import Card from '../components/ui/Card'

const tests = [
  ['Singleton tests', 'tests/test_singleton.py', 'Single instance + centralized state checks'],
  ['Factory tests', 'tests/test_factory.py', 'Correct channel strategy object creation'],
  ['Strategy tests', 'tests/test_strategy.py', 'Interchangeable delivery behavior checks'],
  ['Observer tests', 'tests/test_observer.py', 'Subscription + event dispatch behavior'],
  ['Integration tests', 'tests/test_integration.py', 'End-to-end event to notification flow'],
]

export default function TestResults() {
  return (
    <div className='space-y-4'>
      <Card>
        <h2 className='text-xl font-semibold'>Testing and Verification</h2>
        <p className='mt-2 text-sm text-[#9898a8]'>
          Use this checklist during evaluation to prove the implementation is correct and pattern-compliant.
        </p>
      </Card>
      <Card>
        <h3 className='font-semibold'>How to run tests</h3>
        <pre className='mt-2 rounded bg-[#0d1117] p-3 text-sm text-[#cbd5e1]'>python run_tests.py</pre>
        <pre className='mt-2 rounded bg-[#0d1117] p-3 text-sm text-[#cbd5e1]'>python -m pytest tests/ -v</pre>
      </Card>
      <Card>
        <h3 className='mb-2 font-semibold'>Test Coverage Areas</h3>
        <div className='space-y-2'>
          {tests.map(([title, file, desc]) => (
            <div key={file} className='rounded bg-[#22222f] p-3'>
              <p className='text-sm font-medium'>{title}</p>
              <p className='font-mono text-xs text-[#94a3b8]'>{file}</p>
              <p className='mt-1 text-sm text-[#cbd5e1]'>{desc}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
