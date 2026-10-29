
import { usePrivy } from "@privy-io/react-auth"
export function PrivyWallet(){
  const { login, logout, authenticated, user } = usePrivy()
  return (
    <div className="bg-white p-4 rounded-2xl">
      {authenticated ? <>
        <div className="text-sm">Logged in as {user?.email?.address}</div>
        <div className="text-xs font-mono">Wallet: {user?.wallet?.address?.slice(0,10)}...</div>
        <button onClick={logout} className="mt-2 text-xs underline">Logout</button>
      </> : <button onClick={login} className="bg-black text-white px-4 py-2 rounded">Login with Email - No Seed Phrase</button>}
    </div>
  )
}
// In main.jsx wrap with <PrivyProvider appId={import.meta.env.VITE_PRIVY_APP_ID}>
