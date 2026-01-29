import { Request, Response, NextFunction } from 'express';

/**
 * Global error handling middleware
 * Returns a consistent error format
 */
export function errorMiddleware(
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error (in production, you might want to use a proper logging library)
  console.error(err);
  
  // Default error
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  // Return consistent error format
  return res.status(statusCode).json({
    error: {
      message,
      code: err.code
    }
  });
}