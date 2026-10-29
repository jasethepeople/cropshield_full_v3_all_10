
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
contract RiskMarketplace {
    IERC20 public usdc;
    struct Listing { address seller; string riskType; uint256 amount; uint256 premium; bool sold; address buyer; }
    Listing[] public listings;
    constructor(address _usdc){ usdc = IERC20(_usdc); }
    function listRisk(string calldata riskType, uint256 amount, uint256 premium) external { listings.push(Listing(msg.sender, riskType, amount, premium, false, address(0))); }
    function buyRisk(uint256 id) external { Listing storage l = listings[id]; require(!l.sold); usdc.transferFrom(msg.sender, l.seller, l.premium); l.sold=true; l.buyer=msg.sender; }
}
