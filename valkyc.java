const validateKYC = async (userId) => {
    const response = await axios.post('https://api.persona.com/validate', { userId });
    if (response.data.status === "approved") {
        console.log(`User ${userId} approved.`);
    } else {
        console.log(`User ${userId} flagged for review.`);
    }
};