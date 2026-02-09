import React from 'react';
import { Navbar } from './components/Navbar';
import { PageHeader } from './components/PageHeader';
import { KPICards } from './components/KPICards';
import { ChartsSection } from './components/ChartsSection';
import { AIInsights } from './components/AIInsights';
import { SubjectTable } from './components/SubjectTable';
import { QuickActions } from './components/QuickActions';
import { ChatBot } from './components/ChatBot';

export default function App() {
  const [isChatOpen, setIsChatOpen] = React.useState(false);
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  return (
    <div className={`min-h-screen transition-colors ${
      isDarkMode 
        ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900' 
        : 'bg-gradient-to-br from-sky-100 via-blue-50 to-cyan-100'
    }`}>
      <Navbar isDarkMode={isDarkMode} onToggleDarkMode={() => setIsDarkMode(!isDarkMode)} />
      
      <main className="max-w-[1440px] mx-auto px-8 py-6">
        <PageHeader isDarkMode={isDarkMode} />
        
        <div className="mt-8">
          <KPICards isDarkMode={isDarkMode} />
        </div>
        
        <div className="mt-8">
          <ChartsSection isDarkMode={isDarkMode} />
        </div>
        
        <div className="mt-8">
          <AIInsights isDarkMode={isDarkMode} />
        </div>
        
        <div className="mt-8">
          <SubjectTable isDarkMode={isDarkMode} />
        </div>
        
        <div className="mt-8">
          <QuickActions onOpenChat={() => setIsChatOpen(true)} isDarkMode={isDarkMode} />
        </div>
      </main>
      
      <ChatBot isOpen={isChatOpen} onToggle={() => setIsChatOpen(!isChatOpen)} isDarkMode={isDarkMode} />
    </div>
  );
}