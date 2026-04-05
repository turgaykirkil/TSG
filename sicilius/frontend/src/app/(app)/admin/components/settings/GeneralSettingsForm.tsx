'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

export default function GeneralSettingsForm() {
    const [maintenanceMode, setMaintenanceMode] = useState(false);
    const [publicRegistration, setPublicRegistration] = useState(true);
    const [loading, setLoading] = useState(false);

    const handleSave = async () => {
        setLoading(true);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setLoading(false);
        toast.success('Ayarlar başarıyla güncellendi.');
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Sistem Durumu</CardTitle>
                    <CardDescription>
                        Sistemin genel erişilebilirlik ayarlarını yönetin.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between rounded-lg border p-4">
                        <div className="space-y-0.5">
                            <Label className="text-base">Bakım Modu</Label>
                            <p className="text-sm text-muted-foreground">
                                Sistemi bakım moduna alırsanız, adminler dışındaki tüm kullanıcılar "Bakım" sayfasıyla karşılaşır.
                            </p>
                        </div>
                        <Switch
                            checked={maintenanceMode}
                            onCheckedChange={setMaintenanceMode}
                            aria-readonly
                        />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Üye Alımı</CardTitle>
                    <CardDescription>
                        Yeni kullanıcı kayıtlarını kontrol edin.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between rounded-lg border p-4">
                        <div className="space-y-0.5">
                            <Label className="text-base">Halka Açık Kayıt</Label>
                            <p className="text-sm text-muted-foreground">
                                Kapalı olduğunda, sadece admin daveti ile yeni kullanıcı eklenebilir.
                            </p>
                        </div>
                        <Switch
                            checked={publicRegistration}
                            onCheckedChange={setPublicRegistration}
                        />
                    </div>
                </CardContent>
            </Card>

            <div className="flex justify-end">
                <Button onClick={handleSave} disabled={loading}>
                    {loading ? 'Kaydediliyor...' : 'Değişiklikleri Kaydet'}
                </Button>
            </div>
        </div>
    );
}
