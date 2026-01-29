import { Request, Response, NextFunction } from 'express';
import { AuthUtils } from '../utils/auth.utils.js';
import { prisma } from '../utils/prisma.js';

/**
 * Authentication middleware
 * Checks for JWT in Authorization header or refresh token in cookies
 */
export async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  try {
    // Check for access token in Authorization header
    const authHeader = req.headers.authorization;
    let token: string | undefined;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7);
    }
    
    // If no access token, check for refresh token in cookies
    if (!token && req.cookies?.refreshToken) {
      token = req.cookies.refreshToken;
    }
    
    // If no token found, return error
    if (!token) {
      return res.status(401).json({ error: { message: 'Authentication required' } });
    }
    
    // Verify token
    const payload = AuthUtils.verifyToken(token);
    
    if (!payload) {
      return res.status(401).json({ error: { message: 'Invalid token' } });
    }
    
    // Find user
    const user = await prisma.user.findUnique({
      where: { id: payload.userId }
    });
    
    if (!user) {
      return res.status(401).json({ error: { message: 'User not found' } });
    }
    
    // Attach user to request
    (req as any).user = user;
    
    next();
  } catch (error) {
    return res.status(500).json({ error: { message: 'Internal server error' } });
  }
}