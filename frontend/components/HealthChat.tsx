'use client';

import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  ShieldAlert, 
  RefreshCw, 
  Stethoscope, 
  HeartPulse 
} from 'lucide-react';
import { Message, QuickPrompt } from '@/types/chat';
import { sendHealthQuery } from '@/lib/api';

const QUICK_PROMPTS: QuickPrompt[] = [
  { id: '1', label: 'Prevención de Dengue', prompt: '¿Cuáles son las medidas preventivas clave contra el Dengue en la comunidad?' },
  { id: '2', label: 'Esquema de Vacunación', prompt: '¿Cuál es la importancia de mantener el esquema de vacunación al día?' },
  { id: '3', label: 'Estilos de Vida Saludables', prompt: '¿Qué recomendaciones hay para prevenir enfermedades cardiovasculares?' },
];

export default function HealthChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'agent',
      content: '¡Hola! Soy tu asistente virtual del sector salud. ¿En qué puedo orientarte hoy sobre servicios, prevención o información general?',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim() || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setIsLoading(true);

    try {
      const replyText = await sendHealthQuery(query);
      const agentMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'agent',
        content: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, agentMsg]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'agent',
          content: 'Ocurrió un error al procesar tu solicitud. Por favor intenta de nuevo en unos momentos.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[85vh] max-w-4xl mx-auto bg-slate-50 border border-slate-200 rounded-2xl shadow-xl overflow-hidden">
      
      {/* Header */}
      <header className="bg-gradient-to-r from-sky-700 via-teal-700 to-teal-800 text-white p-4 flex items-center justify-between shadow-md">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-white/10 backdrop-blur-md rounded-xl border border-white/20">
            <Stethoscope className="w-6 h-6 text-teal-200" />
          </div>
          <div>
            <h1 className="font-semibold text-lg tracking-wide flex items-center gap-2">
              Asistente Inteligente de Salud
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-teal-500/30 text-teal-100 border border-teal-300/30">
                <HeartPulse className="w-3 h-3 mr-1 animate-pulse text-emerald-300" /> Activo
              </span>
            </h1>
            <p className="text-xs text-sky-100/80">Respuestas informativas sobre el sector salud</p>
          </div>
        </div>
        <button
          onClick={() => setMessages([messages[0]])}
          className="p-2 text-sky-100 hover:text-white hover:bg-white/10 rounded-lg transition-colors text-xs flex items-center gap-1"
          title="Reiniciar conversación"
        >
          <RefreshCw className="w-4 h-4" />
          <span className="hidden sm:inline">Limpiar</span>
        </button>
      </header>

      {/* Aviso Médico Preventivo */}
      <div className="bg-amber-50/90 border-b border-amber-200/80 px-4 py-2.5 flex items-center space-x-2 text-amber-900 text-xs">
        <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
        <p>
          <span className="font-semibold">Aviso importante:</span> Este agente proporciona información de carácter informativo basada en documentación oficial del Ministerio de Salud y Protección Social. No sustituye los canales oficiales ni constituye asesoría médica, legal o administrativa.
        </p>
      </div>

      {/* Área de Mensajes */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-slate-50">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start gap-3 ${
              msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            {/* Avatar */}
            <div
              className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 shadow-sm ${
                msg.sender === 'user'
                  ? 'bg-sky-600 text-white'
                  : 'bg-teal-600 text-white'
              }`}
            >
              {msg.sender === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>

            {/* Burbuja de Mensaje */}
            <div
              className={`max-w-[80%] sm:max-w-[70%] rounded-2xl px-4 py-3 shadow-sm text-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-sky-600 text-white rounded-tr-none'
                  : 'bg-white border border-slate-200/80 text-slate-800 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>
              <span
                className={`block text-[10px] mt-1.5 text-right ${
                  msg.sender === 'user' ? 'text-sky-200' : 'text-slate-400'
                }`}
              >
                {msg.timestamp}
              </span>
            </div>
          </div>
        ))}

        {/* Skeleton de Carga */}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-full bg-teal-600 text-white flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5" />
            </div>
            <div className="bg-white border border-slate-200/80 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm text-slate-500 text-sm flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-bounce"></div>
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.2s]"></div>
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.4s]"></div>
              <span className="text-xs text-slate-400 ml-2">Consultando información...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Sugerencias Rápidas */}
      {messages.length === 1 && (
        <div className="px-4 py-2 bg-slate-100/60 border-t border-slate-200/60">
          <p className="text-xs text-slate-500 mb-2 font-medium flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-teal-600" /> Consultas frecuentes:
          </p>
          <div className="flex flex-wrap gap-2">
            {QUICK_PROMPTS.map((item) => (
              <button
                key={item.id}
                onClick={() => handleSend(item.prompt)}
                className="text-xs bg-white hover:bg-teal-50 text-slate-700 hover:text-teal-700 border border-slate-200 hover:border-teal-300 rounded-full px-3 py-1.5 transition-all shadow-xs active:scale-95"
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input de Pregunta */}
      <div className="p-3 sm:p-4 bg-white border-t border-slate-200">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu consulta sobre el sector salud..."
            disabled={isLoading}
            className="flex-1 bg-slate-50 text-slate-800 border border-slate-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-200 rounded-xl px-4 py-2.5 text-sm outline-none transition-all placeholder:text-slate-400 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-teal-600 hover:bg-teal-700 disabled:bg-slate-300 text-white rounded-xl px-4 py-2.5 font-medium transition-colors shadow-sm flex items-center justify-center shrink-0 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}