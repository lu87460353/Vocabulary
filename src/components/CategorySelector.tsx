import { GraduationCap, BookOpen, Award, Trophy } from 'lucide-react';
import { CategoryInfo } from '../types/vocabulary';

interface CategorySelectorProps {
  categories: CategoryInfo[];
  selectedCategory: string;
  onSelect: (category: string) => void;
}

const iconMap = {
  GraduationCap,
  BookOpen,
  Award,
  Trophy,
};

export default function CategorySelector({ categories, selectedCategory, onSelect }: CategorySelectorProps) {
  return (
    <div className="grid grid-cols-2 gap-4 mb-8">
      {categories.map((category) => {
        const IconComponent = iconMap[category.icon as keyof typeof iconMap] || BookOpen;
        const isSelected = selectedCategory === category.key;

        return (
          <button
            key={category.key}
            onClick={() => onSelect(category.key)}
            className={`p-4 rounded-xl border-2 transition-all text-left ${
              isSelected
                ? 'border-blue-500 bg-blue-50 shadow-lg'
                : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
            }`}
          >
            <div className="flex items-center gap-3 mb-2">
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: `${category.color}20` }}
              >
                <IconComponent
                  className="w-5 h-5"
                  style={{ color: category.color }}
                />
              </div>
              <span className="font-bold text-gray-800">{category.name}</span>
            </div>
            <p className="text-sm text-gray-500">{category.description}</p>
          </button>
        );
      })}
    </div>
  );
}
