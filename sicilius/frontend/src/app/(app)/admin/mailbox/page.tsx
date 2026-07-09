"use client";

import React, { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { 
    Mail, 
    Send, 
    Plus, 
    Trash2, 
    Search, 
    CornerUpLeft, 
    Inbox as InboxIcon, 
    Clock, 
    User, 
    Check, 
    AlertCircle, 
    Loader2,
    Star,
    RefreshCw,
    ChevronLeft,
    ChevronRight,
    MousePointerClick,
    ArrowLeft,
    Paperclip
} from "lucide-react";

interface IncomingEmail {
    id: string;
    from_address: string;
    to_address: string;
    subject: string | null;
    body_text: string | null;
    body_html: string | null;
    received_at: string;
    is_read: boolean;
    cloudflare_message_id: string | null;
    reply_text?: string;
    replied_at?: string;
    is_outbound: boolean;
}

interface IncomingEmailList {
    items: IncomingEmail[];
    total: number;
    page: number;
    per_page: number;
}

async function fetchIncomingEmails(page: number, unreadOnly: boolean, mailboxType: "inbox" | "sent"): Promise<IncomingEmailList> {
    const params = new URLSearchParams({
        page: page.toString(),
        per_page: "15",
        mailbox_type: mailboxType,
        ...(unreadOnly && mailboxType === "inbox" && { unread_only: "true" }),
    });

    const res = await fetch(`/api/v1/incoming-emails?${params}`, {
        credentials: "include",
    });

    if (!res.ok) {
        throw new Error("E-postalar yüklenemedi");
    }

    return res.json();
}

async function markAsRead(emailId: string): Promise<void> {
    const res = await fetch(`/api/v1/incoming-emails/${emailId}/mark-read`, {
        method: "PATCH",
        credentials: "include",
    });

    if (!res.ok) {
        throw new Error("E-posta okundu işaretlenemedi");
    }
}

async function deleteEmail(emailId: string): Promise<void> {
    const res = await fetch(`/api/v1/incoming-emails/${emailId}`, {
        method: "DELETE",
        credentials: "include",
    });

    if (!res.ok) {
        throw new Error("E-posta silinemedi");
    }
}

export default function AdminMailboxPage() {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    
    // States
    const [page, setPage] = useState(1);
    const [mailboxType, setMailboxType] = useState<"inbox" | "sent">("inbox");
    const [unreadOnly, setUnreadOnly] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    
    // Star & Selection States
    const [selectedIds, setSelectedIds] = useState<string[]>([]);
    const [starredIds, setStarredIds] = useState<string[]>([]);

    // Detail & Modals
    const [detailEmail, setDetailEmail] = useState<IncomingEmail | null>(null);
    const [detailOpen, setDetailOpen] = useState(false);
    
    const [replyMessage, setReplyMessage] = useState("");
    const [replySubmitting, setReplySubmitting] = useState(false);

    const [composeOpen, setComposeOpen] = useState(false);
    const [composeTo, setComposeTo] = useState("");
    const [composeSubject, setComposeSubject] = useState("");
    const [composeBody, setComposeBody] = useState("");
    const [composeFrom, setComposeFrom] = useState("info@sicilius.com.tr");
    const [composeSubmitting, setComposeSubmitting] = useState(false);

    // Sync stars from localStorage
    useEffect(() => {
        if (typeof window !== "undefined") {
            try {
                const stored = localStorage.getItem("sicilius_starred_emails");
                if (stored) setStarredIds(JSON.parse(stored));
            } catch (e) {
                console.error("Starred loading failed", e);
            }
        }
    }, []);

    // Queries
    const { data, isLoading, error, refetch, isFetching } = useQuery({
        queryKey: ["incoming-emails", page, unreadOnly, mailboxType],
        queryFn: () => fetchIncomingEmails(page, unreadOnly, mailboxType),
    });

    // Mutations
    const markAsReadMutation = useMutation({
        mutationFn: markAsRead,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["incoming-emails"] });
        },
    });

    const deleteEmailMutation = useMutation({
        mutationFn: deleteEmail,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["incoming-emails"] });
            setSelectedIds([]);
            toast({ title: "Başarılı", description: "Seçilen e-postalar başarıyla silindi." });
        },
        onError: (err: any) => {
            toast({ title: "Hata", description: err.message || "Silme işlemi başarısız.", variant: "destructive" });
        }
    });

    // Bulk Delete
    const handleBulkDelete = () => {
        if (selectedIds.length === 0) return;
        if (confirm(`Seçilen ${selectedIds.length} e-postayı kalıcı olarak silmek istediğinizden emin misiniz?`)) {
            // Delete sequentially or via promise.all
            Promise.all(selectedIds.map(id => deleteEmail(id)))
                .then(() => {
                    queryClient.invalidateQueries({ queryKey: ["incoming-emails"] });
                    setSelectedIds([]);
                    setDetailOpen(false);
                    setDetailEmail(null);
                    toast({ title: "Başarılı", description: "Seçilen tüm postalar silindi." });
                })
                .catch((err) => {
                    toast({ title: "Kısmi Hata", description: "Bazı postalar silinemedi.", variant: "destructive" });
                    queryClient.invalidateQueries({ queryKey: ["incoming-emails"] });
                });
        }
    };

    // Double-click row handler to open Viewer Modal
    const handleRowDoubleClick = (email: IncomingEmail) => {
        setDetailEmail(email);
        setDetailOpen(true);
        if (!email.is_read && !email.is_outbound) {
            markAsReadMutation.mutate(email.id);
        }
    };

    const toggleStar = (id: string, e: React.MouseEvent) => {
        e.stopPropagation();
        setStarredIds(prev => {
            const next = prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id];
            localStorage.setItem("sicilius_starred_emails", JSON.stringify(next));
            return next;
        });
    };

    const handleSelectAll = (checked: boolean) => {
        if (checked && filteredItems.length > 0) {
            setSelectedIds(filteredItems.map(item => item.id));
        } else {
            setSelectedIds([]);
        }
    };

    const handleSelectOne = (id: string, checked: boolean) => {
        if (checked) {
            setSelectedIds(prev => [...prev, id]);
        } else {
            setSelectedIds(prev => prev.filter(x => x !== id));
        }
    };

    const handleSendReply = async () => {
        if (!detailEmail) return;
        const msg = replyMessage.trim();
        if (!msg) {
            toast({ title: "Hata", description: "Cevap metni boş olamaz.", variant: "destructive" });
            return;
        }
        setReplySubmitting(true);
        try {
            const res = await fetch(`/api/v1/incoming-emails/${detailEmail.id}/reply`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg }),
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data?.detail || "Cevap gönderilemedi");
            }

            toast({ title: "Başarılı", description: "Cevap e-postası başarıyla gönderildi." });
            setReplyMessage("");
            queryClient.invalidateQueries({ queryKey: ["incoming-emails"] });
            
            // Update details view state dynamically
            setDetailEmail({
                ...detailEmail,
                is_read: true,
                reply_text: msg,
                replied_at: new Date().toISOString()
            });
        } catch (error: any) {
            toast({
                title: "Hata",
                description: error?.message || "Cevap gönderilirken bir sorun oluştu.",
                variant: "destructive",
            });
        } finally {
            setReplySubmitting(false);
        }
    };

    const handleSendNewEmail = async (e: React.FormEvent) => {
        e.preventDefault();
        const to = composeTo.trim();
        const subject = composeSubject.trim();
        const body = composeBody.trim();

        if (!to || !subject || !body) {
            toast({ title: "Hata", description: "Lütfen tüm alanları doldurun.", variant: "destructive" });
            return;
        }

        setComposeSubmitting(true);
        try {
            const res = await fetch("/api/v1/incoming-emails/send", {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    to_address: to, 
                    subject, 
                    body,
                    from_address: composeFrom
                }),
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data?.detail || "E-posta gönderilemedi");
            }

            toast({ title: "Başarılı", description: "E-posta başarıyla gönderildi." });
            setComposeOpen(false);
            setComposeTo("");
            setComposeSubject("");
            setComposeBody("");
            
            // Switch to sent tab to show the sent mail
            setMailboxType("sent");
            setPage(1);
            queryClient.invalidateQueries({ queryKey: ["incoming-emails"] });
        } catch (error: any) {
            toast({
                title: "Hata",
                description: error?.message || "E-posta gönderilirken bir hata oluştu.",
                variant: "destructive",
            });
        } finally {
            setComposeSubmitting(false);
        }
    };

    // Filter email list locally by search term
    const filteredItems = React.useMemo(() => {
        if (!data?.items) return [];
        const query = searchQuery.toLowerCase().trim();
        if (!query) return data.items;
        return data.items.filter(item => 
            item.from_address.toLowerCase().includes(query) ||
            item.to_address.toLowerCase().includes(query) ||
            (item.subject && item.subject.toLowerCase().includes(query)) ||
            (item.body_text && item.body_text.toLowerCase().includes(query))
        );
    }, [data?.items, searchQuery]);

    // Format Initials
    const getInitials = (emailStr: string) => {
        if (!emailStr) return "U";
        // Clean display name pattern "Name Lastname <email>"
        let cleanStr = emailStr;
        if (emailStr.includes("<")) {
            const match = emailStr.match(/<([^>]+)>/);
            if (match) cleanStr = match[1];
        }
        const parts = cleanStr.split("@")[0].split(/[._-]/);
        if (parts.length >= 2) {
            return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return cleanStr.substring(0, 2).toUpperCase();
    };

    // Calculate unread count locally for badge
    const localUnreadCount = data?.items?.filter(item => !item.is_read && !item.is_outbound).length || 0;

    return (
        <div className="flex flex-col h-[calc(100vh-6.5rem)] max-w-[1600px] mx-auto p-4 space-y-4 overflow-hidden">
            {/* Page Header */}
            <div className="flex items-center justify-between border-b pb-3">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-slate-800 dark:text-slate-100 flex items-center gap-2">
                        <Mail className="h-6 w-6 text-blue-600" />
                        <span>Mailbox Yönetimi</span>
                    </h1>
                    <p className="text-xs text-muted-foreground mt-0.5">
                        Kurumsal e-posta iletilerini, iletişim mesajlarını ve gönderimleri tek bir noktadan yönetin.
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-[11px] text-muted-foreground bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-md hidden md:inline-flex items-center gap-1.5 font-medium">
                        <MousePointerClick className="h-3.5 w-3.5 text-blue-500 animate-pulse" />
                        Açmak istediğiniz maile çift tıklayın
                    </span>
                    <Button 
                        onClick={() => setComposeOpen(true)} 
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium shadow-md shadow-blue-500/10 gap-2 h-9 px-4 rounded-xl text-xs transition-all duration-200 hover:scale-[1.02]"
                    >
                        <Plus className="h-4 w-4" /> Yeni E-posta Yaz
                    </Button>
                </div>
            </div>

            {/* Layout Workspace */}
            <div className="flex flex-1 gap-6 overflow-hidden">
                
                {/* Left Navigation (Sidebar) */}
                <div className="w-56 flex-shrink-0 flex flex-col space-y-4 hidden md:block">
                    {/* Action Button */}
                    <Button 
                        onClick={() => setComposeOpen(true)}
                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-5 rounded-xl shadow-lg shadow-blue-500/10 flex items-center justify-center gap-2 transition-all duration-300 hover:scale-[1.02]"
                    >
                        <Plus className="h-4.5 w-4.5" /> Yeni Yaz
                    </Button>

                    {/* Navigation Menu */}
                    <div className="bg-white dark:bg-slate-900 border rounded-xl p-2 space-y-1 shadow-sm">
                        <button
                            onClick={() => {
                                setMailboxType("inbox");
                                setPage(1);
                                setSelectedIds([]);
                            }}
                            className={`flex items-center justify-between w-full px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                                mailboxType === "inbox"
                                    ? "bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-300"
                                    : "text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900"
                            }`}
                        >
                            <div className="flex items-center gap-2.5">
                                <InboxIcon className={`h-4.5 w-4.5 ${mailboxType === "inbox" ? "text-blue-600" : "text-slate-400"}`} />
                                <span>Gelen Kutusu</span>
                            </div>
                            {localUnreadCount > 0 && mailboxType === "inbox" && (
                                <Badge className="bg-blue-600 text-white font-bold text-[10px] px-1.5 py-0.5 rounded-full">
                                    {localUnreadCount}
                                </Badge>
                            )}
                        </button>
                        
                        <button
                            onClick={() => {
                                setMailboxType("sent");
                                setPage(1);
                                setSelectedIds([]);
                            }}
                            className={`flex items-center justify-between w-full px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                                mailboxType === "sent"
                                    ? "bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-300"
                                    : "text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900"
                            }`}
                        >
                            <div className="flex items-center gap-2.5">
                                <Send className={`h-4.5 w-4.5 ${mailboxType === "sent" ? "text-blue-600" : "text-slate-400"}`} />
                                <span>Gönderilenler</span>
                            </div>
                        </button>
                    </div>

                    {/* Stats Box */}
                    <div className="bg-slate-50 dark:bg-slate-900/40 border rounded-xl p-4 shadow-sm text-center">
                        <div className="text-[11px] text-muted-foreground font-semibold uppercase tracking-wider">Durum</div>
                        <div className="text-2xl font-bold text-slate-800 dark:text-slate-200 mt-1">
                            {data ? data.total : 0}
                        </div>
                        <div className="text-[10px] text-muted-foreground mt-0.5">Kayıtlı E-posta</div>
                    </div>
                </div>

                {/* Right Area (Main Mailbox Board) */}
                <div className="flex-1 bg-white dark:bg-slate-900 border rounded-2xl shadow-sm flex flex-col overflow-hidden">
                    
                    {/* Toolbar Header */}
                    <div className="px-6 py-4 border-b flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-50/50 dark:bg-slate-950/20">
                        <div className="flex items-center gap-2">
                            <h2 className="text-sm font-bold text-slate-800 dark:text-slate-200">
                                {mailboxType === "inbox" ? "Gelen Kutusu" : "Gönderilenler"}
                            </h2>
                            {data?.total ? (
                                <Badge variant="secondary" className="text-[10px] font-semibold">
                                    {data.total} İleti
                                </Badge>
                            ) : null}
                        </div>

                        {/* Search Input */}
                        <div className="relative w-full sm:w-64">
                            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="E-posta veya konu ara..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-9 h-9 text-xs rounded-lg shadow-sm"
                            />
                        </div>
                    </div>

                    {/* Control Bar (AdminLTE Style Action Row) */}
                    <div className="px-6 py-3 border-b flex items-center justify-between bg-slate-50/20 dark:bg-slate-950/5 text-slate-500 text-xs">
                        <div className="flex items-center gap-4">
                            {/* Select All Checkbox */}
                            <label className="flex items-center gap-2 cursor-pointer select-none">
                                <input
                                    type="checkbox"
                                    checked={filteredItems.length > 0 && selectedIds.length === filteredItems.length}
                                    onChange={(e) => handleSelectAll(e.target.checked)}
                                    className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                                />
                                <span className="text-[11px] font-medium hidden sm:inline">Tümünü Seç</span>
                            </label>

                            {/* Refresh Button */}
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => refetch()}
                                disabled={isFetching}
                                className="h-8 w-8 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 rounded-lg"
                                title="Yenile"
                            >
                                <RefreshCw className={`h-4 w-4 ${isFetching ? "animate-spin text-blue-500" : ""}`} />
                            </Button>

                            {/* Delete Selected Button */}
                            {selectedIds.length > 0 && (
                                <Button
                                    onClick={handleBulkDelete}
                                    variant="ghost"
                                    size="sm"
                                    className="h-8 text-red-600 hover:bg-red-50 hover:text-red-700 dark:hover:bg-red-950/20 rounded-lg gap-1.5"
                                >
                                    <Trash2 className="h-4 w-4" />
                                    <span>Sil ({selectedIds.length})</span>
                                </Button>
                            )}

                            {mailboxType === "inbox" && (
                                <label className="flex items-center gap-1.5 cursor-pointer select-none ml-2 border-l pl-4 border-slate-200">
                                    <input
                                        type="checkbox"
                                        checked={unreadOnly}
                                        onChange={(e) => {
                                            setUnreadOnly(e.target.checked);
                                            setPage(1);
                                        }}
                                        className="w-3.5 h-3.5 rounded border-slate-300 text-blue-600 cursor-pointer"
                                    />
                                    <span className="text-[11px] font-semibold text-slate-500">Sadece Okunmamışlar</span>
                                </label>
                            )}
                        </div>

                        {/* Pagination controls */}
                        {data && data.total > 0 && (
                            <div className="flex items-center gap-3">
                                <span>
                                    {Math.min((page - 1) * 15 + 1, data.total)} - {Math.min(page * 15, data.total)} / {data.total}
                                </span>
                                <div className="flex gap-1">
                                    <Button
                                        variant="outline"
                                        size="icon"
                                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                                        disabled={page === 1}
                                        className="h-7 w-7 rounded-md"
                                    >
                                        <ChevronLeft className="h-4 w-4" />
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="icon"
                                        onClick={() => setPage((p) => p + 1)}
                                        disabled={page >= Math.ceil(data.total / 15)}
                                        className="h-7 w-7 rounded-md"
                                    >
                                        <ChevronRight className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Table View (AdminLTE Style List) */}
                    <div className="flex-1 overflow-y-auto divide-y bg-slate-50/10 dark:bg-slate-900/5">
                        {isLoading && (
                            <div className="flex flex-col items-center justify-center py-20 space-y-3">
                                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                                <span className="text-xs font-semibold text-slate-500">E-postalar yükleniyor...</span>
                            </div>
                        )}

                        {error && (
                            <div className="p-4 m-4 rounded-xl bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30 text-xs text-red-600 flex gap-2">
                                <AlertCircle className="h-4 w-4 flex-shrink-0" />
                                <span>Bağlantı hatası: {(error as Error).message}</span>
                            </div>
                        )}

                        {!isLoading && filteredItems.length === 0 && (
                            <div className="text-center py-24 text-muted-foreground text-sm flex flex-col items-center justify-center space-y-3">
                                <Mail className="h-10 w-10 text-slate-300" />
                                <span>Gösterilecek e-posta kaydı bulunmuyor.</span>
                            </div>
                        )}

                        {!isLoading && filteredItems.length > 0 && (
                            <div className="w-full">
                                <table className="w-full text-left border-collapse">
                                    <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                                        {filteredItems.map((email) => {
                                            const isSelected = selectedIds.includes(email.id);
                                            const isStarred = starredIds.includes(email.id);
                                            const isUnread = !email.is_read && !email.is_outbound;

                                            return (
                                                <tr
                                                    key={email.id}
                                                    onDoubleClick={() => handleRowDoubleClick(email)}
                                                    className={`group transition-all hover:bg-blue-50/20 dark:hover:bg-slate-800/40 cursor-pointer select-none ${
                                                        isSelected ? "bg-blue-50/50 dark:bg-blue-950/10" : ""
                                                    } ${isUnread ? "bg-white dark:bg-slate-900 font-semibold" : "bg-slate-50/30 dark:bg-slate-900/10 text-slate-600 dark:text-slate-400"}`}
                                                >
                                                    {/* Checkbox column */}
                                                    <td className="w-10 pl-4 py-3 text-center">
                                                        <input
                                                            type="checkbox"
                                                            checked={isSelected}
                                                            onChange={(e) => handleSelectOne(email.id, e.target.checked)}
                                                            onClick={(e) => e.stopPropagation()}
                                                            className="w-4 h-4 rounded border-slate-300 text-blue-600 cursor-pointer"
                                                        />
                                                    </td>

                                                    {/* Star column */}
                                                    <td className="w-8 py-3 text-center">
                                                        <button 
                                                            onClick={(e) => toggleStar(email.id, e)}
                                                            className="text-slate-300 hover:text-amber-500 transition-colors"
                                                        >
                                                            <Star className={`h-4.5 w-4.5 ${isStarred ? "text-amber-400 fill-amber-400" : ""}`} />
                                                        </button>
                                                    </td>

                                                    {/* Mail Sender column */}
                                                    <td className="w-44 px-3 py-3 text-xs max-w-[160px] truncate">
                                                        <div className="flex items-center gap-2">
                                                            {/* Mini Dot for Unread */}
                                                            {isUnread && <span className="w-2 h-2 rounded-full bg-blue-600 flex-shrink-0"></span>}
                                                            <span className={isUnread ? "font-bold text-slate-950 dark:text-white" : "font-normal text-slate-800 dark:text-slate-300"}>
                                                                {email.is_outbound ? `Alıcı: ${email.to_address.split("@")[0]}` : email.from_address.split("@")[0]}
                                                            </span>
                                                        </div>
                                                    </td>

                                                    {/* Mail Subject & snippet column */}
                                                    <td className="px-3 py-3 text-xs max-w-xs sm:max-w-md truncate">
                                                        <span className={isUnread ? "font-bold text-slate-900 dark:text-white" : "text-slate-800 dark:text-slate-300"}>
                                                            {email.subject || "(Konu yok)"}
                                                        </span>
                                                        <span className="text-slate-400 dark:text-slate-500 font-normal ml-2">
                                                            - {email.body_text || "İçerik bulunmuyor..."}
                                                        </span>
                                                    </td>

                                                    {/* Date column */}
                                                    <td className="w-32 pr-4 py-3 text-right text-[10px] text-slate-400 font-medium whitespace-nowrap">
                                                        <div className="flex items-center justify-end gap-1.5">
                                                            {email.reply_text && (
                                                                <Badge className="bg-emerald-100 hover:bg-emerald-100 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 text-[9px] px-1.5 py-0 rounded-md font-bold">
                                                                    Yanıtlandı
                                                                </Badge>
                                                            )}
                                                            <span>
                                                                {new Date(email.received_at).toLocaleDateString("tr-TR", {
                                                                    day: "numeric",
                                                                    month: "short",
                                                                    hour: "2-digit",
                                                                    minute: "2-digit"
                                                                })}
                                                            </span>
                                                        </div>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Email Detail Viewer Dialog (Opens on Double Click) */}
            <Dialog open={detailOpen} onOpenChange={(o) => { setDetailOpen(o); if(!o) { setReplyMessage(""); setDetailEmail(null); } }}>
                <DialogContent className="sm:max-w-[750px] max-h-[85vh] overflow-y-auto flex flex-col p-0 border border-slate-200 dark:border-slate-800 rounded-2xl">
                    {detailEmail && (
                        <div className="flex flex-col flex-1">
                            {/* Modal Header */}
                            <div className="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b flex items-center justify-between sticky top-0 z-10">
                                <div className="flex items-center gap-3">
                                    <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-white bg-blue-600`}>
                                        {getInitials(detailEmail.is_outbound ? detailEmail.to_address : detailEmail.from_address)}
                                    </div>
                                    <div className="min-w-0">
                                        <h3 className="text-xs font-bold text-slate-800 dark:text-slate-200 truncate">
                                            {detailEmail.is_outbound ? "Yönetici (Sistem)" : detailEmail.from_address}
                                        </h3>
                                        <p className="text-[10px] text-muted-foreground">
                                            Kime: {detailEmail.to_address}
                                        </p>
                                    </div>
                                </div>
                                <div className="text-right flex flex-col items-end">
                                    <span className="text-[10px] text-slate-500 font-semibold flex items-center gap-1">
                                        <Clock className="h-3 w-3" />
                                        {new Date(detailEmail.received_at).toLocaleString("tr-TR")}
                                    </span>
                                    {detailEmail.is_outbound ? (
                                        <Badge className="bg-emerald-100 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 border-none font-bold text-[9px] mt-1 px-2 py-0">
                                            Gönderilen Posta
                                        </Badge>
                                    ) : (
                                        <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-950/40 dark:text-blue-300 border-none font-bold text-[9px] mt-1 px-2 py-0">
                                            Gelen İleti
                                        </Badge>
                                    )}
                                </div>
                            </div>

                            {/* Modal Content Details */}
                            <div className="p-6 space-y-6 flex-1">
                                <div className="space-y-1">
                                    <span className="text-[10px] font-bold text-blue-600 uppercase tracking-wider">Konu</span>
                                    <h2 className="text-base font-extrabold text-slate-900 dark:text-white">
                                        {detailEmail.subject || "(Konu Başlığı Belirtilmemiş)"}
                                    </h2>
                                </div>

                                {/* Full HTML or Plain Body */}
                                <div className="p-5 rounded-xl border bg-slate-50/50 dark:bg-slate-900/30 overflow-auto max-h-[350px] shadow-inner">
                                    {detailEmail.body_html ? (
                                        <div
                                            className="prose dark:prose-invert max-w-none text-slate-800 dark:text-slate-200 text-xs leading-relaxed"
                                            dangerouslySetInnerHTML={{ __html: detailEmail.body_html }}
                                        />
                                    ) : (
                                        <pre className="whitespace-pre-wrap text-xs text-slate-800 dark:text-slate-200 leading-relaxed font-sans">
                                            {detailEmail.body_text || "(İleti metni boş)"}
                                        </pre>
                                    )}
                                </div>

                                {/* Threaded Outbound Response Timeline (If reply exists) */}
                                {detailEmail.reply_text && (
                                    <div className="relative pl-6 border-l-2 border-emerald-500 space-y-2 mt-4 bg-emerald-50/20 dark:bg-emerald-950/10 p-4 rounded-r-xl border border-l-0">
                                        <div className="absolute left-[-5px] top-4 w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <Badge className="bg-emerald-100 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 font-bold text-[9px]">
                                                Cevabınız Gönderildi
                                            </Badge>
                                            {detailEmail.replied_at && (
                                                <span className="text-[10px] text-slate-500 font-semibold">
                                                    {new Date(detailEmail.replied_at).toLocaleString("tr-TR")}
                                                </span>
                                            )}
                                        </div>
                                        <div className="text-xs text-slate-700 dark:text-slate-300 whitespace-pre-wrap">
                                            {detailEmail.reply_text}
                                        </div>
                                    </div>
                                )}

                                {/* Quick inline reply editor (If not replied and not outbound) */}
                                {!detailEmail.is_outbound && !detailEmail.reply_text && (
                                    <div className="space-y-3 pt-2 border-t">
                                        <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 dark:text-slate-300">
                                            <CornerUpLeft className="h-4 w-4 text-blue-600" />
                                            <span>Hızlı Cevap Yaz</span>
                                        </div>
                                        <textarea
                                            value={replyMessage}
                                            onChange={(e) => setReplyMessage(e.target.value)}
                                            rows={4}
                                            placeholder={`${detailEmail.from_address} adresine gönderilecek yanıtı buraya yazın...`}
                                            className="w-full text-xs rounded-xl border border-slate-200 dark:border-slate-800 bg-background p-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-all placeholder:text-slate-400"
                                        />
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="outline" 
                                                onClick={() => setDetailOpen(false)}
                                                className="text-xs h-8 px-3 rounded-lg"
                                            >
                                                Kapat
                                            </Button>
                                            <Button 
                                                onClick={handleSendReply} 
                                                disabled={replySubmitting} 
                                                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs h-8 px-4 rounded-lg shadow-sm"
                                            >
                                                {replySubmitting ? (
                                                    <>
                                                        <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
                                                        Gönderiliyor...
                                                    </>
                                                ) : (
                                                    <>
                                                        <Send className="mr-1.5 h-3.5 w-3.5" />
                                                        Cevabı Gönder
                                                    </>
                                                )}
                                            </Button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </DialogContent>
            </Dialog>

            {/* Compose Mail Modal */}
            <Dialog open={composeOpen} onOpenChange={(o) => { setComposeOpen(o); if (!o) { setComposeTo(""); setComposeSubject(""); setComposeBody(""); } }}>
                <DialogContent className="sm:max-w-[600px] border rounded-2xl">
                    <DialogHeader>
                        <DialogTitle className="text-base font-bold">Yeni E-posta Yaz</DialogTitle>
                        <DialogDescription className="text-xs">
                            Kendi doğrulanmış alan adınızı kullanarak dışarıya e-posta gönderin.
                        </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleSendNewEmail} className="space-y-4 py-2 text-xs">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {/* Dynamic Sender Alias Selector */}
                            <div className="space-y-1.5">
                                <Label htmlFor="from_alias" className="font-semibold text-slate-700">Kimden (Sender Alias)</Label>
                                <select
                                    id="from_alias"
                                    value={composeFrom}
                                    onChange={(e) => setComposeFrom(e.target.value)}
                                    className="flex h-9 w-full rounded-lg border border-input bg-background px-3 py-1 text-xs ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 cursor-pointer"
                                >
                                    <option value="info@sicilius.com.tr">info@sicilius.com.tr (Sistem Genel)</option>
                                    <option value="iletisim@sicilius.com.tr">iletisim@sicilius.com.tr (İletişim / Destek)</option>
                                    <option value="privacy@sicilius.com.tr">privacy@sicilius.com.tr (Gizlilik / KVKK)</option>
                                    <option value="legal@sicilius.com.tr">legal@sicilius.com.tr (Hukuk Departmanı)</option>
                                </select>
                            </div>
                            
                            <div className="space-y-1.5">
                                <Label htmlFor="to_email" className="font-semibold text-slate-700">Alıcı E-posta (To)</Label>
                                <Input
                                    id="to_email"
                                    type="email"
                                    placeholder="kisi@example.com"
                                    value={composeTo}
                                    onChange={(e) => setComposeTo(e.target.value)}
                                    required
                                    className="rounded-lg h-9"
                                />
                            </div>
                        </div>

                        <div className="space-y-1.5">
                            <Label htmlFor="mail_subject" className="font-semibold text-slate-700">Konu (Subject)</Label>
                            <Input
                                id="mail_subject"
                                placeholder="E-posta konu başlığı..."
                                value={composeSubject}
                                onChange={(e) => setComposeSubject(e.target.value)}
                                required
                                className="rounded-lg h-9"
                            />
                        </div>

                        <div className="space-y-1.5">
                            <Label htmlFor="mail_body" className="font-semibold text-slate-700">Mesaj (Message Body)</Label>
                            <textarea
                                id="mail_body"
                                rows={8}
                                value={composeBody}
                                onChange={(e) => setComposeBody(e.target.value)}
                                placeholder="E-posta içeriğini buraya yazın..."
                                className="flex min-h-[140px] w-full rounded-lg border border-input bg-background px-3 py-2 text-xs ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                                required
                            />
                        </div>

                        <div className="flex justify-end gap-2 pt-3 border-t">
                            <Button type="button" variant="outline" onClick={() => setComposeOpen(false)} className="h-8.5 rounded-lg text-xs font-semibold">İptal</Button>
                            <Button type="submit" disabled={composeSubmitting} className="bg-blue-600 hover:bg-blue-700 h-8.5 rounded-lg text-xs font-semibold px-4 text-white">
                                {composeSubmitting ? (
                                    <>
                                        <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
                                        Gönderiliyor...
                                    </>
                                ) : (
                                    <>
                                        <Send className="mr-1.5 h-3.5 w-3.5" />
                                        Gönder
                                    </>
                                )}
                            </Button>
                        </div>
                    </form>
                </DialogContent>
            </Dialog>
        </div>
    );
}
