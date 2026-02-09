import React from 'react';
import { Users, TrendingUp, TrendingDown, UserX, Award } from 'lucide-react';

const kpiData = [
  {
    title: 'Total Students',
    value: '156',
    icon: Users,
    color: 'bg-blue-50',
    iconColor: 'text-blue-600',
    darkColor: 'dark:bg-blue-900/30',
    darkIconColor: 'dark:text-blue-400',
  },
  {
    title: 'Pass Percentage',
    value: '87.2%',
    icon: TrendingUp,
    color: 'bg-green-50',
    iconColor: 'text-green-600',
    darkColor: 'dark:bg-green-900/30',
    darkIconColor: 'dark:text-green-400',
  },
  {
    title: 'Fail Percentage',
    value: '12.8%',
    icon: TrendingDown,
    color: 'bg-red-50',
    iconColor: 'text-red-600',
    darkColor: 'dark:bg-red-900/30',
    darkIconColor: 'dark:text-red-400',
  },
  {
    title: 'Absentees',
    value: '8',
    icon: UserX,
    color: 'bg-orange-50',
    iconColor: 'text-orange-600',
    darkColor: 'dark:bg-orange-900/30',
    darkIconColor: 'dark:text-orange-400',
  },
  {
    title: '10 SGPA / CGPA Students',
    value: '12',
    icon: Award,
    color: 'bg-purple-50',
    iconColor: 'text-purple-600',
    darkColor: 'dark:bg-purple-900/30',
    darkIconColor: 'dark:text-purple-400',
  },
];

interface KPICardsProps {
  isDarkMode: boolean;
}

export function KPICards({ isDarkMode }: KPICardsProps) {
  return (
    <div className="grid grid-cols-5 gap-6">
      {kpiData.map((kpi, index) => (
        <div key={index} className={`rounded-xl p-6 shadow-sm hover:shadow-md transition-all ${
          isDarkMode ? 'bg-gray-800' : 'bg-white'
        }`}>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className={`text-sm mb-2 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>{kpi.title}</p>
              <p className={isDarkMode ? 'text-white' : 'text-gray-900'}>{kpi.value}</p>
            </div>
            <div className={`${kpi.color} ${isDarkMode ? kpi.darkColor : ''} ${kpi.iconColor} ${isDarkMode ? kpi.darkIconColor : ''} p-3 rounded-lg`}>
              <kpi.icon className="w-5 h-5" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
