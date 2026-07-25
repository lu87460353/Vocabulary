import { UserProgress } from '../types/vocabulary';

const PROGRESS_KEY = 'vocabulary_progress';
const SETTINGS_KEY = 'vocabulary_settings';

export const getProgress = (): Record<string, UserProgress> => {
  try {
    const data = localStorage.getItem(PROGRESS_KEY);
    return data ? JSON.parse(data) : {};
  } catch {
    return {};
  }
};

export const saveProgress = (progress: Record<string, UserProgress>): void => {
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
};

export const updateWordProgress = (
  wordId: string,
  update: Partial<UserProgress>
): void => {
  const progress = getProgress();
  const existing = progress[wordId] || {
    wordId,
    status: 'unlearned' as const,
    lastReview: null,
    reviewCount: 0,
    correctCount: 0,
  };
  progress[wordId] = {
    ...existing,
    ...update,
    reviewCount: 'reviewCount' in update ? (update.reviewCount as number) : existing.reviewCount,
    correctCount: 'correctCount' in update ? (update.correctCount as number) : existing.correctCount,
  };
  saveProgress(progress);
};

export const getWordProgress = (wordId: string): UserProgress => {
  const progress = getProgress();
  return progress[wordId] || {
    wordId,
    status: 'unlearned',
    lastReview: null,
    reviewCount: 0,
    correctCount: 0,
  };
};

export const getCategoryStats = (category: string): {
  total: number;
  learned: number;
  mastered: number;
} => {
  const progress = getProgress();
  const wordIds = Object.keys(progress).filter(id => id.startsWith(category));
  
  let learned = 0;
  let mastered = 0;
  
  wordIds.forEach(id => {
    const status = progress[id].status;
    if (status === 'learning') learned++;
    else if (status === 'mastered') mastered++;
  });
  
  return {
    total: wordIds.length,
    learned,
    mastered,
  };
};

export interface Settings {
  currentCategory: 'gaokao' | 'kaoyan' | 'cet4' | 'cet6';
  studyMode: 'recite' | 'quiz';
  dailyGoal: number;
}

export const getSettings = (): Settings => {
  try {
    const data = localStorage.getItem(SETTINGS_KEY);
    return data ? JSON.parse(data) : {
      currentCategory: 'gaokao',
      studyMode: 'recite',
      dailyGoal: 20,
    };
  } catch {
    return {
      currentCategory: 'gaokao',
      studyMode: 'recite',
      dailyGoal: 20,
    };
  }
};

export const saveSettings = (settings: Settings): void => {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
};
