import { IsEmail, IsString, MinLength, MaxLength } from 'class-validator';
import { BaseDto } from './base.dto.js';

export class RegisterDto extends BaseDto {
  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(3)
  @MaxLength(20)
  username!: string;

  @IsString()
  @MinLength(6)
  @MaxLength(50)
  password!: string;
}

export class LoginDto extends BaseDto {
  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(6)
  password!: string;
}