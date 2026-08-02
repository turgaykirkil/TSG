import { useState, useCallback, useMemo } from 'react';

export const useSearch = <T>(
  items: T[],
  searchableFields: (keyof T)[],
  initialQuery: string = ''
) => {
  const [searchQuery, setSearchQuery] = useState(initialQuery);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const filteredItems = useMemo(() => {
    if (!searchQuery) return items;

    const searchTerms = searchQuery.toLowerCase().split(' ').filter(term => term.length > 0);

    return items.filter(item => {
      const searchableText = searchableFields
        .map(field => String(item[field]))
        .join(' ')
        .toLowerCase();

      return searchTerms.every(term => searchableText.includes(term));
    });
  }, [items, searchQuery, searchableFields]);

  return {
    searchQuery,
    setSearchQuery: handleSearch,
    filteredItems,
  };
};
