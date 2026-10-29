Wrap App in PrivyProvider in main.jsx:
import {PrivyProvider} from '@privy-io/react-auth'
<PrivyProvider appId={import.meta.env.VITE_PRIVY_APP_ID} config={{embeddedWallets:{createOnLogin:'users-without-wallets'}}}><App/></PrivyProvider>