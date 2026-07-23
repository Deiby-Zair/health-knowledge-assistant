import { Message } from '@/types/chat';

export async function sendHealthQuery(prompt: string): Promise<string> {

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error('No se pudo conectar con el servicio de salud.');
  }

  const data = await response.json();
  return data.reply;
}