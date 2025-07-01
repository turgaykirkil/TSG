export default function CompanyDetailPage({ params }: { params: { id: string } }) {
  return <div>Company ID: {params.id}</div>;
}
