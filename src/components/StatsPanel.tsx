import { BookOpen, CheckCircle, Clock, Target } from 'lucide-react';

interface StatsPanelProps {
  total: number;
  learned: number;
  mastered: number;
  todayProgress: number;
  dailyGoal: number;
}

export default function StatsPanel({ total, learned, mastered, todayProgress, dailyGoal }: StatsPanelProps) {
  const todayPercentage = dailyGoal > 0 ? (todayProgress / dailyGoal) * 100 : 0;

  return (
    <div className="grid grid-cols-2 gap-4 mb-8">
      <div className="bg-white rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <BookOpen className="w-5 h-5 text-blue-500" />
          <span className="text-sm text-gray-500">总词汇</span>
        </div>
        <p className="text-2xl font-bold text-gray-800">{total}</p>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Clock className="w-5 h-5 text-orange-500" />
          <span className="text-sm text-gray-500">学习中</span>
        </div>
        <p className="text-2xl font-bold text-gray-800">{learned}</p>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <CheckCircle className="w-5 h-5 text-green-500" />
          <span className="text-sm text-gray-500">已掌握</span>
        </div>
        <p className="text-2xl font-bold text-gray-800">{mastered}</p>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Target className="w-5 h-5 text-purple-500" />
          <span className="text-sm text-gray-500">今日进度</span>
        </div>
        <p className="text-2xl font-bold text-gray-800">{todayProgress}/{dailyGoal}</p>
        <div className="w-full h-2 bg-gray-200 rounded-full mt-2 overflow-hidden">
          <div
            className="h-full bg-purple-500 transition-all"
            style={{ width: `${Math.min(todayPercentage, 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
}
