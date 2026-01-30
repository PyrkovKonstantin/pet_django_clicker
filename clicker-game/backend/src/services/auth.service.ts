import { injectable } from 'inversify';
import { prisma } from '../utils/prisma.js';
import { AuthUtils } from '../utils/auth.utils.js';

@injectable()
export class AuthService {
  /**
   * Register a new user
   */
  async register(email: string, username: string, password: string): Promise<any> {
    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email }
    });

    if (existingUser) {
      throw new Error('User already exists');
    }

    // Hash password
    const hashedPassword = await AuthUtils.hashPassword(password);

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        username,
        password: hashedPassword
      }
    });

    // Create player profile
    const player = await prisma.player.create({
      data: {
        userId: user.id,
        username: user.username
      }
    });

    // Generate tokens
    const accessToken = AuthUtils.generateAccessToken(user);
    
    // For refresh token, we'll store it in the database
    const refreshToken = AuthUtils.generateAccessToken({ ...user, id: user.id * 2 }); // Simple way to generate different token
    
    // In a real implementation, you would store the refresh token in the database
    // await prisma.user.update({
    //   where: { id: user.id },
    //   data: { refreshToken }
    // });

    return {
      user: {
        id: user.id,
        email: user.email,
        username: user.username
      },
      accessToken,
      refreshToken
    };
  }

  /**
   * Login user
   */
  async login(email: string, password: string): Promise<any> {
    // Find user
    const user = await prisma.user.findUnique({
      where: { email }
    });

    if (!user) {
      throw new Error('Invalid credentials');
    }

    // Check password
    const isValidPassword = await AuthUtils.comparePasswords(password, user.password);
    
    if (!isValidPassword) {
      throw new Error('Invalid credentials');
    }

    // Update last login
    await prisma.user.update({
      where: { id: user.id },
      data: { lastLogin: new Date() }
    });

    // Create player if not exists
    let player = await prisma.player.findUnique({
      where: { userId: user.id }
    });

    if (!player) {
      player = await prisma.player.create({
        data: {
          userId: user.id,
          username: user.username
        }
      });
    }

    // Generate tokens
    const accessToken = AuthUtils.generateAccessToken(user);
    const refreshToken = AuthUtils.generateAccessToken({ ...user, id: user.id * 2 }); // Simple way to generate different token

    return {
      user: {
        id: user.id,
        email: user.email,
        username: user.username
      },
      accessToken,
      refreshToken
    };
  }

  /**
   * Refresh access token
   */
  async refreshToken(refreshToken: string): Promise<any> {
    // Verify refresh token
    const payload = AuthUtils.verifyToken(refreshToken);
    
    if (!payload) {
      throw new Error('Invalid refresh token');
    }

    // Find user
    const user = await prisma.user.findUnique({
      where: { id: payload.userId }
    });

    if (!user) {
      throw new Error('Invalid refresh token');
    }

    // In a real implementation, you would check if the refresh token exists in the database
    // and hasn't been revoked

    // Generate new tokens
    const newAccessToken = AuthUtils.generateAccessToken(user);
    const newRefreshToken = AuthUtils.generateAccessToken({ ...user, id: user.id * 2 }); // Simple way to generate different token

    return {
      user: {
        id: user.id,
        email: user.email,
        username: user.username
      },
      accessToken: newAccessToken,
      refreshToken: newRefreshToken
    };
  }
}