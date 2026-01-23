import { getLatestGroceryList } from '@/lib/meals';
import GroceryListClient from './components/GroceryListClient';

export default function GroceryListPage() {
  const groceryList = getLatestGroceryList();
  return <GroceryListClient initialGroceryList={groceryList} />;
}

