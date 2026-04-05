'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { Mail, MailOpen, RefreshCw } from 'lucide-react';

interface ContactMessage {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    subject: string;
    message: string;
    created_at: string;
    read: string;
}

export default function AdminContactMessagesPage() {
    const [messages, setMessages] = useState<ContactMessage[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<'ALL' | 'UNREAD' | 'READ'>('ALL');
    const { toast } = useToast();

    const fetchMessages = async () => {
        setLoading(true);
        try {
            const unreadParam = filter === 'UNREAD' ? '?unread_only=true' : '';
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const res = await fetch(`${baseUrl}/api/v1/contact/${unreadParam}`, {
                credentials: 'include',
            });

            if (!res.ok) {
                throw new Error('Mesajlar yüklenemedi');
            }

            const data = await res.json();
            setMessages(Array.isArray(data) ? data : []);
        } catch (error: any) {
            toast({
                title: 'Hata',
                description: error?.message || 'Mesajlar alınırken bir sorun oluştu.',
                variant: 'destructive',
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMessages();
    }, [filter]);

    const markAsRead = async (messageId: string) => {
        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const res = await fetch(`${baseUrl}/api/v1/contact/${messageId}/read`, {
                method: 'PATCH',
                credentials: 'include',
            });

            if (!res.ok) {
                throw new Error('Mesaj işaretlenemedi');
            }

            // Update local state
            setMessages(messages.map(msg =>
                msg.id === messageId ? { ...msg, read: 'READ' } : msg
            ));

            toast({
                title: 'Başarılı',
                description: 'Mesaj okundu olarak işaretlendi.',
            });
        } catch (error) {
            toast({
                title: 'Hata',
                description: 'Mesaj işaretlenirken bir hata oluştu.',
                variant: 'destructive',
            });
        }
    };

    const filteredMessages = filter === 'READ'
        ? messages.filter(m => m.read === 'READ')
        : messages;

    const unreadCount = messages.filter(m => m.read === 'UNREAD').length;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">İletişim Mesajları</h1>
                    <p className="text-muted-foreground">
                        İletişim formundan gelen mesajları görüntüleyin
                    </p>
                </div>
                <Button onClick={fetchMessages} variant="outline" size="sm">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Yenile
                </Button>
            </div>

            {/* Filters */}
            <div className="flex gap-2">
                <Button
                    variant={filter === 'ALL' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setFilter('ALL')}
                >
                    Tümü ({messages.length})
                </Button>
                <Button
                    variant={filter === 'UNREAD' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setFilter('UNREAD')}
                >
                    Okunmamış ({unreadCount})
                </Button>
                <Button
                    variant={filter === 'READ' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setFilter('READ')}
                >
                    Okunmuş ({messages.length - unreadCount})
                </Button>
            </div>

            {/* Messages List */}
            {loading ? (
                <div className="text-center p-12">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
                    <p className="mt-4 text-muted-foreground">Yükleniyor...</p>
                </div>
            ) : filteredMessages.length === 0 ? (
                <div className="text-center p-12 text-slate-500 bg-slate-50 dark:bg-slate-900 rounded-lg border border-dashed">
                    {filter === 'UNREAD' && 'Okunmamış mesaj bulunmuyor.'}
                    {filter === 'READ' && 'Okunmuş mesaj bulunmuyor.'}
                    {filter === 'ALL' && 'Henüz hiç mesaj bulunmuyor.'}
                </div>
            ) : (
                <div className="space-y-4">
                    {filteredMessages.map((message) => (
                        <Card key={message.id} className="p-6">
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex items-start gap-4">
                                    <div className={`mt-1 ${message.read === 'UNREAD' ? 'text-primary' : 'text-muted-foreground'}`}>
                                        {message.read === 'UNREAD' ? (
                                            <Mail className="h-5 w-5" />
                                        ) : (
                                            <MailOpen className="h-5 w-5" />
                                        )}
                                    </div>
                                    <div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <h3 className="font-semibold text-lg">
                                                {message.first_name} {message.last_name}
                                            </h3>
                                            {message.read === 'UNREAD' && (
                                                <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                                                    Yeni
                                                </Badge>
                                            )}
                                        </div>
                                        <p className="text-sm text-muted-foreground mb-1">
                                            <a href={`mailto:${message.email}`} className="hover:underline">
                                                {message.email}
                                            </a>
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            {new Date(message.created_at).toLocaleString('tr-TR', {
                                                dateStyle: 'long',
                                                timeStyle: 'short'
                                            })}
                                        </p>
                                    </div>
                                </div>
                                {message.read === 'UNREAD' && (
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => markAsRead(message.id)}
                                    >
                                        Okundu İşaretle
                                    </Button>
                                )}
                            </div>

                            <div className="ml-9">
                                <h4 className="font-medium mb-2">{message.subject}</h4>
                                <p className="text-sm text-muted-foreground whitespace-pre-wrap bg-slate-50 dark:bg-slate-900 p-4 rounded-lg">
                                    {message.message}
                                </p>
                            </div>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
