import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const gradeData = [
  { grade: 'A+', students: 28 },
  { grade: 'A', students: 42 },
  { grade: 'B+', students: 35 },
  { grade: 'B', students: 24 },
  { grade: 'C', students: 7 },
  { grade: 'F', students: 20 },
];

const passFailData = [
  { name: 'Pass', value: 136, color: '#16a34a' },
  { name: 'Fail', value: 20, color: '#dc2626' },
];

interface ChartsSectionProps {
  isDarkMode: boolean;
}

export function ChartsSection({ isDarkMode }: ChartsSectionProps) {
  return (
    <div className="grid grid-cols-2 gap-6">
      {/* Bar Chart */}
      <div className={`rounded-xl p-6 shadow-sm transition-colors ${
        isDarkMode ? 'bg-gray-800' : 'bg-white'
      }`}>
        <h3 className={`mb-6 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>Grade Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={gradeData}>
            <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? '#374151' : '#f0f0f0'} />
            <XAxis dataKey="grade" stroke={isDarkMode ? '#9ca3af' : '#6b7280'} />
            <YAxis stroke={isDarkMode ? '#9ca3af' : '#6b7280'} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: isDarkMode ? '#1f2937' : '#fff', 
                border: `1px solid ${isDarkMode ? '#374151' : '#e5e7eb'}`,
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
                color: isDarkMode ? '#fff' : '#000'
              }}
            />
            <Bar dataKey="students" fill="#2563eb" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      {/* Pie Chart */}
      <div className={`rounded-xl p-6 shadow-sm transition-colors ${
        isDarkMode ? 'bg-gray-800' : 'bg-white'
      }`}>
        <h3 className={`mb-6 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>Pass vs Fail</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={passFailData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {passFailData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: isDarkMode ? '#1f2937' : '#fff', 
                border: `1px solid ${isDarkMode ? '#374151' : '#e5e7eb'}`,
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
                color: isDarkMode ? '#fff' : '#000'
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
