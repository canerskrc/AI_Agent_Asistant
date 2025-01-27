import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [isListening, setIsListening] = useState(false);

  const handleSpeechRecognition = () => {
    const recognition = new (window.SpeechRecognition ||
      window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const spokenQuery = event.results[0][0].transcript;
      setQuery(spokenQuery);
      handleQuery(spokenQuery);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const handleQuery = async (inputQuery) => {
    try {
      const res = await axios.post("http://localhost:8000/query", {
        query: inputQuery,
        context: { sector: "general" },
      });
      setResponse(res.data.response);
    } catch (error) {
      setResponse("An error occurred: " + error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-md max-w-md w-full">
        <h1 className="text-2xl font-bold mb-4 text-center">AI Agent Assistant</h1>
        <textarea
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type your query here..."
          rows={4}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        ></textarea>
        <button
          onClick={() => handleQuery(query)}
          disabled={!query.trim()}
          className="mt-4 w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 transition-colors"
        >
          Submit
        </button>
        <button
          onClick={handleSpeechRecognition}
          className={`mt-2 w-full py-2 px-4 ${
            isListening ? "bg-gray-400" : "bg-green-500"
          } text-white font-semibold rounded-lg shadow-md hover:bg-green-600 transition-colors`}
        >
          {isListening ? "Listening..." : "Start Voice Command"}
        </button>
        {response && (
          <div className="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <h2 className="text-lg font-semibold">Response:</h2>
            <p className="mt-2 text-gray-700">{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
