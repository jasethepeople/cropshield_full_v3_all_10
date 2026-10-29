# CropShield - Turnkey Parametric Crop Insurance for Small Farms
Turnkey stack: FastAPI + Sentinel-2 + Chainlink + Solidity + React + IPFS

## Quickstart
cp .env.example .env
docker-compose up --build
Backend: http://localhost:8000/docs
Frontend: http://localhost:3000
Hardhat: http://localhost:8545

## Flow
1. Farmer draws field on map
2. Backend fetches Sentinel-2, computes NDVI/NDMI/LST, pins to IPFS
3. Weekly job checks SPI + temp triggers
4. If trigger -> Chainlink Functions -> contract triggerPayout -> USDC to farmer
5. Co-op pool rebalances
