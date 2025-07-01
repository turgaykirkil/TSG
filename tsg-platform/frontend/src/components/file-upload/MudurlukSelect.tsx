import { MÜDÜRLÜKLER } from "@/lib/constants/mudurlukler";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface MudurlukSelectProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function MudurlukSelect({ value, onChange, disabled }: MudurlukSelectProps) {
  const mudurlukOptions = MÜDÜRLÜKLER.map(mudurluk => ({
    value: mudurluk,
    label: mudurluk
  }));

  return (
    <div className="w-full">
      <label className="block text-sm font-medium mb-1">Müdürlük Seçin</label>
      <Select value={value} onValueChange={onChange} disabled={disabled}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Müdürlük seçin" />
        </SelectTrigger>
        <SelectContent>
          {mudurlukOptions.map(({ value, label }) => (
            <SelectItem key={value} value={value}>
              {label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
