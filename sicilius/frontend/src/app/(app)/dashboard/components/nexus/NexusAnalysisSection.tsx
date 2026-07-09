"use client";

import React, { useEffect, useState, useRef, useCallback } from 'react';
import dynamic from 'next/dynamic';
import { api } from '@/lib/api';

const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), { ssr: false });

interface NexusAnalysisSectionProps {
    companyId: string;
}

type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export default function NexusAnalysisSection({ companyId }: NexusAnalysisSectionProps) {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [limit, setLimit] = useState(25);
    const containerRef = useRef<HTMLDivElement>(null);
    const [dimensions, setDimensions] = useState({ width: 0, height: 360 });

    const [started, setStarted] = useState(false);
    const [expandedNodeIds, setExpandedNodeIds] = useState<Set<string>>(new Set());
    const [expanding, setExpanding] = useState(false);

    const handleNodeClick = (node: any) => {
        if (!node || !node.id || expanding) return;
        setExpandedNodeIds(prev => new Set(prev).add(node.id));
        setExpanding(true);
        api.get(`/api/v1/nexus/network/${node.id}?limit=10`)
            .then(res => {
                const newData = res.data;
                if (!newData?.graph) return;
                setData((prev: any) => {
                    if (!prev) return newData;
                    const existingIds = new Set(prev.graph.nodes.map((n: any) => n.id));
                    const newNodes = newData.graph.nodes.filter((n: any) => !existingIds.has(n.id));
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
                    height: entry.contentRect.height,
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
            .then(res => setData(res.data))
            .catch(() => setError("Ağ analizi yüklenemedi."))
            .finally(() => setLoading(false));
    }, [companyId, limit, started]);

    const graph = data?.graph || { nodes: [], links: [] };
    const analysis = data?.analysis || {};
    const fraudLevel: RiskLevel = analysis?.fraud_level || 'LOW';
    const isHighRisk = fraudLevel === 'HIGH';
    const isMediumRisk = fraudLevel === 'MEDIUM';

    const riskBadgeEl = started && data ? (
        isHighRisk ? (
            <span style={styles.badgeHigh}>⚠ YÜKSEK RİSK</span>
        ) : isMediumRisk ? (
            <span style={styles.badgeMedium}>◎ ORTA RİSK</span>
        ) : (
            <span style={styles.badgeLow}>✓ GÜVENLİ AĞ</span>
        )
    ) : null;

    return (
        <section style={styles.wrapper}>
            {/* Animated grid overlay */}
            <div style={styles.gridOverlay} aria-hidden />

            {/* Header */}
            <div style={styles.header}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    {/* NEXUS SVG Icon */}
                    <svg width="28" height="28" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M50 5 L93.3 30 V80 L50 105 L6.7 80 V30 L50 5Z" stroke="#0ea5e9" strokeWidth="2" strokeOpacity="0.6" />
                        <circle cx="50" cy="55" r="8" fill="#0ea5e9" />
                        <circle cx="50" cy="25" r="4" fill="#6366f1" />
                        <circle cx="25" cy="70" r="4" fill="#6366f1" />
                        <circle cx="75" cy="70" r="4" fill="#6366f1" />
                        <line x1="50" y1="55" x2="50" y2="25" stroke="#38bdf8" strokeWidth="2" />
                        <line x1="50" y1="55" x2="25" y2="70" stroke="#38bdf8" strokeWidth="2" />
                        <line x1="50" y1="55" x2="75" y2="70" stroke="#38bdf8" strokeWidth="2" />
                    </svg>
                    <div>
                        <h3 style={styles.title}>
                            NEXUS Ağ Analizi
                        </h3>
                        <p style={styles.subtitle}>
                            {(loading || expanding)
                                ? (expanding ? '↗ Düğüm genişletiliyor...' : '⟳ Ağ taranıyor...')
                                : started && data
                                    ? `${analysis?.total_nodes || graph.nodes.length} düğüm · ${graph.links.length} bağlantı`
                                    : 'Ortaklık & Risk Haritası'}
                        </p>
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    {riskBadgeEl}
                    {/* Loader bar */}
                    {(loading || expanding) && (
                        <div style={styles.loaderBar}>
                            <div style={styles.loaderBarFill} />
                        </div>
                    )}
                </div>
            </div>

            {/* Body */}
            <div style={styles.body}>
                {error ? (
                    <div style={styles.errorBox}>
                        <span>⚠</span> {error}
                    </div>
                ) : !started ? (
                    /* ── NOT STARTED STATE ── */
                    <div style={styles.idleState}>
                        {/* Animated network illustration */}
                        <div style={styles.idleGraphic}>
                            <svg width="120" height="100" viewBox="0 0 120 100">
                                <circle cx="60" cy="50" r="12" fill="none" stroke="#0ea5e9" strokeWidth="1.5" opacity="0.8">
                                    <animate attributeName="r" values="12;16;12" dur="3s" repeatCount="indefinite" />
                                    <animate attributeName="opacity" values="0.8;0.4;0.8" dur="3s" repeatCount="indefinite" />
                                </circle>
                                <circle cx="60" cy="50" r="6" fill="#0ea5e9" opacity="0.9" />
                                {/* Satellite nodes */}
                                {[[20, 20], [100, 20], [10, 75], [110, 75], [60, 10]].map(([cx, cy], i) => (
                                    <g key={i}>
                                        <line x1="60" y1="50" x2={cx} y2={cy} stroke="#334155" strokeWidth="1" strokeDasharray="3 3">
                                            <animate attributeName="stroke-opacity" values="0.3;0.7;0.3" dur={`${2 + i * 0.4}s`} repeatCount="indefinite" />
                                        </line>
                                        <circle cx={cx} cy={cy} r="4" fill="#6366f1" opacity="0.6">
                                            <animate attributeName="opacity" values="0.6;1;0.6" dur={`${2 + i * 0.3}s`} repeatCount="indefinite" />
                                        </circle>
                                    </g>
                                ))}
                            </svg>
                        </div>
                        <h4 style={styles.idleTitle}>Ağ Analizi Başlatılmadı</h4>
                        <p style={styles.idleDesc}>
                            Bu şirketin ortaklık yapısını, risk analizini ve ilişkili olduğu kurumları görselleştirmek için analizi başlatın.
                        </p>
                        <button onClick={() => setStarted(true)} style={styles.startBtn}>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <circle cx="12" cy="12" r="10" />
                                <path d="M12 8v8M8 12h8" />
                            </svg>
                            Analizi Başlat
                        </button>
                    </div>
                ) : loading && graph.nodes.length === 0 ? (
                    /* ── LOADING STATE ── */
                    <div style={styles.loadingState}>
                        <div style={styles.spinner} />
                        <p style={styles.loadingText}>Bağlantılar taranıyor...</p>
                        <p style={{ ...styles.loadingText, fontSize: '11px', opacity: 0.5, marginTop: 4 }}>NEXUS Ağ Motoru aktif</p>
                    </div>
                ) : (
                    /* ── ANALYSIS RESULTS ── */
                    <div style={styles.resultsGrid}>

                        {/* ── LEFT: Risk Cards ── */}
                        <div style={styles.riskPanel}>

                            <RiskCard
                                label="Döngüsel Sermaye"
                                icon="⟳"
                                alert={!!analysis?.cycle_detected}
                                color={analysis?.cycle_detected ? '#ef4444' : '#22c55e'}
                                value={analysis?.cycle_detected
                                    ? `${analysis.cycles_count || 0} döngü tespit edildi`
                                    : 'Çapraz ortaklık döngüsü yok'}
                            />

                            <RiskCard
                                label="Risk Bulaşımı"
                                icon="⚡"
                                alert={!!(analysis?.risky_neighbors?.length > 0 || analysis?.fraud_meta?.risky_at_addr > 0)}
                                color={analysis?.risky_neighbors?.length > 0 || analysis?.fraud_meta?.risky_at_addr > 0 ? '#f97316' : '#22c55e'}
                                value={analysis?.fraud_meta?.risky_at_addr > 0
                                    ? `Aynı adreste ${analysis.fraud_meta.risky_at_addr} riskli kurum`
                                    : analysis?.risky_neighbors?.length > 0
                                        ? `${analysis.risky_neighbors.length} riskli kurum bağlantısı`
                                        : 'Riskli kurum bağlantısı yok'}
                            />

                            <RiskCard
                                label="Adres Yoğunluğu"
                                icon="⊕"
                                alert={!!(analysis?.suspicious_addresses?.length > 0 || analysis?.fraud_meta?.total_at_addr > 3)}
                                color={analysis?.suspicious_addresses?.length > 0 || analysis?.fraud_meta?.total_at_addr > 3 ? '#eab308' : '#22c55e'}
                                value={analysis?.fraud_meta?.total_at_addr > 3
                                    ? `Bu adreste ${analysis.fraud_meta.total_at_addr} şirket kayıtlı`
                                    : analysis?.suspicious_addresses?.length > 0
                                        ? `${analysis.suspicious_addresses.length} adreste yığılma`
                                        : 'Adres paravan riski düşük'}
                            />

                            {analysis?.fraud_signals?.length > 0 && (
                                <div style={{ ...styles.riskCard, borderColor: 'rgba(239,68,68,0.3)', background: 'rgba(239,68,68,0.08)' }}>
                                    <div style={styles.riskCardHeader}>
                                        <span style={{ ...styles.riskDot, background: '#ef4444' }} />
                                        <span style={{ ...styles.riskLabel, color: '#ef4444' }}>Fraud Sinyalleri</span>
                                        <span style={{ marginLeft: 'auto', fontSize: '10px', color: '#ef4444', fontWeight: 700 }}>
                                            {analysis.fraud_score} puan
                                        </span>
                                    </div>
                                    <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
                                        {analysis.fraud_signals.slice(0, 4).map((sig: string, i: number) => (
                                            <li key={i} style={{ fontSize: '10px', color: '#fca5a5', display: 'flex', gap: 4, marginTop: 4 }}>
                                                <span style={{ color: '#ef4444', flexShrink: 0 }}>▸</span>
                                                <span>{sig}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Legend */}
                            <div style={styles.legend}>
                                <p style={styles.legendTitle}>Lejant</p>
                                <LegendItem color="#3b82f6" label="Hedef Firma" />
                                <LegendItem color="#a855f7" label="Genişletilmiş" />
                                <LegendItem color="#ef4444" label="Yüksek Riskli" />
                                <LegendItem color="#22c55e" label="Bağlantılı" />
                            </div>

                            {/* Load More */}
                            {analysis?.limit_reached && limit < 60 && !loading && (
                                <button
                                    onClick={() => setLimit(prev => Math.min(prev + 15, 60))}
                                    style={styles.loadMoreBtn}
                                >
                                    ↗ Genişlet ({limit}/60)
                                </button>
                            )}
                        </div>

                        {/* ── RIGHT: Graph Canvas ── */}
                        <div ref={containerRef} style={styles.graphCanvas}>
                            {/* Subtle corner lines */}
                            <div style={{ ...styles.cornerLine, top: 8, left: 8, borderTop: '1px solid rgba(14,165,233,0.4)', borderLeft: '1px solid rgba(14,165,233,0.4)' }} />
                            <div style={{ ...styles.cornerLine, top: 8, right: 8, borderTop: '1px solid rgba(14,165,233,0.4)', borderRight: '1px solid rgba(14,165,233,0.4)' }} />
                            <div style={{ ...styles.cornerLine, bottom: 8, left: 8, borderBottom: '1px solid rgba(14,165,233,0.4)', borderLeft: '1px solid rgba(14,165,233,0.4)' }} />
                            <div style={{ ...styles.cornerLine, bottom: 8, right: 8, borderBottom: '1px solid rgba(14,165,233,0.4)', borderRight: '1px solid rgba(14,165,233,0.4)' }} />

                            {/* Status badge overlay */}
                            <div style={styles.graphStatus}>
                                <span style={styles.graphStatusDot} />
                                NEXUS ENGINE
                            </div>

                            {dimensions.width > 0 && (
                                <ForceGraph2D
                                    width={dimensions.width}
                                    height={dimensions.height}
                                    graphData={graph}
                                    onNodeClick={handleNodeClick}
                                    backgroundColor="#050b14"
                                    nodeLabel={(node: any) => {
                                        let text = node.label || '';
                                        if (node.anomaly_score !== undefined) {
                                            text += `\n🤖 AI Skor: ${parseFloat(node.anomaly_score).toFixed(2)}`;
                                            if (node.risk_reason) text += `\n⚠ ${node.risk_reason}`;
                                        }
                                        return text;
                                    }}
                                    nodeColor={(node: any) => {
                                        if (node.id === companyId) return '#3b82f6';
                                        if (expandedNodeIds.has(node.id)) return '#a855f7';
                                        if (node.risk_status === 'HIGH') return '#ef4444';
                                        return '#22c55e';
                                    }}
                                    nodeRelSize={5}
                                    linkColor={() => 'rgba(100,116,139,0.5)'}
                                    linkWidth={1.5}
                                    linkDirectionalArrowLength={4}
                                    linkDirectionalArrowRelPos={1}
                                    cooldownTicks={120}
                                />
                            )}

                            {/* Expanding indicator */}
                            {expanding && (
                                <div style={styles.expandingOverlay}>
                                    <div style={styles.spinnerSm} />
                                    <span style={{ color: '#94a3b8', fontSize: '11px' }}>Düğüm genişletiliyor...</span>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </section>
    );
}

/* ── Sub-components ── */

function RiskCard({ label, icon, alert, color, value }: {
    label: string; icon: string; alert: boolean; color: string; value: string;
}) {
    return (
        <div style={{
            ...styles.riskCard,
            borderColor: alert ? `${color}44` : 'rgba(51,65,85,0.5)',
            background: alert ? `${color}11` : 'rgba(15,23,42,0.5)',
        }}>
            <div style={styles.riskCardHeader}>
                <span style={{ ...styles.riskDot, background: color }} />
                <span style={{ ...styles.riskLabel, color: alert ? color : '#94a3b8' }}>{label}</span>
                <span style={{ marginLeft: 'auto', fontSize: '14px', color }}>{icon}</span>
            </div>
            <p style={{ margin: '6px 0 0', fontSize: '11px', color: alert ? '#e2e8f0' : '#64748b', lineHeight: 1.4 }}>
                {value}
            </p>
        </div>
    );
}

function LegendItem({ color, label }: { color: string; label: string }) {
    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 4 }}>
            <div style={{ width: 8, height: 8, borderRadius: '50%', background: color, flexShrink: 0 }} />
            <span style={{ fontSize: '10px', color: '#64748b' }}>{label}</span>
        </div>
    );
}

/* ── Inline Styles (Dark Theme) ── */
const styles: Record<string, React.CSSProperties> = {
    wrapper: {
        marginTop: 24,
        borderRadius: 14,
        overflow: 'hidden',
        background: 'rgba(5,11,20,0.95)',
        border: '1px solid rgba(56,189,248,0.15)',
        boxShadow: '0 4px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(56,189,248,0.06)',
        position: 'relative',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
    },
    gridOverlay: {
        position: 'absolute',
        inset: 0,
        backgroundImage: `linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px)`,
        backgroundSize: '32px 32px',
        pointerEvents: 'none',
        zIndex: 0,
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '14px 18px',
        borderBottom: '1px solid rgba(56,189,248,0.1)',
        background: 'rgba(10,18,35,0.8)',
        position: 'relative',
        zIndex: 1,
    },
    title: {
        margin: 0,
        fontSize: '14px',
        fontWeight: 700,
        color: '#e2e8f0',
        letterSpacing: '-0.02em',
    },
    subtitle: {
        margin: '2px 0 0',
        fontSize: '10px',
        color: '#4b6a8a',
        letterSpacing: '0.02em',
    },
    loaderBar: {
        width: 80,
        height: 2,
        background: 'rgba(14,165,233,0.2)',
        borderRadius: 2,
        overflow: 'hidden',
    },
    loaderBarFill: {
        height: '100%',
        width: '40%',
        background: '#0ea5e9',
        borderRadius: 2,
        animation: 'nexus-slide 1.5s linear infinite',
    },
    body: {
        padding: '16px',
        position: 'relative',
        zIndex: 1,
    },
    errorBox: {
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        padding: '12px 16px',
        borderRadius: 8,
        background: 'rgba(239,68,68,0.1)',
        border: '1px solid rgba(239,68,68,0.3)',
        color: '#fca5a5',
        fontSize: '13px',
    },
    idleState: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 20px',
        textAlign: 'center',
        gap: 16,
    },
    idleGraphic: {
        background: 'rgba(14,165,233,0.05)',
        borderRadius: '50%',
        width: 120,
        height: 100,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px solid rgba(14,165,233,0.15)',
    },
    idleTitle: {
        margin: 0,
        color: '#e2e8f0',
        fontSize: '15px',
        fontWeight: 600,
    },
    idleDesc: {
        margin: 0,
        color: '#64748b',
        fontSize: '12px',
        maxWidth: 400,
        lineHeight: 1.6,
    },
    startBtn: {
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        padding: '10px 24px',
        background: 'linear-gradient(135deg, #0ea5e9, #6366f1)',
        border: 'none',
        borderRadius: 8,
        color: '#fff',
        fontWeight: 600,
        fontSize: '13px',
        cursor: 'pointer',
        boxShadow: '0 0 20px rgba(14,165,233,0.3)',
        transition: 'transform 0.2s, box-shadow 0.2s',
    },
    loadingState: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '60px 20px',
        gap: 12,
    },
    spinner: {
        width: 36,
        height: 36,
        borderRadius: '50%',
        border: '3px solid rgba(14,165,233,0.2)',
        borderTopColor: '#0ea5e9',
        animation: 'nexus-spin 0.8s linear infinite',
    },
    spinnerSm: {
        width: 16,
        height: 16,
        borderRadius: '50%',
        border: '2px solid rgba(14,165,233,0.2)',
        borderTopColor: '#0ea5e9',
        animation: 'nexus-spin 0.8s linear infinite',
    },
    loadingText: {
        margin: 0,
        color: '#64748b',
        fontSize: '12px',
    },
    resultsGrid: {
        display: 'grid',
        gridTemplateColumns: '200px 1fr',
        gap: 12,
    },
    riskPanel: {
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
    },
    riskCard: {
        padding: '10px 12px',
        borderRadius: 8,
        border: '1px solid',
        transition: 'border-color 0.3s',
    },
    riskCardHeader: {
        display: 'flex',
        alignItems: 'center',
        gap: 6,
    },
    riskDot: {
        width: 6,
        height: 6,
        borderRadius: '50%',
        flexShrink: 0,
    },
    riskLabel: {
        fontSize: '11px',
        fontWeight: 700,
        letterSpacing: '0.03em',
    },
    legend: {
        marginTop: 4,
        padding: '10px 12px',
        borderRadius: 8,
        background: 'rgba(15,23,42,0.5)',
        border: '1px solid rgba(51,65,85,0.5)',
    },
    legendTitle: {
        margin: '0 0 4px',
        fontSize: '10px',
        fontWeight: 700,
        color: '#475569',
        letterSpacing: '0.05em',
        textTransform: 'uppercase' as const,
    },
    loadMoreBtn: {
        padding: '7px 12px',
        borderRadius: 6,
        background: 'rgba(14,165,233,0.1)',
        border: '1px solid rgba(14,165,233,0.3)',
        color: '#38bdf8',
        fontSize: '11px',
        fontWeight: 600,
        cursor: 'pointer',
        width: '100%',
    },
    graphCanvas: {
        position: 'relative',
        height: '360px',
        borderRadius: 10,
        background: '#050b14',
        border: '1px solid rgba(56,189,248,0.12)',
        overflow: 'hidden',
    },
    cornerLine: {
        position: 'absolute',
        width: 12,
        height: 12,
        zIndex: 2,
        pointerEvents: 'none',
    },
    graphStatus: {
        position: 'absolute',
        top: 10,
        right: 10,
        zIndex: 3,
        display: 'flex',
        alignItems: 'center',
        gap: 5,
        padding: '4px 8px',
        borderRadius: 4,
        background: 'rgba(5,11,20,0.9)',
        border: '1px solid rgba(14,165,233,0.2)',
        fontSize: '9px',
        fontWeight: 700,
        color: '#0ea5e9',
        letterSpacing: '0.1em',
    },
    graphStatusDot: {
        width: 5,
        height: 5,
        borderRadius: '50%',
        background: '#0ea5e9',
        display: 'inline-block',
        boxShadow: '0 0 4px #0ea5e9',
    },
    expandingOverlay: {
        position: 'absolute',
        bottom: 10,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 4,
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        padding: '6px 12px',
        borderRadius: 6,
        background: 'rgba(5,11,20,0.9)',
        border: '1px solid rgba(14,165,233,0.2)',
    },
    badgeHigh: {
        padding: '3px 10px',
        borderRadius: 4,
        background: 'rgba(239,68,68,0.15)',
        border: '1px solid rgba(239,68,68,0.4)',
        color: '#fca5a5',
        fontSize: '10px',
        fontWeight: 700,
        letterSpacing: '0.05em',
    },
    badgeMedium: {
        padding: '3px 10px',
        borderRadius: 4,
        background: 'rgba(234,179,8,0.15)',
        border: '1px solid rgba(234,179,8,0.4)',
        color: '#fde047',
        fontSize: '10px',
        fontWeight: 700,
        letterSpacing: '0.05em',
    },
    badgeLow: {
        padding: '3px 10px',
        borderRadius: 4,
        background: 'rgba(34,197,94,0.12)',
        border: '1px solid rgba(34,197,94,0.3)',
        color: '#86efac',
        fontSize: '10px',
        fontWeight: 700,
        letterSpacing: '0.05em',
    },
};
