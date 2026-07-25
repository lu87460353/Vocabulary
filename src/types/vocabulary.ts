export interface Word {
  id: string;
  word: string;
  phonetic: string;
  meaning: string;
  example: string;
  category: 'gaokao' | 'kaoyan' | 'cet4' | 'cet6';
}

export interface UserProgress {
  wordId: string;
  status: 'unlearned' | 'learning' | 'mastered';
  lastReview: string | null;
  reviewCount: number;
  correctCount: number;
}

export interface CategoryInfo {
  key: 'gaokao' | 'kaoyan' | 'cet4' | 'cet6';
  name: string;
  description: string;
  icon: string;
  color: string;
}

export type StudyMode = 'recite' | 'quiz';
