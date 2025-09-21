import { useEffect, useState } from "react";

function History() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError("");
      try {
        const response = await fetch("http://localhost:8080/oracle/valid-transactions");
        if (!response.ok) throw new Error("Failed to fetch");
        const result = await response.json();
        for (let index = 0; index < 100; index++) {
          result.push(result[0])  
        }
        setData(result);
      } catch (err) {
        setError("Error fetching history");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-gray-900 px-4">
      <h1 className="text-4xl font-bold text-white mb-4">Transaction History</h1>
      {loading && <p className="text-blue-200 mb-4">Loading...</p>}
      {error && <p className="text-red-400 mb-4">{error}</p>}
      {!loading && !error && (
        <div className="overflow-x-auto w-full ">
          <table className="min-w-full bg-gray-800 rounded-lg shadow-lg">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left text-purple-300">Sender</th>
                <th className="px-4 py-2 text-left text-purple-300">Receiver</th>
                <th className="px-4 py-2 text-left text-purple-300">Amount</th>
                <th className="px-4 py-2 text-left text-purple-300">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {data.map((tx, idx) => (
                <tr key={idx} className="border-b border-gray-700 hover:bg-gray-700 transition">
                  <td className="px-4 py-2 text-blue-200 font-mono">{tx.sender}</td>
                  <td className="px-4 py-2 text-blue-200 font-mono">{tx.receiver}</td>
                  <td className="px-4 py-2 text-green-300 font-bold">{tx.amount}</td>
                  <td className="px-4 py-2 text-yellow-200">
                    {new Date(tx.timestamp * 1000).toLocaleString()}
                  </td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-4 py-2 text-center text-gray-400">
                    No transactions found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default History;