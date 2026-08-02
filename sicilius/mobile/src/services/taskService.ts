import { Task, NewTaskInput } from '../types/task';
import db from '../../db.json';
import AsyncStorage from '@react-native-async-storage/async-storage';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const formatTask = (t: any): Task => ({
  id: String(t.id),
  title: t.title || '',
  description: t.description || '',
  dueDate: t.dueDate || new Date().toISOString(),
  priority: (t.priority as any) || 'medium',
  customerId: String(t.customerId || '1'),
  customerName: t.customerName || 'Müşteri',
  assignedTo: String(t.salesRepId || t.assignedTo || '1'),
  assigneeName: t.assigneeName || 'Temsilci',
  status: (t.status as any) || 'todo',
  progress: t.progress || 0,
  checklist: t.checklist || [],
  createdAt: t.createdAt || new Date().toISOString(),
  updatedAt: t.updatedAt || new Date().toISOString(),
});

export const taskService = {
  getTasks: async (params?: {
    search?: string;
    status?: string[];
    priority?: string[];
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    userId?: string;
    role?: 'admin' | 'supervisor' | 'sales_rep';
  }): Promise<Task[]> => {
    let tasks: Task[] = [];
    try {
      const { taskAPI } = require('./api');
      const apiTasks = await taskAPI.getAll();
      if (Array.isArray(apiTasks) && apiTasks.length > 0) {
        tasks = apiTasks.map(formatTask);
      }
    } catch (e) {
      // API error handled by fallback below
    }

    if (tasks.length === 0) {
      tasks = db.tasks.map(formatTask);
    }
    
    if (params?.search) {
      const searchLower = params.search.toLowerCase();
      tasks = tasks.filter(task => 
        task.title.toLowerCase().includes(searchLower) ||
        task.description.toLowerCase().includes(searchLower)
      );
    }

    if (params?.status?.length) {
      tasks = tasks.filter(task => params.status!.includes(task.status));
    }

    if (params?.priority?.length) {
      tasks = tasks.filter(task => params.priority!.includes(task.priority));
    }

    return tasks;
  },

  getTaskById: async (id: string): Promise<Task | null> => {
    await delay(300);
    const task = db.tasks.find(t => String(t.id) === String(id));
    return task ? formatTask(task) : null;
  },

  createTask: async (input: NewTaskInput): Promise<Task> => {
    await delay(300);
    const newTask: Task = {
      ...input,
      id: Date.now().toString(),
      status: 'todo',
      progress: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    return newTask;
  },

  updateTask: async (id: string, updates: Partial<Task>): Promise<Task> => {
    await delay(300);
    const task = db.tasks.find(t => String(t.id) === String(id));
    if (!task) throw new Error('Task not found');
    const updated = formatTask({ ...task, ...updates, updatedAt: new Date().toISOString() });
    return updated;
  },

  deleteTask: async (id: string): Promise<void> => {
    await delay(300);
  },

  updateChecklistItem: async (
    taskId: string,
    itemId: string,
    completed: boolean
  ): Promise<Task> => {
    await delay(300);
    const rawTask = db.tasks.find(t => String(t.id) === String(taskId));
    if (!rawTask) throw new Error('Task not found');
    const task = formatTask(rawTask);
    const checklistItem = task.checklist.find(item => item.id === itemId);
    if (checklistItem) {
      checklistItem.completed = completed;
    }
    task.updatedAt = new Date().toISOString();
    return task;
  },

  updateTaskStatus: async (
    id: string,
    status: Task['status']
  ): Promise<Task> => {
    await delay(300);
    const rawTask = db.tasks.find(t => String(t.id) === String(id));
    if (!rawTask) throw new Error('Task not found');
    const task = formatTask(rawTask);
    task.status = status;
    task.updatedAt = new Date().toISOString();
    return task;
  },

  updateTaskProgress: async (
    id: string,
    progress: number
  ): Promise<Task> => {
    await delay(300);
    const rawTask = db.tasks.find(t => String(t.id) === String(id));
    if (!rawTask) throw new Error('Task not found');
    const task = formatTask(rawTask);
    task.progress = progress;
    task.updatedAt = new Date().toISOString();
    return task;
  },
};
