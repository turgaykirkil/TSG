"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

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
}

interface IncomingEmailList {
    items: IncomingEmail[];
    total: number;
    page: number;
    per_page: number;
}

async function fetchIncomingEmails(page: number, unreadOnly: boolean): Promise<IncomingEmailList> {
    const params = new URLSearchParams({
        page: page.toString(),
        per_page: "20",
        ...(unreadOnly && { unread_only: "true" }),
    });

    const res = await fetch(`/api/v1/incoming-emails?${params}`, {
        credentials: "include",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch incoming emails");
    }

    return res.json();
}

async function markAsRead(emailId: string): Promise<void> {
    const res = await fetch(`/api/v1/incoming-emails/${emailId}/mark-read`, {
        method: "PATCH",
        credentials: "include",
    });

    if (!res.ok) {
        throw new Error("Failed to mark email as read");
    }
}

async function deleteEmail(emailId: string): Promise<void> {
    const res = await fetch(`/api/v1/incoming-emails/${emailId}`, {
        method: "DELETE",
        credentials: "include",
    });

    if (!res.ok) {
        throw new Error("Failed to delete email");
    }
}

export default function AdminInboxPage() {
    const [page, setPage] = useState(1);
    const [unreadOnly, setUnreadOnly] = useState(false);
    const [selectedEmail, setSelectedEmail] = useState<IncomingEmail | null>(null);
    const queryClient = useQueryClient();

    const { data, isLoading, error } = useQuery({
        queryKey: ["incoming-emails", page, unreadOnly],
        queryFn: () => fetchIncomingEmails(page, unreadOnly),
    });

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
            setSelectedEmail(null);
        },
    });

    const handleEmailClick = (email: IncomingEmail) => {
        setSelectedEmail(email);
        if (!email.is_read) {
            markAsReadMutation.mutate(email.id);
        }
    };

    return (
        <div className="max-w-7xl mx-auto p-6">
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Gelen Mailler</h1>
                    <p className="text-sm text-muted-foreground mt-1">
                        Cloudflare Email Routing ile alınan mesajlar
                    </p>
                </div>

                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={unreadOnly}
                        onChange={(e) => {
                            setUnreadOnly(e.target.checked);
                            setPage(1);
                        }}
                        className="w-4 h-4"
                    />
                    <span className="text-sm">Sadece okunmamışlar</span>
                </label>
            </div>

            {isLoading && <div className="text-center py-8">Yükleniyor...</div>}

            {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                    Hata: {(error as Error).message}
                </div>
            )}

            {data && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Email List */}
                    <div className="lg:col-span-1 space-y-2">
                        {data.items.length === 0 && (
                            <div className="text-center py-8 text-muted-foreground">
                                Mesaj bulunamadı
                            </div>
                        )}

                        {data.items.map((email) => (
                            <div
                                key={email.id}
                                onClick={() => handleEmailClick(email)}
                                className={`p-4 border rounded-lg cursor-pointer transition-colors ${selectedEmail?.id === email.id
                                        ? "bg-blue-50 border-blue-300"
                                        : !email.is_read
                                            ? "bg-white border-gray-300 font-semibold"
                                            : "bg-gray-50 border-gray-200"
                                    }`}
                            >
                                <div className="flex items-start justify-between mb-1">
                                    <span className="text-sm text-gray-600 truncate flex-1">
                                        {email.from_address}
                                    </span>
                                    {!email.is_read && (
                                        <span className="ml-2 w-2 h-2 bg-blue-500 rounded-full flex-shrink-0"></span>
                                    )}
                                </div>
                                <div className="font-medium text-sm truncate mb-1">
                                    {email.subject || "(Konu yok)"}
                                </div>
                                <div className="text-xs text-gray-500">
                                    {new Date(email.received_at).toLocaleDateString("tr-TR", {
                                        day: "numeric",
                                        month: "short",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    })}
                                </div>
                            </div>
                        ))}

                        {/* Pagination */}
                        {data.total > data.per_page && (
                            <div className="flex items-center justify-between pt-4">
                                <button
                                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                                    disabled={page === 1}
                                    className="px-3 py-1 text-sm border rounded disabled:opacity-50"
                                >
                                    Önceki
                                </button>
                                <span className="text-sm text-muted-foreground">
                                    Sayfa {page} / {Math.ceil(data.total / data.per_page)}
                                </span>
                                <button
                                    onClick={() => setPage((p) => p + 1)}
                                    disabled={page >= Math.ceil(data.total / data.per_page)}
                                    className="px-3 py-1 text-sm border rounded disabled:opacity-50"
                                >
                                    Sonraki
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Email Detail */}
                    <div className="lg:col-span-2">
                        {selectedEmail ? (
                            <div className="border rounded-lg p-6 bg-white">
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex-1">
                                        <h2 className="text-xl font-bold mb-2">
                                            {selectedEmail.subject || "(Konu yok)"}
                                        </h2>
                                        <div className="text-sm text-gray-600 space-y-1">
                                            <div>
                                                <strong>Gönderen:</strong> {selectedEmail.from_address}
                                            </div>
                                            <div>
                                                <strong>Alıcı:</strong> {selectedEmail.to_address}
                                            </div>
                                            <div>
                                                <strong>Tarih:</strong>{" "}
                                                {new Date(selectedEmail.received_at).toLocaleString("tr-TR")}
                                            </div>
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => {
                                            if (confirm("Bu e-postayı silmek istediğinizden emin misiniz?")) {
                                                deleteEmailMutation.mutate(selectedEmail.id);
                                            }
                                        }}
                                        className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
                                    >
                                        Sil
                                    </button>
                                </div>

                                <div className="border-t pt-4">
                                    {selectedEmail.body_html ? (
                                        <div
                                            className="prose max-w-none"
                                            dangerouslySetInnerHTML={{ __html: selectedEmail.body_html }}
                                        />
                                    ) : (
                                        <pre className="whitespace-pre-wrap text-sm">
                                            {selectedEmail.body_text || "(İçerik yok)"}
                                        </pre>
                                    )}
                                </div>
                            </div>
                        ) : (
                            <div className="border rounded-lg p-12 bg-gray-50 text-center text-muted-foreground">
                                Sol taraftan bir e-posta seçin
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
