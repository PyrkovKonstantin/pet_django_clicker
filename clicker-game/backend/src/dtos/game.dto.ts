import { IsInt, IsString, IsDateString, Min, Max } from 'class-validator';
import { BaseDto } from './base.dto.js';

export class ClickDto extends BaseDto {
  @IsInt()
  @Min(1)
  @Max(100)
  clicks!: number;

  @IsDateString()
  timestamp!: string;

  @IsInt()
  @Min(0)
  energy!: number;

  @IsInt()
  @Min(0)
  balance!: number;
}

export class UpgradePurchaseDto extends BaseDto {
  @IsInt()
  @Min(1)
  upgradeId!: number;

  @IsInt()
  @Min(0)
  expectedCost!: number;
}

export class ClaimTaskRewardDto extends BaseDto {
  @IsInt()
  @Min(1)
  taskId!: number;
}