import { useEffect,useState } from 'react'
import Card from './Card'
import Sparkline from '../../charts/Sparkline'
export default function StatCard({title,value=0,icon:Icon}){const[display,setDisplay]=useState(value);const[history,setHistory]=useState([value]);useEffect(()=>{const s=display,d=value-s;let f=0;const id=setInterval(()=>{f+=1;setDisplay(Math.round(s+(d*f)/10));if(f>=10)clearInterval(id)},16);setHistory(p=>[...p.slice(-9),value]);return()=>clearInterval(id)},[value]);return <Card><div className='flex items-center justify-between'><div><p className='text-sm text-[#9898a8]'>{title}</p><p className='text-2xl font-semibold'>{display}</p></div>{Icon&&<Icon/>}</div><Sparkline values={history}/></Card>}
