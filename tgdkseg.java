const logTransaction = async (txHash, userId) => {
    const log = { txHash, userId, timestamp: Date.now() };
    await azureMonitor.log(log);
};