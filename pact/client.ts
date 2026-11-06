import axios from "axios";

export async function getAccountById(baseUrl: string, accountId: string) {
  return axios.get(`${baseUrl}/accounts/${accountId}`, {
    headers: {
      Accept: "application/json",
    },
  });
}
