
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract DisputeDAO {
    struct Dispute { uint256 policyId; address farmer; string reason; string photoIpfs; uint256 votesFor; uint256 votesAgainst; bool resolved; bool overturned; mapping(address=>bool) voted; }
    uint256 public nextDisputeId;
    mapping(uint256=>Dispute) public disputes;
    mapping(string=>address[]) public coopMembers; // coopId => members

    event DisputeOpened(uint256 id, uint256 policyId, address farmer);
    event Voted(uint256 id, address voter, bool support);
    event Resolved(uint256 id, bool overturned);

    function openDispute(uint256 policyId, string calldata reason, string calldata photoIpfs) external returns(uint256){
        uint256 id = nextDisputeId++;
        Dispute storage d = disputes[id];
        d.policyId = policyId; d.farmer = msg.sender; d.reason = reason; d.photoIpfs = photoIpfs;
        emit DisputeOpened(id, policyId, msg.sender);
        return id;
    }
    function vote(uint256 disputeId, bool support) external {
        Dispute storage d = disputes[disputeId];
        require(!d.voted[msg.sender], "already voted");
        d.voted[msg.sender]=true;
        if(support) d.votesFor++; else d.votesAgainst++;
        emit Voted(disputeId, msg.sender, support);
    }
    function resolve(uint256 disputeId) external {
        Dispute storage d = disputes[disputeId];
        require(!d.resolved, "resolved");
        require(d.votesFor + d.votesAgainst >= 3, "need 3 votes");
        d.resolved = true;
        d.overturned = d.votesFor > d.votesAgainst;
        emit Resolved(disputeId, d.overturned);
    }
}
