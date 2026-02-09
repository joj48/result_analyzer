import React from 'react';
import { TrendingUp, AlertCircle, Activity, Sparkles } from 'lucide-react';

const insights = [
  {
    title: 'Top Performing Subject',
    value: 'Data Structures (CS301)',
    description: '94% pass rate with avg. grade B+',
    icon: TrendingUp,
    color: 'bg-green-50',
    iconColor: 'text-green-600',
    borderColor: 'border-green-200',
    darkColor: 'dark:bg-green-900/20',
    darkBorderColor: 'dark:border-green-800',
    darkIconColor: 'dark:text-green-400',
  },
  {
    title: 'Most Difficult Subject',
    value: 'Discrete Mathematics (MA301)',
    description: '68% pass rate, requires attention',
    icon: AlertCircle,
    color: 'bg-red-50',
    iconColor: 'text-red-600',
    borderColor: 'border-red-200',
    darkColor: 'dark:bg-red-900/20',
    darkBorderColor: 'dark:border-red-800',
    darkIconColor: 'dark:text-red-400',
  },
  {
    title: 'Performance Trend',
    value: 'Improving',
    description: '+5.2% compared to last semester',
    icon: Activity,
    color: 'bg-blue-50',
    iconColor: 'text-blue-600',
    borderColor: 'border-blue-200',
    darkColor: 'dark:bg-blue-900/20',
    darkBorderColor: 'dark:border-blue-800',
    darkIconColor: 'dark:text-blue-400',
  },
];

interface AIInsightsProps {
  isDarkMode: boolean;
}

export function AIInsights({ isDarkMode }: AIInsightsProps) {
  return (
    <div className={`rounded-xl p-6 shadow-sm transition-colors ${
      isDarkMode ? 'bg-gray-800' : 'bg-white'
    }`}>
      <div className="flex items-center gap-2 mb-6">
        <Sparkles className={`w-5 h-5 ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`} />
        <h3 className={isDarkMode ? 'text-white' : 'text-gray-900'}>AI Insights</h3>
      </div>
      
      <div className="grid grid-cols-3 gap-6">
        {insights.map((insight, index) => (
          <div 
            key={index} 
            className={`${insight.color} ${isDarkMode ? insight.darkColor : ''} border ${insight.borderColor} ${isDarkMode ? insight.darkBorderColor : ''} rounded-lg p-4`}
          >
            <div className="flex items-start gap-3">
              <div className={`${insight.iconColor} ${isDarkMode ? insight.darkIconColor : ''} mt-1`}>
                <insight.icon className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <p className={`text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>{insight.title}</p>
                <p className={`mb-1 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>{insight.value}</p>
                <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>{insight.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
