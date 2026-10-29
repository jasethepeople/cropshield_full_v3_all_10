
export function CoopPool({coop}){
  return <div className="grid grid-cols-3 gap-2">
    {coop.farms.map(f=> <div key={f.id} className="bg-green-50 p-3 rounded-xl"><div className="font-bold">{f.name}</div><div className="text-xs">{f.acres} ac - ${f.share} - Trust {f.trust}</div></div>)}
  </div>
}
