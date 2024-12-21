const provideLiquidity = async (tokenAmount, ethAmount) => {
    const tx = await dexContract.methods.addLiquidity(tokenAddress, tokenAmount, ethAmount).send({
        from: liquidityPoolAddress,
        gas: 3000000,
    });
    console.log(`Added liquidity: ${tokenAmount} TGDK and ${ethAmount} ETH`);
};

provideLiquidity(5000, 1); // Add liquidity to DEX