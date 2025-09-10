import JobsDashboardDynamic from "../components/Dashboard";


const FilteredJobs = [];

const ManualReview = [];

const Index = () => {
  return (
    <JobsDashboardDynamic
      filteredJobs={FilteredJobs}
      manualReviewJobs={ManualReview}
    />
  );
};

export default Index;