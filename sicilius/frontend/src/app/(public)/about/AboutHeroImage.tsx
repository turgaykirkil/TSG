"use client";

import Image, { ImageProps } from "next/image";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface AboutHeroImageProps extends Omit<ImageProps, "onLoad" | "className"> {
    containerClassName?: string;
    imageClassName?: string;
}

export default function AboutHeroImage({
    containerClassName,
    imageClassName,
    alt,
    ...props
}: AboutHeroImageProps) {
    const [isLoading, setIsLoading] = useState(true);

    return (
        <div className={cn("relative overflow-hidden bg-gray-200 dark:bg-slate-800", containerClassName)}>
            {/* Skeleton / Shimmer Effect while loading */}
            {isLoading && (
                <div className="absolute inset-0 z-10 animate-pulse bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full"
                    style={{ animation: 'shimmer 1.5s infinite' }}
                />
            )}

            <Image
                alt={alt}
                className={cn(
                    "duration-700 ease-in-out",
                    isLoading
                        ? "scale-110 blur-xl opacity-0"
                        : "scale-100 blur-0 opacity-100",
                    imageClassName
                )}
                onLoad={() => setIsLoading(false)}
                {...props}
            />
        </div>
    );
}
