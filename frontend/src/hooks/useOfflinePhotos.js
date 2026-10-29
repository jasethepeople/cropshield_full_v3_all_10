
import { useState } from "react"
export function useOfflinePhotos(){
  const [pending, setPending] = useState(0)
  const saveOffline = async (file) => {
    const db = await new Promise((res,rej)=>{
      const r = indexedDB.open("cropshield",1)
      r.onupgradeneeded = e=> e.target.result.createObjectStore("pending_photos",{keyPath:"id",autoIncrement:true})
      r.onsuccess = ()=> res(r.result)
    })
    const tx = db.transaction("pending_photos","readwrite")
    tx.objectStore("pending_photos").add({blob: file, timestamp: Date.now(), farm_id: "clark_22"})
    setPending(p=> p+1)
    if('serviceWorker' in navigator && 'SyncManager' in window){
      const reg = await navigator.serviceWorker.ready
      await reg.sync.register("upload-photos")
    }
  }
  return { saveOffline, pending }
}
