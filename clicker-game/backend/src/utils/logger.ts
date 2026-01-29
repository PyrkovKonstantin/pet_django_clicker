import pino from 'pino';

/**
 * Logger utility using pino
 */
const logger = pino({
  level: process.env['LOG_LEVEL'] || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'yyyy-mm-dd HH:MM:ss.l',
      ignore: 'pid,hostname'
    }
  }
});

export default logger;