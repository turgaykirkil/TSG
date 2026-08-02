import { rest } from 'msw';
import db from '../../db.json';

const BASE_URL = 'http://localhost:3000';

export const handlers = [
  // Auth handlers
  rest.post(`${BASE_URL}/users`, (req, res, ctx) => {
    const { email, password } = req.body as { email: string; password: string };
    const user = db.users.find(
      (u) => u.email === email && u.password === password
    );

    if (!user) {
      return res(
        ctx.status(401),
        ctx.json({ message: 'Invalid email or password' })
      );
    }

    return res(ctx.json({ user }));
  }),

  // Customer handlers
  rest.get(`${BASE_URL}/customers`, (req, res, ctx) => {
    return res(ctx.json(db.customers));
  }),

  rest.get(`${BASE_URL}/customers/:id`, (req, res, ctx) => {
    const { id } = req.params;
    const customer = db.customers.find((c) => c.id === id);

    if (!customer) {
      return res(ctx.status(404), ctx.json({ message: 'Customer not found' }));
    }

    return res(ctx.json(customer));
  }),

  rest.post(`${BASE_URL}/customers`, (req, res, ctx) => {
    const newCustomer = {
      id: String(db.customers.length + 1),
      ...req.body,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    db.customers.push(newCustomer);
    return res(ctx.status(201), ctx.json(newCustomer));
  }),

  // Task handlers
  rest.get(`${BASE_URL}/tasks`, (req, res, ctx) => {
    return res(ctx.json(db.tasks));
  }),

  rest.get(`${BASE_URL}/tasks/:id`, (req, res, ctx) => {
    const { id } = req.params;
    const task = db.tasks.find((t) => t.id === id);

    if (!task) {
      return res(ctx.status(404), ctx.json({ message: 'Task not found' }));
    }

    return res(ctx.json(task));
  }),

  rest.post(`${BASE_URL}/tasks`, (req, res, ctx) => {
    const newTask = {
      id: String(db.tasks.length + 1),
      ...req.body,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    db.tasks.push(newTask);
    return res(ctx.status(201), ctx.json(newTask));
  }),
];
