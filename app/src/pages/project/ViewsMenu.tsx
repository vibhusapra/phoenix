import React, { useCallback } from "react";
import { graphql, useMutation, usePreloadedQuery, useQueryLoader } from "react-relay";
import { Flex, Button } from "@phoenix/components";
import { useSpanFilterCondition } from "@phoenix/pages/project/SpanFilterConditionContext";
import { useTimeRange } from "@phoenix/components/datetime";
import { useProjectContext } from "@phoenix/contexts/ProjectContext";
import environment from "@phoenix/RelayEnvironment";

const SavedViewsQuery = graphql`
  query ViewsMenuQuery($projectId: ID!) {
    project: node(id: $projectId) {
      __typename
      ... on Project {
        id
        savedViews {
          id
          name
          filterCondition
          timeRangeKey
          timeRangeStart
          timeRangeEnd
          treatOrphansAsRoots
        }
      }
    }
  }
`;

const CreateSavedViewMutation = graphql`
  mutation ViewsMenuCreateMutation($input: CreateSavedViewInput!) {
    createSavedView(input: $input) {
      node { id name }
    }
  }
`;

export function ViewsMenu({ projectId }: { projectId: string }) {
  const { filterCondition, setFilterCondition } = useSpanFilterCondition();
  const { timeRange, setTimeRange } = useTimeRange();
  const treatOrphansAsRoots = useProjectContext((s) => s.treatOrphansAsRoots);
  const setTreatOrphansAsRoots = useProjectContext((s) => s.setTreatOrphansAsRoots);

  const [queryRef, loadQuery] = useQueryLoader(SavedViewsQuery);
  React.useEffect(() => {
    loadQuery({ projectId });
  }, [projectId, loadQuery]);
  const data = queryRef ? usePreloadedQuery(SavedViewsQuery, queryRef) : null;

  const [commitCreate] = useMutation(CreateSavedViewMutation);

  const onSave = useCallback(() => {
    const name = window.prompt("Save view as:");
    if (!name) return;
    commitCreate({
      variables: {
        input: {
          projectId,
          name,
          payload: {
            filterCondition,
            timeRangeKey: timeRange.timeRangeKey,
            timeRangeStart: timeRange.start?.toISOString?.(),
            timeRangeEnd: timeRange.end?.toISOString?.(),
            treatOrphansAsRoots,
          },
        },
      },
      onCompleted: () => loadQuery({ projectId }),
    });
  }, [projectId, filterCondition, timeRange, treatOrphansAsRoots, commitCreate, loadQuery]);

  const onApply = useCallback(
    (id: string) => {
      const view = data?.project?.savedViews?.find((v: any) => v.id === id);
      if (!view) return;
      if (typeof view.filterCondition === "string") {
        setFilterCondition(view.filterCondition);
      }
      if (typeof view.treatOrphansAsRoots === "boolean") {
        setTreatOrphansAsRoots(view.treatOrphansAsRoots);
      }
      if (view.timeRangeKey || view.timeRangeStart || view.timeRangeEnd) {
        setTimeRange({
          timeRangeKey: (view.timeRangeKey as any) ?? ("custom" as any),
          start: view.timeRangeStart ? new Date(view.timeRangeStart) : undefined,
          end: view.timeRangeEnd ? new Date(view.timeRangeEnd) : undefined,
        } as any);
      }
    },
    [data, setFilterCondition, setTimeRange, setTreatOrphansAsRoots]
  );

  const views = (data?.project as any)?.savedViews ?? [];

  return (
    <Flex gap="size-100" direction="row" alignItems="center">
      <select
        aria-label="Saved Views"
        onChange={(e) => e.target.value && onApply(e.target.value)}
        defaultValue=""
      >
        <option value="" disabled>Apply view</option>
        {views.map((v: any) => (
          <option key={v.id} value={v.id}>{v.name}</option>
        ))}
      </select>
      <Button size="S" onPress={onSave}>Save view</Button>
    </Flex>
  );
}
