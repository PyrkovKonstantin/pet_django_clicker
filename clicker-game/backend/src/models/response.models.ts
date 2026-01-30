/**
 * Standardized response format for all API responses
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code?: string;
    details?: any;
  };
  timestamp: string;
  requestId?: string;
}

/**
 * Pagination metadata
 */
export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

/**
 * Paginated response format
 */
export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  meta?: PaginationMeta;
}

/**
 * Authentication response
 */
export interface AuthResponse {
  user: {
    id: number;
    email: string;
    username: string;
  };
  accessToken: string;
  refreshToken?: string;
}

/**
 * Player profile response
 */
export interface PlayerProfileResponse {
  id: number;
  username: string;
  balance: string;
  level: number;
  energy: number;
  maxEnergy: number;
  energyRegenRate: number;
  coinsPerClick: number;
  lastLogin: Date;
  createdAt: Date;
}

/**
 * Upgrade response
 */
export interface UpgradeResponse {
  id: number;
  name: string;
  description: string;
  icon: string;
  baseCost: number;
  costMultiplier: number;
  upgradeType: string;
  baseEffectValue: number;
  effectPerLevel: number;
  maxLevel: number;
  isActive: boolean;
  order: number;
}

/**
 * Daily reward response
 */
export interface DailyRewardResponse {
  id: number;
  day: number;
  rewardType: string;
  rewardAmount: number;
  isSpecial: boolean;
}

/**
 * Player daily reward response
 */
export interface PlayerDailyRewardResponse {
  id: number;
  reward: DailyRewardResponse;
  claimedAt: Date;
  isConsecutive: boolean;
}

/**
 * Task response
 */
export interface TaskResponse {
  id: number;
  name: string;
  description: string;
  taskType: string;
  targetValue: number;
  rewardCoins: number;
  rewardEnergy: number;
  isActive: boolean;
  order: number;
}

/**
 * Player task response
 */
export interface PlayerTaskResponse {
  id: number;
  task: TaskResponse;
  progress: number;
  isCompleted: boolean;
  completedAt: Date | null;
}