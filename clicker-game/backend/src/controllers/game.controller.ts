import { Request, Response } from 'express';
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { ClickDto, UpgradePurchaseDto, ClaimTaskRewardDto } from '../dtos/game.dto.js';
import { GameService } from '../services/game.service.js';

export class GameController {
  private gameService: GameService;

  constructor() {
    this.gameService = new GameService();
  }

  /**
   * Get player profile
   */
  async getPlayerProfile(req: Request, res: Response) {
    try {
      const userId = (req as any).user.id;
      const player = await this.gameService.getPlayerProfile(userId);
      return res.status(200).json(player);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Sync player state
   */
  async syncPlayerState(req: Request, res: Response) {
    try {
      const userId = (req as any).user.id;
      const { energy, balance } = req.body;
      
      const player = await this.gameService.syncPlayerState(userId, energy, balance);
      return res.status(200).json(player);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Process click
   */
  async processClick(req: Request, res: Response) {
    try {
      // Validate input
      const clickDto = plainToInstance(ClickDto, req.body);
      const errors = await validate(clickDto);

      if (errors.length > 0) {
        return res.status(400).json({ 
          error: { 
            message: 'Validation failed',
            details: errors.map(e => Object.values(e.constraints || {})).flat()
          }
        });
      }

      const userId = (req as any).user.id;
      const result = await this.gameService.processClick(
        userId,
        clickDto.clicks,
        clickDto.timestamp,
        clickDto.energy,
        clickDto.balance
      );
      
      return res.status(200).json(result);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      if (error.message === 'Not enough energy') {
        return res.status(400).json({ error: { message: 'Not enough energy' } });
      }
      if (error.message === 'Invalid timestamp') {
        return res.status(400).json({ error: { message: 'Invalid timestamp' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * List upgrades
   */
  async listUpgrades(req: Request, res: Response) {
    try {
      const upgrades = await this.gameService.listUpgrades();
      return res.status(200).json(upgrades);
    } catch (error) {
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Purchase upgrade
   */
  async purchaseUpgrade(req: Request, res: Response) {
    try {
      // Validate input
      const upgradeDto = plainToInstance(UpgradePurchaseDto, req.body);
      const errors = await validate(upgradeDto);

      if (errors.length > 0) {
        return res.status(400).json({ 
          error: { 
            message: 'Validation failed',
            details: errors.map(e => Object.values(e.constraints || {})).flat()
          }
        });
      }

      const userId = (req as any).user.id;
      const result = await this.gameService.purchaseUpgrade(
        userId,
        upgradeDto.upgradeId,
        upgradeDto.expectedCost
      );
      
      return res.status(200).json(result);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      if (error.message === 'Upgrade not found') {
        return res.status(404).json({ error: { message: 'Upgrade not found' } });
      }
      if (error.message === 'Upgrade already at max level') {
        return res.status(400).json({ error: { message: 'Upgrade already at max level' } });
      }
      if (error.message === 'Cost mismatch') {
        return res.status(400).json({ error: { message: 'Cost mismatch' } });
      }
      if (error.message === 'Not enough coins') {
        return res.status(400).json({ error: { message: 'Not enough coins' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Get daily rewards status
   */
  async getDailyRewardsStatus(req: Request, res: Response) {
    try {
      const userId = (req as any).user.id;
      const result = await this.gameService.getDailyRewardsStatus(userId);
      return res.status(200).json(result);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Claim daily reward
   */
  async claimDailyReward(req: Request, res: Response) {
    try {
      const userId = (req as any).user.id;
      const result = await this.gameService.claimDailyReward(userId);
      return res.status(200).json(result);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      if (error.message === 'Reward already claimed today') {
        return res.status(400).json({ error: { message: 'Reward already claimed today' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * List tasks
   */
  async listTasks(req: Request, res: Response) {
    try {
      const userId = (req as any).user.id;
      const tasks = await this.gameService.listTasks(userId);
      return res.status(200).json(tasks);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Claim task reward
   */
  async claimTaskReward(req: Request, res: Response) {
    try {
      // Validate input
      const claimDto = plainToInstance(ClaimTaskRewardDto, req.body);
      const errors = await validate(claimDto);

      if (errors.length > 0) {
        return res.status(400).json({ 
          error: { 
            message: 'Validation failed',
            details: errors.map(e => Object.values(e.constraints || {})).flat()
          }
        });
      }

      const userId = (req as any).user.id;
      const result = await this.gameService.claimTaskReward(userId, claimDto.taskId);
      
      return res.status(200).json(result);
    } catch (error: any) {
      if (error.message === 'Player not found') {
        return res.status(404).json({ error: { message: 'Player not found' } });
      }
      if (error.message === 'Task not found') {
        return res.status(404).json({ error: { message: 'Task not found' } });
      }
      if (error.message === 'Task not completed') {
        return res.status(400).json({ error: { message: 'Task not completed' } });
      }
      if (error.message === 'Reward already claimed') {
        return res.status(400).json({ error: { message: 'Reward already claimed' } });
      }
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }
}