import { decode } from '@msgpack/msgpack';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export async function loadSessions() {
  try {
    const dataPath = join(__dirname, 'sessions.msgpack');
    const buffer = readFileSync(dataPath);
    const data = decode(buffer);
    
    // Debug output removed for MCP compatibility
    return data;
  } catch (error) {
    console.error('Failed to load sessions:', error);
    throw error;
  }
}
