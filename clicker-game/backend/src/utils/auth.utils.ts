import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { SignOptions } from 'jsonwebtoken';
import { User } from '../../generated/prisma/browser';

const JWT_SECRET = process.env['JWT_SECRET'] || 'your-secret-key';
const JWT_EXPIRES_IN = process.env['JWT_EXPIRES_IN'] || '1h';

export class AuthUtils {
  static async hashPassword(password: string): Promise<string> {
    const saltRounds = 10;
    return await bcrypt.hash(password, saltRounds);
  }

  static async comparePasswords(
    password: string,
    hashedPassword: string
  ): Promise<boolean> {
    return await bcrypt.compare(password, hashedPassword);
  }

  static generateAccessToken(user: User): string {
    const payload = { userId: user.id, email: user.email };
    const options: SignOptions = { expiresIn: Number(JWT_EXPIRES_IN) };
    return jwt.sign(payload, JWT_SECRET, options);
  }

  static verifyToken(token: string): any {
    try {
      return jwt.verify(token, JWT_SECRET);
    } catch (error) {
      return null;
    }
  }
}