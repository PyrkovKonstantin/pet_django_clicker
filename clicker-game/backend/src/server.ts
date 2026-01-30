import 'reflect-metadata';
import dotenv from 'dotenv';
// import app from './app';
import { container } from './container';
import { InversifyExpressHttpAdapter } from '@inversifyjs/http-express';
import express from 'express'; 

// Load environment variables
dotenv.config();

const PORT = process.env['PORT'] || 3000;


const adapter: InversifyExpressHttpAdapter = new InversifyExpressHttpAdapter(
  container,
);

const application: express.Application = await adapter.build();

application.listen(3000);

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('Gracefully shutting down...');
  process.exit(0);
});