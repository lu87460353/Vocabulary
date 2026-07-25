import { useState } from 'react';
import { Volume2, RotateCcw, Check, X } from 'lucide-react';
import { Word } from '../types/vocabulary';

interface WordCardProps {
  word: Word;
  onNext: () => void;
  onMarkMastered: () => void;
  onMarkLearning: () => void;
}

export default function WordCard({ word, onNext, onMarkMastered, onMarkLearning }: WordCardProps) {
  const [showAnswer, setShowAnswer] = useState(false);
  const [isFlipped, setIsFlipped] = useState(false);

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
    setShowAnswer(!showAnswer);
  };

  const handleSpeak = () => {
    const utterance = new SpeechSynthesisUtterance(word.word);
    utterance.lang = 'en-US';
    speechSynthesis.speak(utterance);
  };

  return (
    <div className="relative w-full max-w-md mx-auto perspective-1000">
      <div
        className={`relative w-full h-80 transition-transform duration-500 transform-style-3d cursor-pointer ${
          isFlipped ? 'rotate-y-180' : ''
        }`}
        onClick={handleFlip}
        style={{
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}
      >
        <div
          className="absolute inset-0 bg-white rounded-2xl shadow-xl p-8 flex flex-col items-center justify-center backface-hidden"
          style={{ backfaceVisibility: 'hidden' }}
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleSpeak();
            }}
            className="absolute top-4 right-4 p-3 bg-blue-50 rounded-full hover:bg-blue-100 transition-colors"
          >
            <Volume2 className="w-5 h-5 text-blue-500" />
          </button>
          <h2 className="text-4xl font-bold text-gray-800 mb-4">{word.word}</h2>
          <p className="text-lg text-gray-500">{word.phonetic}</p>
          <p className="mt-8 text-gray-400 text-sm">点击卡片查看释义</p>
        </div>

        <div
          className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl shadow-xl p-8 flex flex-col items-center justify-center overflow-y-auto"
          style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
        >
          <h2 className="text-3xl font-bold text-gray-800 mb-3">{word.word}</h2>
          <p className="text-gray-500 mb-4">{word.phonetic}</p>
          <div className="w-full bg-white/80 rounded-xl p-4 mb-4">
            <p className="text-gray-700 text-lg leading-relaxed">{word.meaning}</p>
          </div>
          <div className="w-full bg-white/80 rounded-xl p-4">
            <p className="text-gray-600 text-sm italic">{word.example}</p>
          </div>
        </div>
      </div>

      {showAnswer && (
        <div className="flex justify-center gap-4 mt-8">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onMarkLearning();
              onNext();
            }}
            className="flex items-center gap-2 px-6 py-3 bg-orange-100 text-orange-600 rounded-xl hover:bg-orange-200 transition-colors font-medium"
          >
            <X className="w-5 h-5" />
            <span>还没记住</span>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onMarkMastered();
              onNext();
            }}
            className="flex items-center gap-2 px-6 py-3 bg-green-100 text-green-600 rounded-xl hover:bg-green-200 transition-colors font-medium"
          >
            <Check className="w-5 h-5" />
            <span>已掌握</span>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowAnswer(false);
              setIsFlipped(false);
            }}
            className="flex items-center gap-2 px-6 py-3 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200 transition-colors font-medium"
          >
            <RotateCcw className="w-5 h-5" />
            <span>再看一次</span>
          </button>
        </div>
      )}
    </div>
  );
}
