const transferTokens = async (recipient, amount) => {
    const tx = await contract.methods.transfer(recipient, amount).send({
        from: senderAddress,
        gas: 2000000,
    });
    console.log(`Transaction successful: ${tx.transactionHash}`);
};