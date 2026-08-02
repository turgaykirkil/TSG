import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { Task } from '../types/task';
import { taskService } from '../services/taskService';

interface UseTaskDetailProps {
  taskId: string;
}

export const useTaskDetail = ({ taskId }: UseTaskDetailProps) => {
  const [task, setTask] = useState<Task | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const loggedInUser = useSelector((state: RootState) => state.auth.user);

  useEffect(() => {
    const loadTask = async () => {
      if (!loggedInUser || !taskId) {
        setError('Gerekli bilgiler eksik');
        setLoading(false);
        return;
      }

      try {
        setError(null);
        const response = await taskService.getTaskById(taskId);

        if (!response) {
          setError('Görev bulunamadı');
          setLoading(false);
          return;
        }
        
        setTask(response);
        setLoading(false);
      } catch (err: any) {
        setError(err?.message || 'Görev yüklenirken bir hata oluştu');
        setLoading(false);
      }
    };

    loadTask();
  }, [taskId, loggedInUser]);

  return {
    task,
    error,
    loading,
    setTask
  };
};
