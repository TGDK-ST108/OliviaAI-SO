const distributeTokens = async (recipient, amount) => {
    const tx = await contract.methods.transfer(recipient, amount).send({
        from: ownerAddress,
        gas: 2000000,
    });
    console.log(`Distributed ${amount} TGDK Tokens to ${recipient}`);
};

distributeTokens("0xYourWalletAddressHere", 1000);