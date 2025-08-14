"use client";

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const data = [
  { day: '01', companies: 12 },
  { day: '05', companies: 19 },
  { day: '09', companies: 14 },
  { day: '13', companies: 22 },
  { day: '17', companies: 18 },
  { day: '21', companies: 25 },
  { day: '25', companies: 20 },
  { day: '29', companies: 28 },
];

export function TrendSection() {
  return (
    <Card className="bg-white" role="region" aria-labelledby="trend-title">
      <CardHeader>
        <CardTitle id="trend-title" className="text-sm font-medium">Son 30 Gün · Şirket Aktivitesi</CardTitle>
      </CardHeader>
      <CardContent className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorPrimary" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#64FFDA" stopOpacity={0.6} />
                <stop offset="95%" stopColor="#64FFDA" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="day" stroke="#6b7280" tickLine={false} axisLine={false} />
            <YAxis stroke="#6b7280" tickLine={false} axisLine={false} />
            <Tooltip cursor={{ stroke: '#0A192F', strokeWidth: 1 }} />
            <Area type="monotone" dataKey="companies" stroke="#0A192F" fill="url(#colorPrimary)" />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export default TrendSection;
