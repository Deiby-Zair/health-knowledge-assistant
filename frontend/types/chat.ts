export interface Source {
  title: string;
  location?: string;
  score?: number;
}

export interface Message {
  id: string;
  sender: 'user' | 'agent';
  content: string;
  timestamp: string;
  sources?: Source[];
}

export interface QuickPrompt {
  id: string;
  label: string;
  prompt: string;
}