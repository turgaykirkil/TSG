export type TaskPriority = 'low' | 'medium' | 'high';

export type ChecklistItem = {
  id: string;
  title: string;
  completed: boolean;
};

export type Task = {
  id: string;
  title: string;
  description: string;
  dueDate: Date | string;
  priority: TaskPriority;
  customerId: string;
  customerName: string;
  assignedTo: string;
  assigneeName: string;
  status: 'todo' | 'in_progress' | 'completed';
  progress: number;
  checklist: ChecklistItem[];
  createdAt: Date | string;
  updatedAt: Date | string;
};

export type NewTaskInput = Omit<
  Task,
  'id' | 'status' | 'progress' | 'createdAt' | 'updatedAt'
>;

export type TaskFormValues = {
  title: string;
  description: string;
  dueDate: Date;
  priority: 'low' | 'medium' | 'high';
  customerId: string;
  customerName: string;
  assignedTo: string;
  assigneeName: string;
  checklist: Array<{
    id: string;
    title: string;
    completed: boolean;
  }>;
  status?: 'todo' | 'in_progress' | 'completed' | 'pending';
};

// Memoization için basit bir yardımcı fonksiyon
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map();
  return function(this: any, ...args: any[]) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  } as T;
}

export const getPriorityColor = memoize((priority: TaskPriority): string => {
  switch (priority) {
    case 'high':
      return '#dc3545'; // error red
    case 'medium':
      return '#ffc107'; // warning yellow
    case 'low':
      return '#28a745'; // success green
    default:
      return '#6c757d'; // gray
  }
});

export const getStatusColor = memoize((status: Task['status']): string => {
  switch (status) {
    case 'completed':
      return '#28a745'; // success green
    case 'in_progress':
      return '#007bff'; // primary blue
    case 'todo':
      return '#6c757d'; // gray
    default:
      return '#6c757d';
  }
});

export const calculateProgress = memoize((task: Task): number => {
  if (!task.checklist || task.checklist.length === 0) return 0;
  
  const completedItems = task.checklist.filter(item => item.completed).length;
  return Math.round((completedItems / task.checklist.length) * 100);
});

export const formatDate = (date?: Date | string | null): string => {
  if (!date) return '-';
  try {
    const parsedDate = typeof date === 'string' ? new Date(date) : date;
    if (!parsedDate || isNaN(parsedDate.getTime())) return '-';
    return parsedDate.toLocaleDateString('tr-TR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  } catch (e) {
    return '-';
  }
};
