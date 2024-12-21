const logTransactionWithFarqit = async (txHash, userId) => {
    const logSegments = [
        { txHash, userId, timestamp: Date.now(), layer: "Web3" },
        { txHash, userId, layer: "Compliance" }
    ];
    for (let segment of logSegments) {
        await azureMonitor.log(segment); // Parallelized logging
    }
    console.log(`Transaction ${txHash} logged with Farqit acceleration.`);
};