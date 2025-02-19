// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ParamitaFusionToken is ERC20, Ownable {
    constructor() ERC20("ParamitaFusion", "PFT") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mintTokens(address recipient, uint256 amount) external onlyOwner {
        _mint(recipient, amount);
    }
}

contract ParamitaNFT is ERC721, Ownable {
    uint256 public nextTokenId;

    constructor() ERC721("ParamitaNFT", "PNFT") {}

    function mintNFT(address recipient) external onlyOwner {
        _safeMint(recipient, nextTokenId);
        nextTokenId++;
    }
}

contract ParamitaStaking {
    struct Stake {
        uint256 amount;
        uint256 reward;
        uint256 stakeTime;
        string poolType;
    }

    mapping(address => Stake) public stakes;
    ParamitaFusionToken public rewardToken;
    ParamitaNFT public rewardNFT;

    constructor(address _rewardToken, address _rewardNFT) {
        rewardToken = ParamitaFusionToken(_rewardToken);
        rewardNFT = ParamitaNFT(_rewardNFT);
    }

    function stake(uint256 amount, string memory poolType) external {
        require(amount > 0, "Cannot stake zero.");

        uint256 reward = calculateReward(amount, poolType);
        stakes[msg.sender] = Stake(amount, reward, block.timestamp, poolType);
        
        rewardToken.mintTokens(msg.sender, reward);

        if (reward > 1000) {
            rewardNFT.mintNFT(msg.sender);
        }
    }

    function calculateReward(uint256 amount, string memory poolType) private pure returns (uint256) {
        if (keccak256(abi.encodePacked(poolType)) == keccak256(abi.encodePacked("nuclear"))) {
            return amount * 2;
        } else if (keccak256(abi.encodePacked(poolType)) == keccak256(abi.encodePacked("volcanic"))) {
            return amount * 1.5;
        } else {
            return amount * 1.75;
        }
    }

    function unstake() external {
        Stake memory userStake = stakes[msg.sender];
        require(userStake.amount > 0, "No active stake found.");

        rewardToken.mintTokens(msg.sender, userStake.reward);
        delete stakes[msg.sender];
    }
}