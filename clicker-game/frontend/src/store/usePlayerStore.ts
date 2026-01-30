import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface PlayerState {
  coins: number;
  energy: number;
  maxEnergy: number;
  level: number;
  experience: number;
  experienceToNextLevel: number;
  clickPower: number;
  isOnline: boolean;
  lastOnline: Date | null;
}

interface PlayerActions {
  increaseCoins: (amount: number) => void;
  decreaseCoins: (amount: number) => void;
  increaseEnergy: (amount: number) => void;
  decreaseEnergy: (amount: number) => void;
  increaseExperience: (amount: number) => void;
  levelUp: () => void;
  setOnline: (online: boolean) => void;
  reset: () => void;
}

export type PlayerStore = PlayerState & PlayerActions;

const initialState: PlayerState = {
  coins: 0,
  energy: 100,
  maxEnergy: 100,
  level: 1,
  experience: 0,
  experienceToNextLevel: 100,
  clickPower: 1,
  isOnline: false,
  lastOnline: null,
};

export const usePlayerStore = create<PlayerStore>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      increaseCoins: (amount) => set((state) => ({ coins: state.coins + amount })),
      
      decreaseCoins: (amount) => set((state) => ({ coins: Math.max(0, state.coins - amount) })),
      
      increaseEnergy: (amount) => set((state) => ({ 
        energy: Math.min(state.maxEnergy, state.energy + amount) 
      })),
      
      decreaseEnergy: (amount) => set((state) => ({ 
        energy: Math.max(0, state.energy - amount) 
      })),
      
      increaseExperience: (amount) => {
        const { experience, experienceToNextLevel, level } = get();
        const newExperience = experience + amount;
        
        if (newExperience >= experienceToNextLevel) {
          // Level up
          set({
            level: level + 1,
            experience: newExperience - experienceToNextLevel,
            experienceToNextLevel: Math.floor(experienceToNextLevel * 1.5),
            clickPower: get().clickPower + 1,
          });
        } else {
          set({ experience: newExperience });
        }
      },
      
      levelUp: () => {
        set((state) => ({
          level: state.level + 1,
          experience: 0,
          experienceToNextLevel: Math.floor(state.experienceToNextLevel * 1.5),
          clickPower: state.clickPower + 1,
        }));
      },
      
      setOnline: (online) => set({ 
        isOnline: online, 
        lastOnline: online ? new Date() : get().lastOnline 
      }),
      
      reset: () => set(initialState),
    }),
    {
      name: 'player-storage',
      partialize: (state) => ({
        coins: state.coins,
        energy: state.energy,
        maxEnergy: state.maxEnergy,
        level: state.level,
        experience: state.experience,
        experienceToNextLevel: state.experienceToNextLevel,
        clickPower: state.clickPower,
        lastOnline: state.lastOnline,
      }),
    }
  )
);