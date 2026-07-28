import { Source } from "@/types/chat";

type HealthQueryResponse = {
  reply: string;
  sources: Source[];
};

export async function sendHealthQuery(prompt: string): Promise<HealthQueryResponse> {

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error('No se pudo conectar con el servicio de información.');
  }

  const data = await response.json();
  return data;
}