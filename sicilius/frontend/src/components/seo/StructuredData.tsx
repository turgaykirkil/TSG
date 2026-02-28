import React from 'react';

export default function StructuredData() {
    const organizationData = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Sicilius",
        "url": "https://sicilius.com.tr",
        "logo": "https://sicilius.com.tr/logo.svg",
        "description": "Halka açık kayıtları modernize ederek hızlı arama ve analiz sunan profesyonel veri platformu.",
        "contactPoint": {
            "@type": "ContactPoint",
            "email": "info@sicilius.com.tr",
            "contactType": "customer service"
        }
    };

    const websiteData = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Sicilius",
        "url": "https://sicilius.com.tr",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://sicilius.com.tr/search?q={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationData) }}
            />
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteData) }}
            />
        </>
    );
}
