import { useEffect,useRef } from 'react'
export default function usePolling(callback,interval,enabled=true){const ref=useRef(callback);ref.current=callback;useEffect(()=>{if(!enabled||!interval)return;const id=setInterval(()=>ref.current(),interval);return()=>clearInterval(id)},[interval,enabled])}
