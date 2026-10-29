// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
contract CropShield is Ownable {
    IERC20 public usdc;
    address public oracle;
    struct Policy { address farmer; uint256 coverage; int256 droughtTrigger; uint256 heatTrigger; uint256 premium; bool active; string ipfsCid; }
    uint256 public nextPolicyId;
    mapping(uint256 => Policy) public policies;
    event PolicyCreated(uint256 id, address farmer, uint256 coverage);
    event Payout(uint256 id, uint256 amount, uint256 pct, string ipfsHash, string reason);
    constructor(address _usdc, address _oracle) Ownable(msg.sender) { usdc = IERC20(_usdc); oracle = _oracle; }
    function setOracle(address _oracle) external onlyOwner { oracle = _oracle; }
    function createPolicy(address farmer, uint256 coverage, int256 droughtT, uint256 heatT, uint256 premium) external returns (uint256) {
        uint256 id = nextPolicyId++;
        policies[id] = Policy(farmer, coverage, droughtT, heatT, premium, true, "");
        emit PolicyCreated(id, farmer, coverage);
        return id;
    }
    function triggerPayout(uint256 policyId, int256 spi, uint256 tempMax, uint256 payoutPct, string calldata ipfsHash, string calldata reason) external {
        require(msg.sender == oracle, "not oracle");
        Policy storage p = policies[policyId];
        require(p.active, "inactive");
        uint256 amount = (p.coverage * payoutPct) / 100;
        p.active = false;
        p.ipfsCid = ipfsHash;
        usdc.transfer(p.farmer, amount);
        emit Payout(policyId, amount, payoutPct, ipfsHash, reason);
    }
}
