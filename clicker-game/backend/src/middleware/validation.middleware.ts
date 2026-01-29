import { Request, Response, NextFunction } from 'express';
import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';

/**
 * Validation middleware
 * Validates request body against a DTO class
 */
export function validateDto(dtoClass: any) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      // Convert request body to DTO instance
      const dto = plainToInstance(dtoClass, req.body);
      
      // Validate DTO
      const errors = await validate(dto);
      
      // If validation errors, return them
      if (errors.length > 0) {
        const errorMessages = errors.map(error => 
          Object.values(error.constraints || {})
        ).flat();
        
        return res.status(400).json({
          error: {
            message: 'Validation failed',
            details: errorMessages
          }
        });
      }
      
      // If validation passes, continue
      next();
    } catch (error) {
      return res.status(500).json({ error: { message: 'Internal server error' } });
    }
  };
}