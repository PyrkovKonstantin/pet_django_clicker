import React from 'react';

interface EnergyBarProps {
  current: number;
  max: number;
  className?: string;
}

const EnergyBar: React.FC<EnergyBarProps> = ({ current, max, className = '' }) => {
  const percentage = Math.max(0, Math.min(100, (current / max) * 100));
  
  // Determine color based on percentage
  let barColor = 'bg-green-500';
  if (percentage < 30) {
    barColor = 'bg-red-500';
  } else if (percentage < 60) {
    barColor = 'bg-yellow-500';
  }
  
  return (
    <div className={`w-full ${className}`}>
      <div className="flex justify-between text-sm mb-1">
        <span>Energy</span>
        <span>{current} / {max}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-4">
        <div 
          className={`h-4 rounded-full ${barColor} transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default EnergyBar;