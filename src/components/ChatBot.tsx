import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Sparkles, Maximize2, Minimize2 } from 'lucide-react';

interface Message {
  type: 'user' | 'bot';
  content: string;
  table?: { name: string; rollNo: string; sgpa: string }[];
  stats?: { label: string; value: string }[];
}

const initialMessages: Message[] = [
  {
    type: 'bot',
    content: 'Hello! I\'m your AI Academic Assistant. Ask me anything about result analytics, student performance, or subject insights.',
  },
  {
    type: 'user',
    content: 'Which subject had the highest failure rate?',
  },
  {
    type: 'bot',
    content: 'Discrete Mathematics (MA301) recorded the highest failure rate at 32%, indicating higher difficulty compared to other subjects.',
    stats: [
      { label: 'Failure Rate', value: '32%' },
      { label: 'Subject Code', value: 'MA301' },
      { label: 'Total Students', value: '156' },
    ],
  },
];

const quickSuggestions = [
  'Failed students',
  '10 SGPA students',
  'Subject difficulty',
  'Department comparison',
];

interface ChatBotProps {
  isOpen: boolean;
  onToggle: () => void;
  isDarkMode: boolean;
}

export function ChatBot({ isOpen, onToggle, isDarkMode }: ChatBotProps) {
  const [isMaximized, setIsMaximized] = useState(false);
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const chatAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (inputValue.trim()) {
      const userMessage: Message = {
        type: 'user',
        content: inputValue,
      };
      
      setMessages([...messages, userMessage]);
      setInputValue('');

      // Simulate bot response
      setTimeout(() => {
        const botResponse = getBotResponse(inputValue);
        setMessages((prev) => [...prev, botResponse]);
      }, 800);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
  };

  const getBotResponse = (query: string): Message => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('failed') || lowerQuery.includes('fail')) {
      return {
        type: 'bot',
        content: 'Here are the students who failed in S3 Computer Science Engineering:',
        table: [
          { name: 'Rahul Krishnan', rollNo: 'CSE21001', sgpa: '4.2' },
          { name: 'Priya Nair', rollNo: 'CSE21045', sgpa: '4.8' },
          { name: 'Arjun Menon', rollNo: 'CSE21078', sgpa: '4.5' },
        ],
      };
    }
    
    if (lowerQuery.includes('10 sgpa') || lowerQuery.includes('sgpa')) {
      return {
        type: 'bot',
        content: 'Students with 10 SGPA in S3 Computer Science Engineering:',
        table: [
          { name: 'Anjali Thomas', rollNo: 'CSE21012', sgpa: '10.0' },
          { name: 'Vishnu Prasad', rollNo: 'CSE21023', sgpa: '10.0' },
          { name: 'Sneha Warrier', rollNo: 'CSE21056', sgpa: '10.0' },
        ],
      };
    }
    
    if (lowerQuery.includes('difficulty') || lowerQuery.includes('tough')) {
      return {
        type: 'bot',
        content: 'Subject difficulty analysis for S3 Computer Science Engineering:',
        stats: [
          { label: 'Toughest Subject', value: 'Discrete Mathematics (32% failure)' },
          { label: 'Easiest Subject', value: 'Data Structures (6% failure)' },
          { label: 'Average Pass Rate', value: '87.2%' },
        ],
      };
    }
    
    if (lowerQuery.includes('department') || lowerQuery.includes('compare')) {
      return {
        type: 'bot',
        content: 'Department-wise pass percentage comparison:',
        stats: [
          { label: 'Computer Science Engg.', value: '87.2%' },
          { label: 'Electrical & Electronics', value: '84.5%' },
          { label: 'Mechanical Engg.', value: '79.8%' },
          { label: 'Civil Engg.', value: '82.1%' },
        ],
      };
    }
    
    return {
      type: 'bot',
      content: 'I can help you analyze student performance, subject difficulty, pass/fail rates, and department comparisons. Try asking about failed students, top performers, or subject insights.',
    };
  };

  return (
    <>
      {/* Floating Widget */}
      {!isOpen && (
        <button
          onClick={onToggle}
          className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all flex items-center justify-center z-50 group"
        >
          <MessageCircle className="w-6 h-6" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></span>
        </button>
      )}

      {/* Chat Panel */}
      {isOpen && (
        <div className={`fixed shadow-2xl flex flex-col z-50 border transition-all ${
          isDarkMode 
            ? 'bg-gray-800 border-gray-700' 
            : 'bg-white border-gray-200'
        } ${
          isMaximized 
            ? 'inset-4 rounded-2xl' 
            : 'bottom-6 right-6 w-[380px] h-[540px] rounded-2xl'
        }`}>
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-5 py-4 rounded-t-2xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-white text-sm">AI Academic Assistant</h3>
                <p className="text-blue-100 text-xs">Result Insights Bot</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsMaximized(!isMaximized)}
                className="text-white hover:bg-white/20 rounded-lg p-1 transition-colors"
                title={isMaximized ? 'Restore' : 'Maximize'}
              >
                {isMaximized ? (
                  <Minimize2 className="w-5 h-5" />
                ) : (
                  <Maximize2 className="w-5 h-5" />
                )}
              </button>
              <button
                onClick={() => {
                  onToggle();
                  setIsMaximized(false);
                }}
                className="text-white hover:bg-white/20 rounded-lg p-1 transition-colors"
                title="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Chat Area */}
          <div
            ref={chatAreaRef}
            className={`flex-1 overflow-y-auto p-4 space-y-4 ${isDarkMode ? 'bg-gray-700' : 'bg-gray-50'}`}
          >
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : isDarkMode 
                        ? 'bg-gray-600 border border-gray-500' 
                        : 'bg-white border border-gray-200'
                  }`}
                >
                  <p className={`text-sm ${message.type === 'user' ? 'text-white' : isDarkMode ? 'text-gray-100' : 'text-gray-800'}`}>
                    {message.content}
                  </p>

                  {/* Stats Display */}
                  {message.stats && (
                    <div className="mt-3 space-y-2">
                      {message.stats.map((stat, idx) => (
                        <div
                          key={idx}
                          className={`flex justify-between items-center rounded-lg px-3 py-2 ${
                            isDarkMode ? 'bg-blue-900/30' : 'bg-blue-50'
                          }`}
                        >
                          <span className={`text-xs ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>{stat.label}</span>
                          <span className={`text-xs ${isDarkMode ? 'text-blue-400' : 'text-blue-700'}`}>{stat.value}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Table Display */}
                  {message.table && (
                    <div className={`mt-3 overflow-hidden rounded-lg border ${
                      isDarkMode ? 'border-gray-500' : 'border-gray-200'
                    }`}>
                      <table className="w-full text-xs">
                        <thead className={isDarkMode ? 'bg-gray-700' : 'bg-gray-100'}>
                          <tr>
                            <th className={`px-2 py-2 text-left ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Name</th>
                            <th className={`px-2 py-2 text-left ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Roll No</th>
                            <th className={`px-2 py-2 text-left ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>SGPA</th>
                          </tr>
                        </thead>
                        <tbody className={`divide-y ${isDarkMode ? 'bg-gray-600 divide-gray-500' : 'bg-white divide-gray-200'}`}>
                          {message.table.map((row, idx) => (
                            <tr key={idx}>
                              <td className={`px-2 py-2 ${isDarkMode ? 'text-gray-200' : 'text-gray-800'}`}>{row.name}</td>
                              <td className={`px-2 py-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>{row.rollNo}</td>
                              <td className={`px-2 py-2 ${isDarkMode ? 'text-gray-200' : 'text-gray-800'}`}>{row.sgpa}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Quick Suggestions */}
          <div className={`px-4 py-3 border-t ${
            isDarkMode ? 'border-gray-600 bg-gray-800' : 'border-gray-200 bg-white'
          }`}>
            <div className="flex flex-wrap gap-2">
              {quickSuggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className={`px-3 py-1.5 rounded-full text-xs transition-colors ${
                    isDarkMode 
                      ? 'bg-blue-900/30 hover:bg-blue-900/50 text-blue-400' 
                      : 'bg-blue-50 hover:bg-blue-100 text-blue-700'
                  }`}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {/* Input Area */}
          <div className={`p-4 border-t rounded-b-2xl ${
            isDarkMode ? 'border-gray-600 bg-gray-800' : 'border-gray-200 bg-white'
          }`}>
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask for result insights…"
                className={`flex-1 px-4 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  isDarkMode 
                    ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
                    : 'bg-gray-50 border-gray-200 text-gray-900'
                }`}
              />
              <button
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}