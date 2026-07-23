export interface Message {
  id: string;
  sender: 'user' | 'agent';
  content: string;
  timestamp: string;
}

export interface QuickPrompt {
  id: string;
  label: string;
  prompt: string;
}