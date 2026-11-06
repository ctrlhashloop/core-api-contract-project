import { PactV3, MatchersV3 } from "@pact-foundation/pact";
import { getAccountById } from "./client"; // your API client

const { like, uuid } = MatchersV3;

const provider = new PactV3({
  consumer: "WebFrontendClient",
  provider: "CoreBankingService",
});

describe("Get Account API", () => {
  it("returns account details when valid ID is provided", async () => {
    const accountId = "123e4567-e89b-12d3-a456-426614174000";

    provider
      .given("account exists with id 123e4567-e89b-12d3-a456-426614174000")
      .uponReceiving("a request for account details")
      .withRequest({
        method: "GET",
        path: `/accounts/${accountId}`,
      })
      .willRespondWith({
        status: 200,
        headers: { "Content-Type": "application/json" },
        body: {
          id: accountId,
          accountNumber: like("ACC-987654"),
          balance: like(1500.5),
          currency: "USD",
        },
      });

    await provider.executeTest(async (mockServer) => {
      const response = await getAccountById(mockServer.url, accountId);
      expect(response.status).toEqual(200);
      expect(response.data.currency).toEqual("USD");
    });
  });
});
