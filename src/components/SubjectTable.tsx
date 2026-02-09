import React from 'react';

const subjects = [
  {
    code: 'CS301',
    name: 'Data Structures',
    passPercent: 94,
    failPercent: 6,
    difficulty: 'Easy',
    difficultyColor: 'bg-green-100 text-green-700',
    darkDifficultyColor: 'dark:bg-green-900/30 dark:text-green-400',
  },
  {
    code: 'CS302',
    name: 'Object Oriented Programming',
    passPercent: 89,
    failPercent: 11,
    difficulty: 'Moderate',
    difficultyColor: 'bg-yellow-100 text-yellow-700',
    darkDifficultyColor: 'dark:bg-yellow-900/30 dark:text-yellow-400',
  },
  {
    code: 'CS303',
    name: 'Computer Organization',
    passPercent: 85,
    failPercent: 15,
    difficulty: 'Moderate',
    difficultyColor: 'bg-yellow-100 text-yellow-700',
    darkDifficultyColor: 'dark:bg-yellow-900/30 dark:text-yellow-400',
  },
  {
    code: 'MA301',
    name: 'Discrete Mathematics',
    passPercent: 68,
    failPercent: 32,
    difficulty: 'Tough',
    difficultyColor: 'bg-red-100 text-red-700',
    darkDifficultyColor: 'dark:bg-red-900/30 dark:text-red-400',
  },
  {
    code: 'CS304',
    name: 'Database Management Systems',
    passPercent: 91,
    failPercent: 9,
    difficulty: 'Easy',
    difficultyColor: 'bg-green-100 text-green-700',
    darkDifficultyColor: 'dark:bg-green-900/30 dark:text-green-400',
  },
  {
    code: 'CS305',
    name: 'Operating Systems',
    passPercent: 82,
    failPercent: 18,
    difficulty: 'Moderate',
    difficultyColor: 'bg-yellow-100 text-yellow-700',
    darkDifficultyColor: 'dark:bg-yellow-900/30 dark:text-yellow-400',
  },
];

interface SubjectTableProps {
  isDarkMode: boolean;
}

export function SubjectTable({ isDarkMode }: SubjectTableProps) {
  return (
    <div className={`rounded-xl shadow-sm overflow-hidden transition-colors ${
      isDarkMode ? 'bg-gray-800' : 'bg-white'
    }`}>
      <div className={`p-6 border-b ${isDarkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <h3 className={isDarkMode ? 'text-white' : 'text-gray-900'}>Subject-wise Performance</h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className={`border-b ${isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
            <tr>
              <th className={`px-6 py-3 text-left text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Subject Code</th>
              <th className={`px-6 py-3 text-left text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Subject Name</th>
              <th className={`px-6 py-3 text-left text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Pass %</th>
              <th className={`px-6 py-3 text-left text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Fail %</th>
              <th className={`px-6 py-3 text-left text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Difficulty</th>
            </tr>
          </thead>
          <tbody className={`divide-y ${isDarkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
            {subjects.map((subject, index) => (
              <tr key={index} className={`transition-colors ${
                isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'
              }`}>
                <td className={`px-6 py-4 text-sm ${isDarkMode ? 'text-gray-200' : 'text-gray-900'}`}>{subject.code}</td>
                <td className={`px-6 py-4 text-sm ${isDarkMode ? 'text-gray-200' : 'text-gray-900'}`}>{subject.name}</td>
                <td className="px-6 py-4 text-sm">
                  <span className={isDarkMode ? 'text-green-400' : 'text-green-700'}>{subject.passPercent}%</span>
                </td>
                <td className="px-6 py-4 text-sm">
                  <span className={isDarkMode ? 'text-red-400' : 'text-red-700'}>{subject.failPercent}%</span>
                </td>
                <td className="px-6 py-4 text-sm">
                  <span className={`inline-flex px-3 py-1 rounded-full text-xs ${subject.difficultyColor} ${isDarkMode ? subject.darkDifficultyColor : ''}`}>
                    {subject.difficulty}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
