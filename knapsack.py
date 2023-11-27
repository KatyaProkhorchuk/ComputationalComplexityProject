class Item:
    '''
    Предмет который можно положить в рюкзак
    '''
    def __init__(self, weight, cost):
        '''
        :param weight: вес
        :param cost: стоимость
        :param cost: стоимость с учетом округления
        '''
        self.weight = weight
        self.cost = cost
        self.cost_eps = cost
        
class KnapsackArr:
    '''
    Для представления решения задачи
    '''
    def __init__(self, total_id = None, total_weight=None, total_cost=None):
        '''
        :param total_id: идентификаторы - что кладем
        :param total_weight: общий вес
        :param total_cost: общая стоимость
        '''
        self.total_id = []
        self.total_weight = 0
        self.total_cost = 0
        if not total_id is None:
            self.total_id = total_id
        if not total_weight is None:
            self.total_weight = total_weight
        if not total_cost is None:
            self.total_cost = total_cost
            
            
class KnapsackFTPS:
    '''
    Алгоритм FPTAS для задачи о рюкзаке
    '''
    def __init__(self, eps, capacity):
        '''
        :param eps: точность приближения
        :param capacity: вместимость
        max_cost - максимальная стоимость вещи
        scale - коэффициент масштабирования для стоимости вещей
        count - счетчик добавленных вещей
        '''
        self.eps = eps
        self.capacity = capacity
        self.max_cost = 0
        self.count = 0
        self.scale = 1
        self.items = dict()
    
    def round_cost(self, cost):
        '''
        округление стоимости
        '''
        return int(cost / self.scale)
    
    def add_subject(self, weight, cost):
        '''
        добавляем вещь в рюкзак, учитывая вместимость
        '''
        if weight <= self.capacity:
            self.items[self.count] = Item(weight, cost)
            if cost > self.max_cost:
                self.max_cost = cost
        self.count += 1
        
    def solver(self):
        '''
        Решает задачу о рюкзаке с использованием алгоритма  Fully Polynomial Time Approximation Scheme
        
        Алгоритм:
        1. Масштабирование стоимости каждой вещи 
        2. Создаем словарь solution, где ключи - стоимость рюкзака, а значения - объекты KnapsackArr(возможные решения)
        3. Перебор вещей и возможных решений для поиска оптимального решения.
        4. Возвращаем оптимальное решения KnapsackArr.
        '''
        if self.items is None:
            return KnapsackArr()
        
        n = len(self.items)
        self.scale = self.max_cost * self.eps / (n * (1 + self.eps))
        [item.__setattr__('cost_scaled', self.round_cost(item.cost)) for item in self.items.values()]

        solution = {0 : KnapsackArr()}
        
        for key, value in self.items.items():
            for knapsack in list(solution.values()):
                new_weight, new_cost = knapsack.total_weight + value.weight, knapsack.total_cost + value.cost_eps
                if new_weight <= self.capacity and (new_cost not in solution or new_weight < solution[new_cost].total_weight):
                    solution[new_cost] = KnapsackArr(knapsack.total_id + [key], new_weight, new_cost)
        best_sol = solution[max(solution.keys())]
        best_sol.total_cost = 0
        #пройдем по id которые ложим в рюкзак и посчитаем стоимость
        for i in best_sol.total_id:
            best_sol.total_cost += self.items[i].cost
        return best_sol
def main():
    try:
        eps = float(input("eps = "))
        capacity = int(input("W = "))
        count = int(input("Кол-во предметов "))
    except Exception:
        print("Некоректные данные")
        return
        
    knapsack = KnapsackFTPS(eps, capacity)
    # считываем вес - стоимость пока есть что читать
    for _ in range(count):
        line = input()
        if not line:
            continue
        knapsack.add_subject(*map(int, line.split()))
    
    sol = knapsack.solver()
    
    print(sol.total_cost, sol.total_weight)
    print(*[ind + 1 for ind in sol.total_id])
    
main()
            
