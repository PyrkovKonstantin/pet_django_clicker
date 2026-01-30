import { Request, Response } from 'express';
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { RegisterDto, LoginDto } from '../dtos/auth.dto.js';
import { AuthService } from '../services/auth.service.js';
import { inject } from 'inversify';
import { TYPES } from '../types.js';

export class AuthController {
  private authService: AuthService;

  constructor(@inject(TYPES.AuthService) authService: AuthService) {
    this.authService = authService;
  }

  /**
   * Register a new user
   */
  async register(req: Request, res: Response) {
    try {
      // Validate input
      const registerDto = plainToInstance(RegisterDto, req.body);
      const errors = await validate(registerDto);

      if (errors.length > 0) {
        return res.status(400).json({ 
          error: { 
            message: 'Validation failed',
            details: errors.map(e => Object.values(e.constraints || {})).flat()
          }
        });
      }

      // Register user
      const result = await this.authService.register(
        registerDto.email,
        registerDto.username,
        registerDto.password
      );

      return res.status(201).json(result);
    } catch (error: any) {
      if (error.message === 'User already exists') {
        return res.status(409).json({ error: { message: 'User already exists' } });
      }
      
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Login user
   */
  async login(req: Request, res: Response) {
    try {
      // Validate input
      const loginDto = plainToInstance(LoginDto, req.body);
      const errors = await validate(loginDto);

      if (errors.length > 0) {
        return res.status(400).json({ 
          error: { 
            message: 'Validation failed',
            details: errors.map(e => Object.values(e.constraints || {})).flat()
          }
        });
      }

      // Login user
      const result = await this.authService.login(
        loginDto.email,
        loginDto.password
      );

      // Set refresh token in HTTP-only cookie
      res.cookie('refreshToken', result.refreshToken, {
        httpOnly: true,
        secure: process.env['NODE_ENV'] === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      // Return access token in response body
      return res.status(200).json({
        accessToken: result.accessToken,
        user: result.user
      });
    } catch (error: any) {
      if (error.message === 'Invalid credentials') {
        return res.status(401).json({ error: { message: 'Invalid credentials' } });
      }
      
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Logout user
   */
  async logout(req: Request, res: Response) {
    try {
      // Clear refresh token cookie
      res.clearCookie('refreshToken');
      
      return res.status(200).json({ message: 'Logged out successfully' });
    } catch (error) {
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }

  /**
   * Refresh access token
   */
  async refresh(req: Request, res: Response) {
    try {
      const refreshToken = req.cookies['refreshToken'];
      
      if (!refreshToken) {
        return res.status(401).json({ error: { message: 'Refresh token required' } });
      }

      const result = await this.authService.refreshToken(refreshToken);
      
      // Set new refresh token in HTTP-only cookie
      res.cookie('refreshToken', result.refreshToken, {
        httpOnly: true,
        secure: process.env['NODE_ENV'] === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      // Return new access token in response body
      return res.status(200).json({
        accessToken: result.accessToken,
        user: result.user
      });
    } catch (error: any) {
      if (error.message === 'Invalid refresh token') {
        return res.status(401).json({ error: { message: 'Invalid refresh token' } });
      }
      
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  }
}