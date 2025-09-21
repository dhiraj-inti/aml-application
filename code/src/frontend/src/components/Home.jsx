import { useEffect, useState } from "react";
import toast, { Toaster } from 'react-hot-toast';

function Home() {
  const [csvFile, setCsvFile] = useState(null);
  const [apiMessage, setApiMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showResponse, setShowResponse] = useState(false);
  const [responseData, setResponseData] = useState(null);

  // New state for inputs
  const [sender, setSender] = useState("");
  const [receiver, setReceiver] = useState("");
  const [amount, setAmount] = useState("");
  const [timestamp, setTimestamp] = useState("");

  const handleFileChange = (e) => {
    setCsvFile(e.target.files[0]);
    console.log(e.target.files[0]);

    setApiMessage("");
    setShowResponse(false);
    setResponseData(null);
  };

  useEffect(() => {
    const fetchCSVStatus = async () => {
      try {
        const response = await fetch("http://localhost:5000/check-csv");
        const data = await response.json();
        if (response.status === 200) {
          if (data.exists) {
            setCsvFile({ name: "exists" });
          } else {
            setCsvFile(null);
          }
        } else {
          toast.error(data.message || "Error submitting data");
        }
      } catch (error) {}
    };

    fetchCSVStatus();
  }, []);

  const handleUploadFile = async (e) => {
    e.preventDefault();
    setLoading(true);
    setApiMessage("");
    setShowResponse(false);
    setResponseData(null);
    let csvBase64 = "";
    if (csvFile) {
      const fileReader = new FileReader();
      await new Promise((resolve, reject) => {
        fileReader.onload = () => {
          const result = fileReader.result.split(",")[1]; // Remove data:...;base64,
          csvBase64 = result;
          resolve();
        };
        fileReader.onerror = reject;
        fileReader.readAsDataURL(csvFile);
      });
    }

    try {
      // Example POST request
      const response = await fetch("http://localhost:5000/input-csv", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ csv_base64: csvBase64 }),
      });
      const data = await response.json();
      if (response.status === 200) {
        toast.success(data.message);
      } else {
        toast.error("Error submitting data");
      }
    } catch (error) {
      toast.error("Error submitting data");
    } finally {
      setLoading(false);
    }
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setApiMessage("");
    setShowResponse(false);
    setResponseData(null);

    // Prepare payload
    const payload = {
      sender,
      receiver,
      amount,
      timestamp: timestamp ? new Date(timestamp).toISOString().replace('Z', '') : "",
    };
    console.log(payload);
    

    try {
      // Example POST request
      const response = await fetch('http://localhost:5000/aml-checks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      console.log(data);
      
      if (response.status === 200) {
      setResponseData(payload); // For demo, show payload
      setShowResponse(true);
      } else {
        setApiMessage(data.message || 'Error submitting data');
      }
    } catch (error) {
      setApiMessage("Error submitting data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex flex-col items-center justify-center font-sans relative">
      <Toaster />
      <div className="flex items-center gap-4 mb-8">
        <img
          src="https://www.svgrepo.com/show/303287/bitcoin-logo.svg"
          className="h-12"
          alt="Bitcoin logo"
        />
        <img
          src="https://www.svgrepo.com/show/464900/ethereum.svg"
          className="h-12"
          alt="Ethereum logo"
        />
      </div>
      <h1 className="text-4xl font-bold text-white mb-2">
        Blockchain CSV Uploader
      </h1>
      <p className="text-lg text-blue-200 mb-6">
        Enter transaction details and upload your transaction CSV (sender,
        receiver, amount, timestamp).
      </p>
     
      <div className="bg-gray-800 rounded-xl shadow-lg p-8 w-full max-w-md mb-6">
        <label className="block text-white mb-2 font-semibold">Step-1</label>
        <label className="block text-white mb-2 font-semibold">
          CSV File (History)
        </label>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="block w-full text-gray-200 bg-gray-700 border border-gray-600 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {csvFile && (
          <div className="flex items-center justify-between bg-blue-900 text-blue-100 rounded px-3 py-2 mb-4 shadow">
            <span className="truncate">History CSV exists</span>
            <button
              onClick={() => setCsvFile(null)}
              className="ml-2 text-blue-300 hover:text-blue-500 font-bold text-lg"
              aria-label="Delete CSV"
              type="button"
            >
              ×
            </button>
          </div>
        )}
        <button
          onClick={handleUploadFile}
          disabled={!csvFile || loading}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-2 px-4 rounded hover:from-blue-700 hover:to-purple-700 transition disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload & Analyze"}
        </button>
      </div>
      <form
        className="bg-gray-800 rounded-xl shadow-lg p-8 w-full max-w-md "
        onSubmit={handleSubmit}
      >
        <label className="block text-white mb-2 font-semibold">Step-2</label>
        <label className="block text-white mb-2 font-semibold">Sender</label>
        <input
          type="text"
          value={sender}
          onChange={(e) => setSender(e.target.value)}
          className="block w-full text-gray-200 bg-gray-700 border border-gray-600 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <label className="block text-white mb-2 font-semibold">Receiver</label>
        <input
          type="text"
          value={receiver}
          onChange={(e) => setReceiver(e.target.value)}
          className="block w-full text-gray-200 bg-gray-700 border border-gray-600 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <label className="block text-white mb-2 font-semibold">Amount</label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="block w-full text-gray-200 bg-gray-700 border border-gray-600 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <label className="block text-white mb-2 font-semibold">Timestamp</label>
        <input
          type="datetime-local"
          value={timestamp}
          onChange={(e) => setTimestamp(e.target.value)}
          className="block w-full text-gray-200 bg-gray-700 border border-gray-600 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
       
        <button
          type="submit"
          disabled={loading || !csvFile}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-2 px-4 rounded hover:from-blue-700 hover:to-purple-700 transition disabled:opacity-50 mb-2"
        >
          {loading ? "Submitting..." : "Submit Transaction"}
        </button>
        
      </form>

      {/* Success response container */}
      {showResponse && (
        <div
          className={`fixed top-8 right-0 bg-white bg-opacity-95 border border-purple-400 rounded-xl shadow-2xl w-96 max-h-[70vh] overflow-y-auto z-50 flex flex-col
      transition-transform duration-500 ease-in-out
      ${showResponse ? "translate-x-0" : "translate-x-full"}
    `}
          style={{ right: "2rem" }}
        >
          <div className="flex justify-between items-center p-4 border-b border-purple-200">
            <span className="font-bold text-purple-700">API Response</span>
            <button
              onClick={() => setShowResponse(false)}
              className="text-purple-700 hover:text-purple-900 font-bold text-lg"
              aria-label="Close"
            >
              ×
            </button>
          </div>
          <div className="p-4 text-gray-800 animate-fade-in">
            <div className="mb-2 text-sm text-gray-500">
              Blockchain Analysis Result:
            </div>
            <pre className="bg-gray-100 rounded p-2 text-xs overflow-x-auto">
              {JSON.stringify(responseData, null, 2)}
            </pre>
            <div className="mt-4 flex items-center gap-2">
              <img
                src="https://www.svgrepo.com/show/303287/bitcoin-logo.svg"
                className="h-6"
                alt="Bitcoin logo"
              />
              <img
                src="https://www.svgrepo.com/show/464900/ethereum.svg"
                className="h-6"
                alt="Ethereum logo"
              />
              <span className="text-purple-600 font-semibold">
                Crypto Insights
              </span>
            </div>
            <div className="mt-2 text-xs text-gray-500 italic">
              Transactions analyzed on-chain for sender, receiver, amount, and
              timestamp.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
