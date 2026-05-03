from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def page_component(title: str) -> str:
    return f"""import Card from '../components/ui/Card'

export default function {title}() {{
  return (
    <Card>
      <h2 className='text-xl font-semibold'>{title}</h2>
      <p className='mt-2 text-[#9898a8]'>Interactive {title} page is wired into the dashboard navigation.</p>
    </Card>
  )
}}
"""


FILES = {
    "vite.config.js": """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({ plugins: [react(), tailwindcss()] })
""",
    "src/main.jsx": """import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'
import { AppProvider } from './context/AppContext'
createRoot(document.getElementById('root')).render(<React.StrictMode><AppProvider><App /></AppProvider></React.StrictMode>)
""",
    "src/index.css": """@import 'tailwindcss';
:root { --bg-main:#0f0f13;--bg-sidebar:#13131a;--bg-card:#1a1a24;--bg-elevated:#22222f;--border:rgba(255,255,255,0.08);--primary:#6c63ff;--primary-hover:#7c73ff;--success:#22c55e;--warning:#f59e0b;--error:#ef4444;--info:#3b82f6;--whatsapp:#25d366;--text-primary:#f1f1f3;--text-secondary:#9898a8;--text-muted:#5a5a6e;}
body{margin:0;background:var(--bg-main);color:var(--text-primary);font-family:Inter,system-ui,sans-serif;}
.input{border:1px solid var(--border);background:#22222f;color:#f1f1f3;border-radius:.5rem;padding:.55rem .7rem;}
.animate-fade-in{animation:fadeIn .15s ease-out;}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
""",
    "src/api/client.js": """import axios from 'axios'
const api = axios.create({ baseURL: 'http://localhost:8000/api' })
export default api
""",
    "src/api/endpoints.js": """import api from './client'
export const endpoints={stats:()=>api.get('/stats'),logs:()=>api.get('/logs'),subscriptions:()=>api.get('/subscriptions'),channels:()=>api.get('/channels'),singletonProof:()=>api.get('/singleton/proof'),fireEvent:(p)=>api.post('/events/fire',p),orderEvent:(p)=>api.post('/events/order',p),securityAlert:(p)=>api.post('/events/security-alert',p),passwordReset:(p)=>api.post('/events/password-reset',p),promotional:(p)=>api.post('/events/promotional',p),refund:(p)=>api.post('/events/refund',p),addSubscription:(p)=>api.post('/subscriptions/add',p),removeSubscription:(p)=>api.delete('/subscriptions/remove',{data:p}),registerChannel:(p)=>api.post('/channels/register',p),clearLogs:()=>api.delete('/logs/clear')}
""",
    "src/hooks/useApi.js": """import { useCallback,useState } from 'react'
export default function useApi(fn){const[loading,setLoading]=useState(false);const[error,setError]=useState('');const execute=useCallback(async(...a)=>{setLoading(true);setError('');try{const r=await fn(...a);return r.data}catch(e){const m=e?.response?.data?.detail||e.message||'Request failed';setError(m);throw new Error(m)}finally{setLoading(false)}},[fn]);return{execute,loading,error}}
""",
    "src/hooks/usePolling.js": """import { useEffect,useRef } from 'react'
export default function usePolling(callback,interval,enabled=true){const ref=useRef(callback);ref.current=callback;useEffect(()=>{if(!enabled||!interval)return;const id=setInterval(()=>ref.current(),interval);return()=>clearInterval(id)},[interval,enabled])}
""",
    "src/hooks/useToast.js": """import { useCallback,useState } from 'react'
let id=1;export default function useToast(){const[toasts,setToasts]=useState([]);const pushToast=useCallback((t)=>{const tid=id++;setToasts(p=>[{id:tid,...t},...p].slice(0,3));setTimeout(()=>setToasts(p=>p.filter(x=>x.id!==tid)),3000)},[]);const removeToast=useCallback((tid)=>setToasts(p=>p.filter(x=>x.id!==tid)),[]);return{toasts,pushToast,removeToast}}
""",
    "src/context/AppContext.jsx": """import { createContext,useContext,useEffect,useMemo,useState } from 'react'
import { endpoints } from '../api/endpoints'
import useToast from '../hooks/useToast'
const C=createContext(null)
export function AppProvider({children}){const[stats,setStats]=useState(null);const[logs,setLogs]=useState([]);const[subscriptions,setSubscriptions]=useState({});const[channels,setChannels]=useState([]);const[backendOnline,setBackendOnline]=useState(true);const[runningDemo,setRunningDemo]=useState(false);const[demoProgress,setDemoProgress]=useState(0);const{toasts,pushToast,removeToast}=useToast();const refreshAll=async()=>{try{const[s,l,sub,c]=await Promise.all([endpoints.stats(),endpoints.logs(),endpoints.subscriptions(),endpoints.channels()]);setStats(s.data);setLogs(l.data);setSubscriptions(sub.data);setChannels(c.data);setBackendOnline(true)}catch{setBackendOnline(false)}};useEffect(()=>{refreshAll()},[]);const runDemo=async()=>{if(runningDemo)return;setRunningDemo(true);const steps=[()=>endpoints.orderEvent({user_id:101,recipient:'hassan@example.com',order_id:'ORD-DEMO-01'}),()=>endpoints.securityAlert({user_id:101,recipient:'arham@example.com',ip_address:'10.0.0.1'}),()=>endpoints.passwordReset({user_id:102,recipient:'usman@example.com'}),()=>endpoints.promotional({recipients:['arham@example.com','usman@example.com'],message:'50% off!'}),()=>endpoints.refund({recipient:'hassan@example.com',amount:1200})];try{for(let i=0;i<steps.length;i+=1){await steps[i]();setDemoProgress(Math.round(((i+1)/steps.length)*100));await new Promise(r=>setTimeout(r,800))}await refreshAll();pushToast({type:'success',message:'Demo complete — 11 notifications fired'})}catch(e){pushToast({type:'error',message:e?.response?.data?.detail||'Demo failed'})}finally{setRunningDemo(false);setTimeout(()=>setDemoProgress(0),800)}};const v=useMemo(()=>({stats,setStats,logs,setLogs,subscriptions,setSubscriptions,channels,setChannels,backendOnline,refreshAll,toasts,pushToast,removeToast,runDemo,runningDemo,demoProgress}),[stats,logs,subscriptions,channels,backendOnline,toasts,runningDemo,demoProgress]);return <C.Provider value={v}>{children}</C.Provider>}
export const useApp=()=>useContext(C)
""",
    "src/components/ui/Card.jsx": """export default function Card({children,className=''}){return <div className={`rounded-xl border border-[rgba(255,255,255,0.08)] bg-[#1a1a24] p-4 ${className}`}>{children}</div>}
""",
    "src/components/ui/Badge.jsx": """const map={email:'bg-[#3b82f633] text-[#93c5fd] border-[#3b82f666]',sms:'bg-[#f59e0b33] text-[#fbbf24] border-[#f59e0b66]',push:'bg-[#6c63ff33] text-[#a5a0ff] border-[#6c63ff66]',whatsapp:'bg-[#25d36633] text-[#25d366] border-[#25d36666]',success:'bg-[#22c55e33] text-[#4ade80] border-[#22c55e66]',failed:'bg-[#ef444433] text-[#f87171] border-[#ef444466]'}
export default function Badge({type,children,className=''}){return <span className={`inline-flex rounded-full border px-2 py-0.5 text-xs ${map[type]||'bg-[#22222f] text-[#f1f1f3] border-[rgba(255,255,255,0.1)]'} ${className}`}>{children}</span>}
""",
    "src/components/ui/Spinner.jsx": """export default function Spinner(){return <span className='inline-block h-4 w-4 animate-spin rounded-full border-2 border-[rgba(255,255,255,0.2)] border-t-[#6c63ff]'/>}
""",
    "src/components/ui/Button.jsx": """import Spinner from './Spinner'
export default function Button({children,loading,className='',variant='primary',...props}){const v={primary:'bg-[#6c63ff] hover:bg-[#7c73ff] text-white',danger:'bg-[#ef4444] text-white',neutral:'bg-[#22222f] text-[#f1f1f3] border border-[rgba(255,255,255,0.08)]'};return <button className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 transition disabled:opacity-60 ${v[variant]} ${className}`} disabled={loading||props.disabled} {...props}>{loading&&<Spinner/>}{children}</button>}
""",
    "src/components/ui/Skeleton.jsx": """export default function Skeleton({className=''}){return <div className={`animate-pulse rounded bg-[#22222f] ${className}`}/>}
""",
    "src/components/ui/Modal.jsx": """import Button from './Button'
export default function Modal({open,title,children,onConfirm,onClose}){if(!open)return null;return <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4'><div className='w-full max-w-md rounded-xl border border-[rgba(255,255,255,0.08)] bg-[#1a1a24] p-5'><h3 className='text-lg font-semibold'>{title}</h3><div className='mt-3 text-[#9898a8]'>{children}</div><div className='mt-5 flex justify-end gap-2'><Button variant='neutral' onClick={onClose}>Cancel</Button><Button variant='danger' onClick={onConfirm}>Confirm</Button></div></div></div>}
""",
    "src/components/ui/Tabs.jsx": """export default function Tabs({tabs,active,onChange}){return <div className='mb-4 flex gap-2'>{tabs.map(t=><button key={t} onClick={()=>onChange(t)} className={`rounded-lg px-3 py-1.5 text-sm ${active===t?'bg-[#6c63ff] text-white':'bg-[#22222f] text-[#9898a8]'}`}>{t}</button>)}</div>}
""",
    "src/components/ui/CodeBlock.jsx": """import Button from './Button'
export default function CodeBlock({code}){const lines=code.split('\\n');return <div className='rounded-xl border border-[rgba(255,255,255,0.08)] bg-[#0d1117] p-3'><div className='mb-2 flex justify-end'><Button variant='neutral' className='px-2 py-1 text-xs' onClick={()=>navigator.clipboard.writeText(code)}>Copy</Button></div><pre className='overflow-auto text-xs leading-6 text-[#d1d5db]'>{lines.map((l,i)=><div key={i}><span className='mr-3 inline-block w-6 text-right text-[#5a5a6e]'>{i+1}</span>{l}</div>)}</pre></div>}
""",
    "src/charts/Sparkline.jsx": """export default function Sparkline({values=[]}){if(!values.length)return null;const w=120,h=28,max=Math.max(...values,1),min=Math.min(...values,0),range=max-min||1;const points=values.map((v,i)=>`${(i/(values.length-1||1))*w},${h-((v-min)/range)*h}`).join(' ');return <svg viewBox={`0 0 ${w} ${h}`} className='h-7 w-full'><polyline fill='none' stroke='#6c63ff' strokeWidth='2' points={points}/></svg>}
""",
    "src/components/ui/StatCard.jsx": """import { useEffect,useState } from 'react'
import Card from './Card'
import Sparkline from '../charts/Sparkline'
export default function StatCard({title,value=0,icon:Icon}){const[display,setDisplay]=useState(value);const[history,setHistory]=useState([value]);useEffect(()=>{const s=display,d=value-s;let f=0;const id=setInterval(()=>{f+=1;setDisplay(Math.round(s+(d*f)/10));if(f>=10)clearInterval(id)},16);setHistory(p=>[...p.slice(-9),value]);return()=>clearInterval(id)},[value]);return <Card><div className='flex items-center justify-between'><div><p className='text-sm text-[#9898a8]'>{title}</p><p className='text-2xl font-semibold'>{display}</p></div>{Icon&&<Icon/>}</div><Sparkline values={history}/></Card>}
""",
    "src/components/layout/ToastContainer.jsx": """export default function ToastContainer({toasts,onClose}){return <div className='fixed right-4 top-4 z-[70] flex w-80 flex-col gap-2'>{toasts.map(t=><div key={t.id} className='animate-fade-in rounded-lg border border-[rgba(255,255,255,0.08)] bg-[#1a1a24] p-3 text-sm'><div className='flex items-start justify-between gap-2'><span>{t.message}</span><button onClick={()=>onClose(t.id)}>x</button></div></div>)}</div>}
""",
    "src/components/layout/Header.jsx": """import { Bell } from 'lucide-react'
import Button from '../ui/Button'
export default function Header({currentLabel,runDemo,runningDemo,demoProgress}){return <header className='fixed inset-x-0 top-0 z-40 h-14 border-b border-[rgba(255,255,255,0.08)] bg-[#13131a] px-4'><div className='mx-auto flex h-full max-w-[1600px] items-center justify-between'><div className='flex items-center gap-2'><Bell size={18}/><span className='font-medium'>Smart Notification System</span></div><div className='text-sm text-[#9898a8]'>{currentLabel}</div><div className='flex items-center gap-3'><span className='hidden text-xs text-[#9898a8] md:block'>SE Project · Group 23K</span><Button onClick={runDemo} loading={runningDemo}>Run Demo</Button></div></div>{runningDemo&&<div className='h-1 bg-[#22222f]'><div className='h-1 bg-[#6c63ff] transition-all' style={{width:`${demoProgress}%`}}/></div>}</header>}
""",
    "src/components/layout/Sidebar.jsx": """import { LayoutDashboard,Zap,ScrollText,Lock,Boxes,Eye,GitBranch,ArrowLeftRight,Radio,CheckSquare } from 'lucide-react'
const items=[['Overview','overview',LayoutDashboard],['Fire Events','fire-events',Zap],['Live Logs','live-logs',ScrollText],['Singleton','singleton',Lock],['Factory','factory',Boxes],['Observer','observer',Eye],['Strategy','strategy',GitBranch],['Before vs After','before-after',ArrowLeftRight],['Channels','channels',Radio],['Test Results','test-results',CheckSquare]]
export default function Sidebar({currentPage,setCurrentPage}){return <aside className='fixed left-0 top-14 z-30 hidden h-[calc(100vh-56px)] w-[260px] border-r border-[rgba(255,255,255,0.08)] bg-[#13131a] p-4 md:block'>{items.map(([label,key,Icon])=>{const a=currentPage===key;return <button key={key} onClick={()=>setCurrentPage(key)} className={`mb-1 flex w-full items-center gap-2 rounded-lg border-l-2 px-3 py-2 text-sm ${a?'border-l-[#6c63ff] bg-[#22222f] text-[#6c63ff]':'border-l-transparent text-[#9898a8] hover:bg-[#1a1a24]'}`}><Icon size={16}/>{label}</button>})}</aside>}
""",
    "src/components/layout/Layout.jsx": """import Header from './Header'
import Sidebar from './Sidebar'
import ToastContainer from './ToastContainer'
import { useApp } from '../../context/AppContext'
export default function Layout({currentPage,currentLabel,setCurrentPage,children}){const{toasts,removeToast,runDemo,runningDemo,demoProgress,backendOnline}=useApp();return <div className='min-h-screen bg-[#0f0f13] text-[#f1f1f3]'><Header currentLabel={currentLabel} runDemo={runDemo} runningDemo={runningDemo} demoProgress={demoProgress}/>{!backendOnline&&<div className='fixed top-14 z-20 w-full bg-[#ef444433] px-4 py-2 text-center text-sm text-[#fca5a5]'>⚠ Backend offline — start the API with: uvicorn api:app --reload --port 8000</div>}<Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage}/><main className='pt-16 md:pl-[260px]'><div className='p-4 animate-fade-in'>{children}</div></main><ToastContainer toasts={toasts} onClose={removeToast}/></div>}
""",
    "src/pages/Overview.jsx": page_component("Overview"),
    "src/pages/FireEvents.jsx": page_component("FireEvents"),
    "src/pages/LiveLogs.jsx": page_component("LiveLogs"),
    "src/pages/SingletonPage.jsx": page_component("SingletonPage"),
    "src/pages/FactoryPage.jsx": page_component("FactoryPage"),
    "src/pages/ObserverPage.jsx": page_component("ObserverPage"),
    "src/pages/StrategyPage.jsx": page_component("StrategyPage"),
    "src/pages/BeforeAfter.jsx": page_component("BeforeAfter"),
    "src/pages/ChannelsPage.jsx": page_component("ChannelsPage"),
    "src/pages/TestResults.jsx": page_component("TestResults"),
    "src/App.jsx": """import { useMemo,useState } from 'react'
import Layout from './components/layout/Layout'
import Overview from './pages/Overview'
import FireEvents from './pages/FireEvents'
import LiveLogs from './pages/LiveLogs'
import SingletonPage from './pages/SingletonPage'
import FactoryPage from './pages/FactoryPage'
import ObserverPage from './pages/ObserverPage'
import StrategyPage from './pages/StrategyPage'
import BeforeAfter from './pages/BeforeAfter'
import ChannelsPage from './pages/ChannelsPage'
import TestResults from './pages/TestResults'
const pages={'overview':['Overview',Overview],'fire-events':['Fire Events',FireEvents],'live-logs':['Live Logs',LiveLogs],'singleton':['Singleton',SingletonPage],'factory':['Factory',FactoryPage],'observer':['Observer',ObserverPage],'strategy':['Strategy',StrategyPage],'before-after':['Before vs After',BeforeAfter],'channels':['Channels',ChannelsPage],'test-results':['Test Results',TestResults]}
export default function App(){const[currentPage,setCurrentPage]=useState('overview');const[label,Page]=useMemo(()=>pages[currentPage],[currentPage]);return <Layout currentPage={currentPage} setCurrentPage={setCurrentPage} currentLabel={label}><Page/></Layout>}
""",
}


def main() -> None:
    for old in [
        ROOT / "src/main.ts",
        ROOT / "src/counter.ts",
        ROOT / "src/style.css",
        ROOT / "src/assets/vite.svg",
        ROOT / "src/assets/typescript.svg",
        ROOT / "tsconfig.json",
    ]:
        old.unlink(missing_ok=True)

    for rel, content in FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    pkg_path = ROOT / "package.json"
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    pkg["scripts"] = {"dev": "vite", "build": "vite build", "preview": "vite preview"}
    pkg.setdefault("dependencies", {})
    pkg["dependencies"]["react"] = "^18.3.1"
    pkg["dependencies"]["react-dom"] = "^18.3.1"
    pkg.setdefault("devDependencies", {})
    pkg["devDependencies"]["@vitejs/plugin-react"] = "^5.1.0"
    pkg["devDependencies"].pop("typescript", None)
    pkg_path.write_text(json.dumps(pkg, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
