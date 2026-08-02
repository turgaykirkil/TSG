import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Task, NewTaskInput } from '../../types/task';
import { taskService } from '../../services/taskService';

export type TaskStatus = 'todo' | 'in_progress' | 'completed';

interface TaskState {
  tasks: Task[];
  selectedTask: Task | null;
  loading: boolean;
  error: string | null;
}

const initialState: TaskState = {
  tasks: [],
  selectedTask: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchTasks = createAsyncThunk('tasks/fetchTasks', async () => {
  const tasks = await taskService.getTasks();
  return tasks.map(task => ({
    ...task,
    dueDate: new Date(task.dueDate).toISOString(),
    createdAt: new Date(task.createdAt).toISOString(),
    updatedAt: new Date(task.updatedAt).toISOString(),
  }));
});

export const fetchTaskById = createAsyncThunk(
  'tasks/fetchTaskById',
  async (id: string) => {
    const task = await taskService.getTaskById(id);
    if (!task) throw new Error('Task not found');
    return {
      ...task,
      dueDate: new Date(task.dueDate).toISOString(),
      createdAt: new Date(task.createdAt).toISOString(),
      updatedAt: new Date(task.updatedAt).toISOString(),
    };
  }
);

export const createTask = createAsyncThunk(
  'tasks/createTask',
  async (newTask: NewTaskInput) => {
    const task = await taskService.createTask(newTask);
    return {
      ...task,
      dueDate: new Date(task.dueDate).toISOString(),
      createdAt: new Date(task.createdAt).toISOString(),
      updatedAt: new Date(task.updatedAt).toISOString(),
    };
  }
);

export const updateTask = createAsyncThunk(
  'tasks/updateTask',
  async ({ id, updates }: { id: string; updates: Partial<Task> }) => {
    const task = await taskService.updateTask(id, updates);
    return {
      ...task,
      dueDate: new Date(task.dueDate).toISOString(),
      createdAt: new Date(task.createdAt).toISOString(),
      updatedAt: new Date(task.updatedAt).toISOString(),
    };
  }
);

export const deleteTask = createAsyncThunk(
  'tasks/deleteTask',
  async (id: string) => {
    await taskService.deleteTask(id);
    return id;
  }
);

export const updateTaskStatus = createAsyncThunk(
  'tasks/updateTaskStatus',
  async ({ id, status }: { id: string; status: Task['status'] }) => {
    const task = await taskService.updateTaskStatus(id, status);
    return {
      ...task,
      dueDate: new Date(task.dueDate).toISOString(),
      createdAt: new Date(task.createdAt).toISOString(),
      updatedAt: new Date(task.updatedAt).toISOString(),
    };
  }
);

export const updateTaskProgress = createAsyncThunk(
  'tasks/updateTaskProgress',
  async ({ id, progress }: { id: string; progress: number }) => {
    const task = await taskService.updateTaskProgress(id, progress);
    return {
      ...task,
      dueDate: new Date(task.dueDate).toISOString(),
      createdAt: new Date(task.createdAt).toISOString(),
      updatedAt: new Date(task.updatedAt).toISOString(),
    };
  }
);

export const updateChecklistItem = createAsyncThunk(
  'tasks/updateChecklistItem',
  async ({
    taskId,
    itemId,
    completed,
  }: {
    taskId: string;
    itemId: string;
    completed: boolean;
  }) => {
    const task = await taskService.updateChecklistItem(taskId, itemId, completed);
    return {
      ...task,
      dueDate: new Date(task.dueDate).toISOString(),
      createdAt: new Date(task.createdAt).toISOString(),
      updatedAt: new Date(task.updatedAt).toISOString(),
    };
  }
);

const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    clearSelectedTask: (state) => {
      state.selectedTask = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(fetchTasks.fulfilled, (state, action) => {
      state.tasks = action.payload;
      state.loading = false;
      state.error = null;
    });
    builder.addCase(fetchTaskById.fulfilled, (state, action) => {
      state.selectedTask = action.payload;
      state.loading = false;
      state.error = null;
    });
    builder.addCase(createTask.fulfilled, (state, action) => {
      state.tasks.push(action.payload);
      state.loading = false;
      state.error = null;
    });
    builder.addCase(updateTask.fulfilled, (state, action) => {
      const index = state.tasks.findIndex(task => task.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
      }
      state.loading = false;
      state.error = null;
    });
    builder.addCase(deleteTask.fulfilled, (state, action) => {
      state.tasks = state.tasks.filter(task => task.id !== action.payload);
      state.loading = false;
      state.error = null;
    });
    builder.addCase(updateTaskStatus.fulfilled, (state, action) => {
      const index = state.tasks.findIndex(task => task.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
      }
      state.loading = false;
      state.error = null;
    });
    builder.addCase(updateTaskProgress.fulfilled, (state, action) => {
      const index = state.tasks.findIndex(task => task.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
      }
      state.loading = false;
      state.error = null;
    });
    builder.addCase(updateChecklistItem.fulfilled, (state, action) => {
      const index = state.tasks.findIndex(task => task.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
      }
      state.loading = false;
      state.error = null;
    });
  }
});

export const { clearSelectedTask, clearError } = taskSlice.actions;

export default taskSlice.reducer;
