import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller.js';
import { container } from '../container.js';

const router = Router();
const authController = container.get<AuthController>('AuthController');

/**
 * @route POST /auth/register
 * @desc Register a new user
 * @access Public
 */
router.post('/register', (req, res) => authController.register(req, res));

/**
 * @route POST /auth/login
 * @desc Login user
 * @access Public
 */
router.post('/login', (req, res) => authController.login(req, res));

/**
 * @route POST /auth/logout
 * @desc Logout user
 * @access Public
 */
router.post('/logout', (req, res) => authController.logout(req, res));

/**
 * @route POST /auth/refresh
 * @desc Refresh access token
 * @access Public
 */
router.post('/refresh', (req, res) => authController.refresh(req, res));

export default router;