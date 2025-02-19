// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ParamitaNFT is ERC721, Ownable {
    uint256 public nextTokenId;
    mapping(uint256 => string) public tokenRarity;

    constructor() ERC721("ParamitaNFT", "PNFT") {}

    function mintNFT(address recipient, uint256 rewardAmount) external onlyOwner {
        uint256 tokenId = nextTokenId++;
        _safeMint(recipient, tokenId);

        if (rewardAmount < 1000) {
            tokenRarity[tokenId] = "Common";
        } else if (rewardAmount < 5000) {
            tokenRarity[tokenId] = "Rare";
        } else {
            tokenRarity[tokenId] = "Legendary";
        }
    }

    function getTokenRarity(uint256 tokenId) external view returns (string memory) {
        return tokenRarity[tokenId];
    }
}