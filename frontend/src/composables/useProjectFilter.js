import { ref, computed } from 'vue';

export function useProjectFilter(projects) {
    const searchQuery = ref('');
    const selectedYear = ref(new Date().getFullYear());
    const currentPage = ref(1);
    const itemsPerPage = 6;

    const filteredProjects = computed(() => {
        if (!projects.value) return [];

        return projects.value.filter((project) => {
            const projectYearStart = new Date(project.start_date).getFullYear();
            const projectYearEnd = new Date(project.end_date).getFullYear();
            const isYearInRange =
                (Number(selectedYear.value) >= projectYearStart && Number(selectedYear.value) <= projectYearEnd);

            const isKeywordMatch = (project.description + project.name + project.coordinator + project.processo_sei)
                .toLowerCase()
                .includes((searchQuery.value || '').toLowerCase());

            return isYearInRange && isKeywordMatch;
        });
    });

    const paginatedProjects = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return filteredProjects.value.slice(start, end);
    });

    const totalPages = computed(() => {
        return Math.max(1, Math.ceil(filteredProjects.value.length / itemsPerPage));
    });

    const getYearRange = (projectsList) => {
        if (!projectsList || projectsList.length === 0)
            return [new Date().getFullYear()];

        const currentYear = new Date().getFullYear();
        let maxEndYear = currentYear;
        let minStartYear = currentYear;

        projectsList.forEach(project => {
            const projectEndDate = new Date(project.end_date + 'T00:00:00');
            const projectStartDate = new Date(project.start_date + 'T00:00:00');

            const projectEndYear = projectEndDate.getFullYear();
            const projectStartYear = projectStartDate.getFullYear();

            maxEndYear = Math.max(maxEndYear, projectEndYear);
            minStartYear = Math.min(minStartYear, projectStartYear);
        });

        return Array.from({ length: maxEndYear - minStartYear + 1 }, (_, i) => minStartYear + i);
    };

    return {
        searchQuery,
        selectedYear,
        currentPage,
        filteredProjects,
        paginatedProjects,
        totalPages,
        getYearRange
    };
}
