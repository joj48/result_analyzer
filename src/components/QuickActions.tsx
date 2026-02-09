import React from 'react';
import { Download, FileSpreadsheet, MessageCircle } from 'lucide-react';

interface QuickActionsProps {
  onOpenChat: () => void;
  isDarkMode: boolean;
}

export function QuickActions({ onOpenChat, isDarkMode }: QuickActionsProps) {
  return (
    <div className={`rounded-xl p-6 shadow-sm mb-8 transition-colors ${
      isDarkMode ? 'bg-gray-800' : 'bg-white'
    }`}>
      <h3 className={`mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>Quick Actions</h3>
      
      <div className="flex gap-4">
        <button className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <Download className="w-4 h-4" />
          <span className="text-sm">Download PDF Report</span>
        </button>
        
        <button className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
          <FileSpreadsheet className="w-4 h-4" />
          <span className="text-sm">Export Excel</span>
        </button>
        
        <button 
          onClick={onOpenChat}
          className="flex items-center gap-2 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
        >
          <MessageCircle className="w-4 h-4" />
          <span className="text-sm">Ask AI Chatbot</span>
        </button>
      </div>
    </div>
  );
}
