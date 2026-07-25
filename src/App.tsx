import { useState, useEffect } from 'react';
import { BookOpen, Brain, Home, Settings } from 'lucide-react';
import WordCard from './components/WordCard';
import QuizMode from './components/QuizMode';
import CategorySelector from './components/CategorySelector';
import ProgressBar from './components/ProgressBar';
import StatsPanel from './components/StatsPanel';
import { categories, getWordsByCategory, getTotalWordCount } from './data/vocabulary';
import {
  getProgress,
  getWordProgress,
  updateWordProgress,
  getCategoryStats,
  getSettings,
  saveSettings,
} from './utils/storage';
import { Word, StudyMode } from './types/vocabulary';

type TabType = 'home' | 'study' | 'stats' | 'settings';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('home');
  const [selectedCategory, setSelectedCategory] = useState<string>('gaokao');
  const [studyMode, setStudyMode] = useState<StudyMode>('recite');
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [words, setWords] = useState<Word[]>([]);
  const [todayProgress, setTodayProgress] = useState(0);
  const [dailyGoal, setDailyGoal] = useState(20);
  const [categoryStats, setCategoryStats] = useState({ total: 0, learned: 0, mastered: 0 });

  useEffect(() => {
    const settings = getSettings();
    setSelectedCategory(settings.currentCategory);
    setStudyMode(settings.studyMode);
    setDailyGoal(settings.dailyGoal);
  }, []);

  useEffect(() => {
    const newWords = getWordsByCategory(selectedCategory);
    setWords(newWords);
    setCurrentWordIndex(0);
    const stats = getCategoryStats(selectedCategory);
    setCategoryStats(stats);
  }, [selectedCategory]);

  useEffect(() => {
    const today = new Date().toDateString();
    const progress = getProgress();
    const count = Object.values(progress).filter(
      p => p.lastReview === today && p.status !== 'unlearned'
    ).length;
    setTodayProgress(count);
  }, [currentWordIndex]);

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category);
    saveSettings({ currentCategory: category as any, studyMode, dailyGoal });
  };

  const handleStudyModeChange = (mode: StudyMode) => {
    setStudyMode(mode);
    saveSettings({ currentCategory: selectedCategory as any, studyMode: mode, dailyGoal });
    if (mode === 'recite') {
      setCurrentWordIndex(0);
    }
  };

  const handleNextWord = () => {
    if (currentWordIndex < words.length - 1) {
      setCurrentWordIndex(prev => prev + 1);
    }
  };

  const handleMarkMastered = () => {
    const word = words[currentWordIndex];
    const currentProgress = getWordProgress(word.id);
    updateWordProgress(word.id, {
      status: 'mastered',
      lastReview: new Date().toDateString(),
      reviewCount: currentProgress.reviewCount + 1,
      correctCount: currentProgress.correctCount + 1,
    });
    setCategoryStats(prev => ({ ...prev, mastered: prev.mastered + 1 }));
  };

  const handleMarkLearning = () => {
    const word = words[currentWordIndex];
    const currentProgress = getWordProgress(word.id);
    updateWordProgress(word.id, {
      status: 'learning',
      lastReview: new Date().toDateString(),
      reviewCount: currentProgress.reviewCount + 1,
    });
    setCategoryStats(prev => ({ ...prev, learned: prev.learned + 1 }));
  };

  const handleQuizComplete = (_score: number, _total: number) => {
  };

  const handleDailyGoalChange = (value: number) => {
    setDailyGoal(value);
    saveSettings({ currentCategory: selectedCategory as any, studyMode, dailyGoal: value });
  };

  const currentWord = words[currentWordIndex];
  const totalWords = getTotalWordCount(selectedCategory);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-lg mx-auto pb-20">
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="px-4 py-4">
            <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
              <Brain className="w-6 h-6 text-blue-500" />
              词汇背诵助手
            </h1>
          </div>
        </header>

        <main className="p-4">
          {activeTab === 'home' && (
            <div>
              <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-6 text-white mb-8">
                <h2 className="text-2xl font-bold mb-2">开始今天的学习</h2>
                <p className="text-blue-100 mb-4">每天坚持，词汇量稳步提升</p>
                <button
                  onClick={() => setActiveTab('study')}
                  className="bg-white text-blue-600 px-6 py-2 rounded-xl font-medium hover:bg-blue-50 transition-colors flex items-center gap-2"
                >
                  <BookOpen className="w-5 h-5" />
                  <span>开始学习</span>
                </button>
              </div>

              <h3 className="text-lg font-bold text-gray-800 mb-4">选择词汇类别</h3>
              <CategorySelector
                categories={categories}
                selectedCategory={selectedCategory}
                onSelect={handleCategorySelect}
              />

              <div className="bg-white rounded-xl p-4 shadow-sm mt-8">
                <h3 className="font-bold text-gray-800 mb-3">学习模式</h3>
                <div className="flex gap-4">
                  <button
                    onClick={() => handleStudyModeChange('recite')}
                    className={`flex-1 p-3 rounded-xl border-2 transition-all ${
                      studyMode === 'recite'
                        ? 'border-blue-500 bg-blue-50 text-blue-600'
                        : 'border-gray-200 text-gray-600 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-center gap-2">
                      <BookOpen className="w-5 h-5" />
                      <span>背诵模式</span>
                    </div>
                  </button>
                  <button
                    onClick={() => handleStudyModeChange('quiz')}
                    className={`flex-1 p-3 rounded-xl border-2 transition-all ${
                      studyMode === 'quiz'
                        ? 'border-green-500 bg-green-50 text-green-600'
                        : 'border-gray-200 text-gray-600 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-center gap-2">
                      <Brain className="w-5 h-5" />
                      <span>测验模式</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'study' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <button
                  onClick={() => setActiveTab('home')}
                  className="text-gray-500 hover:text-gray-700 transition-colors"
                >
                  返回
                </button>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleStudyModeChange('recite')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      studyMode === 'recite'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    背诵
                  </button>
                  <button
                    onClick={() => handleStudyModeChange('quiz')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      studyMode === 'quiz'
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    测验
                  </button>
                </div>
              </div>

              {studyMode === 'recite' ? (
                <>
                  <ProgressBar
                    current={currentWordIndex + 1}
                    total={totalWords}
                    label="学习进度"
                  />
                  <div className="mt-8">
                    {currentWord && (
                      <WordCard
                        word={currentWord}
                        onNext={handleNextWord}
                        onMarkMastered={handleMarkMastered}
                        onMarkLearning={handleMarkLearning}
                      />
                    )}
                  </div>
                </>
              ) : (
                <QuizMode
                  words={words}
                  onComplete={handleQuizComplete}
                  onBack={() => setActiveTab('home')}
                />
              )}
            </div>
          )}

          {activeTab === 'stats' && (
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-6">学习统计</h2>
              <StatsPanel
                total={totalWords}
                learned={categoryStats.learned}
                mastered={categoryStats.mastered}
                todayProgress={todayProgress}
                dailyGoal={dailyGoal}
              />

              <div className="bg-white rounded-xl p-4 shadow-sm">
                <h3 className="font-bold text-gray-800 mb-4">各分类进度</h3>
                <div className="space-y-4">
                  {categories.map((category) => {
                    const stats = getCategoryStats(category.key);
                    const percentage = stats.total > 0 ? (stats.mastered / stats.total) * 100 : 0;
                    return (
                      <div key={category.key}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-gray-700">{category.name}</span>
                          <span className="text-sm text-gray-500">
                            {stats.mastered}/{stats.total} ({percentage.toFixed(0)}%)
                          </span>
                        </div>
                        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full rounded-full transition-all"
                            style={{ width: `${percentage}%`, backgroundColor: category.color }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-6">设置</h2>
              <div className="bg-white rounded-xl p-4 shadow-sm mb-4">
                <h3 className="font-bold text-gray-800 mb-4">每日学习目标</h3>
                <div className="flex items-center gap-4">
                  {[10, 20, 30, 50].map((goal) => (
                    <button
                      key={goal}
                      onClick={() => handleDailyGoalChange(goal)}
                      className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
                        dailyGoal === goal
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      {goal}词/天
                    </button>
                  ))}
                </div>
              </div>

              <div className="bg-white rounded-xl p-4 shadow-sm">
                <h3 className="font-bold text-gray-800 mb-4">当前设置</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">当前词汇类别</span>
                    <span className="font-medium text-gray-800">
                      {categories.find(c => c.key === selectedCategory)?.name}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">学习模式</span>
                    <span className="font-medium text-gray-800">
                      {studyMode === 'recite' ? '背诵模式' : '测验模式'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">每日目标</span>
                    <span className="font-medium text-gray-800">{dailyGoal}词</span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => {
                  localStorage.clear();
                  window.location.reload();
                }}
                className="w-full mt-6 py-3 bg-red-50 text-red-600 rounded-xl hover:bg-red-100 transition-colors"
              >
                重置所有数据
              </button>
            </div>
          )}
        </main>

        <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200">
          <div className="max-w-lg mx-auto flex justify-around items-center h-16">
            <button
              onClick={() => setActiveTab('home')}
              className={`flex flex-col items-center justify-center w-full h-full transition-colors ${
                activeTab === 'home' ? 'text-blue-500' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <Home className="w-6 h-6" />
              <span className="text-xs mt-1">首页</span>
            </button>
            <button
              onClick={() => setActiveTab('study')}
              className={`flex flex-col items-center justify-center w-full h-full transition-colors ${
                activeTab === 'study' ? 'text-blue-500' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <BookOpen className="w-6 h-6" />
              <span className="text-xs mt-1">学习</span>
            </button>
            <button
              onClick={() => setActiveTab('stats')}
              className={`flex flex-col items-center justify-center w-full h-full transition-colors ${
                activeTab === 'stats' ? 'text-blue-500' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <Brain className="w-6 h-6" />
              <span className="text-xs mt-1">统计</span>
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`flex flex-col items-center justify-center w-full h-full transition-colors ${
                activeTab === 'settings' ? 'text-blue-500' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <Settings className="w-6 h-6" />
              <span className="text-xs mt-1">设置</span>
            </button>
          </div>
        </nav>
      </div>
    </div>
  );
}

export default App;
