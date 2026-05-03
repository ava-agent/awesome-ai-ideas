/**
 * GigFlex AI - Income Prediction Function
 * Predicts gig worker income based on historical data and trends
 * 
 * @param {Array} historicalData - Array of past earnings data
 * @param {Object} factors - External factors affecting income (weather, events, etc.)
 * @returns {Object} Prediction result with confidence interval
 */
function predictIncome(historicalData, factors = {}) {
    const avg = historicalData.reduce((sum, val) => sum + val, 0) / historicalData.length;
    const volatility = Math.sqrt(historicalData.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / historicalData.length);
    const trend = historicalData.length > 1 ? (historicalData[historicalData.length - 1] - historicalData[0]) / historicalData.length : 0;
    
    const prediction = avg + trend + (factors.boost || 0);
    const confidence = {
        low: Math.max(0, prediction - volatility),
        high: prediction + volatility,
        confidence: Math.max(0, 1 - (volatility / prediction))
    };
    
    return {
        prediction: Math.round(prediction * 100) / 100,
        confidence,
        factors
    };
}