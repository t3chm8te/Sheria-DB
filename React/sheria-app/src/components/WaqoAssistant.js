import '../styles/WaqoAssistant.css';
import React, { useState} from 'react';

function WaqoAssistant() {
    const [text, setText] = useState('')

    return (
        <div className="waqo-container">
            <div className="waqo-content">
                <h1>Meet Wakili a Quick One - Your Legal Assistant</h1>
                <p>Powered by advanced AI, Waqo helps you navigate through Kenya's legal landscape with ease. Ask questions, get insights, and find relevant legal information instantly.</p>

                <div className="waqo-demo">
                    <div className="demo-question"> {/* Added a wrapper for the question */}
                        <p>"What are the requirements for company registration in Kenya?"</p>
                    </div>
                    <div className="demo-answer"> {/* Added a wrapper for the answer */}
                        <p>Based on the Companies Act 2015, company registration requires...</p>
                    </div>
                    <button className="my-button">Ask WAQO now</button>
                </div>
            </div>

            

            <div className="waqo-prompt">
                <h3>Waqo AI assistant</h3>
                <div className="text-input-container">
                <input type="text" value={text} onChange={(e) => setText(e.target.value)} className="text-input"  
                placeholder="Ask your legal question ..." />
                </div>
                <div className="prompt-buttons"> {/* Added a wrapper for the buttons */}
                    <button className="my-button">Company Law</button>
                    <button className="my-button">Land Law</button>
                    <button className="my-button">Criminal Law</button>
                </div>
                <p>Powered by the Newman...</p>
            </div>
        </div>
    );
}

export default WaqoAssistant;