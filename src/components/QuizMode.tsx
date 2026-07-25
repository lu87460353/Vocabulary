import { useState, useEffect } from 'react';
import { Check, X, RotateCcw, ArrowRight } from 'lucide-react';
import { Word } from '../types/vocabulary';

interface QuizModeProps {
  words: Word[];
  onComplete: (score: number, total: number) => void;
  onBack: () => void;
}

export default function QuizMode({ words, onComplete, onBack }: QuizModeProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);

  const currentWord = words[currentIndex];

  const getOptions = () => {
    const correctOption = currentWord.meaning;
    const otherWords = words.filter(w => w.id !== currentWord.id);
    const shuffled = otherWords.sort(() => Math.random() - 0.5).slice(0, 3);
    const options = [...shuffled.map(w => w.meaning), correctOption];
    return options.sort(() => Math.random() - 0.5);
  };

  const [options] = useState(() => getOptions());

  useEffect(() => {
    setSelectedAnswer(null);
    setIsCorrect(null);
  }, [currentIndex]);

  const handleSelect = (option: string) => {
    if (selectedAnswer !== null) return;
    
    setSelectedAnswer(option);
    const correct = option === currentWord.meaning;
    setIsCorrect(correct);
    if (correct) {
      setScore(prev => prev + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < words.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      setShowResult(true);
      onComplete(score, words.length);
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setScore(0);
    setShowResult(false);
  };

  if (showResult) {
    const percentage = (score / words.length) * 100;
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="mb-6">
            {percentage >= 80 ? (
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Check className="w-10 h-10 text-green-500" />
              </div>
            ) : percentage >= 60 ? (
              <div className="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">👍</span>
              </div>
            ) : (
              <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">💪</span>
              </div>
            )}
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">测验完成!</h2>
          <p className="text-gray-600 mb-6">
            你的得分: <span className="text-3xl font-bold text-blue-600">{score}</span> / {words.length}
          </p>
          <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden mb-6">
            <div
              className={`h-full transition-all duration-500 rounded-full ${
                percentage >= 80 ? 'bg-green-500' : percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${percentage}%` }}
            />
          </div>
          <div className="flex gap-4">
            <button
              onClick={handleRestart}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors"
            >
              <RotateCcw className="w-5 h-5" />
              <span>再测一次</span>
            </button>
            <button
              onClick={onBack}
              className="flex-1 px-4 py-3 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200 transition-colors"
            >
              返回
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={onBack}
          className="text-gray-500 hover:text-gray-700 transition-colors"
        >
          返回
        </button>
        <div className="text-sm text-gray-500">
          {currentIndex + 1} / {words.length}
        </div>
        <div className="text-sm font-medium text-blue-600">
          得分: {score}
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-2">{currentWord.word}</h2>
          <p className="text-gray-500">{currentWord.phonetic}</p>
          <p className="mt-4 text-gray-600 font-medium">请选择正确的释义:</p>
        </div>

        <div className="space-y-3">
          {options.map((option, index) => {
            let bgColor = 'bg-gray-50';
            let textColor = 'text-gray-700';
            let borderColor = 'border-gray-200';

            if (selectedAnswer === option) {
              if (isCorrect) {
                bgColor = 'bg-green-100';
                textColor = 'text-green-700';
                borderColor = 'border-green-500';
              } else {
                bgColor = 'bg-red-100';
                textColor = 'text-red-700';
                borderColor = 'border-red-500';
              }
            } else if (isCorrect !== null && option === currentWord.meaning) {
              bgColor = 'bg-green-100';
              textColor = 'text-green-700';
              borderColor = 'border-green-500';
            }

            return (
              <button
                key={index}
                onClick={() => handleSelect(option)}
                disabled={selectedAnswer !== null}
                className={`w-full p-4 rounded-xl border-2 transition-all text-left ${bgColor} ${textColor} ${borderColor} ${
                  selectedAnswer === null ? 'hover:bg-gray-100 cursor-pointer' : 'cursor-default'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium">{option}</span>
                  {selectedAnswer === option && isCorrect && (
                    <Check className="w-5 h-5 text-green-500" />
                  )}
                  {selectedAnswer === option && !isCorrect && (
                    <X className="w-5 h-5 text-red-500" />
                  )}
                  {selectedAnswer !== null && option === currentWord.meaning && (
                    <Check className="w-5 h-5 text-green-500" />
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {selectedAnswer !== null && (
          <div className="mt-6">
            <button
              onClick={handleNext}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors"
            >
              <span>{currentIndex < words.length - 1 ? '下一题' : '查看结果'}</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
