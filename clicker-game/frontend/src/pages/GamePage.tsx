import React from 'react';
import { usePlayerStore } from '../store/usePlayerStore';
import Button from '../components/Button';
import EnergyBar from '../components/EnergyBar';

const GamePage: React.FC = () => {
  const { coins, energy, maxEnergy, level, experience, experienceToNextLevel, clickPower, increaseCoins, decreaseEnergy, increaseExperience } = usePlayerStore();
  
  const handleMainClick = () => {
    if (energy > 0) {
      increaseCoins(clickPower);
      decreaseEnergy(1);
      increaseExperience(1);
    }
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-md mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mt-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">Clicker Game</h1>
            <p className="text-gray-600 dark:text-gray-300">Level {level}</p>
          </div>
          
          <div className="mb-6">
            <div className="text-center mb-4">
              <p className="text-4xl font-bold text-gray-800 dark:text-white">{coins}</p>
              <p className="text-gray-600 dark:text-gray-300">Coins</p>
            </div>
            
            <EnergyBar current={energy} max={maxEnergy} className="mb-6" />
            
            <div className="mb-6">
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(experience / experienceToNextLevel) * 100}%` }}
                />
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-300 flex justify-between">
                <span>EXP: {experience}</span>
                <span>{experienceToNextLevel - experience} to next level</span>
              </div>
            </div>
          </div>
          
          <div className="flex justify-center mb-8">
            <button
              onClick={handleMainClick}
              disabled={energy <= 0}
              className={`w-32 h-32 rounded-full text-2xl font-bold shadow-lg transform transition-all duration-150 ${
                energy <= 0 
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                  : 'bg-gradient-to-br from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 active:scale-95'
              }`}
            >
              CLICK
            </button>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4 text-center">
              <p className="text-lg font-semibold text-gray-800 dark:text-white">{clickPower}</p>
              <p className="text-sm text-gray-600 dark:text-gray-300">Power</p>
            </div>
            <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4 text-center">
              <p className="text-lg font-semibold text-gray-800 dark:text-white">{energy}</p>
              <p className="text-sm text-gray-600 dark:text-gray-300">Energy</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GamePage;