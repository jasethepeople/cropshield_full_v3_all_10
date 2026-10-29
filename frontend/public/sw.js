
const CACHE = "cropshield-v2";
self.addEventListener("install", e=> e.waitUntil(caches.open(CACHE).then(c=> c.addAll(["/","/index.html"]))));
self.addEventListener("fetch", e=> {
  e.respondWith(
    caches.match(e.request).then(cached=> {
      return cached || fetch(e.request).then(res=>{
        if(e.request.method==="GET") caches.open(CACHE).then(c=> c.put(e.request, res.clone()));
        return res;
      });
    })
  )
});
// Background sync for photo uploads
self.addEventListener("sync", e=> {
  if(e.tag==="upload-photos") e.waitUntil(uploadPendingPhotos());
});
async function uploadPendingPhotos(){
  const db = await openDB();
  const photos = await db.getAll("pending_photos");
  for(const p of photos){
    await fetch("http://localhost:8000/field/upload_photo", {method:"POST", body: p.blob});
    await db.delete("pending_photos", p.id);
  }
}
function openDB(){ return new Promise((res,rej)=>{ const r=indexedDB.open("cropshield",1); r.onupgradeneeded=e=> e.target.result.createObjectStore("pending_photos",{keyPath:"id",autoIncrement:true}); r.onsuccess=()=> res({getAll: (s)=> new Promise(r2=>{ const tx=r.result.transaction(s); const req=tx.objectStore(s).getAll(); req.onsuccess=()=> r2(req.result)}), delete: (s,id)=>{ const tx=r.result.transaction(s,"readwrite"); tx.objectStore(s).delete(id)}}); }); }
