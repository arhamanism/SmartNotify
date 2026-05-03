import Header from './Header'
import Sidebar from './Sidebar'
import ToastContainer from './ToastContainer'
import { useApp } from '../../context/AppContext'
export default function Layout({currentPage,currentLabel,setCurrentPage,children}){const{toasts,removeToast,runDemo,runningDemo,demoProgress,backendOnline}=useApp();return <div className='min-h-screen bg-[#0f0f13] text-[#f1f1f3]'><Header currentLabel={currentLabel} runDemo={runDemo} runningDemo={runningDemo} demoProgress={demoProgress}/>{!backendOnline&&<div className='fixed top-14 z-20 w-full bg-[#ef444433] px-4 py-2 text-center text-sm text-[#fca5a5]'>⚠ Backend offline — start the API with: uvicorn api:app --reload --port 8000</div>}<Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage}/><main className='pt-16 md:pl-[260px]'><div className='p-4 animate-fade-in'>{children}</div></main><ToastContainer toasts={toasts} onClose={removeToast}/></div>}
