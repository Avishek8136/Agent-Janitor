export class PaymentGateway {
    private apiKey: string;

    constructor(apiKey: string) {
        this.apiKey = apiKey;
    }

    // TODO(PAY-202): implement webhook idempotency key deduplication
    async processPayment(amount: number, currency: string) {
        console.log(`Processing ${amount} ${currency}`);
        return { success: true, txnId: "tx_12345" };
    }

    // TODO(CORE-707): rewrite retry logic to use exponential backoff with jitter
    async checkRefundStatus(refundId: string) {
        return { status: "pending", id: refundId };
    }
}
