
export function NDVIMap({ndvi=0.68}){
  const cells = Array.from({length:64},(_,i)=> Math.random()*0.4+0.4)
  return <div className="grid grid-cols-8 gap-1">
    {cells.map((v,i)=><div key={i} className="h-6 rounded" style={{background: v>0.65?'#16a34a': v>0.45?'#facc15':'#dc2626'}}/>)}
  </div>
}
