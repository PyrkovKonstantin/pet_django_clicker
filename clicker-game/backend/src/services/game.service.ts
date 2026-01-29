import {
  DailyReward,
  PlayerDailyReward,
  PlayerTask,
  Player,
  Task,
  Upgrade,
} from "../../generated/prisma/browser";
import { prisma } from "../utils/prisma.js";

export class GameService {
  /**
   * Get player profile
   */
  async getPlayerProfile(userId: number) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Update last login
    await prisma.player.update({
      where: { id: player.id },
      data: { lastLogin: new Date() },
    });

    // Update energy before returning data
    const updatedPlayer = await this.updateEnergy(player);

    return {
      id: updatedPlayer.id,
      username: updatedPlayer.username,
      balance: updatedPlayer.balance.toString(),
      level: updatedPlayer.level,
      energy: updatedPlayer.energy,
      maxEnergy: updatedPlayer.maxEnergy,
      energyRegenRate: updatedPlayer.energyRegenRate,
      coinsPerClick: updatedPlayer.coinsPerClick,
      lastLogin: updatedPlayer.lastLogin,
      createdAt: updatedPlayer.createdAt,
    };
  }

  /**
   * Sync player state
   */
  async syncPlayerState(userId: number, energy: number, balance: number) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Validate energy (can't exceed max_energy)
    const validatedEnergy = Math.min(energy, player.maxEnergy);

    // Update player state
    const updatedPlayer = await prisma.player.update({
      where: { id: player.id },
      data: {
        energy: validatedEnergy,
        balance: BigInt(balance),
        lastEnergyUpdate: new Date(),
      },
    });

    return {
      balance: updatedPlayer.balance.toString(),
      energy: updatedPlayer.energy,
      maxEnergy: updatedPlayer.maxEnergy,
    };
  }

  /**
   * Process a click action
   */
  async processClick(
    userId: number,
    clicks: number,
    timestamp: string,
    clientEnergy: number,
    clientBalance: number,
  ) {
    // Find player
    let player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Update energy before processing click
    player = await this.updateEnergy(player);

    // Validate energy
    if (player.energy < clicks) {
      throw new Error("Not enough energy");
    }

    // Validate timestamp (should be recent)
    const clickTime = new Date(timestamp);
    const timeDiff = Math.abs(
      (new Date().getTime() - clickTime.getTime()) / 1000,
    );
    if (timeDiff > 30) {
      // More than 30 seconds old
      throw new Error("Invalid timestamp");
    }

    // Update player
    const updatedPlayer = await prisma.player.update({
      where: { id: player.id },
      data: {
        energy: player.energy - clicks,
        balance: {
          increment: BigInt(clicks * player.coinsPerClick),
        },
        lastEnergyUpdate: new Date(),
      },
    });

    // Return updated player state
    return {
      balance: updatedPlayer.balance.toString(),
      energy: updatedPlayer.energy,
      maxEnergy: updatedPlayer.maxEnergy,
    };
  }

  /**
   * List all available upgrades
   */
  async listUpgrades() {
    const upgrades = await prisma.upgrade.findMany({
      where: { isActive: true },
    });

    return upgrades.map((upgrade: Upgrade) => ({
      id: upgrade.id,
      name: upgrade.name,
      description: upgrade.description,
      icon: upgrade.icon,
      baseCost: upgrade.baseCost,
      costMultiplier: upgrade.costMultiplier,
      upgradeType: upgrade.upgradeType,
      baseEffectValue: upgrade.baseEffectValue,
      effectPerLevel: upgrade.effectPerLevel,
      maxLevel: upgrade.maxLevel,
      isActive: upgrade.isActive,
      order: upgrade.order,
    }));
  }

  /**
   * Purchase an upgrade
   */
  async purchaseUpgrade(
    userId: number,
    upgradeId: number,
    expectedCost: number,
  ) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Find upgrade
    const upgrade = await prisma.upgrade.findUnique({
      where: { id: upgradeId, isActive: true },
    });

    if (!upgrade) {
      throw new Error("Upgrade not found");
    }

    // Get current upgrade level for player
    let playerUpgrade = await prisma.playerUpgrade.findUnique({
      where: {
        playerId_upgradeId: {
          playerId: player.id,
          upgradeId: upgrade.id,
        },
      },
    });

    // If player doesn't have this upgrade, create it with level 0
    if (!playerUpgrade) {
      playerUpgrade = await prisma.playerUpgrade.create({
        data: {
          playerId: player.id,
          upgradeId: upgrade.id,
          level: 0,
        },
      });
    }

    // Calculate actual cost
    const actualCost = this.calculateUpgradeCost(upgrade, playerUpgrade.level);
    if (actualCost === null) {
      throw new Error("Upgrade already at max level");
    }

    // Validate expected cost matches actual cost
    if (expectedCost !== actualCost) {
      throw new Error("Cost mismatch");
    }

    // Check if player has enough coins
    if (player.balance < BigInt(actualCost)) {
      throw new Error("Not enough coins");
    }

    // Process purchase
    const updatedPlayer = await prisma.player.update({
      where: { id: player.id },
      data: {
        balance: {
          decrement: BigInt(actualCost),
        },
      },
    });

    const updatedPlayerUpgrade = await prisma.playerUpgrade.update({
      where: { id: playerUpgrade.id },
      data: {
        level: playerUpgrade.level + 1,
        purchasedAt: new Date(),
      },
    });

    // Apply upgrade effect
    let playerUpdateData: any = {};

    if (upgrade.upgradeType === "coins_per_click") {
      playerUpdateData.coinsPerClick = {
        increment:
          upgrade.baseEffectValue +
          upgrade.effectPerLevel * (updatedPlayerUpgrade.level - 1),
      };
    } else if (upgrade.upgradeType === "max_energy") {
      playerUpdateData.maxEnergy = {
        increment:
          upgrade.baseEffectValue +
          upgrade.effectPerLevel * (updatedPlayerUpgrade.level - 1),
      };
      // Restore energy to new max if it was at max
      if (player.energy === player.maxEnergy) {
        playerUpdateData.energy =
          player.maxEnergy +
          (upgrade.baseEffectValue +
            upgrade.effectPerLevel * (updatedPlayerUpgrade.level - 1));
      }
    } else if (upgrade.upgradeType === "energy_regen") {
      playerUpdateData.energyRegenRate = {
        increment:
          upgrade.baseEffectValue +
          upgrade.effectPerLevel * (updatedPlayerUpgrade.level - 1),
      };
    }

    const finalPlayer = await prisma.player.update({
      where: { id: player.id },
      data: playerUpdateData,
    });

    // Return updated player and upgrade info
    return {
      player: {
        id: finalPlayer.id,
        username: finalPlayer.username,
        balance: finalPlayer.balance.toString(),
        level: finalPlayer.level,
        energy: finalPlayer.energy,
        maxEnergy: finalPlayer.maxEnergy,
        energyRegenRate: finalPlayer.energyRegenRate,
        coinsPerClick: finalPlayer.coinsPerClick,
        lastLogin: finalPlayer.lastLogin,
        createdAt: finalPlayer.createdAt,
      },
      upgrade: {
        id: updatedPlayerUpgrade.id,
        upgradeId: updatedPlayerUpgrade.upgradeId,
        level: updatedPlayerUpgrade.level,
        purchasedAt: updatedPlayerUpgrade.purchasedAt,
      },
    };
  }

  /**
   * Get daily reward status
   */
  async getDailyRewardsStatus(userId: number) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Get all rewards
    const rewards = await prisma.dailyReward.findMany();

    // Get player's claimed rewards
    const playerRewards = await prisma.playerDailyReward.findMany({
      where: { playerId: player.id },
      include: { reward: true },
    });

    return {
      rewards: rewards.map((reward: DailyReward) => ({
        id: reward.id,
        day: reward.day,
        rewardType: reward.rewardType,
        rewardAmount: reward.rewardAmount,
        isSpecial: reward.isSpecial,
      })),
      playerRewards: playerRewards.map(
        (playerReward: PlayerDailyReward & { reward: DailyReward }) => ({
          id: playerReward.id,
          reward: {
            id: playerReward.reward.id,
            day: playerReward.reward.day,
            rewardType: playerReward.reward.rewardType,
            rewardAmount: playerReward.reward.rewardAmount,
            isSpecial: playerReward.reward.isSpecial,
          },
          claimedAt: playerReward.claimedAt,
          isConsecutive: playerReward.isConsecutive,
        }),
      ),
    };
  }

  /**
   * Claim daily reward
   */
  async claimDailyReward(userId: number) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Determine which day reward to give (based on last claim)
    const lastClaim = await prisma.playerDailyReward.findFirst({
      where: { playerId: player.id },
      orderBy: { claimedAt: "desc" },
    });

    let nextDay: number;

    if (lastClaim) {
      // Check if already claimed today
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const lastClaimDate = new Date(lastClaim.claimedAt);
      lastClaimDate.setHours(0, 0, 0, 0);

      if (lastClaimDate.getTime() === today.getTime()) {
        throw new Error("Reward already claimed today");
      }

      // Calculate next day
      nextDay = lastClaim.rewardId + 1;
    } else {
      // First claim
      nextDay = 1;
    }

    // Find reward
    let reward = await prisma.dailyReward.findUnique({
      where: { day: nextDay },
    });

    // If reward not found, reset to day 1
    if (!reward) {
      reward = await prisma.dailyReward.findUnique({
        where: { day: 1 },
      });

      if (!reward) {
        throw new Error("No rewards available");
      }
    }

    // Award reward
    let updatedPlayer = player;
    if (reward.rewardType === "coins") {
      updatedPlayer = await prisma.player.update({
        where: { id: player.id },
        data: {
          balance: {
            increment: BigInt(reward.rewardAmount),
          },
        },
      });
    }

    // Record claim
    const playerReward = await prisma.playerDailyReward.create({
      data: {
        playerId: player.id,
        rewardId: reward.id,
        isConsecutive: lastClaim !== null,
      },
      include: { reward: true },
    });

    // Return updated player and reward info
    return {
      player: {
        id: updatedPlayer.id,
        username: updatedPlayer.username,
        balance: updatedPlayer.balance.toString(),
        level: updatedPlayer.level,
        energy: updatedPlayer.energy,
        maxEnergy: updatedPlayer.maxEnergy,
        energyRegenRate: updatedPlayer.energyRegenRate,
        coinsPerClick: updatedPlayer.coinsPerClick,
        lastLogin: updatedPlayer.lastLogin,
        createdAt: updatedPlayer.createdAt,
      },
      reward: {
        id: playerReward.id,
        reward: {
          id: playerReward.reward.id,
          day: playerReward.reward.day,
          rewardType: playerReward.reward.rewardType,
          rewardAmount: playerReward.reward.rewardAmount,
          isSpecial: playerReward.reward.isSpecial,
        },
        claimedAt: playerReward.claimedAt,
        isConsecutive: playerReward.isConsecutive,
      },
    };
  }

  /**
   * List all tasks with player progress
   */
  async listTasks(userId: number) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Get all active tasks
    const tasks = await prisma.task.findMany({
      where: { isActive: true },
    });

    // Get player's task progress
    const playerTasks = await prisma.playerTask.findMany({
      where: {
        playerId: player.id,
        taskId: { in: tasks.map((task: Task) => task.id) },
      },
      include: { task: true },
    });

    // Create a map of player tasks for easy lookup
    const playerTasksMap = new Map(
      playerTasks.map((pt: PlayerTask & { task: Task }) => [pt.taskId, pt]),
    );

    // Prepare response data
    const taskData = tasks.map((task: Task) => {
      const playerTask = playerTasksMap.get(task.id);

      if (playerTask) {
        return {
          id: playerTask.id,
          task: {
            id: playerTask.task.id,
            name: playerTask.task.name,
            description: playerTask.task.description,
            taskType: playerTask.task.taskType,
            targetValue: playerTask.task.targetValue,
            rewardCoins: playerTask.task.rewardCoins,
            rewardEnergy: playerTask.task.rewardEnergy,
            isActive: playerTask.task.isActive,
            order: playerTask.task.order,
          },
          progress: playerTask.progress,
          isCompleted: playerTask.isCompleted,
          completedAt: playerTask.completedAt,
        };
      } else {
        // Create a default player task
        return {
          id: 0,
          task: {
            id: task.id,
            name: task.name,
            description: task.description,
            taskType: task.taskType,
            targetValue: task.targetValue,
            rewardCoins: task.rewardCoins,
            rewardEnergy: task.rewardEnergy,
            isActive: task.isActive,
            order: task.order,
          },
          progress: 0,
          isCompleted: false,
          completedAt: null,
        };
      }
    });

    return taskData;
  }

  /**
   * Claim reward for completed task
   */
  async claimTaskReward(userId: number, taskId: number) {
    // Find player
    const player = await prisma.player.findUnique({
      where: { userId },
    });

    if (!player) {
      throw new Error("Player not found");
    }

    // Find task
    const task = await prisma.task.findUnique({
      where: { id: taskId, isActive: true },
    });

    if (!task) {
      throw new Error("Task not found");
    }

    // Get or create player task
    let playerTask = await prisma.playerTask.findUnique({
      where: {
        playerId_taskId: {
          playerId: player.id,
          taskId: task.id,
        },
      },
    });

    if (!playerTask) {
      playerTask = await prisma.playerTask.create({
        data: {
          playerId: player.id,
          taskId: task.id,
          progress: 0,
          isCompleted: false,
        },
      });
    }

    // Check if task is completed
    if (!playerTask.isCompleted) {
      throw new Error("Task not completed");
    }

    // Check if reward already claimed
    if (playerTask.completedAt) {
      throw new Error("Reward already claimed");
    }

    // Award reward
    const updatedPlayer = await prisma.player.update({
      where: { id: player.id },
      data: {
        balance: {
          increment: BigInt(task.rewardCoins),
        },
        energy: {
          increment: task.rewardEnergy,
        },
      },
    });

    // Make sure energy doesn't exceed max energy
    let finalPlayer = updatedPlayer;
    if (updatedPlayer.energy > updatedPlayer.maxEnergy) {
      finalPlayer = await prisma.player.update({
        where: { id: player.id },
        data: {
          energy: updatedPlayer.maxEnergy,
        },
      });
    }

    // Mark reward as claimed
    const updatedPlayerTask = await prisma.playerTask.update({
      where: { id: playerTask.id },
      data: {
        completedAt: new Date(),
      },
    });

    // Return updated player and task info
    return {
      player: {
        id: finalPlayer.id,
        username: finalPlayer.username,
        balance: finalPlayer.balance.toString(),
        level: finalPlayer.level,
        energy: finalPlayer.energy,
        maxEnergy: finalPlayer.maxEnergy,
        energyRegenRate: finalPlayer.energyRegenRate,
        coinsPerClick: finalPlayer.coinsPerClick,
        lastLogin: finalPlayer.lastLogin,
        createdAt: finalPlayer.createdAt,
      },
      task: {
        id: updatedPlayerTask.id,
        task: {
          id: updatedPlayerTask.taskId,
          name: task.name,
          description: task.description,
          taskType: task.taskType,
          targetValue: task.targetValue,
          rewardCoins: task.rewardCoins,
          rewardEnergy: task.rewardEnergy,
          isActive: task.isActive,
          order: task.order,
        },
        progress: updatedPlayerTask.progress,
        isCompleted: updatedPlayerTask.isCompleted,
        completedAt: updatedPlayerTask.completedAt,
      },
    };
  }

  /**
   * Update energy based on time passed
   */
  private async updateEnergy(player: Player) {
    // If energy is already at max, no need to update
    if (player.energy >= player.maxEnergy) {
      return player;
    }

    // Calculate seconds passed since last energy update
    const timePassed =
      (new Date().getTime() - player.lastEnergyUpdate.getTime()) / 1000;
    const secondsPassed = Math.floor(timePassed);

    // If less than 1 second, no need to update
    if (secondsPassed < 1) {
      return player;
    }

    // Calculate energy regenerated
    const energyRegenerated = secondsPassed * player.energyRegenRate;

    // Update energy (but not above max_energy)
    const newEnergy = Math.min(
      player.energy + energyRegenerated,
      player.maxEnergy,
    );

    // If energy hasn't changed, no need to update
    if (newEnergy === player.energy) {
      return player;
    }

    // Update player
    const updatedPlayer = await prisma.player.update({
      where: { id: player.id },
      data: {
        energy: newEnergy,
        lastEnergyUpdate: new Date(),
      },
    });

    return updatedPlayer;
  }

  /**
   * Calculate the cost of upgrading to the next level
   */
  private calculateUpgradeCost(upgrade: Upgrade, currentLevel: number) {
    if (currentLevel >= upgrade.maxLevel) {
      return null; // Already at max level
    }
    return Math.floor(
      upgrade.baseCost * Math.pow(upgrade.costMultiplier, currentLevel),
    );
  }
}
