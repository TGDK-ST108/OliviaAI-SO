const transferTokens = async (recipient, amount) => {
    const tx = await contract.methods.transfer(recipient, amount).send({
        from: ownerAddress, // Contract owner or designated sender
        gas: 2000000,
    });
    console.log(`Transferred ${amount} TGDK Tokens to ${recipient}`);
};

transferTokens("0xYourWalletAddressHere", 1000); // Transfer 1000 TGDK Tokens