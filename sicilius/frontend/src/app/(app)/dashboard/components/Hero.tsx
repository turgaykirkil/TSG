import { cn } from '@/lib/utils';

export function Hero() {
  return (
    <section
      className={cn(
        'w-full rounded-xl p-6 md:p-8',
        'bg-gradient-to-br from-[#0A192F] via-[#0F274A] to-[#143556]',
        'text-white shadow'
      )}
      role="region"
      aria-labelledby="dashboard-heading"
      aria-describedby="dashboard-desc"
    >
      <div className="flex flex-col gap-2">
        <h1 id="dashboard-heading" className="text-2xl md:text-3xl font-bold tracking-tight">Hoş geldiniz</h1>
        <p id="dashboard-desc" className="text-sm md:text-base text-white/80">
          Sicilius ile şirketleri, kişileri ve şirket geçmişlerini tek ekrandan keşfedin.
        </p>
      </div>
    </section>
  );
}
