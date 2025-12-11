"use client";

import React, { useEffect, useState, useRef } from 'react';
import dynamic from 'next/dynamic';
import { api } from '@/lib/api';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle, CheckCircle, Share2, Info } from 'lucide-react';

const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), { ssr: false });

interface NexusAnalysisSectionProps {
    companyId: string;
}

export default function NexusAnalysisSection({ companyId }: NexusAnalysisSectionProps) {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [limit, setLimit] = useState(10);
    const containerRef = useRef<HTMLDivElement>(null);
    const [dimensions, setDimensions] = useState({ width: 0, height: 300 });

    const [started, setStarted] = useState(false);
    const [expandedNodeIds, setExpandedNodeIds] = useState<Set<string>>(new Set());
    const [expanding, setExpanding] = useState(false);

    const handleNodeClick = (node: any) => {
        if (!node || !node.id || expanding) return;

        // Mark as expanded (visually distinctive)
        setExpandedNodeIds(prev => new Set(prev).add(node.id));

        setExpanding(true);
        // Fetch neighborhood for the clicked node (limit=10 to avoid explosion)
        api.get(`/api/v1/nexus/network/${node.id}?limit=10`)
            .then(res => {
                const newData = res.data;
                if (!newData?.graph) return;

                setData((prev: any) => {
                    if (!prev) return newData;

                    // Merge nodes (prevent duplicates)
                    const existingIds = new Set(prev.graph.nodes.map((n: any) => n.id));
                    const newNodes = newData.graph.nodes.filter((n: any) => !existingIds.has(n.id));

                    // Merge links
                    const existingLinks = new Set(prev.graph.links.map((l: any) => {
                        const s = typeof l.source === 'object' ? l.source.id : l.source;
                        const t = typeof l.target === 'object' ? l.target.id : l.target;
                        return `${s}-${t}`;
                    }));

                    const newLinks = newData.graph.links.filter((l: any) => {
                        const key = `${l.source}-${l.target}`;
                        return !existingLinks.has(key);
                    });

                    return {
                        ...prev,
                        graph: {
                            nodes: [...prev.graph.nodes, ...newNodes],
                            links: [...prev.graph.links, ...newLinks]
                        },
                        analysis: {
                            ...prev.analysis,
                            total_nodes: (prev.analysis?.total_nodes || 0) + newNodes.length
                        }
                    };
                });
            })
            .catch(console.error)
            .finally(() => setExpanding(false));
    };

    useEffect(() => {
        if (!containerRef.current) return;
        const resizeObserver = new ResizeObserver((entries) => {
            for (const entry of entries) {
                setDimensions({
                    width: entry.contentRect.width,
                    height: entry.contentRect.height
                });
            }
        });
        resizeObserver.observe(containerRef.current);
        return () => resizeObserver.disconnect();
    }, [started, loading]);

    useEffect(() => {
        if (!companyId || !started) return;

        setLoading(true);
        api.get(`/api/v1/nexus/network/${companyId}?limit=${limit}`)
            .then(res => {
                setData(res.data);
            })
            .catch(err => {
                setError("Ağ analizi yüklenemedi.");
            })
            .finally(() => setLoading(false));
    }, [companyId, limit, started]);
    if (error) return <div className="text-sm text-red-500">{error}</div>;

    // Default empty state or data results
    const graph = data?.graph || { nodes: [], links: [] };
    const analysis = data?.analysis || {};
    const isRisky = analysis?.cycle_detected || analysis?.risky_neighbors?.length > 0 || analysis?.suspicious_addresses?.length > 0;

    return (
        <section className="mt-6 border rounded-lg overflow-hidden bg-slate-50 dark:bg-slate-800/50 border-slate-200 dark:border-slate-700">
            <div className="p-3 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center bg-white dark:bg-slate-900">
                <h3 className="font-semibold text-slate-800 dark:text-slate-100 flex items-center gap-2">
                    <Share2 className="w-4 h-4 text-purple-600" />
                    NEXUS Ağ Analizi
                    {(loading || expanding) && <span className="text-xs text-slate-400 font-normal animate-pulse ml-2">({expanding ? 'Genişletiliyor...' : 'Yükleniyor...'})</span>}
                </h3>
                {isRisky && started ? (
                    <Badge variant="destructive" className="animate-pulse">YÜKSEK RİSK</Badge>
                ) : started && data ? (
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">GÜVENLİ AĞ</Badge>
                ) : null}
            </div>

            <div className="p-4">
                {!started ? (
                    <div className="flex flex-col items-center justify-center py-8 text-center space-y-3">
                        <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-full">
                            <Share2 className="w-8 h-8 text-purple-600 dark:text-purple-400" />
                        </div>
                        <div className="space-y-1">
                            <h4 className="font-medium">Ağ Analizi Başlatılmadı</h4>
                            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto">
                                Bu şirketin ortaklık yapısını, risk analizini ve ilişkili olduğu diğer kurumları görmek için analizi başlatın.
                            </p>
                        </div>
                        <button
                            onClick={() => setStarted(true)}
                            className="mt-2 bg-purple-600 hover:bg-purple-700 text-white font-medium px-6 py-2 rounded-lg transition-colors flex items-center gap-2"
                        >
                            <Share2 size={16} />
                            Analizi Başlat
                        </button>
                    </div>
                ) : loading && limit === 10 ? (
                    <div className="flex flex-col items-center justify-center py-12 space-y-3 animate-pulse">
                        <div className="w-8 h-8 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
                        <p className="text-sm text-slate-500">Bağlantılar taranıyor...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Sol Panel: Risk Kartları */}
                        <div className="space-y-3">
                            <div className={`p-3 rounded border text-xs ${analysis?.cycle_detected ? 'bg-red-50 border-red-200 text-red-800' : 'bg-white border-slate-200 text-slate-600'}`}>
                                <div className="font-bold flex items-center gap-1">
                                    {analysis?.cycle_detected ? <AlertCircle size={14} /> : <CheckCircle size={14} />}
                                    Döngüsel Sermaye
                                </div>
                                <div className="mt-1">
                                    {analysis?.cycle_detected
                                        ? `${analysis.cycles_count} adet sermaye döngüsü tespit edildi.`
                                        : "Çapraz ortaklık döngüsü yok."}
                                </div>
                            </div>

                            <div className={`p-3 rounded border text-xs ${analysis?.risky_neighbors?.length > 0 ? 'bg-orange-50 border-orange-200 text-orange-800' : 'bg-white border-slate-200 text-slate-600'}`}>
                                <div className="font-bold flex items-center gap-1">
                                    {analysis?.risky_neighbors?.length > 0 ? <AlertCircle size={14} /> : <CheckCircle size={14} />}
                                    Risk Bulaşımı (Contagion)
                                </div>
                                <div className="mt-1">
                                    {analysis?.risky_neighbors?.length > 0
                                        ? `İlişkili ${analysis.risky_neighbors.length} riskli kurum tespit edildi.`
                                        : "Riskli kurum bağlantısı yok."}
                                </div>
                            </div>

                            <div className={`p-3 rounded border text-xs ${analysis?.suspicious_addresses?.length > 0 ? 'bg-yellow-50 border-yellow-200 text-yellow-800' : 'bg-white border-slate-200 text-slate-600'}`}>
                                <div className="font-bold flex items-center gap-1">
                                    {analysis?.suspicious_addresses?.length > 0 ? <AlertCircle size={14} /> : <CheckCircle size={14} />}
                                    Adres Yoğunluğu
                                </div>
                                <div className="mt-1">
                                    {analysis?.suspicious_addresses?.length > 0
                                        ? `${analysis.suspicious_addresses.length} adreste anormal şirket yığılması var.`
                                        : "Adres paravan riski düşük."}
                                </div>
                            </div>
                        </div>

                        {/* Sağ Panel: Graf Görselleştirme */}
                        <div
                            ref={containerRef}
                            className="md:col-span-2 h-[300px] bg-slate-900 rounded border border-slate-700 overflow-hidden relative group"
                        >
                            {/* Legend (Lejant) Overlay */}
                            <div className="absolute top-2 left-2 z-10 bg-slate-900/80 backdrop-blur-sm p-2 rounded border border-slate-700 text-[10px] text-slate-300 space-y-1 shadow-sm select-none pointer-events-none">
                                <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Hedef Firma</div>
                                <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-purple-500"></div> İncelenen (Genişletilmiş)</div>
                                <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-red-500"></div> Yüksek Riskli</div>
                                <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-green-500"></div> Bağlantılı Firma</div>
                            </div>

                            {dimensions.width > 0 && (
                                <ForceGraph2D
                                    width={dimensions.width}
                                    height={300}
                                    graphData={graph}
                                    onNodeClick={handleNodeClick}
                                    nodeLabel="label"
                                    nodeColor={(node: any) => {
                                        if (node.id === companyId) return '#3b82f6'; // Hedef şirket (Mavi)
                                        if (expandedNodeIds.has(node.id)) return '#a855f7'; // Genişletilmiş Node (Mor)
                                        if (node.risk_status === 'HIGH') return '#ef4444'; // Riskli (Kırmızı)
                                        return '#22c55e'; // Şirket (Yeşil)
                                    }}
                                    linkLabel="label"
                                    linkWidth={2}
                                    nodeRelSize={6}
                                    linkColor={() => '#64748b'}
                                    linkDirectionalArrowLength={3.5}
                                    linkDirectionalArrowRelPos={1}
                                    cooldownTicks={100}
                                />
                            )}

                            {/* Load More Overlay Button */}
                            {analysis?.limit_reached && !loading && (
                                <div className="absolute bottom-4 right-4 z-20">
                                    <button
                                        onClick={() => setLimit(prev => prev + 10)}
                                        className="bg-blue-600 hover:bg-blue-700 text-white text-xs px-3 py-1.5 rounded shadow-lg flex items-center gap-1 transition-colors"
                                    >
                                        <Share2 size={12} />
                                        Daha Fazla (+10)
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </section>
    );
}
