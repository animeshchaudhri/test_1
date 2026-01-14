import React, { useState, useEffect } from 'react';
import './VoiceSearch.css';

function VoiceSearch({ onVoiceResult, isActive, setIsActive }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    // Initialize Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onstart = () => {
        setIsListening(true);
        setIsActive(true);
      };

      recognitionInstance.onresult = (event) => {
        const current = event.resultIndex;
        const transcriptResult = event.results[current][0].transcript;
        setTranscript(transcriptResult);
        
        if (event.results[current].isFinal) {
          onVoiceResult(transcriptResult);
        }
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        setIsActive(false);
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
        setIsActive(false);
      };

      setRecognition(recognitionInstance);
    }
  }, [setIsActive, onVoiceResult]);

  const toggleListening = () => {
    if (!recognition) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      recognition.stop();
    } else {
      setTranscript('');
      recognition.start();
    }
  };

  return (
    <div className="voice-search">
      <button
        className={`voice-button ${isListening ? 'voice-active' : ''}`}
        onClick={toggleListening}
        title="Click to speak"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="mic-icon">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
        </svg>
        {isListening && (
          <div className="voice-waveform">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
      </button>
      
      {transcript && (
        <div className="transcript-display">
          <p>"{transcript}"</p>
        </div>
      )}
    </div>
  );
}

export default VoiceSearch;
