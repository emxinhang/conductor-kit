# API Integration Pattern

Mọi module phải tuân theo cấu trúc API sau để đảm bảo tính ổn định và Type-safety.

### 1. File: `src/api/<module>.ts`

```typescript
import { client } from "./client";

// Interface Definitions (Preferably imported from src/types)
export interface Entity {
  id: number;
  title: string;
  status: string;
}

// Function Implementations
export const getEntities = async (params?: any) => {
  const response = await client.get<Entity[]>("/entities/", { params });
  return response.data;
};

export const getEntity = async (id: number) => {
  const response = await client.get<Entity>(`/entities/${id}`);
  return response.data;
};

export const createEntity = async (data: Partial<Entity>) => {
  const response = await client.post<Entity>("/entities/", data);
  return response.data;
};
```

### 2. React Query Integration

Sử dụng hooks trong Component:

```tsx
const { data, isLoading } = useQuery({
    queryKey: ["entities", filters],
    queryFn: () => getEntities(filters),
});

const mutation = useMutation({
    mutationFn: createEntity,
    onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["entities"] });
    },
});
```
