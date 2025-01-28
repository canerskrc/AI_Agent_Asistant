// Yeni state ve işlevler eklendi
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [sheetName, setSheetName] = useState("");
  const [sheetData, setSheetData] = useState("");
  const [emailRecipient, setEmailRecipient] = useState("");
  const [emailSubject, setEmailSubject] = useState("");
  const [emailMessage, setEmailMessage] = useState("");
  const [response, setResponse] = useState("");

  const addToSheet = async () => {
    try {
      const res = await axios.post("http://localhost:8000/add_to_sheet", {
        sheet_name: sheetName,
        data: JSON.parse(sheetData),
      });
      setResponse(res.data.message);
    } catch (error) {
      setResponse("Error: " + error.message);
    }
  };

  const sendEmail = async () => {
    try {
      const res = await axios.post("http://localhost:8000/send_email", {
        recipient: emailRecipient,
        subject: emailSubject,
        message: emailMessage,
      });
      setResponse(res.data.message);
    } catch (error) {
      setResponse("Error: " + error.message);
    }
  };

  return (
    <div>
      <h1>Google Sheets and Email Integration</h1>
      
      <div>
        <h2>Add to Google Sheet</h2>
        <input
          type="text"
          placeholder="Sheet Name"
          value={sheetName}
          onChange={(e) => setSheetName(e.target.value)}
        />
        <textarea
          placeholder='Data as JSON (e.g., {"Name": "John", "Age": 30})'
          value={sheetData}
          onChange={(e) => setSheetData(e.target.value)}
        ></textarea>
        <button onClick={addToSheet}>Add to Sheet</button>
      </div>
      
      <div>
        <h2>Send Email</h2>
        <input
          type="email"
          placeholder="Recipient"
          value={emailRecipient}
          onChange={(e) => setEmailRecipient(e.target.value)}
        />
        <input
          type="text"
          placeholder="Subject"
          value={emailSubject}
          onChange={(e) => setEmailSubject(e.target.value)}
        />
        <textarea
          placeholder="Message"
          value={emailMessage}
          onChange={(e) => setEmailMessage(e.target.value)}
        ></textarea>
        <button onClick={sendEmail}>Send Email</button>
      </div>

      {response && <p>{response}</p>}
    </div>
  );
}

export default App;
