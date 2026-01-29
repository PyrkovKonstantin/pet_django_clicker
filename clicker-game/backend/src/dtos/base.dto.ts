import { plainToInstance } from 'class-transformer';
import { validate } from 'class-validator';
import { Request, Response, NextFunction } from 'express';

export abstract class BaseDto {
  async validate() {
    const errors = await validate(this);
    if (errors.length > 0) {
      throw new Error(JSON.stringify(errors));
    }
  }

  static async validateRequest<T extends BaseDto>(
    req: Request,
    res: Response,
    next: NextFunction,
    DtoClass: new () => T
  ): Promise<void> {
    try {
      const dto = plainToInstance(DtoClass, req.body);
      await dto.validate();
      req.body = dto;
      next();
    } catch (error) {
      res.status(400).json({ 
        error: { 
          message: 'Validation failed', 
          details: error instanceof Error ? error.message : 'Unknown error' 
        } 
      });
    }
  }
}