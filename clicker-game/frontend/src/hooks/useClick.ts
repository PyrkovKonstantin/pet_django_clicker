import { useCallback } from 'react';
import { usePlayerStore } from '../store/usePlayerStore';

export const useClick = () => {
  const { energy, clickPower, increaseCoins, decreaseEnergy, increaseExperience } = usePlayerStore();
  
  const handleClick = useCallback(() => {
    if (energy > 0) {
      increaseCoins(clickPower);
      decreaseEnergy(1);
      increaseExperience(1);
      return true;
    }
    return false;
  }, [energy, clickPower, increaseCoins, decreaseEnergy, increaseExperience]);
  
  return { handleClick };
};