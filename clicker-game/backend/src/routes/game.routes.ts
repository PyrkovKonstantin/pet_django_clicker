import { Router } from 'express';
import { GameController } from '../controllers/game.controller.js';
import { authMiddleware } from '../middleware/auth.middleware.js';
import { container } from '../container.js';

const router = Router();
const gameController = container.get<GameController>('GameController');

/**
 * @route GET /game/player
 * @desc Get player profile
 * @access Private
 */
router.get('/player', authMiddleware, (req, res) => gameController.getPlayerProfile(req, res));

/**
 * @route POST /game/sync
 * @desc Sync player state
 * @access Private
 */
router.post('/sync', authMiddleware, (req, res) => gameController.syncPlayerState(req, res));

/**
 * @route POST /game/click
 * @desc Process click
 * @access Private
 */
router.post('/click', authMiddleware, (req, res) => gameController.processClick(req, res));

/**
 * @route GET /game/upgrades
 * @desc List upgrades
 * @access Private
 */
router.get('/upgrades', authMiddleware, (req, res) => gameController.listUpgrades(req, res));

/**
 * @route POST /game/upgrades/purchase
 * @desc Purchase upgrade
 * @access Private
 */
router.post('/upgrades/purchase', authMiddleware, (req, res) => gameController.purchaseUpgrade(req, res));

/**
 * @route GET /game/daily-rewards
 * @desc Get daily rewards status
 * @access Private
 */
router.get('/daily-rewards', authMiddleware, (req, res) => gameController.getDailyRewardsStatus(req, res));

/**
 * @route POST /game/daily-rewards/claim
 * @desc Claim daily reward
 * @access Private
 */
router.post('/daily-rewards/claim', authMiddleware, (req, res) => gameController.claimDailyReward(req, res));

/**
 * @route GET /game/tasks
 * @desc List tasks
 * @access Private
 */
router.get('/tasks', authMiddleware, (req, res) => gameController.listTasks(req, res));

/**
 * @route POST /game/tasks/claim
 * @desc Claim task reward
 * @access Private
 */
router.post('/tasks/claim', authMiddleware, (req, res) => gameController.claimTaskReward(req, res));

export default router;