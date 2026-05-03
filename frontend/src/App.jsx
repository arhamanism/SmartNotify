import { useMemo,useState } from 'react'
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
const pages={'overview':['Overview & Live Status',Overview],'fire-events':['Manual Event Firing',FireEvents],'live-logs':['Live Notification Logs',LiveLogs],'singleton':['Singleton Pattern',SingletonPage],'factory':['Factory Pattern',FactoryPage],'observer':['Observer Pattern',ObserverPage],'strategy':['Strategy Pattern',StrategyPage],'before-after':['Before vs After Comparison',BeforeAfter],'channels':['Channel Guide',ChannelsPage],'test-results':['Testing & Verification',TestResults]}
export default function App(){const[currentPage,setCurrentPage]=useState('overview');const[label,Page]=useMemo(()=>pages[currentPage],[currentPage]);return <Layout currentPage={currentPage} setCurrentPage={setCurrentPage} currentLabel={label}><Page/></Layout>}
