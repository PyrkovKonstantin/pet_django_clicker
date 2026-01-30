import { Container } from 'inversify';
import { TYPES } from './types.js';
import { AuthService } from './services/auth.service.js';
import { GameService } from './services/game.service.js';
import { AuthController } from './controllers/auth.controller.js';
import { GameController } from './controllers/game.controller.js';

const container = new Container();

// Bind services
container.bind<AuthService>(TYPES.AuthService).to(AuthService).inSingletonScope();
container.bind<GameService>(TYPES.GameService).to(GameService).inSingletonScope();

// Bind controllers
container.bind<AuthController>('AuthController').to(AuthController).inSingletonScope();
container.bind<GameController>('GameController').to(GameController).inSingletonScope();

export { container };