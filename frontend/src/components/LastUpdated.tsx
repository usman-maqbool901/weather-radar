import { Badge } from './ui/badge';
import { formatDate, formatRelativeTime } from '../utils/formatters';

interface LastUpdatedProps {
  lastUpdated: string | null;
  dataTimestamp: string | null;
  loading?: boolean;
}

const LastUpdated = ({ lastUpdated, dataTimestamp, loading }: LastUpdatedProps) => {
  if (loading) {
    return (
      <div className="flex items-center space-x-2">
        <Badge variant="secondary">Loading...</Badge>
      </div>
    );
  }

  if (!lastUpdated) {
    return (
      <div className="flex items-center space-x-2">
        <Badge variant="error">No data available</Badge>
      </div>
    );
  }

  return (
    <div className="flex flex-col space-y-1 bg-white/95 backdrop-blur-sm rounded-lg p-3 shadow-lg border border-slate-200/50">
      <div className="flex items-center space-x-2">
        <Badge variant="success" className="shadow-sm">Updated</Badge>
        <span className="text-sm text-slate-700 font-medium">
          {formatRelativeTime(lastUpdated)}
        </span>
      </div>
      {dataTimestamp && (
        <span className="text-xs text-slate-500 mt-1">
          Data time: {formatDate(dataTimestamp)}
        </span>
      )}
    </div>
  );
};

export default LastUpdated;

